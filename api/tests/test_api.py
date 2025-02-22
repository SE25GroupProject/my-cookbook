# import sys
# import os
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../api')))
from unittest.mock import MagicMock
from fastapi.testclient import TestClient
import pytest

from api.main import app

# Get recipe by ingredients - single

# Get recipe by ingredients - multiple
def test_list_recipes_by_ingredients():
    """Test listing recipes by multiple ingredients."""
    client = TestClient(app)

    data = {
        "ingredients": ["tomato", "basil"],
        "page": 1
    }
    response = client.post(f"recipe/search/", json=data)
    assert response.status_code == 200
    assert "recipes" in response.json()