from fastapi.testclient import TestClient
import pytest
from os import path, remove
import shutil
from api.dbMiddleware import DBConnectionMiddleware
from api.db.convertJsonToSql import insertData

from api.main import app

client = TestClient(app)

MAIN_DB = "cookbook.db"
TEST_DB = "tests/test_cookbook.db"

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Copies the db to a testing db before each test"""
    if path.exists(TEST_DB):
        remove(TEST_DB)
    insertData(TEST_DB, "tests/recipeTest.json")
    yield
    remove(TEST_DB)

@pytest.fixture(scope="module")
def clientSetup():
    app.add_middleware(DBConnectionMiddleware, db_path=TEST_DB)
    with TestClient(app) as client:
        yield client

# Sample data for testing
valid_user = {"email": "test@example.com", "password": "securepassword"}
duplicate_user = {"email": "test@example.com", "password": "newpassword"}
invalid_user_email = {"email": "wrong@example.com", "password": "securepassword"}
invalid_user_password = {"email": "test@example.com", "password": "wrongpassword"}


# Test cases for /signup endpoint
def test_signup_success():
    response = client.post("/signup", json=valid_user)
    assert response.status_code == 200
    assert response.json() == {"message": "Signup successful"}


def test_signup_duplicate_email():
    # Sign up the first time
    client.post("/signup", json=valid_user)
    # Attempt to sign up with the same email
    response = client.post("/signup", json=duplicate_user)
    assert response.status_code == 400
    assert response.json()["detail"] == "User already exists"


# Test cases for /login endpoint
def test_login_success():
    # Sign up before testing login
    client.post("/signup", json=valid_user)
    # Test login with correct credentials
    response = client.post("/login", json=valid_user)
    assert response.status_code == 200
    assert response.json() == {"message": "Login successful"}


def test_login_invalid_email():
    # Test login with an unregistered email
    response = client.post("/login", json=invalid_user_email)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"


def test_login_invalid_password():
    # Sign up before testing login
    client.post("/signup", json=valid_user)
    # Test login with incorrect password
    response = client.post("/login", json=invalid_user_password)
    assert response.status_code == 400
    assert response.json()["detail"] == "Incorrect email or password"
