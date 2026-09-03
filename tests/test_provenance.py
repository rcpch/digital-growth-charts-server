"""Tests for calculation provenance in Measurement responses."""

from importlib.metadata import version as distribution_version

import pytest
from fastapi.testclient import TestClient
from pydantic import ValidationError

from main import app
from schemas.response_schema_classes import APIServer, MeasurementObject
from server_metadata import API_SERVER_COMMIT, API_SERVER_NAME, API_SERVER_VERSION


client = TestClient(app)

CALCULATION_REQUEST = {
    "birth_date": "2020-04-12",
    "observation_date": "2028-06-12",
    "observation_value": 115,
    "sex": "female",
    "gestation_weeks": 40,
    "gestation_days": 0,
    "measurement_method": "height",
}


def assert_api_server_provenance(provenance):
    assert provenance["api_server"] == {
        "name": API_SERVER_NAME,
        "version": API_SERVER_VERSION,
        "commit": API_SERVER_COMMIT,
    }


@pytest.mark.parametrize(
    ("endpoint", "growth_reference"),
    [
        ("uk-who", "uk-who"),
        ("trisomy-21", "trisomy-21"),
        ("trisomy-21-aap", "trisomy-21-aap"),
        ("turner", "turners-syndrome"),
        ("cdc", "cdc"),
        ("who", "who"),
    ],
)
def test_calculation_passes_through_package_provenance(endpoint, growth_reference):
    response = client.post(f"/{endpoint}/calculation", json=CALCULATION_REQUEST)

    assert response.status_code == 200
    provenance = response.json()["provenance"]
    assert provenance["growth_reference"] == growth_reference
    assert provenance["calculation_engine"]["name"] == "rcpchgrowth"
    assert provenance["calculation_engine"]["version"] == distribution_version(
        "rcpchgrowth"
    )
    assert provenance["calculation_engine"]["commit"]
    assert_api_server_provenance(provenance)


def test_bulk_calculation_passes_through_provenance_without_changing_inline_errors():
    response = client.post(
        "/uk-who/bulk-calculation",
        json={
            "birth_date": "2020-04-12",
            "sex": "female",
            "gestation_weeks": 40,
            "gestation_days": 0,
            "measurement_method": "height",
            "observations": [
                {"observation_date": "2028-06-12", "observation_value": 115},
                {"observation_date": "2019-06-12", "observation_value": 115},
            ],
        },
    )

    assert response.status_code == 200
    assert response.json()["results"][0]["provenance"]["growth_reference"] == "uk-who"
    assert_api_server_provenance(response.json()["results"][0]["provenance"])
    assert response.json()["results"][1]["type"] == "value_error"
    assert "provenance" not in response.json()["results"][1]


def test_fictional_child_measurements_pass_through_provenance():
    response = client.post(
        "/uk-who/fictional-child-data",
        json={
            "measurement_method": "height",
            "sex": "female",
            "start_chronological_age": 0,
            "end_age": 0.1,
            "gestation_weeks": 40,
            "gestation_days": 0,
            "measurement_interval_type": "days",
            "measurement_interval_number": 30,
            "start_sds": 0,
            "drift": False,
            "noise": False,
        },
    )

    assert response.status_code == 200
    assert response.json()
    assert all(
        measurement["provenance"]["growth_reference"] == "uk-who"
        for measurement in response.json()
    )
    assert all(
        measurement["provenance"]["api_server"]
        == {
            "name": API_SERVER_NAME,
            "version": API_SERVER_VERSION,
            "commit": API_SERVER_COMMIT,
        }
        for measurement in response.json()
    )


def test_measurement_schema_rejects_invalid_reference_and_filters_unknown_fields():
    response = client.post("/uk-who/calculation", json=CALCULATION_REQUEST)
    measurement = response.json()
    measurement["unrelated_field"] = "filtered"

    validated = MeasurementObject.model_validate(measurement)

    assert "unrelated_field" not in validated.model_dump()

    measurement["provenance"]["growth_reference"] = "invalid"
    with pytest.raises(ValidationError):
        MeasurementObject.model_validate(measurement)


def test_api_server_schema_rejects_invalid_build_identity():
    with pytest.raises(ValidationError):
        APIServer(
            name="digital-growth-charts-server",
            version="5.0.0",
            commit="not-a-commit",
        )


def test_openapi_documents_required_provenance_contract():
    schema = app.openapi()["components"]["schemas"]

    assert "provenance" in schema["MeasurementObject"]["required"]
    assert schema["Provenance"]["required"] == [
        "growth_reference",
        "calculation_engine",
        "api_server",
    ]
    assert schema["Provenance"]["properties"]["growth_reference"]["enum"] == [
        "uk-who",
        "trisomy-21",
        "trisomy-21-aap",
        "turners-syndrome",
        "cdc",
        "who",
    ]
    assert schema["APIServer"]["required"] == ["name", "version", "commit"]
    assert (
        schema["APIServer"]["properties"]["name"]["const"]
        == "digital-growth-charts-server"
    )
