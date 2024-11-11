
from model.database import get_db, Base, engine



# Initialize database
Base.metadata.create_all(bind=engine)



# Run the FastAPI application
if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
