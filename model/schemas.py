# schemas.py

from pydantic import BaseModel
from datetime import datetime


class UserCreate(BaseModel):
    username: str
    password: str


from pydantic import BaseModel

class User(BaseModel):
    id: int
    username: str

    class Config:
        from_attributes = True  


class Message(BaseModel):
    sender: str  
    recipient: str 
    content: str
    timestamp: datetime

    class Config:
        from_attributes = True




class Token(BaseModel):
    access_token: str
    token_type: str
