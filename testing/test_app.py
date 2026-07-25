import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import pytest
from unittest.mock import patch
from app import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_get_inventory(client):
    response = client.get("/inventory")
    assert response.status_code == 200
    assert isinstance(response.get_json(), list)

def test_add_item(client):
    new_item = {"name": "Test Chips", "price": 1.99, "stock": 10}
    response = client.post("/inventory", json=new_item)
    assert response.status_code == 201
    assert response.get_json()["name"] == "Test Chips"

@patch("app.fetch_external_product")
def test_fetch_external_mock(mock_fetch, client):
    mock_fetch.return_value = {
        "name": "Mocked Soda",
        "barcode": "12345",
        "price": 2.50,
        "stock": 15
    }
    response = client.post("/inventory/fetch-external/12345")
    assert response.status_code == 201
    assert response.get_json()["name"] == "Mocked Soda"
