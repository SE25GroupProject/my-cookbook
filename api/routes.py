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
from api.models import Recipe, RecipeListRequest, RecipeListResponse, RecipeListRequest2, RecipeQuery, MealPlanEntry, UserCred, ShoppingListItem, PostUpdate, Post, Comment
from api.db.objects import User
from api.db.database import Database_Connection
from api.dbMiddleware import DBConnectionMiddleware


load_dotenv()  # Load environment variables


users_db = {}
database_con = Database_Connection()

config = {
    "ATLAS_URI": os.getenv("ATLAS_URI"),
    "DB_NAME": os.getenv("DB_NAME"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "PORT": os.getenv("PORT")
}
router = APIRouter()
userRouter = APIRouter()
recipeRouter = APIRouter()
mealPlanRouter = APIRouter()
shoppingRouter = APIRouter()
postRouter = APIRouter()
client = Groq(api_key=config["GROQ_API_KEY"])



# --------------------------------------------------------
# Deprecated Functions
# --------------------------------------------------------

# Deprecated - Replaced
# @app.get("/shopping-list")
async def get_shopping_list():
    """Fetches the shopping list from the database or returns an empty list"""
    collection_name = "shopping-list"
    if collection_name not in app.database.list_collection_names():
        app.database.create_collection(collection_name)

    shopping_list = list(app.database[collection_name].find())
    shopping_list = [{**item, "_id": str(item["_id"])}
                     for item in shopping_list]

    return {"shopping_list": shopping_list}

# Deprecated - Replaced
# @app.post("/shopping-list/update")
async def update_shopping_list(items: List[ShoppingListItem]):
    """
    Extends the shopping list in the database with new items.
    Ensures no duplicate items are added.
    """
    collection_name = "shopping-list"
    if collection_name not in app.database.list_collection_names():
        app.database.create_collection(collection_name)

    collection = app.database[collection_name]

    # Fetch existing items from the database
    existing_items = list(collection.find())
    existing_items_dict = {
        (item["name"], item["unit"]): item for item in existing_items
    }

    # Filter new items to avoid duplicates based on 'name' and 'unit'
    new_items = [
        {"name": item.name, "quantity": item.quantity,
            "unit": item.unit, "checked": item.checked}
        for item in items
        if (item.name, item.unit) not in existing_items_dict
    ]

    if not new_items:
        raise HTTPException(status_code=400, detail="No new items to add.")

    # Insert only new items
    collection.insert_many(new_items)

    # Fetch the updated list
    updated_list = list(collection.find())
    updated_list = [{**item, "_id": str(item["_id"])} for item in updated_list]

    return {"message": "Shopping list updated successfully", "shopping_list": updated_list}

# Deprecated - Replaced
# @app.put("/shopping-list/{item_id}")
async def update_shopping_list_item(item_id: str, item: ShoppingListItem):
    """
    Updates a single item in the shopping list by its ID.
    Ensures the item exists before updating.
    """
    collection_name = "shopping-list"
    collection = app.database[collection_name]

    # Try to find the item by ID
    existing_item = collection.find_one({"_id": ObjectId(item_id)})

    if not existing_item:
        raise HTTPException(status_code=404, detail="Item not found")

    # Prepare the updated data
    updated_item_data = {
        "name": item.name,
        "quantity": item.quantity,
        "unit": item.unit,
        "checked": item.checked
    }

    # Update the item in the database
    result = collection.update_one({"_id": ObjectId(item_id)}, {
                                   "$set": updated_item_data})

    if result.matched_count == 0:
        raise HTTPException(status_code=400, detail="Failed to update item")

    # Fetch the updated list after the update
    updated_item = collection.find_one({"_id": ObjectId(item_id)})
    updated_item = {**updated_item, "_id": str(updated_item["_id"])}

    return {"message": "Item updated successfully", "shopping_list_item": updated_item}

# Deprecated - Replaced
# @app.delete("/shopping-list/{item_id}")
async def delete_shopping_list_item(item_id: str):
    """Deletes an item from the shopping list by its ID"""
    collection_name = "shopping-list"
    collection = app.database[collection_name]

    # Try to find and delete the item
    result = collection.delete_one({"_id": ObjectId(item_id)})

    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Item not found")

    return {"message": f"Item with ID {item_id} deleted successfully"}

# Deprecated - Replaced
# @router.post("/meal-plan/", response_description="Save a meal plan for a specific day", status_code=200)
async def save_meal_plan_old(entry: MealPlanEntry, request: Request):

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

# Deprecated - Replaced
# @router.get("/meal-plan/", response_description="Get the entire meal plan for the week", status_code=200)
async def get_meal_plan_old(request: Request):
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
    

# Deprecated - Unused Route
# @router.get("/", response_description="List all recipes", response_model=List[Recipe])
def list_recipes_old(request: Request):
    """Returns a list of 10 recipes"""
    recipes = list(request.app.database["recipes"].find(limit=10))
    return recipes

# Deprecated - Getting Recreated
# @router.get("/{id}", response_description="Get a recipe by id", response_model=Recipe)
def find_recipe_old(id: str, request: Request):
    """Finds a recipe mapped to the provided ID"""
    if (recipe := request.app.database["recipes"].find_one({"_id": id})) is not None:
        return recipe
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Recipe with ID {id} not found")

# Deprecated - Unused Route
# @router.get("/search/{ingredient}", response_description="List all recipes with the given ingredient", response_model=List[Recipe])
def list_recipes_by_ingregredient_old(ingredient: str,request: Request):

    """Lists recipes containing the given ingredient"""
    recipes = list(request.app.database["recipes"].find({"ingredients": {"$in": [ingredient]}}).limit(10))
    return recipes

# Deprecated - Replaced
# @router.post("/search-old/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
def list_recipes_by_ingredients_old(request: Request, inp: RecipeListRequest = Body(...)):
    """Deprecated - Lists recipes matching all provided ingredients"""
    # Goes into the recipes database, looks in all the ingredients of each to find ingredients matching inp.ing, sorts the recipes by rating and id, then gets 10 by page provided
    recipes = list(request.app.database["recipes"].find({ "ingredients" : { "$all" : inp.ingredients } }).sort([("rating", pymongo.DESCENDING), ("_id", pymongo.ASCENDING)]).skip((inp.page-1)*10).limit(10))
    # Counts how many documents there are in total in this list
    count = request.app.database["recipes"].count_documents({ "ingredients" : { "$all" : inp.ingredients } })
    # Creates a response with the list of 10 recipes, the current page, and the current count
    response = RecipeListResponse(recipes=recipes, page=inp.page, count=count)
    return response

# Deprecated - Replaced
# @router.get("/ingredients-old/{queryString}", response_description="List all ingredients", response_model=List[str])
def list_ingredients_old(queryString : str, request: Request):
    """Lists ingredient suggestions for a query"""
    # Pipeline to: get a list of all ingredients, from each record, match them by regex, and then limit it to only 20 suggestions. The accumulates these into one list
    pipeline = [{"$unwind": "$ingredients"}, {'$match': {'ingredients': {'$regex' : queryString}}}, {"$limit" : 20} ,{"$group": {"_id": "null", "ingredients": {"$addToSet": "$ingredients"}}}]

    data = list(request.app.database["recipes"].aggregate(pipeline))
    if len(data) <= 0:
        return []
    ings = data[0]["ingredients"]
    return ings

# Deprecated - Replaced
# @router.post("/search2-old/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
def list_recipes_by_ingredients_old(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Get a list of recipes up to 1000

    recipes = list(request.app.database["recipes"].find().limit(1000))
    res = []
    for recipe in recipes:
        # For each recipe, look at the the calories, fat, sugar, and protein
        if not recipe["calories"] or not recipe['fat'] or not recipe['sugar'] or not recipe['protein']:
            continue
        try:
            # find all the recipes that are lower than the maxes and report them
            if float(recipe["calories"]) < inp.caloriesMax and float(recipe["fat"]) < inp.fatMax and float(recipe["sugar"]) < inp.sugMax and float(recipe["protein"]) < inp.proMax:
                res.append(recipe)
        except:
            continue
    count = len(res)
    show = res[(inp.page-1)*10 : (inp.page)*10-1]
    response = RecipeListResponse(recipes=show, page=inp.page)
    return response

# Deprecated - Not in Use
# @router.get("/search2/{ingredient},{caloriesLow},{caloriesUp}", response_description="List all recipes with the given ingredient")
def list_recipes_by_ingredient_old(ingredient: str, caloriesLow: int, caloriesUp: int, request: Request):
    recipes = list(request.app.database["recipes"].find({ "ingredients" : { "$in" : [ingredient] } }))
    res = []
    for recipe in recipes:
        if not recipe["calories"]:
            continue
        if caloriesLow < float(recipe["calories"]) < caloriesUp:
            res.append(recipe)
    res.sort(key=lambda x: x['calories'])
    return res

# --------------------------------------------------------
# Shopping List Routes
# --------------------------------------------------------

# In Use - Refactored
@shoppingRouter.get("/{userId}", response_description="Get the current user's shopping list", status_code=200, response_model=List[ShoppingListItem])
async def get_shopping_list(request: Request, userId: int):
    """Retrieves the current user's shopping list."""
    db:Database_Connection = request.state.db

    try:
        return db.get_user_shopping_list(userId)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list."
        )
    
# In Use - Refactored
@shoppingRouter.put("/{userId}", response_description="Update the current user's shopping list", status_code=200)
async def update_shopping_list(request: Request, userId: int, listItem: ShoppingListItem = Body(...)):
    """Update the current user's shopping list."""
    db:Database_Connection = request.state.db
    try:
        res = db.update_shopping_list_item(userId, listItem.name, listItem.quantity, listItem.unit, listItem.checked)
        if(isinstance(res, str)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "User's shopping list was successfully updated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list."
        )
    
# In Use - Refactored
@shoppingRouter.post("/delete/{userId}", response_description="Remove an item from current user's shopping list", status_code=200)
async def remove_from_shopping_list(request: Request, userId: int, name: str = Body(...)):
    """Remove an item from the current user's shopping list."""
    db:Database_Connection = request.state.db
    try:
        res = db.remove_from_shopping_list(userId, name)
        if(isinstance(res, str)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "User's shopping list was successfully updated"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list."
        )

# --------------------------------------------------------
# Meal Plan Routes
# --------------------------------------------------------

# In Use - Refactored
@mealPlanRouter.get("/{userId}", response_description="Get the entire meal plan for the week", status_code=200)
async def get_meal_plan(userId: int, request: Request):
    """Retrieves the meal plan for the week."""
    db:Database_Connection = request.state.db
    try:
        return db.get_user_meal_plan(userId)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the meal plan."
        )

