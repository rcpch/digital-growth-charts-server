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


def test_midparental_height_ukwho_with_valid_request():
    """
    Test the mid-parental height endpoint with a valid request using the UK-WHO reference.
    Note this does not test the centile data response against the file as there are subtle differences 
    in precision between the two calculations at many decimal places.
    """
    body = {"height_paternal": 171, "height_maternal": 168, "sex": "male", "reference":"uk-who" }

    response = client.post("/utilities/mid-parental-height", json=body)

    # load the known-correct response from file
    with open(r"tests/test_data/test_midparental_height_ukwho_valid.json", "r") as file:
        calculation_file = file.read()

    assert response.status_code == 200

    file_data = json.loads(calculation_file)
    assert round(float(file_data['mid_parental_height']),1)==float(response.json()['mid_parental_height']), f"mid_parental_height for uk-who should be {round(float(file_data['mid_parental_height']),1)} but returned {float(response.json()['mid_parental_height'])}"
    assert round(float(file_data['mid_parental_height_sds']),3)==float(response.json()['mid_parental_height_sds']), f"mid_parental_height_sds for uk-who should be {round(float(file_data['mid_parental_height_sds']),3)} but returned {float(response.json()['mid_parental_height_sds'])}"
    assert round(float(file_data['mid_parental_height_centile']),2)==float(response.json()['mid_parental_height_centile']), f"mid_parental_height_centile for uk-who should be {round(float(file_data['mid_parental_height_centile']),2)} but returned {float(response.json()['mid_parental_height_centile'])}"
    assert round(float(file_data["mid_parental_height_upper_value"]),1)==float(response.json()["mid_parental_height_upper_value"]), f"mid_parental_height_upper_value for uk-who should be {round(float(file_data['mid_parental_height_upper_value']),1)} but returned {float(response.json()['mid_parental_height_upper_value'])}"
    assert round(float(file_data["mid_parental_height_lower_value"]),1)==float(response.json()["mid_parental_height_lower_value"]), f"mid_parental_height_lower_value for uk-who should be {round(float(file_data['mid_parental_height_lower_value']),1)} but returned {float(response.json()['mid_parental_height_lower_value'])}"


def test_midparental_height_cdc_with_valid_request():
    """
    Test the mid-parental height endpoint with a valid request using the CDC reference.
    Note this does not test the centile data response against the file as there are subtle differences 
    in precision between the two calculations at many decimal places.
    """
    body = {"height_paternal": 171, "height_maternal": 168, "sex": "male", "reference":"cdc" }

    response = client.post("/utilities/mid-parental-height", json=body)

    # load the known-correct response from file
    with open(r"tests/test_data/test_midparental_height_cdc_valid.json", "r") as file:
        calculation_file = file.read()

    assert response.status_code == 200

    file_data = json.loads(calculation_file)
    assert round(float(file_data['mid_parental_height']),1)==float(response.json()['mid_parental_height']), f"mid_parental_height for uk-who should be {round(float(file_data['mid_parental_height']),1)} but returned {float(response.json()['mid_parental_height'])}"
    assert round(float(file_data['mid_parental_height_sds']),3)==float(response.json()['mid_parental_height_sds']), f"mid_parental_height_sds for uk-who should be {round(float(file_data['mid_parental_height_sds']),3)} but returned {float(response.json()['mid_parental_height_sds'])}"
    assert round(float(file_data['mid_parental_height_centile']),2)==float(response.json()['mid_parental_height_centile']), f"mid_parental_height_centile for uk-who should be {round(float(file_data['mid_parental_height_centile']),2)} but returned {float(response.json()['mid_parental_height_centile'])}"
    assert round(float(file_data["mid_parental_height_upper_value"]),1)==float(response.json()["mid_parental_height_upper_value"]), f"mid_parental_height_upper_value for uk-who should be {round(float(file_data['mid_parental_height_upper_value']),1)} but returned {float(response.json()['mid_parental_height_upper_value'])}"
    assert round(float(file_data["mid_parental_height_lower_value"]),1)==float(response.json()["mid_parental_height_lower_value"]), f"mid_parental_height_lower_value for uk-who should be {round(float(file_data['mid_parental_height_lower_value']),1)} but returned {float(response.json()['mid_parental_height_lower_value'])}"


def test_midparental_height_with_invalid_request():
    body = {
        "height_paternal": "invalid_height_paternal",
        "height_maternal": "invalid_height_maternal",
        "sex": "invalid_sex",
        "reference":"uk-who"
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    # load the known-correct response from file
    with open(r"tests/test_data/test_midparental_height_ukwho_valid.json", "r") as file:
        calculation_file = file.read()

    assert response.status_code == 422

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["loc"][1]: error for error in response.json()["detail"]}

    assert (
        validation_errors["height_paternal"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert (
        validation_errors["height_maternal"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert validation_errors["sex"]["msg"] == "Input should be 'male' or 'female'"


def test_midparental_height_parental_heights_ge_fifty_expected_fail():
    body = {
        "height_paternal": "45",
        "height_maternal": "45",
        "sex": "male",
        "reference":"uk-who"
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["input"]: error["msg"] for error in response.json()["detail"]}

    assert (
        validation_errors["height_paternal"]
        == "Error: The paternal height is < -8 SD. Please check the accuracy of the paternal height and try again."
    )
    assert (
        validation_errors["height_maternal"]
        == "Error: The maternal height is < -8 SD. Please check the accuracy of the maternal height and try again."
    )


def test_midparental_height_paternal_height_lt_sixsd_expected_fail():
    body = {
        "height_paternal": "251",
        "height_maternal": "168",
        "sex": "male",
        "reference":"uk-who"
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    paternal_validation_errors = {error["input"]: error["msg"] for error in response.json()["detail"]}

    assert (
        paternal_validation_errors["height_paternal"] == "Error: The paternal height is > 8 SD. Please check the accuracy of the paternal height and try again."
    )


def test_midparental_height_maternal_height_lt_sixsd_expected_fail():
    body = {
        "height_paternal": "171",
        "height_maternal": "267",
        "sex": "male",
        "reference":"uk-who"
    }

    response = client.post("/utilities/mid-parental-height", json=body)

    assert response.status_code == 422

    maternal_validation_errors = {error["input"]: error["msg"] for error in response.json()["detail"]}

    assert (
        maternal_validation_errors["height_maternal"] == "Error: The maternal height is > 8 SD. Please check the accuracy of the maternal height and try again."
    )
