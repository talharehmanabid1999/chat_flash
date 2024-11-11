import json
from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from sqlalchemy.orm import Session
from datetime import timedelta
from typing import List
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

import model.schemas as schemas 
import model.models as models

import model.crud as crud
from auth.auth import authenticate_user, create_access_token, ACCESS_TOKEN_EXPIRE_MINUTES, get_db, get_current_user
from model.database import get_db, Base, engine
import model.database as database
from fastapi.security import OAuth2PasswordRequestForm


# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Setup templates
templates = Jinja2Templates(directory="templates")


from fastapi import FastAPI, Request  # Import Request

# Root route to serve the HTML page
@app.get("/", response_class=HTMLResponse)
async def serve_frontend(request: Request):  # Add request parameter here
    return templates.TemplateResponse("index.html", {"request": request})



# Connection manager for WebSocket
class ConnectionManager:
    def __init__(self):
        self.active_connections: dict[str, WebSocket] = {}

    async def connect(self, username: str, websocket: WebSocket):
        await websocket.accept()
        self.active_connections[username] = websocket

    def disconnect(self, username: str):
        if username in self.active_connections:
            del self.active_connections[username]

    async def send_personal_message(self, message: str, username: str):
        websocket = self.active_connections.get(username)
        if websocket:
            await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections.values():
            await connection.send_text(message)

manager = ConnectionManager()


# User sign-up endpoint
@app.post("/signup", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    return crud.create_user(db=db, user=user)


# User login and token generation
@app.post("/token", response_model=schemas.Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


# Get all users (with authorization)
@app.get("/users", response_model=List[schemas.User])
def get_users(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return db.query(models.User).all()


# WebSocket chat endpoint
@app.websocket("/ws/chat")
async def chat_endpoint(websocket: WebSocket, token: str = Query(...), db: Session = Depends(get_db)):
    # Authenticate the user using the token
    user = await get_current_user(token, db)
    if user is None:
        await websocket.close(code=status.WS_1008_POLICY_VIOLATION)
        return

    # Connect the user
    await manager.connect(user.username, websocket)
    try:
        while True:
            data = await websocket.receive_text()
            # Parse incoming message (expected to be JSON with 'recipient' and 'message' fields)
            message_data = json.loads(data)
            recipient = message_data['recipient']
            message = message_data['message']

            # Fetch recipient user
            recipient_user = crud.get_user_by_username(db, recipient)
            if recipient_user is None:
                await websocket.send_text("Recipient not found.")
                continue

            # Save message to the database
            db_message = models.Message(
                sender_id=user.id,
                recipient_id=recipient_user.id,
                content=message
            )
            db.add(db_message)
            db.commit()

            # Send message to recipient if they are online
            full_message = {
                "sender": user.username,
                "recipient": recipient,
                "message": message
            }
            await manager.broadcast(json.dumps(full_message))

    except WebSocketDisconnect:
        manager.disconnect(user.username)
    finally:
        db.close()
        
        
from sqlalchemy import or_

@app.get("/messages/{recipient_username}", response_model=List[schemas.Message])
def get_message_history(recipient_username: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    recipient_user = crud.get_user_by_username(db, recipient_username)
    if recipient_user is None:
        raise HTTPException(status_code=404, detail="Recipient not found")

    # Retrieve all messages where the current user is either the sender or the recipient
    messages = db.query(models.Message).filter(
        or_(
            (models.Message.sender_id == current_user.id) & (models.Message.recipient_id == recipient_user.id),
            (models.Message.sender_id == recipient_user.id) & (models.Message.recipient_id == current_user.id)
        )
    ).order_by(models.Message.timestamp).all()

    # Format messages to include sender and recipient usernames
    return [
        {
            "sender": db.query(models.User).get(msg.sender_id).username,
            "recipient": db.query(models.User).get(msg.recipient_id).username,
            "content": msg.content,
            "timestamp": msg.timestamp
        }
        for msg in messages
    ]
@app.post("/messages/send")
def send_message(recipient: str, message: str, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    recipient_user = crud.get_user_by_username(db, recipient)
    if recipient_user is None:
        raise HTTPException(status_code=404, detail="Recipient not found")
    
    db_message = models.Message(sender_id=current_user.id, recipient_id=recipient_user.id, content=message)
    db.add(db_message)
    db.commit()
    return {"message": "Message sent"}



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
