# tests/test_auth.py

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session


from model.database import Base, get_test_db
from model.models import User
from auth.auth import get_db


import sys
import os

# Append the parent directory to sys.path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Now you can import main without using relative import
import main


# Override the get_db dependency to use the test database
main.app.dependency_overrides[get_db] = get_test_db

client = TestClient(main.app)

@pytest.fixture
def db_session():
    # Create a new database session for testing
    yield from get_test_db()

def test_signup(db_session: Session):
    response = client.post(
        "/signup",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["username"] == "testuser"
    assert "id" in data

def test_duplicate_signup(db_session: Session):
    # Sign up the user the first time
    client.post("/signup", json={"username": "testuser", "password": "testpassword"})
    # Try signing up again with the same username
    response = client.post(
        "/signup",
        json={"username": "testuser", "password": "testpassword"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Username already registered"

def test_login(db_session: Session):
    # First, sign up a new user
    client.post("/signup", json={"username": "testuser", "password": "testpassword"})
    # Then, attempt to log in
    response = client.post(
        "/token",
        data={"username": "testuser", "password": "testpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_incorrect_login(db_session: Session):
    # Attempt to log in with wrong credentials
    response = client.post(
        "/token",
        data={"username": "nonexistentuser", "password": "wrongpassword"},
        headers={"Content-Type": "application/x-www-form-urlencoded"}
    )
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect username or password"
