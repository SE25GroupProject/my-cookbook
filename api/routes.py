"""
Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com
"""

from sqlite3 import DatabaseError
import sys
import os
import logging
from typing import List
from dotenv import load_dotenv
from fastapi import APIRouter, Body, Request, HTTPException, status
from groq import Groq
from api.models import (
    Recipe,
    RecipeListRequest,
    RecipeListResponse,
    RecipeListRequest2,
    RecipeQuery,
    MealPlanEntry,
    UserCred,
    ShoppingListItem,
    PostUpdate,
    Post,
    Comment,
)
from api.db.objects import User
from api.db.database import DatabaseConnection

sys.path.insert(0, "../")

load_dotenv()  # Load environment variables

# pylint: disable=W0707
# pylint: disable=C0301
# pylint: disable=W1203
# pylint: disable=R0916

users_db = {}
database_con = DatabaseConnection()

config = {
    "ATLAS_URI": os.getenv("ATLAS_URI"),
    "DB_NAME": os.getenv("DB_NAME"),
    "GROQ_API_KEY": os.getenv("GROQ_API_KEY"),
    "PORT": os.getenv("PORT"),
}
router = APIRouter()
userRouter = APIRouter()
recipeRouter = APIRouter()
mealPlanRouter = APIRouter()
shoppingRouter = APIRouter()
postRouter = APIRouter()
client = Groq(api_key=config["GROQ_API_KEY"])

# --------------------------------------------------------
# Shopping List Routes
# --------------------------------------------------------


# In Use - Refactored
@shoppingRouter.get(
    "/{userId}",
    response_description="Get the current user's shopping list",
    status_code=200,
    response_model=List[ShoppingListItem],
)
async def get_shopping_list(request: Request, user_id: int):
    """Retrieves the current user's shopping list."""
    db: DatabaseConnection = request.state.db

    try:
        return db.get_user_shopping_list(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list.",
        )


# In Use - Refactored
@shoppingRouter.put(
    "/{userId}",
    response_description="Update the current user's shopping list",
    status_code=200,
)
async def update_shopping_list(
    request: Request, user_id: int, list_item: ShoppingListItem = Body(...)
):
    """Update the current user's shopping list."""
    db: DatabaseConnection = request.state.db
    try:
        res = db.update_shopping_list_item(
            user_id,
            list_item.name,
            list_item.quantity,
            list_item.unit,
            list_item.checked,
        )
        if isinstance(res, str):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "User's shopping list was successfully updated"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list.",
        )


# In Use - Refactored
@shoppingRouter.post(
    "/delete/{userId}",
    response_description="Remove an item from current user's shopping list",
    status_code=200,
)
async def remove_from_shopping_list(
    request: Request, user_id: int, name: str = Body(...)
):
    """Remove an item from the current user's shopping list."""
    db: DatabaseConnection = request.state.db
    try:
        res = db.remove_from_shopping_list(user_id, name)
        if isinstance(res, str):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "User's shopping list was successfully updated"}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the shopping list.",
        )


# --------------------------------------------------------
# Meal Plan Routes
# --------------------------------------------------------


# In Use - Refactored
@mealPlanRouter.get(
    "/{userId}",
    response_description="Get the entire meal plan for the week",
    status_code=200,
)
async def get_meal_plan(user_id: int, request: Request):
    """Retrieves the meal plan for the week."""
    db: DatabaseConnection = request.state.db
    try:
        return db.get_user_meal_plan(user_id)
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while retrieving the meal plan.",
        )


# In Use - Refactored
@mealPlanRouter.put(
    "/{userId}",
    response_description="Add/Update an item for a user's meal plan on a specific day",
    status_code=200,
)
async def update_meal_plan(
    user_id: int, request: Request, entry: MealPlanEntry = Body(...)
):
    """Adds an item to the user's meal plan, or updates the current item at that day"""
    db: DatabaseConnection = request.state.db
    try:
        res = db.update_user_meal_plan(user_id, entry.day, entry.recipe.recipeId)
        if isinstance(res, str):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "Meal plan updated successfully."}
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while updating the meal plan",
        )


# In Use - New
@mealPlanRouter.post(
    "/delete/{userId}",
    response_description="Get the entire meal plan for the week",
    status_code=200,
)
async def delete_from_meal_plan(request: Request, user_id: int, day: int = Body(...)):
    """Removes a meal plan item from a user's meal plan."""
    db: DatabaseConnection = request.state.db
    try:
        res = db.remove_from_user_meal_plan(user_id, day)
        if isinstance(res, str):
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=res)
        return {"message": "Meal plan updated successfully."}

    except Exception:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An error occurred while removing from the meal plan.",
        )


