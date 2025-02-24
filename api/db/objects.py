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
    
class Ingredient():
    def __init__(self, name: str, amount: float):
        self.Name = name
        self.Amount = amount

class Instruction():
    def __init__(self, step: int, instruction: str):
        self.Step = step
        self.Instruction = instruction
    
class Recipe():

    def __init__(self, name: str, cookTime: str, prepTime: str, totalTime: str, description: str, category: str, rating: float, calories: float, fat: float, saturatedFat: float,
                cholesterol: float, sodium: float, carbs: float, fiber: float, sugar: float, protein: float, servings: float, images: list[str], 
                tags: list[str], ingredients: list[Ingredient], instructions: list[Instruction], recipeId = -1):
        self.RecipeId = recipeId
        self.Name = name
        self.CookTime = cookTime
        self.PrepTime = prepTime
        self.TotalTime = totalTime
        self.Description = description
        self.Category = category
        self.Rating = rating
        self.Calories = calories
        self.Fat = fat
        self.SaturatedFat = saturatedFat
        self.Cholesterol = cholesterol
        self.Sodium = sodium
        self.Carbs = carbs
        self.Fiber = fiber
        self.Sugar = sugar
        self.Protein = protein
        self.Servings = servings
        self.Images = images
        self.Tags = tags
        self.Ingredients = ingredients
        self.Instructions = instructions
    
    def to_dict(self) -> dict:
        output = {
            "name": self.Name,
            "cookTime": self.CookTime,
            "prepTime": self.PrepTime,
            "totalTime": self.TotalTime,
            "description": self.Description,
            "category": self.Category,
            "rating": self.Rating,
            "calories": self.Calories,
            "fat": self.Fat,
            "saturatedFat": self.SaturatedFat,
            "cholesterol": self.Cholesterol,
            "sodium": self.Sodium,
            "carbs": self.Carbs,
            "fiber": self.Fiber,
            "sugar": self.Sugar,
            "protein": self.Protein,
            "servings": self.Servings,
            "images": self.Images,
            "tags": self.Tags,
            "ingredients": self.Ingredients,
            "instructions": self.Instructions
        }

        return output

class Comment(BaseModel):
    commentId: Optional[int] = Field(default=None, description="Auto-incremented ID of the comment")
    userId: int = Field(..., description="ID of the user who created the comment")
    postId: int = Field(..., description="ID of the post the comment is related to")
    message: str = Field(..., description="Content of the comment")
    date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of the comment")

class Post(BaseModel):
    postId: Optional[int] = Field(default=None, description="Auto-incremented ID from the database")
    userId: int = Field(..., description="ID of the user who created the post")
    message: str = Field(..., description="Content of the post")
    image: Optional[str] = Field(default=None, description="Base64-encoded image data")
    recipe: Optional[int] = Field(default=None, description="id of recipe associated with the post")
    date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of the post")
    likes: List[int] = Field(default_factory=list, description="List of UserIds who liked the post")
    dislikes: List[int] = Field(default_factory=list, description="List of UserIds who disliked the post")
    comments: List[Comment] = Field(default_factory=list, description="List of comments on the post")
