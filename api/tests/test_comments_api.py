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
POSTS_BASE = "/posts"


# @pytest.fixture(scope="function", autouse=True)
# def setup_db():
#     """Copies the db to a testing db before each test"""
#     if path.exists(TEST_DB):
#         remove(TEST_DB)
#     insert_data(TEST_DB, "tests/recipeTest.json")
#     yield

#     # Cleanup after all tests
#     remove(temp_db_path)

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


@pytest.fixture(scope="module")
def test_user_id():
    """Fixture to create a test user and return its ID."""
    signup_data = {"username": "testuser_comments", "password": "testpass"}
    signup_url = "/user/signup"
    print(f"Attempting signup at: {signup_url}")
    signup_response = client.post(signup_url, json=signup_data)
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
    data = {
        "userId": test_user_id,
        "message": "Test post for comments",
        "image": None,
        "recipe_id": None}
    response = client.post("/posts/", json=data)
    assert response.status_code == 201, f"Create post failed: {response.text}"
    posts = client.get("/posts/").json()
    post = next(
        (p for p in posts if p["message"] == "Test post for comments"),
        None)
    assert post is not None, "Test post not found"
    return post["postId"]


def test_add_comment(test_post_id, test_user_id):
    """Test adding a comment to a post."""
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "This is a test comment"
    }
    response = client.post(
        f"/posts/comments/{test_post_id}",
        json=comment_data)
    print(f"Add comment response status: {response.status_code}")
    print(f"Add comment response body: {response.text}")
    assert response.status_code == 201, "Failed with "
    f"{response.status_code}: {response.text}"
    response_json = response.json()
    assert response_json["message"] == "Comment added successfully"
    assert "commentId" in response_json
    comment_id = response_json["commentId"]
    assert isinstance(comment_id, int)


def test_get_post_with_comments(test_post_id, test_user_id):
    """Test retrieving a post with its comments."""
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "Another test comment"
    }
    response = client.post(
        f"/posts/comments/{test_post_id}",
        json=comment_data)
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


def test_add_comment_invalid_user(test_post_id):
    """Test adding a comment with a non-existent user."""
    comment_data = {
        "userId": 9999,  # Non-existent user ID
        "postId": test_post_id,
        "message": "This should fail"
    }
    response = client.post(
        f"/posts/comments/{test_post_id}",
        json=comment_data)
    print(f"Add comment invalid user response status: {response.status_code}")
    print(f"Add comment invalid user response body: {response.text}")
    assert response.status_code == 400, "Expected 400, "
    f"got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "user" in response.json()["detail"].lower()


def test_delete_comment(test_post_id, test_user_id):
    """Test deleting a comment."""
    # Add a comment to delete
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "Comment to delete"
    }
    add_response = client.post(
        f"/posts/comments/{test_post_id}",
        json=comment_data)
    assert add_response.status_code == 201
    comment_id = add_response.json()["commentId"]

    # Delete the comment
    delete_data = {"user_id": test_user_id, "post_id": test_post_id}
    response = client.delete(
        f"/posts/comments/{comment_id}",
        json=delete_data)
    print(f"Delete comment response status: {response.status_code}")
    print(f"Delete comment response body: {response.text}")
    assert response.status_code == 200, "Failed with "
    f"{response.status_code}: {response.text}"
    assert response.json()["message"] == "Comment deleted successfully"

    # Verify comment is gone
    post_response = client.get(f"/posts/{test_post_id}")
    post = post_response.json()
    assert not any(
        c["commentId"] == comment_id for c in post["comments"]), "Comment "
    "was not deleted"


def test_delete_comment_nonexistent(test_post_id, test_user_id):
    """Test deleting a non-existent comment."""
    delete_data = {"user_id": test_user_id}
    response = client.delete(
        f"/posts/comments/{test_post_id}/9999",
        json=delete_data)
    print(f"Delete nonexistent response status: {response.status_code}")
    print(f"Delete nonexistent response body: {response.text}")
    assert response.status_code == 404, "Expected 404, "
    f"got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "not found" in response.json()["detail"].lower()


def test_add_multiple_comments(test_post_id, test_user_id):
    """Test adding multiple comments to a post."""
    comments = [{"userId": test_user_id,
                 "postId": test_post_id,
                 "message": "First comment"},
                {"userId": test_user_id,
                 "postId": test_post_id,
                 "message": "Second comment"}]
    comment_ids = []
    for comment_data in comments:
        response = client.post(
            f"/posts/comments/{test_post_id}",
            json=comment_data)
        print(f"Add multiple comments response status: {response.status_code}")
        print(f"Add multiple comments response body: {response.text}")
        assert response.status_code == 201, "Failed with "
        f"{response.status_code}: {response.text}"
        response_json = response.json()
        assert response_json["message"] == "Comment added successfully"
        comment_ids.append(response_json["commentId"])

    # Verify all comments are present
    response = client.get(f"/posts/{test_post_id}")
    assert response.status_code == 200
    post = response.json()
    assert len(post["comments"]) >= 2, "Expected at least 2 comments"
    messages = [c["message"] for c in post["comments"]]
    assert "First comment" in messages
    assert "Second comment" in messages


def test_delete_comment_by_non_owner(test_post_id, test_user_id):
    """Test deleting a comment by a user who doesn't own it."""
    # Create a second user
    signup_data = {"username": "otheruser_comments", "password": "otherpass"}
    signup_response = client.post("/user/signup", json=signup_data)
    if signup_response.status_code == 400:
        login_response = client.post("/user/login", json=signup_data)
        assert login_response.status_code == 200
        other_user_id = login_response.json()["id"]
    else:
        assert signup_response.status_code == 200
        other_user_id = signup_response.json()["id"]

    # Add a comment with test_user_id
    comment_data = {
        "userId": test_user_id,
        "postId": test_post_id,
        "message": "Comment by owner"
    }
    add_response = client.post(
        f"/posts/comments/{test_post_id}",
        json=comment_data)
    assert add_response.status_code == 201
    comment_id = add_response.json()["commentId"]

    # Attempt to delete with other_user_id
    delete_data = {"post_id": test_post_id, "user_id": other_user_id}
    response = client.request(
        "DELETE",
        f"/posts/comments/{comment_id}",
        json=delete_data)
    print(f"Delete by non-owner response status: {response.status_code}")
    print(f"Delete by non-owner response body: {response.text}")
    assert response.status_code == 403, "Expected 403, "
    f"got {response.status_code}: {response.text}"
    assert "detail" in response.json()
    assert "own comments" in response.json()["detail"].lower()

    # Verify comment still exists
    post_response = client.get(f"/posts/{test_post_id}")
    post = post_response.json()
    assert any(c["commentId"] == comment_id for c in post["comments"]
               ), "Comment was unexpectedly deleted"
