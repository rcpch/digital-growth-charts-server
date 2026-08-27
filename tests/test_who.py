"""
Tests for the UK-WHO endpoints
"""

# standard imports
import json
import hashlib
from unittest import TestCase

# third party imports
from fastapi.testclient import TestClient
import pytest

# local / rcpch imports
from main import app
from tests import without_provenance

client = TestClient(app)


def test_who_calculation_with_valid_request():

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

    response = client.post("/who/calculation", json=body)

    assert response.status_code == 200

    # load the known-correct response from file
    with open(r"tests/test_data/test_who_calculation_valid.json", "r") as file:
        calculation_file = file.read()
    
    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    expected = json.loads(calculation_file)
    actual = without_provenance(response.json())

    TestCase().assertDictEqual(expected, actual)


def test_who_calculation_with_invalid_request():

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

    response = client.post("/who/calculation", json=body)

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
    { "measurement_method": "height", "observation_value": 200, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # height too tall
    { "measurement_method": "height", "observation_value": 5, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # height too short
    { "measurement_method": "weight", "observation_value": 200, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # weight too high
    { "measurement_method": "weight", "observation_value": 1, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # weight too low
    { "measurement_method": "ofc", "observation_value": 500, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # head circumference too high
    { "measurement_method": "ofc", "observation_value": 1, "birth_date": "2015-10-26", "observation_date": "2020-09-01", "sex": "female" }, # head circumference too low
    { "measurement_method": "ofc", "observation_value": 500, "birth_date": "2015-10-26", "observation_date": "2034-09-01", "sex": "male" }, # 19y boy head circumference beyond age range
    { "measurement_method": "ofc", "observation_value": 1, "birth_date": "2015-10-26", "observation_date": "2033-09-01", "sex": "female" }, # 18y girl head circumference beyond age range
    { "measurement_method": "height", "observation_value": 175, "birth_date": "2015-10-26", "observation_date": "2036-09-01", "sex": "female" }, # height too old (>20y)
    { "measurement_method": "height", "observation_value": 45, "birth_date": "2015-10-26", "observation_date": "2015-10-26", "sex": "female", "gestation_weeks": 23, "gestation_days": 0 }, # height too young (<25 weeks)
    { "measurement_method": "weight", "observation_value": 200, "birth_date": "2015-10-26", "observation_date": "2036-09-01", "sex": "female" }, # weight too old (>20y)
    { "measurement_method": "weight", "observation_value": 1, "birth_date": "2015-10-26", "observation_date": "2015-10-26", "sex": "female", "gestation_weeks": 22, "gestation_days": 0 }, # weight too young (<23 weeks)
])
def test_who_chart_with_valid_request_for_outside_range_values(input):

    body = input
    response = client.post("/who/calculation", json=body)

    assert response.status_code == 422


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
def test_who_chart_data_with_valid_request(input):
    body = input | {
        "centile_format": "cole-nine-centiles",
        "is_sds": False,
    }

    response = client.post("/who/chart-coordinates", json=body)

    assert response.status_code == 200

    # TODO: Check the actual values returned. We do already validate it against the schema though.


def test_who_chart_data_with_invalid_request():
    body = {"measurement_method": "invalid_measurement_method", "sex": "invalid_sex"}

    response = client.post("/who/chart-coordinates", json=body)

    assert response.status_code == 422


def test_who_fictional_child_data_with_valid_request():

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
        "noise_range": 0.005,
    }

    response = client.post("/who/fictional-child-data", json=body)

    assert response.status_code == 200

    # load the known-correct response from file
    with open(
        r"tests/test_data/test_who_fictional_child_data_valid.json", "r"
    ) as file:
        fictional_child_data_file = file.read()
    
    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    expected = json.loads(fictional_child_data_file)
    actual = without_provenance(response.json())

    TestCase().assertListEqual(expected, actual)


def test_who_fictional_child_data_with_invalid_request():

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

    response = client.post("/who/fictional-child-data", json=body)

    assert response.status_code == 422

    # COMMENTED OUT FOR BRANCH 'dockerise' PENDING DECISION ON #166 (API Test Suite) (pacharanero, 2024-02-07 )
    # restructure the response to make it easier to assert tests specifically


def test_who_bulk_calculation_all_valid():
    body = {
        "measurement_method": "height",
        "birth_date": "2020-04-12",
        "sex": "female",
        "gestation_weeks": 40,
        "gestation_days": 0,
        "observations": [
            {"observation_date": "2028-06-12", "observation_value": 115},
            {"observation_date": "2028-07-12", "observation_value": 118},
        ],
    }
    response = client.post("/who/bulk-calculation", json=body)
    assert response.status_code == 200
    data = response.json()
    assert "results" in data
    assert len(data["results"]) == 2
    assert all("measurement_calculated_values" in r for r in data["results"])


def test_who_bulk_calculation_partially_valid():
    body = {
        "measurement_method": "height",
        "birth_date": "2020-04-12",
        "sex": "female",
        "gestation_weeks": 40,
        "gestation_days": 0,
        "observations": [
            {"observation_date": "2028-06-12", "observation_value": 115},  # valid
            {"observation_date": "2028-07-12", "observation_value": 500},  # invalid height too large
        ],
    }
    response = client.post("/who/bulk-calculation", json=body)
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 2
    assert any("measurement_calculated_values" in r for r in results)
    assert any("msg" in r for r in results)


def test_who_bulk_calculation_all_invalid():
    body = {
        "measurement_method": "height",
        "birth_date": "2020-04-12",
        "sex": "female",
        "gestation_weeks": 40,
        "gestation_days": 0,
        "observations": [
            {"observation_date": "2028-06-12", "observation_value": 500},
            {"observation_date": "2028-07-12", "observation_value": 501},
        ],
    }
    response = client.post("/who/bulk-calculation", json=body)
    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 2
    assert all("msg" in r for r in results)
