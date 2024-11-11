
from model.database import get_db, Base, engine

from fastapi import FastAPI, Depends, HTTPException, status, WebSocket, WebSocketDisconnect, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

# Initialize database
Base.metadata.create_all(bind=engine)

app = FastAPI()

# Serve static files
app.mount("/templates", StaticFiles(directory="templates"), name="templates")

# Setup templates
templates = Jinja2Templates(directory="templates")



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
