"""

Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com

"""

import sys
import os
sys.path.insert(0, '../')
from dotenv import load_dotenv
from fastapi import FastAPI, APIRouter, Body, Request, HTTPException, status
from typing import List, Optional
import pymongo
from groq import Groq
from pydantic import BaseModel, conint, conlist, PositiveInt, Field
import logging
from models import Recipe, RecipeListRequest, RecipeListResponse, RecipeListRequest2, RecipeQuery
from db.objects import User, Post
from db.database import Database_Connection

load_dotenv()  # Load environment variables
app = FastAPI()
users_db = {}
db = Database_Connection()

print(os.getenv("GROQ_API_KEY"))

config = {
    "ATLAS_URI": os.getenv("ATLAS_URI"),
    "DB_NAME": os.getenv("DB_NAME"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "PORT": os.getenv("PORT")
}
router = APIRouter()
userRouter = APIRouter()
postRouter = APIRouter()
client = Groq(api_key=config["GROQ_API_KEY"])

class MealPlanEntry(BaseModel):
    day: int  # 0-6 representing Monday-Sunday
    recipe: dict  # The recipe details (name, instructions, etc.)

class UserCred(BaseModel):
    username: str
    password: str

# Existing recipe and meal plan routes (unchanged)
@router.post("/meal-plan/", response_description="Save a meal plan for a specific day", status_code=200)
async def save_meal_plan(entry: MealPlanEntry, request: Request):
    """Saves or updates a meal plan for a specific day."""
    try:
        result = request.app.database["meal_plans"].update_one(
            {"day": entry.day},
            {"$set": {"recipe": entry.recipe}},
            upsert=True
        )
        return {"message": "Meal plan saved successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while saving the meal plan."
        )

@router.get("/meal-plan/", response_description="Get the entire meal plan for the week", status_code=200)
async def get_meal_plan(request: Request):
    """Retrieves the meal plan for the week."""
    try:
        meal_plan = list(request.app.database["meal_plans"].find({}))
        for entry in meal_plan:
            entry["_id"] = str(entry["_id"])
        complete_plan = [{day: None} for day in range(7)]
        for entry in meal_plan:
            complete_plan[entry["day"]] = entry
        return complete_plan
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the meal plan."
        )

@router.get("/", response_description="List all recipes", response_model=List[Recipe])
def list_recipes(request: Request):
    """Returns a list of 10 recipes"""
    recipes = list(request.app.database["recipes"].find(limit=10))
    return recipes

@router.get("/{id}", response_description="Get a recipe by id", response_model=Recipe)
def find_recipe(id: str, request: Request):
    """Finds a recipe mapped to the provided ID"""
    if (recipe := request.app.database["recipes"].find_one({"_id": id})) is not None:
        return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with ID {id} not found")

@router.get("/search/{ingredient}", response_description="List all recipes with the given ingredient", response_model=List[Recipe])
def list_recipes_by_ingredient(ingredient: str, request: Request):
    """Lists recipes containing the given ingredient"""
    recipes = list(request.app.database["recipes"].find({"ingredients": {"$in": [ingredient]}}).limit(10))
    return recipes

