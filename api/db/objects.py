"""Holds classes of all objects for database use"""
from models import Recipe
from datetime import datetime

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

class Post:
    def __init__(self, userId: int, message: str, image: bytes, recipe: Recipe):
        self.postId = None # should be auto incremented when inserted into database
        self.userId = userId
        self.message = message
        self.image = image 
        self.recipe = recipe
        self.date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.likes = 0
        self.dislikes = 0

    def to_dict(self) -> dict:
        return {
            "postId": self.postId,
            "userId": self.userId,
            "message": self.message,
            "image": self.image, 
            "recipe": self.recipe.model_dump_json(),
            "date": self.date,
            "likes": self.likes,
            "dislikes": self.dislikes,
        }
    