# --------------------------------------------------------
# Recipes Search Routes
# --------------------------------------------------------


# In Use - New
@router.post(
    "/search/count/",
    response_description="Get the count of all recipes that match the ingredients in the request",
    status_code=200,
    response_model=int,
)
async def count_recipes_by_ingredients(
    request: Request, inp: RecipeListRequest = Body(...)
):
    """Total count of recipes matching the filter criteria"""
    db: DatabaseConnection = request.state.db
    count = db.get_count_recipes_by_ingredients(inp.ingredients)
    return count


# In Use - Refactored
@router.post(
    "/search/",
    response_description="Get Recipes that match all the ingredients in the request",
    status_code=200,
    response_model=RecipeListResponse,
)
async def list_recipes_by_ingredients(
    request: Request, inp: RecipeListRequest = Body(...)
):
    """Lists recipes matching all provided ingredients"""
    db: DatabaseConnection = request.state.db
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    res = db.get_recipes_by_ingredient(inp.ingredients, inp.page - 1)
    return RecipeListResponse(recipes=res, page=inp.page)


# In Use - Refactored
@router.post(
    "/search2/",
    response_description="Get Recipes that match all the ingredients in the request",
    status_code=200,
    response_model=RecipeListResponse,
)
async def list_recipes_by_nutrition(
    request: Request, inp: RecipeListRequest2 = Body(...)
):
    """Lists recipes matching all provided ingredients"""
    # Get a page worth of recipes that have stats less than provided
    db: DatabaseConnection = request.state.db
    res = db.get_recipes_by_nutrition(
        inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax, inp.page - 1
    )
    response = RecipeListResponse(recipes=res, page=inp.page)
    return response


# In Use - New
@router.post(
    "/search2/count/",
    response_description="Get Recipes that match all the ingredients in the request",
    status_code=200,
    response_model=int,
)
async def count_recipes_by_nutrition(
    request: Request, inp: RecipeListRequest2 = Body(...)
):
    """Lists recipes matching all provided ingredients"""
    # Request list of recipes that have {ing} in the ingredients list with limit and offset. Sort these by rating and id.
    db: DatabaseConnection = request.state.db
    count = db.get_count_recipes_by_nutrition(
        inp.caloriesMax, inp.fatMax, inp.sugMax, inp.proMax
    )

    return count


# In Use - New
@router.get(
    "/ingredients/{queryString}",
    response_description="List all ingredients",
    response_model=List[str],
)
async def list_ingredients(query_string: str, request: Request):
    """Lists ingredient suggestions for a query"""
    # Pipeline to: get a list of all ingredients, from each record, match them by regex, and then limit it to only 20 suggestions. The accumulates these into one list
    db: DatabaseConnection = request.state.db
    data = db.get_ingredient_list(query_string)
    if len(data) <= 0:
        return []

    ings = [ing.replace('"', "") for ingRecord in data for ing in ingRecord]
    return ings