# In Use - Refactored
@mealPlanRouter.put("/{userId}", response_description="Add/Update an item for a user's meal plan on a specific day", status_code=200)
async def update_meal_plan(userId: int, request: Request, entry: MealPlanEntry = Body(...)):
    """Adds an item to the user's meal plan, or updates the current item at that day"""
    db:Database_Connection = request.state.db
    try:
        res = db.update_user_meal_plan(userId, entry.day, entry.recipe.recipeId)
        if(isinstance(res, str)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "Meal plan updated successfully."}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the meal plan"
        )

# In Use - New
@mealPlanRouter.post("/delete/{userId}", response_description="Get the entire meal plan for the week", status_code=200)
async def delete_from_meal_plan(request: Request, userId: int,  day: int = Body(...)):
    """Removes a meal plan item from a user's meal plan."""
    db:Database_Connection = request.state.db
    try:
        res = db.remove_from_user_meal_plan(userId, day)
        if(isinstance(res, str)):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "Meal plan updated successfully."}

    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while removing from the meal plan."
        )

# --------------------------------------------------------
# Recipes Search Routes
# --------------------------------------------------------

# In Use - New
@router.post("/search/count/", response_description="Get the count of all recipes that match the ingredients in the request", status_code=200, response_model=int)
async def count_recipes_by_ingredients(request: Request, inp: RecipeListRequest = Body(...)):
    """Total count of recipes matching the filter criteria"""
    db:Database_Connection = request.state.db
    count = db.get_count_recipes_by_ingredients(inp.ingredients)
    return count

