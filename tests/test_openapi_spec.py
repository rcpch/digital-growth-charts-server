"""
Tests for the openAPI spec endpoint
"""
# standard imports
import json

# third party imports
from fastapi.testclient import TestClient

# local / rcpch imports
from main import app

client = TestClient(app)

def test_read_root():

    # get the root API endpoint (returns JSON openAPI3 spec)
    response = client.get("/")

    # load the API spec from the static saved test APIspec version
    with open(r'tests/test_data/test_openapi.json', 'r') as file:
        apispec = file.read()

    assert response.status_code == 200

    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response.json() == json.loads(apispec)
