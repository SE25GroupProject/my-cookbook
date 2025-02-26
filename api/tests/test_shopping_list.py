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
def setup_db():
    """Copies the db to a testing db before each test"""
    # if path.exists(TEST_DB):
    #     remove(TEST_DB)
    # insert_data(TEST_DB, "tests/recipeTest.json")
    # yield
    # remove(TEST_DB)
    temp_db = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    temp_db_path = temp_db.name
    temp_db.close()
    insert_data(temp_db_path, "tests/recipeTest.json")

    app.user_middleware = []
    app.add_middleware(DBConnectionMiddleware, db_path=temp_db_path)
    yield
    remove(temp_db_path)


# @pytest.fixture(scope="module")
# def clientSetup():
#     app.add_middleware(DBConnectionMiddleware, db_path=TEST_DB)
#     with TestClient(app) as client:
#         yield client


def test_get_shopping_list(setup_db):
    """Test to fetch shopping list."""
    client = TestClient(app)

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json() == []


def test_update_shopping_list(setup_db):
    """Test to update shopping list."""
    client = TestClient(app)
    response = client.put("/shopping-list/1", params={"user_id": 1}, json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    print(response.json())
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json() == [{
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    }]


def test_update_existing_item(setup_db):
    """Test updating an existing item in the shopping list."""
    # Mock existing item in database with a valid ObjectId
    client = TestClient(app)
    response = client.put("/shopping-list/1", params={"user_id": 1},  json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Apple"
    assert response.json()[0]["quantity"] == 5
    assert not response.json()[0]["checked"]

    # Mock the update response
    response = client.put("/shopping-list/1", params={"user_id": 1}, json={
        "name": "Apple",
        "quantity": 10,
        "unit": "kg",
        "checked": True
    })
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Apple"
    assert response.json()[0]["quantity"] == 10
    assert response.json()[0]["checked"]


# def test_update_nonexistent_item(setup_db):
#     """Test updating a non-existent item in the shopping list."""
#     client = TestClient(app)

#     # Generate a valid ObjectId for the test (simulate a non-existent item)
#     non_existent_item_id = str(ObjectId())  # Random valid ObjectId

#     response = client.put(f"/shopping-list/{non_existent_item_id}", json={
#         "name": "Banana",
#         "quantity": 3,
#         "unit": "kg",
#         "checked": False
#     })
#     Expect a 404 since the item does not exist
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}


def test_delete_item(setup_db):
    """Test deleting an item from the shopping list."""
    # Mock existing item in database with a valid ObjectId
    # app.database["shopping-list"].find.return_value = [{
    #     "_id": ObjectId("60b8d2950d0a2c8b75a3b9f9"),  # Use a valid ObjectId
    #     "name": "Apple", "quantity": 5, "unit": "kg", "checked": False
    # }]

    # Mock the delete response
    # app.database["shopping-list"].delete_one.return_value.deleted_count = 1
    client = TestClient(app)
    response = client.put("/shopping-list/1", params={"user_id": 1},  json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json()[0]["name"] == "Apple"

    response = client.post("/shopping-list/delete/1",
                           params={"user_id": 1}, json="Apple")
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/1", params={"user_id": 1})
    assert response.status_code == 200
    assert response.json() == []

# def test_delete_nonexistent_item(setup_db):
#     """Test deleting a non-existent item from the shopping list."""
#     client = TestClient(app)

#     # Clear the collection to simulate an empty database
#     collection = app.database["shopping-list"]
#     collection.delete_many({})  # Clear the collection

#     # Generate a valid ObjectId to simulate a non-existent item
#     non_existent_item_id = str(ObjectId())  # Random valid ObjectId

#     # Make the delete request
#     response = client.delete(f"/shopping-list/{non_existent_item_id}")

#     # Assert 404 error since the item doesn't exist
#     assert response.status_code == 404
#     assert response.json() == {"detail": "Item not found"}


def test_update_shopping_list_with_duplicates(setup_db):
    """Test trying to add duplicate items to the shopping list."""
    # Mock existing item in database with a valid ObjectId
    # app.database["shopping-list"].find.return_value = [{
    #     "_id": ObjectId("60b8d2950d0a2c8b75a3b9f9"),  # Use a valid ObjectId
    #     "name": "Apple", "quantity": 5, "unit": "kg", "checked": False
    # }]

    client = TestClient(app)
    response = client.put("/shopping-list/1", params={"user_id": 1}, json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"

    response = client.put("/shopping-list/1", params={"user_id": 1}, json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    assert response.status_code == 200
    assert response.json()[
        "message"] == "User's shopping list was successfully updated"
