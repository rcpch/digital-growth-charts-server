"""Tests for versioned API response contracts."""

from fastapi.testclient import TestClient

from main import app
from schemas import UnprocessableEntityResponse


client = TestClient(app, raise_server_exceptions=False)


def test_api_contract_is_version_five():
    assert app.openapi()["info"]["version"] == "5.0.0"


def test_native_validation_error_uses_standard_422_response():
    response = client.post("/who/calculation", json={})

    assert response.status_code == 422
    validated = UnprocessableEntityResponse.model_validate(response.json())
    assert validated.detail
    assert all(error.loc and error.msg and error.type for error in validated.detail)


def test_structured_application_error_uses_standard_422_response():
    response = client.post(
        "/turner/calculation",
        json={
            "birth_date": "2020-04-12",
            "observation_date": "2024-06-12",
            "observation_value": 78,
            "measurement_method": "height",
            "sex": "male",
        },
    )

    assert response.status_code == 422
    validated = UnprocessableEntityResponse.model_validate(response.json())
    assert validated.detail[0].msg == "Turner reference data only exists in girls."


def test_string_application_error_is_normalized_to_standard_422_response():
    response = client.post(
        "/turner/chart-coordinates",
        json={
            "sex": "male",
            "measurement_method": "height",
            "is_sds": False,
            "centile_format": "cole-nine-centiles",
        },
    )

    assert response.status_code == 422
    assert response.json() == {
        "detail": [
            {
                "loc": ["request"],
                "msg": "Turner data only exists for height in girls.",
                "type": "value_error",
                "input": None,
            }
        ]
    }
    UnprocessableEntityResponse.model_validate(response.json())


def test_all_post_operations_document_standard_422_response():
    schema = app.openapi()

    for path, path_item in schema["paths"].items():
        if "post" not in path_item:
            continue
        response_schema = path_item["post"]["responses"]["422"]["content"][
            "application/json"
        ]["schema"]
        assert response_schema == {
            "$ref": "#/components/schemas/UnprocessableEntityResponse"
        }, path

    error_detail_schema = schema["components"]["schemas"]["APIErrorDetail"]
    assert set(error_detail_schema["required"]) == {"type", "loc", "msg"}