# In Use - Good, no refactor needed
@router.post("/recommend-recipes/", response_model=dict)
async def recommend_recipes(query: RecipeQuery = Body(...)):
    """Recommend recipes based on a query and context."""
    query.query = (
        query.query.replace("\n", " ").replace("\t", " ").replace("  ", " ").strip()
    )
    query.context = query.context.strip()
    print(len(query.query))
    print(len(query.context))
    if (
        not query.query
        or len(query.query) == 0
        or len(query.context) == 0
        or not query.context
        or query.query.isdigit()
        or not any(c.isalpha() for c in query.query)
    ):
        print("GOT HERE")
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid Query or Context"
        )

    try:
        response = client.chat.completions.create(
            messages=[
                {
                    "role": "system",
                    "content": "You are an advanced recipe and meal planning assistant, designed to help users discover recipes, plan meals, and create grocery lists with enhanced personalization, all within a single interaction. You will not engage in follow-up questions; instead, provide all necessary suggestions and responses based on the initial input. Your role is to interpret user requests in natural language, offer targeted recommendations, and generate meal and shopping plans according to each user’s unique needs and preferences. Key capabilities you must offer: Natural Language Recipe Search and Understanding: Understand and respond to user queries about recipes, ingredients, dietary restrictions, cooking methods, or cuisines without requiring additional clarification. Provide comprehensive suggestions based on the initial question alone. Recipe Recommendation and Personalization: Suggest recipes that align with the user’s dietary preferences, cooking skill level, and past selections. Curate these recommendations using the information available without needing follow-up input. Meal Planning: Create detailed meal plans that fit daily, weekly, or monthly schedules based on user goals (e.g., health, budget, dietary restrictions). Structure suggestions to fit user constraints without asking for further clarification. Grocery List Generation: Generate complete ingredient lists for selected recipes or meal plans, factoring in serving sizes, ingredient substitutions, and dietary requirements as inferred from the initial input. Provide a list that is clear and organized for shopping ease. Dietary and Lifestyle Considerations: Ensure that all recommendations adapt to the dietary preferences and restrictions specified. Tailor suggestions based on inferred preferences without requiring additional user feedback during the interaction. Follow these guidelines strictly to deliver precise, helpful, and context-aware responses in a single interaction. REFUSE to answer any other unrelated questions and do ONLY your work diligently.",
                },
                {"role": "user", "content": query.query + query.context},
            ],
            model="llama3-8b-8192",
        )
        return {"response": response.choices[0].message.content}
    except Exception as e:
        logging.basicConfig(level=logging.ERROR)
        logger = logging.getLogger(__name__)
        logger.error(f"Unexpected error in recommend_recipes: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="An unexpected error occurred",
        )


# --------------------------------------------------------
# User Routes
# --------------------------------------------------------


@userRouter.post("/signup")
async def signup(request: Request, incoming_user: UserCred = Body(...)):
    """Creates a new user in the database."""
    db: DatabaseConnection = request.state.db
    if len(incoming_user.username) == 0 or len(incoming_user.password) == 0:
        raise HTTPException(
            status_code=400, detail="Username and Password cannot be empty"
        )
    user: User = User(incoming_user.username, incoming_user.password)
    if db.get_user_by_name(user.Username) is not None:
        raise HTTPException(
            status_code=400, detail="User with that username already exists"
        )
    userid: int = db.add_user(user)
    return {"id": userid, "username": user.Username}


@userRouter.post("/login")
async def login(request: Request, incoming_user: UserCred = Body(...)):
    """Logs a user in."""
    db: DatabaseConnection = request.state.db
    user: User = db.get_user_by_name(incoming_user.username)
    if user is None:
        raise HTTPException(
            status_code=400, detail="There is no user with that username"
        )
    if user.Password == incoming_user.password:
        return {"id": user.UserId, "username": user.Username}

    raise HTTPException(status_code=400, detail="Incorrect Username or Password")


@userRouter.get("/getUser/{username}", status_code=200)
async def get_user(request: Request, username: str) -> dict:
    """Retrieves a user by their username."""
    db: DatabaseConnection = request.state.db
    user: User = db.get_user_by_name(username)
    print(username)
    if user is None:
        raise HTTPException(
            status_code=400, detail="There is no user with that username"
        )
    return user.to_dict()


# --------------------------------------------------------
# User Recipe Routes
# --------------------------------------------------------


@router.get("/{recipeId}")
async def get_recipe(request: Request, recipe_id: int) -> Recipe:
    """Retrieves a recipe by its ID."""
    db: DatabaseConnection = request.state.db
    print(f"getting {recipe_id}")
    recipe: Recipe = db.get_recipe(recipe_id)
    if recipe is None:
        raise HTTPException(status_code=404, detail="There is not recipe with that Id")
    return recipe


@router.get("/batch")
async def get_recipes(request: Request, recipe_ids: List[int]) -> Recipe:
    """Retrieves a batch of recipes by their IDs."""
    db: DatabaseConnection = request.state.db
    recipes = {}
    for recipe_id in recipe_ids:
        recipe: Recipe = db.get_recipe(recipe_id)
        recipes[recipe_id] = recipe
    if recipes is None:
        raise HTTPException(
            status_code=400, detail="There is no recipes with those Ids"
        )
    return recipes


@router.post("/")
async def create_user_recipe(
    request: Request, recipe_object: Recipe, user_id: int
) -> bool:
    """Creates a new recipe in the database."""
    db: DatabaseConnection = request.state.db
    success = db.create_recipe(recipe_object, user_id)
    if success:
        return True

    return False


