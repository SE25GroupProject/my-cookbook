from fastapi.testclient import TestClient
import pytest
from os import path, remove
import shutil
from api.dbMiddleware import DBConnectionMiddleware
from api.db.convertJsonToSql import insertData
import tempfile

from api.main import app

@pytest.fixture(scope="module", autouse=True)
def setup_db_and_client():
    """Sets up a temporary database and middleware once for all tests."""
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    insertData(temp_db_path, "tests/recipeTest.json")

    app.user_middleware = []
    middleware = DBConnectionMiddleware(app, db_path=temp_db_path)
    app.add_middleware(lambda *args, **kwargs: middleware)

    client = TestClient(app)
    yield client

    if hasattr(middleware, 'db'):
        middleware.db.close()
    remove(temp_db_path)

@pytest.fixture(scope="module")
def test_user_id(setup_db_and_client):
    """Fixture to create a test user and return its ID."""
    client = setup_db_and_client
    signup_data = {"username": "testuser_comments", "password": "testpass"}
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
def test_post_id(test_user_id, setup_db_and_client):
    """Fixture to create a test post and return its ID."""
    client = setup_db_and_client
    data = {"userId": test_user_id, "message": "Test post for comments", "image": None, "recipe_id": None}
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    posts = client.get("/posts/").json()
    post = next((p for p in posts if p["message"] == "Test post for comments"), None)
    assert post is not None, "Test post not found"
    return post["postId"]

def test_add_comment(test_post_id, test_user_id, setup_db_and_client):
    """Test adding a comment to a post."""
    client = setup_db_and_client
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "This is a test comment"
    }
    response = client.post(f"/posts/{test_post_id}/comments", json=comment_data)
    print(f"Add comment response status: {response.status_code}")
    print(f"Add comment response body: {response.text}")
    assert response.status_code == 201, f"Failed with {response.status_code}: {response.text}"
    response_json = response.json()
    assert response_json["message"] == "Comment added successfully"
    assert "commentId" in response_json
    comment_id = response_json["commentId"]
    assert isinstance(comment_id, int)

def test_get_post_with_comments(test_post_id, test_user_id, setup_db_and_client):
    """Test retrieving a post with its comments."""
    client = setup_db_and_client
    # Add a comment first
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "Another test comment"
    }
    response = client.post(f"/posts/{test_post_id}/comments", json=comment_data)
    assert response.status_code == 201

    # Fetch the post
    response = client.get(f"/posts/{test_post_id}")
    assert response.status_code == 200
    post = response.json()
    assert post["postId"] == test_post_id
    assert isinstance(post["comments"], list)
    assert len(post["comments"]) > 0, "No comments found in post"
    comment = post["comments"][-1]  # Check the latest comment
    assert comment["userId"] == test_user_id
    assert comment["postId"] == test_post_id
    assert comment["message"] == "Another test comment"
    assert "commentId" in comment
    assert "date" in comment

def test_add_comment_invalid_user(test_post_id, setup_db_and_client):
    """Test adding a comment with a non-existent user."""
    client = setup_db_and_client
    comment_data = {
        "userId": 9999,  # Non-existent user ID
        "postId": test_post_id,
        "message": "This should fail"
    }
    response = client.post(f"/posts/{test_post_id}/comments", json=comment_data)
    print(f"Add comment invalid user response status: {response.status_code}")
    print(f"Add comment invalid user response body: {response.text}")
    assert response.status_code == 400, f"Expected 400, got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "user" in response.json()["detail"].lower()

def test_delete_comment(test_post_id, test_user_id, setup_db_and_client):
    """Test deleting a comment."""
    client = setup_db_and_client
    # Add a comment to delete
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "Comment to delete"
    }
    add_response = client.post(f"/posts/{test_post_id}/comments", json=comment_data)
    assert add_response.status_code == 201
    comment_id = add_response.json()["commentId"]

    # Delete the comment
    delete_data = {"user_id": test_user_id}
    response = client.request("DELETE", f"/posts/{test_post_id}/comments/{comment_id}", json=delete_data)
    print(f"Delete comment response status: {response.status_code}")
    print(f"Delete comment response body: {response.text}")
    assert response.status_code == 200, f"Failed with {response.status_code}: {response.text}"
    assert response.json()["message"] == "Comment deleted successfully"

    # Verify comment is gone
    post_response = client.get(f"/posts/{test_post_id}")
    post = post_response.json()
    assert not any(c["commentId"] == comment_id for c in post["comments"]), "Comment was not deleted"

def test_delete_comment_nonexistent(test_post_id, test_user_id, setup_db_and_client):
    """Test deleting a non-existent comment."""
    client = setup_db_and_client
    delete_data = {"user_id": test_user_id}
    response = client.request("DELETE", f"/posts/{test_post_id}/comments/9999", json=delete_data)
    print(f"Delete nonexistent response status: {response.status_code}")
    print(f"Delete nonexistent response body: {response.text}")
    assert response.status_code == 404, f"Expected 404, got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()