import sqlite3
from unittest.mock import MagicMock
from api.routes import db
from fastapi.testclient import TestClient
import pytest

from api.main import app
import api.routes

client = TestClient(app)

# def test_get_shopping_list():
#     """Test to fetch shopping list."""
#     response = client.get("/shopping-list/0")
#     assert response.status_code == 200
#     assert response.json() == []

@pytest.fixture(scope="function")
def setup_db():
    """Fixture to mock the database and avoid actual database calls."""
    # Mocking the database
    db.conn = sqlite3.connect('db/cookbook.db')
    db.cursor = db.conn.cursor()
    yield 
    db.conn.close()


def test_update_shopping_list(setup_db):
    """Test to update shopping list."""
    response = client.put("/shopping-list/0", json={
        "name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False
    })
    print(response.json())
    assert response.status_code == 200
    assert response.json()["message"] == "User's shopping list was successfully updated"

    response = client.get("/shopping-list/0")
    assert response.status_code == 200
    assert response.json() == [{"name": "Apple",
        "quantity": 5,
        "unit": "kg",
        "checked": False}]
