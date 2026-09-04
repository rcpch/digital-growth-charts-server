"""Tests for versioned API response contracts."""

from configparser import ConfigParser
import json
from pathlib import Path

from fastapi.testclient import TestClient

from main import app
from schemas import UnprocessableEntityResponse
from server_metadata import API_SERVER_COMMIT


client = TestClient(app, raise_server_exceptions=False)
PROJECT_ROOT = Path(__file__).parent.parent


def test_api_version_is_consistent():
    bumpversion_config = ConfigParser()
    bumpversion_config.read(PROJECT_ROOT / ".bumpversion.cfg")
    expected_version = bumpversion_config["bumpversion"]["current_version"]

    citation_version = next(
        line.removeprefix("version: ")
        for line in (PROJECT_ROOT / "CITATION.cff").read_text().splitlines()
        if line.startswith("version: ")
    )
    committed_openapi = json.loads((PROJECT_ROOT / "openapi.json").read_text())

    assert {
        "bumpversion:file:server_metadata.py",
        "bumpversion:file:CITATION.cff",
        "bumpversion:file:openapi.json",
    }.issubset(bumpversion_config.sections())
    assert app.openapi()["info"]["version"] == expected_version
    assert citation_version == expected_version
    assert committed_openapi["info"]["version"] == expected_version


def test_root_identifies_api_server_commit():
    response = client.get("/")

    assert response.headers["X-Git-Revision"] == API_SERVER_COMMIT


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


def test_undefined_extreme_centile_chart_points_are_null_not_500():
    # For some ages the inverse Box-Cox transform has no real solution at
    # the 99.99th centile, so the engine emits y: null. The response model
    # must accept null y values and return a valid chart response rather
    # than failing validation with a 500 (#285).
    for path in ("/cdc/chart-coordinates", "/trisomy-21/chart-coordinates"):
        response = client.post(
            path,
            json={
                "sex": "female" if "cdc" in path else "male",
                "measurement_method": "weight" if "cdc" in path else "bmi",
                "is_sds": False,
                "centile_format": "eighty-five-percent-centiles",
            },
        )

        assert response.status_code == 200, path
        body = response.json()

        null_ys = [
            point
            for segment in body["centile_data"]
            if isinstance(segment, dict)
            for reference in segment.values()
            if isinstance(reference, dict)
            for sex in reference.values()
            if isinstance(sex, dict)
            for measurement in sex.values()
            if measurement
            for series in measurement
            for point in (series["data"] or [])
            if point["y"] is None
        ]
        assert null_ys, path


def test_openapi_declares_production_server_and_api_key_security():
    # The embedded Swagger UI on the documentation site resolves relative
    # operation paths against the declared servers and prompts for the
    # declared security credentials. Without them, "Try it out" requests
    # are sent to the host serving the schema instead of the API
    # gateway (#284).
    schema = app.openapi()

    assert {
        "url": "https://api.rcpch.ac.uk/growth/v1",
        "description": "Production (Azure API Management)",
    } in schema["servers"]

    security_scheme = schema["components"]["securitySchemes"]["apiKey"]
    assert security_scheme["type"] == "apiKey"
    assert security_scheme["name"] == "Subscription-Key"
    assert security_scheme["in"] == "header"

    assert schema["security"] == [{"apiKey": []}]