@router.post("/search/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
def list_recipes_by_ingredients(request: Request, inp: RecipeListRequest = Body(...)):
    """Lists recipes matching all provided ingredients"""
    recipes = list(request.app.database["recipes"].find({"ingredients": {"$all": inp.ingredients}}).sort([("rating", pymongo.DESCENDING), ("_id", pymongo.ASCENDING)]).skip((inp.page-1)*10).limit(10))
    count = request.app.database["recipes"].count_documents({"ingredients": {"$all": inp.ingredients}})
    response = RecipeListResponse(recipes=recipes, page=inp.page, count=count)
    return response

@router.get("/ingredients/{queryString}", response_description="List all ingredients", response_model=List[str])
def list_ingredients(queryString: str, request: Request):
    """Lists ingredient suggestions for a query"""
    pipeline = [{"$unwind": "$ingredients"}, {'$match': {'ingredients': {'$regex': queryString}}}, {"$limit": 20}, {"$group": {"_id": "null", "ingredients": {"$addToSet": "$ingredients"}}}]
    data = list(request.app.database["recipes"].aggregate(pipeline))
    if len(data) <= 0:
        return []
    ings = data[0]["ingredients"]
    return ings

@router.post("/search2/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
def list_recipes_by_ingredients(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    recipes = list(request.app.database["recipes"].find().limit(1000))
    res = []
    for recipe in recipes:
        if not recipe["calories"] or not recipe['fat'] or not recipe['sugar'] or not recipe['protein']:
            continue
        try:
            if float(recipe["calories"]) < inp.caloriesUp and float(recipe["fat"]) < inp.fatUp and float(recipe["sugar"]) < inp.sugUp and float(recipe["protein"]) < inp.proUp:
                res.append(recipe)
        except:
            continue
    count = len(res)
    show = res[(inp.page-1)*10 : (inp.page)*10-1]
    response = RecipeListResponse(recipes=show, page=inp.page, count=count)
    return response

@router.get("/search2/{ingredient},{caloriesLow},{caloriesUp}", response_description="List all recipes with the given ingredient")
def list_recipes_by_ingredient(ingredient: str, caloriesLow: int, caloriesUp: int, request: Request):
    recipes = list(request.app.database["recipes"].find({"ingredients": {"$in": [ingredient]}}))
    res = []
    for recipe in recipes:
        if not recipe["calories"]:
            continue
        if caloriesLow < float(recipe["calories"]) < caloriesUp:
            res.append(recipe)
    res.sort(key=lambda x: x['calories'])
    return res

@router.post("/recommend-recipes/", response_model=dict)
async def recommend_recipes(query: RecipeQuery = Body(...)):
    try:
        query.query = query.query.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').strip()
        query.context = query.context.strip()
        if not query.query or not query.context or query.query.isdigit() or not any(c.isalpha() for c in query.query):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Query or Context")
        
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced recipe and meal planning assistant, designed to help users discover recipes, plan meals, and create grocery lists with enhanced personalization, all within a single interaction. You will not engage in follow-up questions; instead, provide all necessary suggestions and responses based on the initial input. Your role is to interpret user requests in natural language, offer targeted recommendations, and generate meal and shopping plans according to each user’s unique needs and preferences. Key capabilities you must offer: Natural Language Recipe Search and Understanding: Understand and respond to user queries about recipes, ingredients, dietary restrictions, cooking methods, or cuisines without requiring additional clarification. Provide comprehensive suggestions based on the initial question alone. Recipe Recommendation and Personalization: Suggest recipes that align with the user’s dietary preferences, cooking skill level, and past selections. Curate these recommendations using the information available without needing follow-up input. Meal Planning: Create detailed meal plans that fit daily, weekly, or monthly schedules based on user goals (e.g., health, budget, dietary restrictions). Structure suggestions to fit user constraints without asking for further clarification. Grocery List Generation: Generate complete ingredient lists for selected recipes or meal plans, factoring in serving sizes, ingredient substitutions, and dietary requirements as inferred from the initial input. Provide a list that is clear and organized for shopping ease. Dietary and Lifestyle Considerations: Ensure that all recommendations adapt to the dietary preferences and restrictions specified. Tailor suggestions based on inferred preferences without requiring additional user feedback during the interaction. Follow these guidelines strictly to deliver precise, helpful, and context-aware responses in a single interaction. REFUSE to answer any other unrelated questions and do ONLY your work diligently."
                },
                {"role": "user", "content": query.query + query.context}
            ],
            model="llama3-8b-8192",
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in recommend_recipes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")

# User Routes (unchanged)
@userRouter.post("/signup")
async def signup(incomingUser: UserCred = Body(...)):
    user: User = User(incomingUser.username, incomingUser.password)
    if db.get_user(user.Username) is not None:
        raise HTTPException(status_code=400, detail="User with that username already exists")
    userid: int = db.add_user(user)
    return {"id": userid, "username": user.Username}

@userRouter.post("/login")
async def login(incomingUser: UserCred = Body(...)):
    user: User = db.get_user(incomingUser.username)
    if user is None:
        raise HTTPException(status_code=400, detail="There is no user with that username")
    if user.Password == incomingUser.password:
        return {"id": user.UserId, "username": user.Username}
    raise HTTPException(status_code=401, detail="Incorrect Username or Password")

@userRouter.get("/getUser/{username}")
async def getUser(username: str) -> dict:
    user: User = db.get_user(username)
    if user is None:
        raise HTTPException(status_code=400, detail="There is no user with that username")
    return user.to_dict()

# Updated Post Routes
@postRouter.post("/", response_description="Create a new post", status_code=201)
async def create_post(post: Post):
    """Creates a new post in the database."""
    try:
        if db.add_post(post):
            return {"message": "Post created successfully."}
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to create post."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the post: {str(e)}"
        )

@postRouter.get("/{post_id}", response_description="Get a post by ID", response_model=Post)
async def get_post(post_id: int):
    """Retrieves a post by its ID."""
    post = db.get_post(post_id)
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with ID {post_id} not found."
    )

