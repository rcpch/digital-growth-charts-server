"""
Tests for the UK-WHO endpoints
"""

# standard imports
import json
import hashlib

# third party imports
from fastapi.testclient import TestClient

# local / rcpch imports
from main import app

client = TestClient(app)

def test_ukwho_calculation_with_valid_request():
    
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
        "events_text": ["Growth hormone start", "Growth Hormone Deficiency diagnosis"]
    }
    
    response = client.post("/uk-who/calculation", json=body)

    # load the known-correct response from file
    with open(r'tests/test_data/test_ukwho_calculation_valid.json', 'r') as file:
        calculation_file = file.read()

    assert response.status_code == 200

    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response.json() == json.loads(calculation_file)


def test_ukwho_calculation_with_invalid_request():
    
    # this is a garbage request which should trigger appropriate validation responses
    body = {
        "birth_date": "invalid_birth_date",
        "observation_date": "invalid_observation_date",
        "observation_value": "invalid_observation_value",
        "sex": "invalid_sex",
        "gestation_weeks": "invalid_gestation_weeks",
        "gestation_days": "invalid_gestation_days",
        "measurement_method": "invalid_measurement_method"
    }

    response = client.post("/uk-who/calculation", json=body)

    assert response.status_code == 422
    
    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error['loc'][1]: error for error in response.json(
    )['detail']}
       
    assert validation_errors['birth_date']['msg'] == "time data 'invalid_birth_date' does not match format '%Y-%m-%d'"
    assert validation_errors['gestation_days']['msg'] == "value is not a valid integer"
    assert validation_errors['gestation_weeks']['msg'] == "value is not a valid integer"
    assert validation_errors['measurement_method']['msg'] == "unexpected value; permitted: 'height', 'weight', 'ofc', 'bmi'"
    assert validation_errors['observation_date']['msg'] == "invalid date format"
    assert validation_errors['observation_value']['msg'] == "value is not a valid float"
    assert validation_errors['sex']['msg'] == "unexpected value; permitted: 'male', 'female'"


def test_ukwho_chart_data_with_valid_request():
    body = {
        "measurement_method": "height",
        "sex": "male",
        "centile_format": "cole-nine-centiles",
        "is_sds": False
    }

    response = client.post("/uk-who/chart-coordinates", json=body)
        
    assert response.status_code == 200

    # load the known-correct response from file and create a hash of it
    with open(r'tests/test_data/test_uk_who_male_height_valid.json', 'r') as file:
        chart_data_file = file.read()

    # hash both JSON objects which should be identical
    # hashing was the only efficient way to compare these two large (~500k) files
    # it will be harder to debug any new difference (consider saving files to disk and compare)
    response_hash = hashlib.sha256(json.dumps(response.json()['centile_data'], separators=(',', ':')).encode('utf-8')).hexdigest()
    chart_data_file_hash = hashlib.sha256(chart_data_file.encode('utf-8')).hexdigest()
    
    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response_hash == chart_data_file_hash

    # IMPORTANT: ONLY MALE, HEIGHT, UK-WHO is currently tested
    # This test is a template which could be used for testing the
    # other chart data responses (female/male and weight/bmi/ofc)


def test_ukwho_chart_data_with_invalid_request():
    body={
            "measurement_method": "invalid_measurement_method",
            "sex": "invalid_sex"
            }

    response=client.post("/uk-who/chart-coordinates", json=body)

    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error['loc'][1]: error for error in response.json(
    )['detail']}
    
    assert response.status_code == 422
    
    # check the vaildation errors are the ones we expect
    assert validation_errors['sex']['msg'] == "unexpected value; permitted: 'male', 'female'"
    assert validation_errors['measurement_method']['msg'] == "unexpected value; permitted: 'height', 'weight', 'ofc', 'bmi'"
    

def test_ukwho_fictional_child_data_with_valid_request():

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
        "reference": "uk-who"
    }

    response = client.post("/uk-who/fictional-child-data", json=body)

    # load the known-correct response from file
    with open(r'tests/test_data/test_ukwho_fictional_child_data_valid.json', 'r') as file:
        fictional_child_data_file = file.read()

    assert response.status_code == 200

    # load the two JSON responses as Python Dicts so enable comparison (slow but more reliable)
    assert response.json() == json.loads(fictional_child_data_file)


def test_ukwho_fictional_child_data_with_invalid_request():

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
        "reference": "invalid_reference"
    }

    response = client.post("/uk-who/fictional-child-data", json=body)
    
    assert response.status_code == 422
    
    # restructure the response to make it easier to assert tests specifically
    validation_errors = {error['loc'][1]: error for error in response.json(
    )['detail']}

    assert validation_errors['measurement_method']['msg'] == "unexpected value; permitted: 'height', 'weight', 'ofc', 'bmi'"
    assert validation_errors['sex']['msg'] == "unexpected value; permitted: 'male', 'female'"
    assert validation_errors['start_chronological_age']['msg'] == "value is not a valid float"
    assert validation_errors['end_age']['msg'] == "value is not a valid float"
    assert validation_errors['gestation_weeks']['msg'] == "value is not a valid integer"
    assert validation_errors['gestation_days']['msg'] == "value is not a valid integer"
    assert validation_errors['measurement_interval_type']['msg'] == "unexpected value; permitted: 'd', 'day', 'days', 'w', 'week', 'weeks', 'm', 'month', 'months', 'y', 'year', 'years'"
    assert validation_errors['measurement_interval_number']['msg'] == "value is not a valid integer"
    assert validation_errors['start_sds']['msg'] == "value is not a valid float"
    assert validation_errors['drift']['msg'] == "value could not be parsed to a boolean"
    assert validation_errors['drift_range']['msg'] == "value is not a valid float"
    assert validation_errors['noise']['msg'] == "value could not be parsed to a boolean"
    assert validation_errors['noise_range']['msg'] == "value is not a valid float"
    assert validation_errors['reference']['msg'] == "unexpected value; permitted: 'uk-who', 'trisomy-21', 'turners-syndrome'"
