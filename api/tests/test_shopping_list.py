import sqlite3
from unittest.mock import MagicMock
from api.routes import db
from fastapi.testclient import TestClient
import pytest
from os import path, remove
import shutil
from api.dbMiddleware import DBConnectionMiddleware
from api.db.convertJsonToSql import insertData

from api.main import app
import api.routes

client = TestClient(app)

# def test_get_shopping_list():
#     """Test to fetch shopping list."""
#     response = client.get("/shopping-list/0")
#     assert response.status_code == 200
#     assert response.json() == []

MAIN_DB = "cookbook.db"
TEST_DB = "test_cookbook.db"

@pytest.fixture(scope="function", autouse=True)
def setup_db():
    """Copies the db to a testing db before each test"""
    if path.exists(TEST_DB):
        remove(TEST_DB)
    shutil.copy(MAIN_DB, TEST_DB)
    print("Copied")
    insertData(MAIN_DB)
    yield
    remove(TEST_DB)

@pytest.fixture(scope="module")
def clientSetup():
    app.add_middleware(DBConnectionMiddleware, db_path=TEST_DB)
    with TestClient(app) as client:
        yield client

def test_update_shopping_list():
    """Test to update shopping list."""

    response = client.post("/user/signup", {
        "username": "test",
        "password": "test",
    })

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
