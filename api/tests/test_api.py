"""
Copyright (C) 2022 SE CookBook - All Rights Reserved
You may use, distribute and modify this code under the
terms of the MIT license.
You should have received a copy of the MIT license with
this file. If not, please write to: help.cookbook@gmail.com
"""

from fastapi.testclient import TestClient
import pytest
from os import remove
from api.db_middleware import DBConnectionMiddleware
from api.db.convert_json_to_sql import insert_data
import tempfile
import time

from api.main import app
from typing import Optional, List

client = TestClient(app)

MAIN_DB = "cookbook.db"
TEST_DB = "tests/test_cookbook.db"

@pytest.fixture(scope="module", autouse=True)
def setup_db_and_middleware():
    """Sets up a temporary database and middleware once for all tests."""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    insert_data(temp_db_path, "tests/recipeTest.json")

    app.user_middleware = []
    app.add_middleware(DBConnectionMiddleware, db_path=temp_db_path)
    yield
    remove(temp_db_path)

@pytest.fixture(scope="module")
def test_user_id():
    """Fixture to create a test user and return its ID."""
    signup_data = {"username": "testuser_recipes", "password": "testpass"}
    print("Attempting signup at: /user/signup")
    signup_response = client.post("/user/signup", json=signup_data)
    print(f"Signup response: {signup_response.status_code} - {signup_response.text}")
    if signup_response.status_code == 400:  # User already exists
        login_response = client.post("/user/login", json=signup_data)
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        return login_response.json()["id"]
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    return signup_response.json()["id"]

def test_list_recipes_by_ingredient():
    """Test listing recipes by ingredient."""
    data = {"ingredients": ["eggs"], "page": 1}
    response = client.request("GET", "/recipe/search/", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert isinstance(response.json()["recipes"], list)

def test_list_recipes_by_ingredients():
    """Test listing recipes by multiple ingredients."""
    data = {"ingredients": ["eggs", "garlic"], "page": 1}
    response = client.request("GET", "/recipe/search/", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert "recipes" in response.json()

def test_list_recipes_by_non_existent_ingredient():
    """Test listing recipes by a non-existent ingredient."""
    data = {"ingredients": ["unicorn"], "page": 1}
    response = client.request("GET", "/recipe/search/", json=data)
    print(f"Response: {response.status_code} - {response.text}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["recipes"] == []

def test_list_ingredients():
    """Test listing ingredient suggestions."""
    query_string = "to"
    response = client.get(f"/recipe/ingredients/{query_string}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert isinstance(response.json(), list)

def test_list_ingredients_no_matches():
    """Test listing ingredient suggestions with no matches."""
    query_string = "xyz"
    response = client.get(f"/recipe/ingredients/{query_string}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json() == []

def test_recommend_recipes():
    """Test recommending recipes based on a query."""
    query_data = {"query": "easy pasta recipe", "context": "Looking for vegetarian options."}
    response = client.post("/recipe/recommend-recipes/", json=query_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert "response" in response.json()

def test_recommend_recipes_with_empty_query():
    """Test recommending recipes with an empty query."""
    query_data = {"query": "", "context": ""}
    response = client.post("/recipe/recommend-recipes/", json=query_data)
    print(f"Response: {response.status_code} - {response.text}")
    assert response.status_code == 400
    assert "detail" in response.json()

def test_find_recipe_non_existent_id():
    """Test retrieving a recipe with a non-existent ID."""
    non_existent_id = 9999
    response = client.get(f"/recipe/{non_existent_id}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"
    assert "detail" in response.json()

def test_count_recipes_by_ingredients():
    """Test counting recipes by ingredients."""
    data = {"ingredients": ["eggs", "garlic"], "page": 1}
    response = client.post("/recipe/search/count/", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert isinstance(response.json(), int)

def test_list_recipes_by_nutrition():
    """Test listing recipes by nutritional criteria."""
    data = {"page": 1, "caloriesMax": 500.0, "fatMax": 30.0, "sugMax": 20.0, "proMax": 25.0}
    response = client.post("/recipe/search2/", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert "recipes" in response.json()
    assert isinstance(response.json()["recipes"], list)

def test_create_user_recipe(test_user_id):
    """Test creating a user recipe."""
    recipe_data = {
        "recipeId": 999,  # Added as a placeholder since model requires it
        "name": "Test Recipe",
        "cookTime": "30",  # String to match model
        "prepTime": "15",  # String to match model
        "totalTime": "45",  # String to match model
        "description": "A simple test recipe",
        "category": "Test Category",
        "rating": "4.5",  # String to match model
        "calories": "300.0",  # String to match model
        "fat": "10.0",  # String to match model
        "saturatedFat": "5.0",  # String to match model
        "cholesterol": "50.0",  # String to match model
        "sodium": "600.0",  # String to match model
        "carbs": "40.0",  # String to match model
        "fiber": "5.0",  # String to match model
        "sugar": "10.0",  # String to match model
        "protein": "15.0",  # String to match model
        "servings": "4",  # String to match model
        "images": ["http://example.com/image.jpg"],
        "tags": ["test", "recipe"],
        "ingredients": ["flour"],
        "instructions": [{"step": 1, "instruction": "Mix ingredients"}],
        "ingredientQuantities": ["1.0"]  # Added to match required field, as strings
    }
    response = client.post(f"/recipe/?userId={test_user_id}", json=recipe_data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json() is True

# Updated Meal Plan Tests
def test_get_meal_plan(test_user_id):
    """Test retrieving a user's meal plan."""
    response = client.get(f"/meal-plan/{test_user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    meal_plan = response.json()
    assert isinstance(meal_plan, list)

def test_update_meal_plan(test_user_id):
    """Test updating a meal plan entry."""
    entry = {"day": 1, "recipe": {"recipeId": 1, "name": "Test Meal"}}
    response = client.put(f"/meal-plan/{test_user_id}", json=entry)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["message"] == "Meal plan updated successfully."

def test_remove_from_meal_plan(test_user_id):
    """Test removing a meal plan entry."""
    entry = {"day": 2, "recipe": {"recipeId": 1, "name": "Test Meal"}}
    client.put(f"/meal-plan/{test_user_id}", json=entry)  # Add entry first
    response = client.request("POST", f"/meal-plan/delete/{test_user_id}", json=2)  # Send day as plain integer
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"

def test_get_empty_meal_plan(test_user_id):
    """Test retrieving an empty meal plan for a user with no entries."""
    response = client.get(f"/meal-plan/{test_user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    meal_plan = response.json()
    assert isinstance(meal_plan, list), f"Expected meal_plan to be a list, but got: {meal_plan}"

# New Tests
def test_count_recipes_by_nutrition():
    """Test counting recipes by nutritional criteria."""
    data = {"page": 1, "caloriesMax": 500.0, "fatMax": 30.0, "sugMax": 20.0, "proMax": 25.0}
    response = client.post("/recipe/search2/count/", json=data)
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert isinstance(response.json(), int)

def test_favorite_recipe(test_user_id):
    """Test favoriting a recipe."""
    response = client.put(f"/recipe/favorite/1/{test_user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json() is True

def test_unfavorite_recipe(test_user_id):
    """Test unfavoriting a recipe."""
    client.put(f"/recipe/favorite/1/{test_user_id}")
    response = client.put(f"/recipe/unfavorite/1/{test_user_id}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json() is True
