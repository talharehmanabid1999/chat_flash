Chat App Project
================

This is a real-time chat application built using FastAPI, WebSocket, SQLAlchemy, and SQLite. The application allows users to sign up, log in, and chat with other registered users. This project includes WebSocket support for real-time communication, user authentication, and message history retrieval.

Features
--------

*   **User Sign-Up and Login**: Register a new user account and log in securely.
    
*   **Real-Time Chat**: Send and receive messages in real time with other users via WebSocket.
    
*   **Message History**: Retrieve past messages with any selected user.
    
*   **Authorization**: Secure API endpoints using JWT-based authentication.
    
*   **Testing**: Complete with unit tests for core functionality.
    

Requirements
------------

Make sure you have **Python 3.7+** installed. Then, set up the project’s dependencies:

pip install -r requirements.txt   `

### Key Dependencies

*   **FastAPI**: Web framework used for building the API.
    
*   **Uvicorn**: ASGI server to serve the FastAPI application.
    
*   **SQLAlchemy**: ORM for interacting with SQLite database.
    
*   **Pydantic**: Data validation and settings management.
    
*   **Passlib**: For password hashing.
    
*   **Python-Jose**: JWT handling for user authentication.
    
*   **Starlette TestClient**: For testing WebSocket connections.
    

Project Structure
-----------------

*   **main.py**: The main application file where the FastAPI app and WebSocket routes are defined.
    
*   **auth.py**: Contains JWT-based authentication utilities.
    
*   **crud.py**: Basic database operations such as creating a user and verifying credentials.
    
*   **database.py**: Configuration for database connections using SQLAlchemy.
    
*   **models.py**: SQLAlchemy models defining database tables.
    
*   **schemas.py**: Pydantic models for request/response validation.
    
*   **tests/**: Contains unit tests to verify the functionality of the application.
    

Setup Instructions
------------------

### Clone the Repository

git clone https://github.com/talharehmanabid1999/chat_flash.git  cd chat_flash  `

### Install Dependencies

Create a virtual environment (recommended) and install dependencies:

python -m venv env  source env/bin/activate  # On Windows, use 'env\Scripts\activate'  pip install -r requirements.txt   `

### Set Up Environment Variables

Create a .env file in the root directory and add the following environment variables:

JWT_SECRET_KEY=your_secret_key  ALGO=HS256  ACCESS_TOKEN_EXPIRE_MINUTES=30   `

### Initialize the Database

Run the following command to create the SQLite database:

python -c "from database import Base, engine; Base.metadata.create_all(bind=engine)"   `

### Run the Application

Start the application using Uvicorn:

uvicorn main:app --reload   `

### Access the Application

The application should now be running on [http://127.0.0.1:8000](http://127.0.0.1:8000).

Running Tests
-------------

To run the tests, use:

pytest 

The tests are located in the tests/ directory and include:

*   **tests/test_auth.py**: Tests for user authentication and authorization.
    
*   **tests/test_crud.py**: Tests for basic CRUD operations on the database.
    
*   **tests/test_async.py**: Tests for the main app routes.

    


Usage Instructions
------------------

### User Registration and Login

*   **Register a new user** by making a POST request to /signup with a JSON payload containing username and password.
    
*   **Log in** by sending a POST request to /token, which returns an access token.
    
*   **Access Protected Routes** using the Authorization header with the token in the format Bearer .
    

### Real-Time Chat

Connect to WebSocket at /ws/chat?token= to establish a real-time chat connection.

*   **Send messages** directly to another user by specifying their username.
    

Troubleshooting
---------------

*   **Error: No Such Table**: Ensure the database has been initialized by running Base.metadata.create\_all(bind=engine).
    
*   **Test Errors**: Verify that .env file variables are correctly set, and pytest is run from the project root.
    

Contributing
------------

Feel free to fork this repository and make pull requests if you have any suggestions or improvements.