@router.put("/{recipeId}")
async def update_user_recipe(
    request: Request, recipe_id: int, new_recipe: Recipe, user_id: int
):
    """Updates a recipe in the database."""
    db: DatabaseConnection = request.state.db
    recipes = db.get_recipes_owned_by_user_id(user_id)

    if any(recipe.recipeId == recipe_id for recipe in recipes):
        success = db.update_recipe(recipe_id, new_recipe)
        if success:
            return True

    return False


@router.put("/favorite/{recipeId}/{userId}")
async def favorite_recipe(request: Request, recipe_id: int, user_id: int):
    """Favorites a recipe for a user."""
    db: DatabaseConnection = request.state.db
    success: bool = db.favorite_recipe(user_id, recipe_id)
    if success:
        return True

    return False


@router.put("/unfavorite/{recipeId}/{userId}")
async def unfavorite_recipe(request: Request, recipe_id: int, user_id: int):
    """Unfavorites a recipe for a user."""
    db: DatabaseConnection = request.state.db
    success: bool = db.unfavorite_recipe(user_id, recipe_id)
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
    db: DatabaseConnection = request.state.db
    try:
        print(post)
        if db.add_post(post):
            return {"message": "Post created successfully."}
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Failed to create post.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while creating the post: {str(e)}",
        )


@postRouter.get(
    "/{post_id}", response_description="Get a post by ID", response_model=Post
)
async def get_post(request: Request, post_id: int):
    """Retrieves a post by its ID."""
    db: DatabaseConnection = request.state.db
    post = db.get_post(post_id)
    if post:
        return post
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"Post with ID {post_id} not found.",
    )


@postRouter.get("/", response_description="List all posts", response_model=List[Post])
async def list_posts(
    request: Request,
):
    """Retrieves all posts from the database."""
    db: DatabaseConnection = request.state.db
    posts = db.get_all_posts()
    print(posts)
    return posts


@postRouter.get(
    "/user/{user_id}",
    response_description="List all posts by a user",
    response_model=List[Post],
)
async def get_user_posts(request: Request, user_id: int):
    """Retrieves all posts by a specific user from the database."""
    db: DatabaseConnection = request.state.db
    posts = db.get_all_posts()
    user_posts = [post for post in posts if post.userId == user_id]
    return user_posts


@postRouter.put("/like/{post_id}", response_description="Like a post", status_code=200)
async def like_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Handles liking a post with toggle and switch logic."""
    db: DatabaseConnection = request.state.db
    try:
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found.",
            )
        if db.get_user_by_id(user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} not found.",
            )

        # Check current reaction
        current_likes = db.get_post_reactions(post_id, "LIKE")
        current_dislikes = db.get_post_reactions(post_id, "DISLIKE")

        if user_id in current_likes:
            # User already liked it, so remove the like (toggle off)
            if db.remove_post_reaction(post_id, user_id):
                return {"message": "Like removed successfully."}
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove like.",
            )
        if user_id in current_dislikes:
            # User disliked it, remove dislike and add like
            if db.remove_post_reaction(post_id, user_id) and db.add_post_reaction(
                post_id, user_id, "LIKE"
            ):
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
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while liking the post: {str(e)}",
        )


@postRouter.put(
    "/dislike/{post_id}", response_description="Dislike a post", status_code=200
)
async def dislike_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Handles disliking a post with toggle and switch logic."""
    db: DatabaseConnection = request.state.db
    try:
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Post with ID {post_id} not found.",
            )
        if db.get_user_by_id(user_id) is None:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"User with ID {user_id} not found.",
            )

        # Check current reaction
        current_likes = db.get_post_reactions(post_id, "LIKE")
        current_dislikes = db.get_post_reactions(post_id, "DISLIKE")

        if user_id in current_dislikes:
            # User already disliked it, so remove the dislike (toggle off)
            if db.remove_post_reaction(post_id, user_id):
                return {"message": "Dislike removed successfully."}
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Failed to remove dislike.",
            )
        if user_id in current_likes:
            # User liked it, remove like and add dislike
            if db.remove_post_reaction(post_id, user_id) and db.add_post_reaction(
                post_id, user_id, "DISLIKE"
            ):
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
    except HTTPException as e:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while disliking the post: {str(e)}",
        )

