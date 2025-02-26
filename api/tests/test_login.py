from fastapi.testclient import TestClient
import pytest
from os import remove
from api.db_middleware import DBConnectionMiddleware
from api.db.convert_json_to_sql import insert_data
import tempfile

from api.main import app

client = TestClient(app)

MAIN_DB = "cookbook.db"
TEST_DB = "tests/test_cookbook.db"

@pytest.fixture(scope="function", autouse=True)
def clientSetup():
    """Copies the db to a testing db before each test"""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    insert_data(temp_db_path, "tests/recipeTest.json")

    app.user_middleware = []
    app.add_middleware(DBConnectionMiddleware, db_path=temp_db_path)
    with TestClient(app) as client:
        yield client
    
    remove(temp_db_path)

def test_signup_user():
    """Test case for user signup"""
    user_data = {
        "username": "newUser",
        "password": "password"
    }

    # Send a POST request to the /signup endpoint
    response = client.post("/user/signup", json=user_data)

    # Assert the response status code is 200 (success)
    assert response.status_code == 200
    assert response.json()["username"] == "newUser"

    # Check that the user is actually added to users_db
    response = client.get("/user/getUser/newUser")
    assert response.status_code == 200

def test_signup_user_already_exists():
    """Test case for attempting to signup an already existing user"""
    user_data = {
        "username": "newUser",
        "password": "password"
    }

    # First signup should succeed
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 200

    # Attempt to signup again with the same email
    response = client.post("/user/signup", json=user_data)

    # Assert the response status code is 400 (bad request)
    assert response.status_code == 400
    assert response.json() == {"detail": "User with that username already exists"}

def test_signup_empty_username():
    user_data = {"username": "", "password": "password123"}
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 400 

def test_signup_empty_password():
    user_data = {"username": "newUser", "password": ""}
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 400

def test_signup_missing_password():
    user_data = {"username": "newUser"}
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 422

def test_signup_long_password():
    user_data = {"username": "longUser", "password": f"{'a' * 129}"}
    response = client.post("/user/signup", json=user_data)

    # Check if the response status code is 200 (success)
    assert response.status_code == 200

    response = client.get("/user/getUser/longUser")
    assert response.status_code == 200

def test_signup_and_login():
    user_data = {"username": "user", "password": "password123"}
    client.post("/user/signup", json=user_data)

    # Attempt login with the same credentials
    login_data = {"username": "user", "password": "password123"}
    response = client.post("/user/login", json=login_data)
    assert response.status_code == 200

def test_signup_with_special_characters():
    user_data = {"username": "user", "password": "password#123"}
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 200

def test_login_incorrect_password():
    user_data = {"username": "user", "password": "password123"}
    response = client.post("/user/signup", json=user_data)
    assert response.status_code == 200


    user_data = {"username": "user", "password": "password1234"}
    response = client.post("/user/login", json=user_data)
    assert response.status_code == 400  # Incorrect email or password