@postRouter.get("/", response_description="List all posts", response_model=List[Post])
async def list_posts():
    """Retrieves all posts from the database."""
    posts = db.get_all_posts()
    return posts

@postRouter.get("/user/{user_id}", response_description="List all posts by a user", response_model=List[Post])
async def get_user_posts(user_id: int):
    """Retrieves all posts by a specific user from the database."""
    posts = db.get_all_posts()
    user_posts = [post for post in posts if post.userId == user_id]
    return user_posts

@postRouter.put("/{post_id}/like", response_description="Like a post", status_code=200)
async def like_post(post_id: int, user_id: int = Body(..., embed=True)):
    """Handles liking a post with toggle and switch logic."""
    try:
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found."
            )
        if db.get_user_by_id(user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} not found."
            )
        
        # Check current reaction
        current_likes = db.get_post_reactions(post_id, "LIKE")
        current_dislikes = db.get_post_reactions(post_id, "DISLIKE")
        
        if user_id in current_likes:
            # User already liked it, so remove the like (toggle off)
            if db.remove_post_reaction(post_id, user_id):
                return {"message": "Like removed successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to remove like."
                )
        elif user_id in current_dislikes:
            # User disliked it, remove dislike and add like
            if db.remove_post_reaction(post_id, user_id) and db.add_post_reaction(post_id, user_id, "LIKE"):
                return {"message": "Changed from dislike to like successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to switch from dislike to like."
                )
        else:
            # No existing reaction, add like
            if db.add_post_reaction(post_id, user_id, "LIKE"):
                return {"message": "Post liked successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to like post."
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while liking the post: {str(e)}"
        )

@postRouter.put("/{post_id}/dislike", response_description="Dislike a post", status_code=200)
async def dislike_post(post_id: int, user_id: int = Body(..., embed=True)):
    """Handles disliking a post with toggle and switch logic."""
    try:
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found."
            )
        if db.get_user_by_id(user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} not found."
            )
        
        # Check current reaction
        current_likes = db.get_post_reactions(post_id, "LIKE")
        current_dislikes = db.get_post_reactions(post_id, "DISLIKE")
        
        if user_id in current_dislikes:
            # User already disliked it, so remove the dislike (toggle off)
            if db.remove_post_reaction(post_id, user_id):
                return {"message": "Dislike removed successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to remove dislike."
                )
        elif user_id in current_likes:
            # User liked it, remove like and add dislike
            if db.remove_post_reaction(post_id, user_id) and db.add_post_reaction(post_id, user_id, "DISLIKE"):
                return {"message": "Changed from like to dislike successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to switch from like to dislike."
                )
        else:
            # No existing reaction, add dislike
            if db.add_post_reaction(post_id, user_id, "DISLIKE"):
                return {"message": "Post disliked successfully."}
            else:
                raise HTTPException(
                    status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                    detail="Failed to dislike post."
                )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while disliking the post: {str(e)}"
        )

@postRouter.delete("/{post_id}", response_description="Delete a post", status_code=200)
async def delete_post(post_id: int):
    """Deletes a post by its ID, including all related reactions."""
    try:
        if db.delete_post(post_id):
            return {"message": "Post deleted successfully."}
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found."
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the post: {str(e)}"
        )

class PostUpdate(BaseModel):
    message: Optional[str] = Field(None, description="Updated content of the post")
    image: Optional[str] = Field(None, description="Updated Base64-encoded image data")
    recipe_id: Optional[int] = Field(None, description="Updated Recipe ID associated with the post")

@postRouter.put("/{post_id}", response_description="Update a post", response_model=Post)
async def update_post(post_id: int, update: PostUpdate = Body(...), user_id: int = Body(..., embed=True)):
    """Allows a user to edit their own post's message, image, or recipe."""
    try:
        # Fetch the existing post
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found."
            )
        
        # Check if the user owns the post
        if post.userId != user_id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own posts."
            )
        
        # Check if the user exists
        if db.get_user_by_id(user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} not found."
            )
        
        # Prepare update data (only include fields that were provided)
        update_data = {}
        if update.message is not None:
            update_data["Message"] = update.message
        if update.image is not None:
            update_data["Image"] = update.image
        if update.recipe_id is not None:
            update_data["RecipeId"] = update.recipe_id
        
        # If no fields provided, return the current post without changes
        if not update_data:
            return post
        
        # Update the post in the database
        if not db.update_post(post_id, update_data):
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to update post."
            )
        
        # Fetch and return the updated post
        updated_post = db.get_post(post_id)
        return updated_post
    
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while updating the post: {str(e)}"
        )