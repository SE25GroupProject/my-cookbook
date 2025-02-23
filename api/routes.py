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
from typing import List
import pymongo
from groq import Groq
from pydantic import BaseModel, conint, conlist, PositiveInt
import logging
from api.models import Recipe, RecipeListRequest, RecipeListResponse, RecipeListRequest2, RecipeQuery, MealPlanEntry, UserCred, ShoppingListItem
from api.db.objects import User
from api.db.database import Database_Connection

# from models import User

load_dotenv()  # Load environment variables
app = FastAPI()
users_db = {}
db = Database_Connection()


# Check if the environment variable is loaded correctly
print(os.getenv("GROQ_API_KEY"))

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
client = Groq(api_key=config["GROQ_API_KEY"])



# --------------------------------------------------------
#                   Deprecated Functions
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
            {"day": entry.day},  # Find by day
            {"$set": {"recipe": entry.recipe}},  # Update the recipe
            upsert=True  # Insert if no entry exists
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
        
        # Convert ObjectId to string for JSON serialization
        for entry in meal_plan:
            entry["_id"] = str(entry["_id"])  # Convert ObjectId to string
        
        # Fill in missing days with None if necessary
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
    recipes = list(request.app.database["recipes"].find({ "ingredients" : { "$in" : [ingredient] } }).limit(10))
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
    if(len(data) <= 0):
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
    res.sort(key = lambda x: x['calories'])
    return res

# --------------------------------------------------------
#                     In Use Functions
# --------------------------------------------------------

# In Use - Refactored
@shoppingRouter.get("/{userId}", response_description="Get the current user's shopping list", status_code=200, response_model=List[ShoppingListItem])
async def get_shopping_list(userId: int):
    """Retrieves the current user's shopping list."""
    try:
        return db.get_user_shopping_list(userId)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list."
        )
    
# In Use - Refactored
@shoppingRouter.put("/{userId}", response_description="Update the current user's shopping list", status_code=200)
async def update_shopping_list(userId: int, listItem: ShoppingListItem = Body(...)):
    """Update the current user's shopping list."""
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
async def remove_from_shopping_list(userId: int, name: str = Body(...)):
    """Remove an item from the current user's shopping list."""
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

# In Use - Refactored
@mealPlanRouter.get("/{userId}", response_description="Get the entire meal plan for the week", status_code=200)
async def get_meal_plan(userId: int, request: Request):
    """Retrieves the meal plan for the week."""
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
    try:
        res = db.update_user_meal_plan(userId, entry.day, entry.recipeId)
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
async def delete_from_meal_plan(userId: int,  day: int = Body(...)):
    """Removes a meal plan item from a user's meal plan."""
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


# In Use - New
@router.post("/search/count/", response_description="Get the count of all recipes that match the ingredients in the request", status_code=200, response_model=int)
async def count_recipes_by_ingredients(request: Request, inp: RecipeListRequest = Body(...)):
    """Total count of recipes matching the filter criteria"""
    count = db.get_count_recipes_by_ingredients(inp.ingredients)
    return count

