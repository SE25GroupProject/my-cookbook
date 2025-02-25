"""

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

"""

from datetime import datetime
from itertools import count
import uuid
from typing import Optional, List
from pydantic import BaseModel, Field
from pydantic import BaseModel, EmailStr


class Instruction(BaseModel):
    step: int
    instruction: str

class Recipe(BaseModel):
    """A data model representing a recipe"""
    recipeId: Optional[int]  # Unique identifier for the recipe
    name: str  # Name of the recipe
    cookTime: Optional[str] = None
    prepTime: Optional[str] = None
    totalTime: Optional[str] = None
    description: Optional[str] = None
    images: Optional[list] = None  # URLs of images related to the recipe
    category: str
    tags: List[str]
    ingredientQuantities: Optional[list[int]]
    ingredients: List[str]  # List of ingredients required
    rating: Optional[str] = None
    calories: Optional[str] = None
    fat: Optional[str] = None
    saturatedFat: Optional[str] = None
    cholesterol: Optional[str] = None
    sodium: Optional[str] = None
    carbs: Optional[str] = None
    fiber: Optional[str] = None
    sugar: Optional[str] = None
    protein: Optional[str] = None
    servings: Optional[str] = None
    instructions: List[Instruction]

    class Config:
        schema_extra = {

            "example": {
                "id": 1,
                "name": "Low-Fat Berry Blue Frozen Dessert",
                "cookTime": "24H",
                "prepTime": "45M",
                "totalTime": "24H45M",
                "description": "Make and share this Low-Fat Berry Blue Frozen Dessert recipe from Food.com.",
                "images": [
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/YUeirxMLQaeE1h3v3qnM_229%20berry%20blue%20frzn%20dess.jpg",
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/AFPDDHATWzQ0b1CDpDAT_255%20berry%20blue%20frzn%20dess.jpg",
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/UYgf9nwMT2SGGJCuzILO_228%20berry%20blue%20frzn%20dess.jpg",
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/PeBMJN2TGSaYks2759BA_20140722_202142.jpg",
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/picuaETeN.jpg",
                    "https://img.sndimg.com/food/image/upload/w_555,h_416,c_fit,fl_progressive,q_95/v1/img/recipes/38/pictzvxW5.jpg"
                ],
                "category": "Frozen Desserts",
                "tags": [
                    "Dessert",
                    "Low Protein",
                    "Low Cholesterol",
                    "Healthy",
                    "Free Of...",
                    "Summer",
                    "Weeknight",
                    "Freezer",
                    "Easy"
                ],
                "ingredientQuantities": [
                    "4",
                    "1/4",
                    "1",
                    "1"
                ],
                "ingredients": [
                    "blueberries",
                    "granulated sugar",
                    "vanilla yogurt",
                    "lemon juice"
                ],
                "rating": "4.5",
                "calories": "170.9",
                "fat": "2.5",
                "saturatedFat": "1.3",
                "cholesterol": "8",
                "sodium": "29.8",
                "carbs": "37.1",
                "fiber": "3.6",
                "sugar": "30.2",
                "protein": "3.2",
                "servings": "4",
                "instructions": [
                    "Toss 2 cups berries with sugar.",
                    "Let stand for 45 minutes, stirring occasionally.",
                    "Transfer berry-sugar mixture to food processor.",
                    "Add yogurt and process until smooth.",
                    "Strain through fine sieve. Pour into baking pan (or transfer to ice cream maker and process according to manufacturers' directions). Freeze uncovered until edges are solid but centre is soft.  Transfer to processor and blend until smooth again.",
                    "Return to pan and freeze until edges are solid.",
                    "Transfer to processor and blend until smooth again.",
                    "Fold in remaining 2 cups of blueberries.",
                    "Pour into plastic mold and freeze overnight. Let soften slightly to serve."
                ]
            }
        }

class RecipeListEntry(BaseModel):
    """A data model representing a recipe"""
    recipeId: int
    name: str  # Name of the recipe
    cookTime: Optional[str] = None
    prepTime: Optional[str] = None
    totalTime: Optional[str] = None
    description: Optional[str] = None
    category: str
    rating: Optional[str] = None
    calories: Optional[str] = None
    fat: Optional[str] = None
    saturatedFat: Optional[str] = None
    cholesterol: Optional[str] = None
    sodium: Optional[str] = None
    carbs: Optional[str] = None
    fiber: Optional[str] = None
    sugar: Optional[str] = None
    protein: Optional[str] = None
    servings: Optional[str] = None

class RecipeListRequest(BaseModel):
    ingredients: List[str] = Field(...,
                                   description="List of ingredients to filter recipes")
    page: int = Field(..., description="Page number for pagination")


class RecipeListResponse(BaseModel):
    recipes: List[RecipeListEntry] = Field(...,
                                  description="List of recipes matching the filter criteria")
    page: int = Field(..., ge=1, description="Current page number, must be at least 1")


class RecipeListRequest2(BaseModel):
    page: int = Field(..., ge=1, description="Current page number, must be at least 1")
    caloriesMax: float = Field(..., ge=0, le=4000,
                              description="Calories upper limit, between 0 and 100")
    fatMax: float = Field(..., ge=0, le=140,
                         description="Fat upper limit, between 0 and 100")
    sugMax: float = Field(..., ge=0, le=150,
                         description="Sugar upper limit, between 0 and 100")
    proMax: float = Field(..., ge=0, le=250,
                         description="Protein upper limit, between 0 and 100")


class RecipeQuery(BaseModel):
    query: str
    context: str


class User(BaseModel):
    email: EmailStr
    password: str


class UserCred(BaseModel):
    username: str
    password: str
    
class PostRecipe(BaseModel):
    recipeId: Optional[int]
    name: Optional[str]

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
    recipe: Optional[PostRecipe] = Field(default=None, description="id and name of recipe associated with the post")
    date: Optional[str] = Field(default_factory=lambda: datetime.now().strftime("%Y-%m-%d %H:%M:%S"), description="Timestamp of the post")
    likes: List[int] = Field(default_factory=list, description="List of UserIds who liked the post")
    dislikes: List[int] = Field(default_factory=list, description="List of UserIds who disliked the post")
    comments: List[Comment] = Field(default_factory=list, description="List of comments on the post")

class PostUpdate(BaseModel):
    userId: Optional[int] = Field(None, description="Id of user the post was created by")
    message: Optional[str] = Field(None, description="Updated content of the post")
    image: Optional[str] = Field(None, description="Updated Base64-encoded image data")
    recipe: Optional[PostRecipe] = Field(None, description="Updated Recipe ID associated with the post")

class ShoppingListItem(BaseModel):
    name: str
    quantity: int
    unit: str
    checked: bool

class MealPlanEntry(BaseModel):
    day: int  # 0-6 representing Monday-Sunday
    recipe: PostRecipe  # The recipe id and name