# In Use - Refactored
@router.get("/search/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
async def list_recipes_by_ingredients(request: Request, inp: RecipeListRequest = Body(...)):
    """Lists recipes matching all provided ingredients"""
    db:Database_Connection = request.state.db
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    res = db.get_recipes_by_ingredient(inp.ingredients, inp.page - 1)
    return RecipeListResponse(recipes=res, page=inp.page)

# In Use - Refactored
@router.post("/search2/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
async def list_recipes_by_nutrition(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Get a page worth of recipes that have stats less than provided
    db:Database_Connection = request.state.db   
    res = db.get_recipes_by_nutrition(inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax, inp.page - 1)
    response = RecipeListResponse(recipes=res, page=inp.page)
    return response

# In Use - New
@router.post("/search2/count/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=int)
async def count_recipes_by_nutrition(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    db:Database_Connection = request.state.db
    count = db.get_count_recipes_by_nutrition(inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax)

    return count

# In Use - New
@router.get("/ingredients/{queryString}", response_description="List all ingredients", response_model=List[str])
async def list_ingredients(queryString : str, request: Request):
    """Lists ingredient suggestions for a query"""
    # Pipeline to: get a list of all ingredients, from each record, match them by regex, and then limit it to only 20 suggestions. The accumulates these into one list
    db:Database_Connection = request.state.db
    data = db.get_ingredient_list(queryString)
    if(len(data) <= 0):
        return []
    
    ings = [ing.replace("\"", "") for ingRecord in data for ing in ingRecord]
    return ings


# In Use - Good, no refactor needed
@router.post("/recommend-recipes/", response_model=dict)
async def recommend_recipes(request: Request, query: RecipeQuery = Body(...)):
    db:Database_Connection = request.state.db

    query.query = query.query.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').strip()
    query.context = query.context.strip()
    print(len(query.query))
    print(len(query.context))
    if not query.query or len(query.query) == 0 or len(query.context) == 0 or not query.context or query.query.isdigit() or not any(c.isalpha() for c in query.query):
        print("GOT HERE")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Query or Context")

    try:
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

# --------------------------------------------------------
# User Routes
# --------------------------------------------------------

@userRouter.post("/signup")
async def signup(request: Request, incomingUser: UserCred = Body(...)):
    db:Database_Connection = request.state.db
    user: User = User(incomingUser.username, incomingUser.password)
    if db.get_user_by_name(user.Username) is not None:
        raise HTTPException(status_code=400, detail="User with that username already exists")
    userid: int = db.add_user(user)
    return {"id": userid, "username": user.Username}

@userRouter.post("/login")
async def login(request: Request, incomingUser: UserCred = Body(...)):
    db:Database_Connection = request.state.db
    user: User = db.get_user_by_name(incomingUser.username)
    if user is None:
        raise HTTPException(status_code=400, detail="There is no user with that username")
    if user.Password == incomingUser.password:
        return {"id": user.UserId, "username": user.Username}
        
    return "Incorrect Username or Password"
    # except:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured when logging in this user")
    
    raise HTTPException(status_code=401, detail="Incorrect Username or Password")

@userRouter.get("/getUser/{username}")
async def getUser(request: Request, username: str) -> dict:
    db:Database_Connection = request.state.db
    user: User = db.get_user_by_name(username)
    if user is None:
        raise HTTPException(status_code=400, detail="There is no user with that username")
    return user.to_dict()

# --------------------------------------------------------
# User Recipe Routes
# --------------------------------------------------------

@router.get("/{recipeId}")
async def get_recipe(request: Request, recipeId: int) -> Recipe:
    db:Database_Connection = request.state.db
    print(f"getting {recipeId}")
    recipe: Recipe = db.get_recipe(recipeId)
    if recipe is None:
        raise HTTPException(status_code=404, detail="There is not recipe with that Id")
    return recipe

@router.get("/batch")
async def get_recipes(request: Request, recipeIds: List[int]) -> Recipe:
    db:Database_Connection = request.state.db
    recipes = {}
    for recipeId in recipeIds:
        recipe: Recipe = db.get_recipe(recipeId)
        recipes[recipeId] = recipe
    if recipes is None:
        raise HTTPException(status_code=400, detail="There is no recipes with those Ids")
    return recipes

# Todo: This may have to change as I am not sure if this is the proper way to expect a body for a post request
@router.post("/")
async def create_user_recipe(request: Request, recipeObject: Recipe, userId: int) -> bool:
    db:Database_Connection = request.state.db
    success = db.create_recipe(recipeObject, userId)
    if success:
        return True
    
    return False

@router.put("/{recipeId}")
async def update_user_recipe(request: Request, recipeId: int, newRecipe: Recipe, userId: int):
    db:Database_Connection = request.state.db
    recipes = db.get_recipes_owned_by_userId(userId)

    if (any(recipe.recipeId == recipeId for recipe in recipes)):
        success = db.update_recipe(recipeId, newRecipe)
        # Todo: Prob need to add a check here to make sure that we are the owner of the recipe to change it
        if success:
            return True
    
    return False


@router.put("/favorite/{recipeId}/{userId}")
async def favorite_recipe(request: Request, recipeId: int, userId: int):
    db:Database_Connection = request.state.db
    success: bool = db.favorite_recipe(userId, recipeId)
    if success:
        return True
    
    return False

@router.put("/unfavorite/{recipeId}/{userId}")
async def unfavorite_recipe(request: Request, recipeId: int, userId: int):
    db:Database_Connection = request.state.db
    success: bool = db.unfavorite_recipe(userId, recipeId)
    if success:
        return True
    
    return False


# --------------------------------------------------------
# Updated Post Routes
# --------------------------------------------------------

# Updated Post Routes
@postRouter.post("/", response_description="Create a new post", status_code=201)
async def create_post(request: Request, post: Post):
    """Creates a new post in the database."""
    db:Database_Connection = request.state.db
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
async def get_post(request: Request, post_id: int):
    """Retrieves a post by its ID."""
    db:Database_Connection = request.state.db
    post = db.get_post(post_id)
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with ID {post_id} not found."
    )

@postRouter.get("/", response_description="List all posts", response_model=List[Post])
async def list_posts(request: Request, ):
    """Retrieves all posts from the database."""
    db:Database_Connection = request.state.db
    posts = db.get_all_posts()
    return posts

@postRouter.get("/user/{user_id}", response_description="List all posts by a user", response_model=List[Post])
async def get_user_posts(request: Request, user_id: int):
    """Retrieves all posts by a specific user from the database."""
    db:Database_Connection = request.state.db
    posts = db.get_all_posts()
    user_posts = [post for post in posts if post.userId == user_id]
    return user_posts

@postRouter.put("/like/{post_id}", response_description="Like a post", status_code=200)
async def like_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Handles liking a post with toggle and switch logic."""
    db:Database_Connection = request.state.db
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


@postRouter.put("/dislike/{post_id}", response_description="Dislike a post", status_code=200)
async def dislike_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Handles disliking a post with toggle and switch logic."""
    db:Database_Connection = request.state.db
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

async def delete_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Deletes a post by its ID, including all related reactions."""
    db:Database_Connection = request.state.db
    try:
        post = db.get_post(post_id)

        if post.userId != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Post with ID {post_id} does not belong to user {user_id}"
            )

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

@router.get("/user/{userId}")
async def get_user_recipes(request: Request, userId: int):
    db: Database_Connection = request.state.db
    recipeIds: list[int] = db.get_recipes_owned_by_userId(userId)
    recipeObj: list[dict] = []
    for recipeId in recipeIds:
        recipeObj.append(db.get_recipe(recipeId).to_dict())
    
    # This should be fine as if there are no recipes owned by a user it should just return the empty list
    # Can be changed to None if needed
    return recipeObj

@postRouter.put("/{post_id}", response_description="Update a post", response_model=Post)
async def update_post(request: Request, post_id: int, update: PostUpdate = Body(...)):
    """Allows a user to edit their own post's message, image, or recipe."""
    db:Database_Connection = request.state.db
    try:
        # Fetch the existing post
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found."
            )
        
        # Check if the user owns the post
        if post.userId != update.userId:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You can only edit your own posts."
            )
        
        # Check if the user exists
        if db.get_user_by_id(update.userId) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {update.userId} not found."
            )       
        
        
        # Prepare update data (only include fields that were provided)
        update_data = {}
        if update.message is not None:
            update_data["Message"] = update.message
        if update.image is not None:
            update_data["Image"] = update.image
        if update.recipe.recipeId is not None:
            update_data["RecipeId"] = update.recipe.recipeId
        
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
        if Exception is HTTPException: 
            raise e
        else:
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail=f"An error occurred while updating the post: {str(e)}"
            )

