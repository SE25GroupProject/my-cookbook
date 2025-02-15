"""Holds classes of all objects for database use"""
from models import Recipe
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional

class User():
    def __init__(self, username: str, password: str, userId: int = -1):
        self.UserId = userId
        self.Username = username
        self.Password = password

    def to_dict(self) -> dict:
        output = {
            "userId": self.UserId,
            "username": self.Username,
        }

        return output

class Post(BaseModel):
    postId: Optional[int] = Field(default=None, description="Auto-incremented ID from the database")
    userId: int = Field(..., description="ID of the user who created the post")
    message: str = Field(..., description="Content of the post")
    image: str = Field(..., description="Base64-encoded image data")
    recipe: Optional[Recipe] = Field(default=None, description="Recipe associated with the post")
    date: str = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of the post")
    likes: int = Field(default=0, description="Number of likes")
    dislikes: int = Field(default=0, description="Number of dislikes")
