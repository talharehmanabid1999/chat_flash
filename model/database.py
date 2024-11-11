# database.py

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Define the SQLite URL (use `sqlite:///filename.db` for file-based or `sqlite:///:memory:` for in-memory)
SQLALCHEMY_DATABASE_URL = "sqlite:///./chat_app.db"  # This will create a file-based SQLite database named 'chat_app.db' in the current directory

# Set up the engine
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# Create a configured session class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a base class for our models
Base = declarative_base()


# database.py

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        
# Function to create a new test database session
def get_test_db():
    from sqlalchemy import create_engine
    from sqlalchemy.orm import sessionmaker

    TEST_SQLALCHEMY_DATABASE_URL = "sqlite:///:memory:"  # In-memory database
    test_engine = create_engine(
        TEST_SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
    )
    TestingSessionLocal = sessionmaker(
        autocommit=False, autoflush=False, bind=test_engine
    )
    Base.metadata.create_all(bind=test_engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()