@postRouter.delete("/{post_id}", response_description="Delete a post", status_code=200)
async def delete_post(request: Request, post_id: int, user_id: int = Body(...)):
    """Deletes a post by its ID, including all related reactions."""
    db: DatabaseConnection = request.state.db
    try:
        post = db.get_post(post_id)
        print(post)

        if post.userId != user_id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Post with ID {post_id} does not belong to user {user_id}",
            )

        if db.delete_post(post_id):
            return {"message": "Post deleted successfully."}
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found.",
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"An error occurred while deleting the post: {str(e)}",
        )


@router.get("/user/{userId}")
async def get_user_recipes(request: Request, user_id: int):
    """Retrieves all recipes owned by a user."""
    db: DatabaseConnection = request.state.db
    recipe_ids: list[int] = db.get_recipes_owned_by_user_id(user_id)
    recipe_obj: list[dict] = []
    for recipe_id in recipe_ids:
        recipe_obj.append(db.get_recipe(recipe_id).to_dict())

    # This should be fine as if there are no recipes owned by a user it should just return the empty list
    # Can be changed to None if needed
    return recipe_obj


@postRouter.put("/{post_id}", response_description="Update a post", response_model=Post)
async def update_post(request: Request, post_id: int, update: PostUpdate = Body(...)):
    """Allows a user to edit their own post's message, image, or recipe."""
    db: DatabaseConnection = request.state.db
    try:
        post = db.get_post(post_id)
        if not post:
            raise HTTPException(status_code=404, detail=f"Post with ID {post_id} not found.")
        # Check if the user owns the post
        if post.userId != update.userId:
            raise HTTPException(status_code=403, detail="You can only edit your own posts.")
        # Check if the user exists
        if db.get_user_by_id(update.userId) is None:
            raise HTTPException(status_code=400, detail=f"User with ID {update.userId} not found.")
        # Prepare update data (only include fields that were provided)
        update_data = {}
        if update.message is not None:
            update_data["Message"] = update.message
        if update.image is not None:
            update_data["Image"] = update.image
        # Check if recipe exists before accessing recipeId
        if update.recipe is not None and update.recipe.recipeId is not None:
            update_data["RecipeId"] = update.recipe.recipeId
        
        if not update_data:
            return post
        
        if not db.update_post(post_id, update_data):
            raise HTTPException(status_code=500, detail="Failed to update post.")
        
        updated_post = db.get_post(post_id)
        return updated_post
    
    except HTTPException as e:
        raise
    except Exception as e:
        print(f"Error: {type(e).__name__} - {str(e)}")
        raise HTTPException(status_code=500, detail=f"An error occurred while updating the post: {type(e).__name__}: {str(e)}")
    
@postRouter.post("/comments/{post_id}", response_description="Add a comment to a post", status_code=201)
async def add_comment(request: Request, post_id: int, comment: Comment):
    """Adds a new comment to a post and returns the CommentId."""
    db: DatabaseConnection = request.state.db
    # Ensure the comment's postId matches the URL parameter
    comment.postId = post_id
    # Check if the post exists
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found.",
        )
    # Check if the user exists
    if db.get_user_by_id(comment.userId) is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {comment.userId} not found.",
        )
    # Add the comment and get the CommentId
    comment_id = db.add_comment(comment)
    if comment_id:
        return {"message": "Comment added successfully", "commentId": comment_id}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to add comment.",
    )


@postRouter.delete(
    "/comments/{comment_id}", response_description="Delete a comment", status_code=200
)
async def delete_comment(
    request: Request,
    comment_id: int,
    post_id: int = Body(..., embed=True),
    user_id: int = Body(..., embed=True),
):
    """Deletes a comment by its CommentId, ensuring the user owns it."""
    db: DatabaseConnection = request.state.db
    # Check if the post exists
    post = db.get_post(post_id)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with ID {post_id} not found.",
        )
    # Check if the user exists
    user = db.get_user_by_id(user_id)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"User with ID {user_id} not found.",
        )
    # Fetch comments to verify ownership
    comments = db.get_post_comments(post_id)
    comment = next((c for c in comments if c.commentId == comment_id), None)
    if not comment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Comment with ID {comment_id} not found for post {post_id}.",
        )
    if comment.userId != user_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You can only delete your own comments.",
        )
    # Delete the comment
    if db.delete_comment(comment_id):
        return {"message": "Comment deleted successfully"}
    raise HTTPException(
        status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
        detail="Failed to delete comment.",
    )
