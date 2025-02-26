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


# @pytest.fixture(scope="function", autouse=True)
# def setup_db():
#     """Copies the db to a testing db before each test"""
#     if path.exists(TEST_DB):
#         remove(TEST_DB)
#     insert_data(TEST_DB, "tests/recipeTest.json")
#     yield
#     remove(TEST_DB)


# @pytest.fixture(scope="module")
# def clientSetup():
#     app.add_middleware(DBConnectionMiddleware, db_path=TEST_DB)
#     with TestClient(app) as client:
#         yield client\

@pytest.fixture(scope="module", autouse=True)
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


# Sample data for testing
valid_user = {"username": "test@example.com",
              "password": "securepassword"}
duplicate_user = {"username": "test@example.com",
                  "password": "newpassword"}
invalid_user_email = {
    "username": "wrong@example.com",
    "password": "securepassword"}
invalid_user_password = {
    "username": "test@example.com",
    "password": "wrongpassword"}


# Test cases for /signup endpoint
def test_signup_success():
    response = client.post("/user/signup", json=valid_user)
    print(response.json())
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'test@example.com'}


def test_signup_duplicate_email():
    # Sign up the first time
    client.post("/user/signup", json=valid_user)
    # Attempt to sign up with the same email
    response = client.post("/user/signup", json=duplicate_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User with that "
    "username already exists"


# Test cases for /login endpoint
def test_login_success():
    # Sign up before testing login
    client.post("/user/signup", json=valid_user)
    # Test login with correct credentials
    response = client.post("/user/login", json=valid_user)
    assert response.status_code == 200
    assert response.json() == {'id': 1, 'username': 'test@example.com'}


def test_login_invalid_email():
    # Test login with an unregistered email
    response = client.post("/user/login", json=invalid_user_email)
    assert response.status_code == 400
    assert response.json()["detail"] == "There is no user with that username"


def test_login_invalid_password():
    # Sign up before testing login
    client.post("/user/signup", json=valid_user)
    # Test login with incorrect password
    response = client.post("/user/login", json=invalid_user_password)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect Username or Password"
