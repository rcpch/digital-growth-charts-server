"""
Tests for the openAPI spec endpoint
"""

# third-party imports
from main import app
from fastapi.testclient import TestClient
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
