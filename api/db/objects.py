"""Holds classes of all objects for database use"""
from models import Recipe
from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional, List

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
    image: Optional[str] = Field(default=None, description="Base64-encoded image data")
    recipe: Optional[int] = Field(default=None, description="id of recipe associated with the post")
    date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of the post")
    likes: List[int] = Field(default_factory=list, description="List of UserIds who liked the post")
    dislikes: List[int] = Field(default_factory=list, description="List of UserIds who disliked the post")
