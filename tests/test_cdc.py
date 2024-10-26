"""
Tests for the CDC endpoints
"""

# standard imports
import json
import hashlib

# third party imports
from fastapi.testclient import TestClient
import pytest

# local / rcpch imports
from main import app

client = TestClient(app)


def test_cdc_calculation_with_valid_request():

    body = {
        "birth_date": "2020-04-12",
        "observation_date": "2028-06-12",
        "observation_value": 115,
        "sex": "female",
        "gestation_weeks": 40,
        "gestation_days": 0,
        "measurement_method": "height",
        "bone_age": 10,
        "bone_age_centile": 98,
        "bone_age_sds": 2.0,
        "bone_age_text": "This bone age is advanced",
        "bone_age_type": "greulich-pyle",
        "events_text": ["Growth hormone start", "Growth Hormone Deficiency diagnosis"],
    }

    response = client.post("/cdc/calculation", json=body)

    assert response.status_code == 200

    # load the known-correct response from file
    with open(r"tests/test_data/test_cdc_calculation_valid.json", "r") as file:
        calculation_file = file.read()
    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)

    assert response.json() == json.loads(calculation_file)


def test_cdc_calculation_with_invalid_request():

    # this is a garbage request which should trigger appropriate validation responses
    body = {
        "birth_date": "invalid_birth_date",
        "observation_date": "invalid_observation_date",
        "observation_value": "invalid_observation_value",
        "sex": "invalid_sex",
        "gestation_weeks": "invalid_gestation_weeks",
        "gestation_days": "invalid_gestation_days",
        "measurement_method": "invalid_measurement_method",
    }

    response = client.post("/cdc/calculation", json=body)

    assert response.status_code == 422

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["loc"][1]: error for error in response.json()["detail"]}
    assert (
        validation_errors["birth_date"]["msg"]
        == "Value error, time data 'invalid_birth_date' does not match format '%Y-%m-%d'"
    )
    assert (
        validation_errors["gestation_days"]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert (
        validation_errors["gestation_weeks"]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert (
        validation_errors["measurement_method"]["msg"]
        == "Input should be 'height', 'weight', 'ofc' or 'bmi'"
    )
    assert (
        validation_errors["observation_date"]["msg"]
        == "Input should be a valid date or datetime, invalid character in year"
    )
    assert (
        validation_errors["observation_value"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert validation_errors["sex"]["msg"] == "Input should be 'male' or 'female'"


@pytest.mark.parametrize("input", [
    { "measurement_method": "height", "sex": "male" },
    { "measurement_method": "weight", "sex": "male" },
    { "measurement_method": "ofc", "sex": "male" },
    { "measurement_method": "bmi", "sex": "male" },
    { "measurement_method": "height", "sex": "female" },
    { "measurement_method": "weight", "sex": "female" },
    { "measurement_method": "ofc", "sex": "female" },
    { "measurement_method": "bmi", "sex": "female" }
])
def test_cdc_chart_data_with_valid_request(input):
    body = input | {
        "centile_format": "cole-nine-centiles",
        "is_sds": False,
    }

    response = client.post("/cdc/chart-coordinates", json=body)

    assert response.status_code == 200

    # TODO: Check the actual values returned. We do already validate it against the schema though.


def test_cdc_chart_data_with_invalid_request():
    body = {"measurement_method": "invalid_measurement_method", "sex": "invalid_sex"}

    response = client.post("/cdc/chart-coordinates", json=body)

    assert response.status_code == 422

    # COMMENTED OUT FOR BRANCH 'dockerise' PENDING DECISION ON #166 (API Test Suite) (pacharanero, 2024-02-07 )
    # restructure the response to make it easier to assert tests specifically
    # validation_errors = {error['loc'][1]: error for error in response.json(
    # )['detail']}
    # check the validation errors are the ones we expect
    # assert validation_errors['sex']['msg'] == "unexpected value; permitted: 'male', 'female'"
    # assert validation_errors['measurement_method']['msg'] == "unexpected value; permitted: 'height', 'weight', 'ofc', 'bmi'"


def test_cdc_fictional_child_data_with_valid_request():

    body = {
        "measurement_method": "height",
        "sex": "female",
        "start_chronological_age": 0,
        "end_age": 1,
        "gestation_weeks": 40,
        "gestation_days": 0,
        "measurement_interval_type": "days",
        "measurement_interval_number": 30,
        "start_sds": 0,
        "drift": False,
        "drift_range": -0.05,
        "noise": False,
        "noise_range": 0.005
    }

    response = client.post("/cdc/fictional-child-data", json=body)

    assert response.status_code == 200

    # load the known-correct response from file
    with open(
        r"tests/test_data/test_cdc_fictional_child_data_valid.json", "r"
    ) as file:
        fictional_child_data_file = file.read()
    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response.json() == json.loads(fictional_child_data_file)


def test_cdc_fictional_child_data_with_invalid_request():

    body = {
        "measurement_method": "invalid_measurement_method",
        "sex": "invalid_sex",
        "start_chronological_age": "invalid_start_chronological_age",
        "end_age": "invalid_end_age",
        "gestation_weeks": "invalid_gestation_weeks",
        "gestation_days": "invalid_gestation_days",
        "measurement_interval_type": "invalid_measurement_interval_type",
        "measurement_interval_number": "invalid_measurement_interval_number",
        "start_sds": "invalid_start_sds",
        "drift": "invalid_drift",
        "drift_range": "invalid_drift_range",
        "noise": "invalid_noise",
        "noise_range": "invalid_noise_range",
    }

    response = client.post("/cdc/fictional-child-data", json=body)

    assert response.status_code == 422

    # COMMENTED OUT FOR BRANCH 'dockerise' PENDING DECISION ON #166 (API Test Suite) (pacharanero, 2024-02-07 )
    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error["loc"][1]: error for error in response.json()["detail"]}
    assert (
        validation_errors["measurement_method"]["msg"]
        == "Input should be 'height', 'weight', 'ofc' or 'bmi'"
    )
    assert validation_errors["sex"]["msg"] == "Input should be 'male' or 'female'"
    assert (
        validation_errors["start_chronological_age"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert (
        validation_errors["end_age"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert (
        validation_errors["gestation_weeks"]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert (
        validation_errors["gestation_days"]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert (
        validation_errors["measurement_interval_type"]["msg"]
        == "Input should be 'd', 'day', 'days', 'w', 'week', 'weeks', 'm', 'month', 'months', 'y', 'year' or 'years'"
    )
    assert (
        validation_errors["measurement_interval_number"]["msg"]
        == "Input should be a valid integer, unable to parse string as an integer"
    )
    assert (
        validation_errors["start_sds"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert (
        validation_errors["drift"]["msg"]
        == "Input should be a valid boolean, unable to interpret input"
    )
    assert (
        validation_errors["drift_range"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
    assert (
        validation_errors["noise"]["msg"]
        == "Input should be a valid boolean, unable to interpret input"
    )
    assert (
        validation_errors["noise_range"]["msg"]
        == "Input should be a valid number, unable to parse string as a number"
    )
