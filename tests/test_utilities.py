"""
Tests for the utilities endpoints
"""

# standard imports
import json
import hashlib

# third party imports
from fastapi.testclient import TestClient

# local / rcpch imports
from main import app

client = TestClient(app)


def test_midparental_height_with_valid_request():
    body = {"height_paternal": 171, "height_maternal": 168, "sex": "male"}

    response = client.post("/utilities/mid-parental-height", json=body)

    # load the known-correct response from file
    with open(r"tests/test_data/test_midparental_height_valid.json", "r") as file:
        calculation_file = file.read()

    assert response.status_code == 200

    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response.json() == json.loads(calculation_file)


def test_midparental_height_with_invalid_request():
    body = {
        "height_paternal": "invalid_height_paternal",
        "height_maternal": "invalid_height_maternal",
        "sex": "invalid_sex",
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    # load the known-correct response from file
    with open(r"tests/test_data/test_midparental_height_valid.json", "r") as file:
        calculation_file = file.read()

    assert response.status_code == 422

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["loc"][1]: error for error in response.json()["detail"]}

    assert validation_errors["height_paternal"]["msg"] == "value is not a valid float"
    assert validation_errors["height_maternal"]["msg"] == "value is not a valid float"
    assert (
        validation_errors["sex"]["msg"]
        == "unexpected value; permitted: 'male', 'female'"
    )


def test_midparental_height_parental_heights_ge_fifty_expected_fail():
    body = {
        "height_paternal": "45",
        "height_maternal": "45",
        "sex": "male",
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["loc"][1]: error for error in response.json()["detail"]}

    assert (
        validation_errors["height_paternal"]["msg"]
        == "ensure this value is greater than or equal to 50"
    )
    assert (
        validation_errors["height_maternal"]["msg"]
        == "ensure this value is greater than or equal to 50"
    )


def test_midparental_height_paternal_height_lt_twofifty_expected_fail():
    body = {
        "height_paternal": "251",
        "height_maternal": "168",
        "sex": "male",
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    paternal_validation_errors = response.json()["detail"][0]

    assert (
        paternal_validation_errors["msg"]
        == "ensure this value is less than or equal to 250"
    )
    assert (
        paternal_validation_errors["msg"]
        == "ensure this value is less than or equal to 250"
    )


def test_midparental_height_maternal_height_lt_twofifty_expected_fail():
    body = {
        "height_paternal": "171",
        "height_maternal": "267",
        "sex": "male",
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    maternal_validation_errors = response.json()["detail"][0]

    assert (
        maternal_validation_errors["msg"]
        == "ensure this value is less than or equal to 250"
    )
    assert (
        maternal_validation_errors["msg"]
        == "ensure this value is less than or equal to 250"
    )
