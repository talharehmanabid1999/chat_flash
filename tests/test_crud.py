# tests/test_crud.py

import pytest
from sqlalchemy.orm import Session
from model.database import Base, get_test_db

import sys
import os

# Append the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import main without using relative import
import model.crud as crud
import model.schemas as schemas

@pytest.fixture
def db_session():
    # Create a new database session for testing
    yield from get_test_db()

def test_create_user(db_session: Session):
    user_schema = schemas.UserCreate(username="testuser", password="testpassword")
    user = crud.create_user(db_session, user_schema)
    assert user.username == "testuser"
    assert user.hashed_password != "testpassword"  # Password should be hashed

def test_get_user_by_username(db_session: Session):
    user_schema = schemas.UserCreate(username="testuser", password="testpassword")
    crud.create_user(db_session, user_schema)
    user = crud.get_user_by_username(db_session, "testuser")
    assert user is not None
    assert user.username == "testuser"

def test_verify_password():
    plain_password = "testpassword"
    hashed_password = crud.pwd_context.hash(plain_password)
    assert crud.verify_password(plain_password, hashed_password)
    assert not crud.verify_password("wrongpassword", hashed_password)
