import requests
import pytest
from fastapi import HTTPException

BASE_URL = "http://localhost:8000" 

@pytest.fixture(scope="module")
def test_user_id():
    """Fixture to create a test user and return its ID."""
    signup_data = {"username": "testuser", "password": "testpass"}
    signup_url = f"{BASE_URL}/user/signup" 
    print(f"Attempting signup at: {signup_url}")
    signup_response = requests.post(signup_url, json=signup_data)
    print(f"Signup response: {signup_response.status_code} - {signup_response.text}")
    if signup_response.status_code == 400:  # User already exists
        login_response = requests.post(f"{BASE_URL}/user/login", json=signup_data)  
        assert login_response.status_code == 200, f"Login failed: {login_response.text}"
        return login_response.json()["id"]
    assert signup_response.status_code == 200, f"Signup failed: {signup_response.text}"
    return signup_response.json()["id"]

@pytest.fixture(scope="module")
def test_post_id(test_user_id):
    """Fixture to create a test post and return its ID."""
    data = {"userId": test_user_id, "message": "Test post for pytest", "image": None, "recipe_id": None}
    response = requests.post(f"{BASE_URL}/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    posts = requests.get(f"{BASE_URL}/posts/").json()
    post = next((p for p in posts if p["message"] == "Test post for pytest"), None)
    assert post is not None, "Test post not found"
    return post["postId"]

def test_list_posts_empty():
    """Test retrieving all posts when database is initially empty."""
    response = requests.get(f"{BASE_URL}/posts/")
    assert response.status_code == 200, f"Expected 200, got {response.status_code}: {response.text}"
    posts = response.json()
    assert isinstance(posts, list)

def test_create_post(test_user_id):
    """Test creating a new post."""
    data = {
        "userId": test_user_id,
        "message": "New test post",
        "image": "base64testdata",
        "recipe_id": None
    }
    response = requests.post(f"{BASE_URL}/posts/", json=data)
    assert response.status_code == 201
    assert response.json()["message"] == "Post created successfully."

def test_get_post(test_post_id):
    """Test retrieving a post by ID."""
    response = requests.get(f"{BASE_URL}/posts/{test_post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["postId"] == test_post_id
    assert "message" in post

def test_list_posts(test_post_id):
    """Test retrieving all posts after creating one."""
    response = requests.get(f"{BASE_URL}/posts/")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert any(p["postId"] == test_post_id for p in posts)

def test_list_posts_by_user(test_user_id, test_post_id):
    """Test retrieving posts by user ID."""
    response = requests.get(f"{BASE_URL}/posts/user/{test_user_id}")
    assert response.status_code == 200
    posts = response.json()
    assert isinstance(posts, list)
    assert all(post["userId"] == test_user_id for post in posts)

def test_like_post(test_post_id, test_user_id):
    """Test liking a post."""
    data = {"user_id": test_user_id}
    response = requests.put(f"{BASE_URL}/posts/{test_post_id}/like", json=data)
    assert response.status_code == 200
    assert response.json()["message"] in ["Post liked successfully.", "Changed from dislike to like successfully."]
    post = requests.get(f"{BASE_URL}/posts/{test_post_id}").json()
    assert test_user_id in post["likes"]

def test_dislike_post(test_post_id, test_user_id):
    """Test disliking a post."""
    data = {"user_id": test_user_id}
    response = requests.put(f"{BASE_URL}/posts/{test_post_id}/dislike", json=data)
    assert response.status_code == 200
    assert response.json()["message"] in ["Post disliked successfully.", "Changed from like to dislike successfully."]
    post = requests.get(f"{BASE_URL}/posts/{test_post_id}").json()
    assert test_user_id in post["dislikes"]

def test_update_post(test_post_id, test_user_id):
    """Test updating a post’s message."""
    data = {
        "update": {
            "message": "Updated test post",
        },
        "user_id": test_user_id
    }
    response = requests.put(f"{BASE_URL}/posts/{test_post_id}", json=data)
    assert response.status_code == 200
    updated_post = response.json()
    assert updated_post["message"] == "Updated test post"

def test_delete_post(test_post_id):
    """Test deleting a post."""
    response = requests.delete(f"{BASE_URL}/posts/{test_post_id}")
    assert response.status_code == 200
    assert response.json()["message"] == "Post deleted successfully."