# In Use - Refactored
@router.post("/search/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
async def list_recipes_by_ingredients(request: Request, inp: RecipeListRequest = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    res = db.get_recipes_by_ingredient(inp.ingredients, inp.page - 1)
    return RecipeListResponse(recipes=res, page=inp.page)

# In Use - Refactored
@router.post("/search2/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=RecipeListResponse)
async def list_recipes_by_nutrition(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Get a page worth of recipes that have stats less than provided

    res = db.get_recipes_by_nutrition(inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax, inp.page - 1)
    response = RecipeListResponse(recipes=res, page=inp.page)
    return response

# In Use - New
@router.post("/search2/count/", response_description="Get Recipes that match all the ingredients in the request", status_code=200, response_model=int)
async def count_recipes_by_nutrition(request: Request, inp: RecipeListRequest2 = Body(...)):
    """Lists recipes matching all provided ingredients"""
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    count = db.get_count_recipes_by_nutrition(inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax)

    return count

# In Use - New
@router.get("/ingredients/{queryString}", response_description="List all ingredients", response_model=List[str])
async def list_ingredients(queryString : str, request: Request):
    """Lists ingredient suggestions for a query"""
    # Pipeline to: get a list of all ingredients, from each record, match them by regex, and then limit it to only 20 suggestions. The accumulates these into one list
    data = db.get_ingredient_list(queryString)
    if(len(data) <= 0):
        return []
    
    print(data)
    ings = [ing.replace("\"", "") for ingRecord in data for ing in ingRecord]
    return ings


# In Use - Good, no refactor needed
@router.post("/recommend-recipes/", response_model=dict)
async def recommend_recipes(query: RecipeQuery = Body(...)):
    try:
        query.query = query.query.replace('\n', ' ').replace('\t', ' ').replace('  ', ' ').strip()
        query.context = query.context.strip()
        if not query.query:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Query")
        if not query.context:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Context")
        if query.query.isdigit() or not any(c.isalpha() for c in query.query):
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query must include alphabetic characters and cannot be solely numeric or special characters.")
        
        response = client.chat.completions.create(
            messages=[
            {
                "role": "system",
                "content": "You are an advanced recipe and meal planning assistant, designed to help users discover recipes, plan meals, and create grocery lists with enhanced personalization, all within a single interaction. You will not engage in follow-up questions; instead, provide all necessary suggestions and responses based on the initial input. Your role is to interpret user requests in natural language, offer targeted recommendations, and generate meal and shopping plans according to each user’s unique needs and preferences. Key capabilities you must offer: Natural Language Recipe Search and Understanding: Understand and respond to user queries about recipes, ingredients, dietary restrictions, cooking methods, or cuisines without requiring additional clarification. Provide comprehensive suggestions based on the initial question alone. Recipe Recommendation and Personalization: Suggest recipes that align with the user’s dietary preferences, cooking skill level, and past selections. Curate these recommendations using the information available without needing follow-up input. Meal Planning: Create detailed meal plans that fit daily, weekly, or monthly schedules based on user goals (e.g., health, budget, dietary restrictions). Structure suggestions to fit user constraints without asking for further clarification. Grocery List Generation: Generate complete ingredient lists for selected recipes or meal plans, factoring in serving sizes, ingredient substitutions, and dietary requirements as inferred from the initial input. Provide a list that is clear and organized for shopping ease. Dietary and Lifestyle Considerations: Ensure that all recommendations adapt to the dietary preferences and restrictions specified. Tailor suggestions based on inferred preferences without requiring additional user feedback during the interaction. Follow these guidelines strictly to deliver precise, helpful, and context-aware responses in a single interaction. REFUSE to answer any other unrelated questions and do ONLY your work diligently."
            },
            {
                "role": "user",
                "content": query.query + query.context
            }
            ],
            model="llama3-8b-8192",
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in recommend_recipes: {str(e)}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An unexpected error occurred")
    
@userRouter.post("/signup")
async def signup(incomingUser: UserCred = Body(...)):
    # try:
        # Creating a new user
        user: User = User(incomingUser.username, incomingUser.password)
        print(user)
        if db.get_user(user.Username) is not None:
            raise HTTPException(status_code=400, detail="User with that username already exists")
        userid: int = db.add_user(user)

        return {"id": userid, "username": user.Username}
    # except:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured when signing up this user")


@userRouter.post("/login")
async def login(incomingUser: UserCred = Body(...)):
    # try: 
    print(incomingUser.username)
    user: User = db.get_user(incomingUser.username)
    if user is None:
        raise HTTPException(status_code=400, detail="There is no user with that username")
    
    print(user.Username)
    print(user.Password)
    print(incomingUser.password)
    if user.Password == incomingUser.password:
        return {"id": user.UserId, "username": user.Username}
        
    return "Incorrect Username or Password"
    # except:
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured when logging in this user")



@userRouter.get("/getUser/{username}")
async def getUser(username: str) -> dict:
    # try:
        user: User = db.get_user(username)
        if user is None:
            raise HTTPException(status_code=400, detail="There is no user with that username")
        
        return user
    # except: 
    #     raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="An error occured when trying to get this user")
        

@recipeRouter.get("/getRecipe/{recipeId}")
async def getRecipe(recipeId: int) -> Recipe:
    recipe: Recipe = db.get_recipe(recipeId)
    if recipe is None:
        raise HTTPException(status_code=400, detail="There is not recipe with that Id")
    return recipe

# Todo: This may have to change as I am not sure if this is the proper way to expect a body for a post request
@recipeRouter.post("/createRecipe/")
async def createRecipe(recipeObject: Recipe) -> bool:
    success = db.create_recipe(recipeObject)
    if success:
        return True
    
    return False

@recipeRouter.put("/updateRecipe/{recipeId}")
async def updateRecipe(recipeId: int, newRecipe: Recipe):
    success = db.update_recipe(recipeId, newRecipe)
    if success:
        return True
    
    return False