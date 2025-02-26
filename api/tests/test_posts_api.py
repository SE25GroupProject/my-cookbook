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

# @pytest.fixture(scope="function", autouse=True)
# def setup_db():
#     """Copies the db to a testing db before each test"""
#     if path.exists(TEST_DB):
#         remove(TEST_DB)
#     insert_data(TEST_DB, "tests/recipeTest.json")
#     yield
#     remove(TEST_DB)

#     # Reset and add middleware once
#     app.user_middleware = []
#     app.add_middleware(DBConnectionMiddleware, db_path=temp_db_path)

#     yield

#     # Cleanup after all tests
#     remove(temp_db_path)


@pytest.fixture(scope="module")
def test_user_id():
    """Fixture to create a test user and return its ID."""
    signup_data = {"username": "testuser", "password": "testpass"}
    print("Attempting signup at: /user/signup")
    signup_response = client.post("/user/signup", json=signup_data)
    print(
        "Signup response: "
        f"{signup_response.status_code} - {signup_response.text}")
    if signup_response.status_code == 400:  # User already exists
        login_response = client.post("/user/login", json=signup_data)
        assert login_response.status_code == 200, "Login failed: "
        f"{login_response.text}"
        return login_response.json()["id"]
    assert signup_response.status_code == 200, "Signup failed: "
    f"{signup_response.text}"
    return signup_response.json()["id"]


@pytest.fixture(scope="module")
def test_post_id(test_user_id):
    """Fixture to create a test post and return its ID."""
    data = {"userId": test_user_id,
            "message": "Test post for pytest", "image": None}
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    posts = client.get("/posts/").json()
    post = next(
        (p for p in posts if p["message"] == "Test post for pytest"), None)
    assert post is not None, "Test post not found"
    return post["postId"]


def test_list_posts_empty():
    """Test retrieving all posts when database is initially empty."""
    response = client.get("/posts/")
    assert response.status_code == 200, "Expected 200, "
    f"got {response.status_code}: {response.text}"
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
    assert response.status_code == 200, "Expected 200, "
    f"got {response.status_code}: {response.text}"
    assert response.json()["message"] in [
        "Post liked successfully.",
        "Changed from dislike to like successfully."]
    post = client.get(f"/posts/{test_post_id}").json()
    assert test_user_id in post["likes"]


def test_dislike_post(test_post_id, test_user_id):
    """Test disliking a post."""
    response = client.put(f"/posts/dislike/{test_post_id}", json=test_user_id)
    assert response.status_code == 200
    assert response.json()["message"] in [
        "Post disliked successfully.",
        "Changed from like to dislike successfully."]
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


def test_create_post_no_image(test_user_id):
    """Test creating a post with no image."""
    data = {
        "userId": test_user_id,
        "message": "Post with no image"
    }
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    assert response.json()["message"] == "Post created successfully."

    
    response = client.get("/posts/")
    posts = response.json()
    print(posts)

    post = next(
        (p for p in posts if p["message"] == "Post with no image"), None)
    print(post)
    assert post is not None, "Post not found"
    assert post["image"] is None


def test_like_non_existent_post(test_user_id):
    """Test liking a post that doesn’t exist."""
    non_existent_post_id = 9999  # Assuming this ID doesn’t exist
    response = client.put(
        f"/posts/like/{non_existent_post_id}", json=test_user_id)
    assert response.status_code == 404, "Expected 404, "
    f"got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_dislike_after_like(test_post_id, test_user_id):
    """Test switching from like to dislike."""
    # First, like the post
    like_response = client.put(
        f"/posts/like/{test_post_id}", json=test_user_id)
    assert like_response.status_code == 200

    # Then, dislike it
    dislike_response = client.put(
        f"/posts/dislike/{test_post_id}", json=test_user_id)
    assert dislike_response.status_code == 200, "Expected 200, "
    f"got {dislike_response.status_code}: {dislike_response.text}"
    post = client.get(f"/posts/{test_post_id}").json()
    assert test_user_id not in post["likes"]
    assert test_user_id in post["dislikes"]


def test_get_non_existent_post():
    """Test retrieving a post that doesn’t exist."""
    non_existent_post_id = 9999  # Assuming this ID doesn’t exist
    response = client.get(f"/posts/{non_existent_post_id}")
    assert response.status_code == 404, "Expected 404, "
    f"got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_delete_post(test_post_id, test_user_id):
    response = client.request(
        "DELETE", f"/posts/{test_post_id}", json=test_user_id)
    print(f"Response: {response.status_code} - {response.text}")
    assert response.status_code == 200, "Expected 200, "
    f"got {response.status_code}: {response.text}"
    assert response.json()["message"] == "Post deleted successfully."
