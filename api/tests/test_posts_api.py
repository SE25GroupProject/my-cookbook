from fastapi.testclient import TestClient
import pytest
from os import path, remove
import shutil
from api.dbMiddleware import DBConnectionMiddleware
from api.db.convertJsonToSql import insertData
import tempfile
from api.main import app

client = TestClient(app)

MAIN_DB = "cookbook.db"
TEST_DB = "tests/test_cookbook.db"

@pytest.fixture(scope="module", autouse=True)
def setup_db_and_middleware():
    """Sets up a temporary database and middleware once for all tests."""
    # Use a single temporary database for the module
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    insertData(temp_db_path, "tests/recipeTest.json")

    # Reset and add middleware once
    app.user_middleware = []
    app.add_middleware(DBConnectionMiddleware, db_path=temp_db_path)

    yield

    # Cleanup after all tests
    remove(temp_db_path)

@pytest.fixture(scope="module")
def test_user_id():
    """Fixture to create a test user and return its ID."""
    signup_data = {"username": "testuser", "password": "testpass"}
    print("Attempting signup at: /user/signup")
    signup_response = client.post("/user/signup", json=signup_data)
    print(f"Signup response: {signup_response.status_code} - {signup_response.text}")
    if signup_response.status_code == 400:  # User already exists
        login_response = client.post("/user/login", json=signup_data)
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        return login_response.json()["id"]
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    return signup_response.json()["id"]

@pytest.fixture(scope="module")
def test_post_id(test_user_id):
    """Fixture to create a test post and return its ID."""
    data = {"userId": test_user_id, "message": "Test post for pytest", "image": None}
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    posts = client.get("/posts/").json()
    post = next((p for p in posts if p["message"] == "Test post for pytest"), None)
    assert post is not None, "Test post not found"
    return post["postId"]

def test_list_posts_empty():
    """Test retrieving all posts when database is initially empty."""
    response = client.get("/posts/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    posts = response.json()
    assert isinstance(posts, list)

def test_create_post(test_user_id):
    """Test creating a new post."""
    data = {
        "userId": test_user_id,
        "message": "New test post",
        "image": "base64testdata",
    }
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    assert response.json()["message"] == "Post created successfully."

def test_get_post(test_post_id):
    """Test retrieving a post by ID."""
    response = client.get(f"/posts/{test_post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["postId"] == test_post_id
    assert "message" in post

def test_list_posts(test_post_id):
    """Test retrieving all posts after creating one."""
    response = client.get("/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert any(p["postId"] == test_post_id for p in posts)

def test_list_posts_by_user(test_user_id, test_post_id):
    """Test retrieving posts by user ID."""
    response = client.get(f"/posts/user/{test_user_id}")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert all(post["userId"] == test_user_id for post in posts)

def test_like_post(test_post_id, test_user_id):
    """Test liking a post."""
    response = client.put(f"/posts/like/{test_post_id}", json=test_user_id) 
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["message"] in ["Post liked successfully.", "Changed from dislike to like successfully."]
    post = client.get(f"/posts/{test_post_id}").json()
    assert test_user_id in post["likes"]

def test_dislike_post(test_post_id, test_user_id):
    """Test disliking a post."""
    response = client.put(f"/posts/dislike/{test_post_id}", json=test_user_id)
    assert response.status_code == 200
    assert response.json()["message"] in ["Post disliked successfully.", "Changed from like to dislike successfully."]
    post = client.get(f"/posts/{test_post_id}").json()
    assert test_user_id in post["dislikes"]

def test_update_post(test_post_id, test_user_id):
    """Test updating a post’s message."""
    data = {
    "userId": 1,
    "message": "Updated test post"
    }
    response = client.put(f"/posts/{test_post_id}", json=data)
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["message"] == "Updated test post"

def test_delete_post(test_post_id, test_user_id):
    response = client.request("DELETE", f"/posts/{test_post_id}", json=test_user_id)
    print(f"Response: {response.status_code} - {response.text}")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    assert response.json()["message"] == "Post deleted successfully."