@postRouter.post("/comments/{post_id}", response_description="Add a comment to a post", status_code=201)
async def add_comment(request: Request, post_id: int, comment: Comment):
    """Adds a new comment to a post and returns the CommentId."""
    db:Database_Connection = request.state.db
    # Ensure the comment's postId matches the URL parameter
    comment.postId = post_id
    # Check if the post exists
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found."
        )
    # Check if the user exists
    if db.get_user_by_id(comment.userId) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {comment.userId} not found."
        )
    # Add the comment and get the CommentId
    comment_id = db.add_comment(comment)
    if comment_id:
        return {"message": "Comment added successfully", "commentId": comment_id}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to add comment."
        )

@postRouter.delete("/comments/{comment_id}", response_description="Delete a comment", status_code=200)
async def delete_comment(request: Request, comment_id: int, postId: int = Body(..., embed=True), userId: int = Body(..., embed=True)):
    """Deletes a comment by its CommentId, ensuring the user owns it."""
    db:Database_Connection = request.state.db
    # Check if the post exists
    post = db.get_post(postId)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {postId} not found."
        )
    # Check if the user exists
    user = db.get_user_by_id(userId)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {userId} not found."
        )
    # Fetch comments to verify ownership
    comments = db.get_post_comments(postId)
    comment = next((c for c in comments if c.commentId == comment_id), None)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found for post {postId}."
        )
    if comment.userId != userId:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments."
        )
    # Delete the comment
    if db.delete_comment(comment_id):
        return {"message": "Comment deleted successfully"}
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to delete comment."
        )