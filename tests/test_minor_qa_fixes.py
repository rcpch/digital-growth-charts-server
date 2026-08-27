"""Focused regression tests for small defects found during Provenance work."""

import pytest
from fastapi.testclient import TestClient

from main import app


client = TestClient(app, raise_server_exceptions=False)

REFERENCE_ROUTES = [
    "/uk-who",
    "/who",
    "/cdc",
    "/trisomy-21",
    "/trisomy-21-aap",
    "/turner",
]


@pytest.mark.parametrize("sex", ["male", "female"])
def test_who_mid_parental_height_uses_who_adult_age(sex):
    response = client.post(
        "/utilities/mid-parental-height",
        json={
            "height_paternal": 178,
            "height_maternal": 165,
            "sex": sex,
            "reference": "who",
        },
    )

    assert response.status_code == 200
    assert response.json()["mid_parental_height"] is not None


@pytest.mark.parametrize("prefix", REFERENCE_ROUTES)
def test_bulk_calculation_keeps_valid_items_when_an_observation_precedes_birth(prefix):
    response = client.post(
        f"{prefix}/bulk-calculation",
        json={
            "measurement_method": "height",
            "birth_date": "2020-01-01",
            "sex": "female",
            "observations": [
                {"observation_date": "2019-01-01", "observation_value": 50},
                {"observation_date": "2021-01-01", "observation_value": 75},
            ],
        },
    )

    assert response.status_code == 200
    results = response.json()["results"]
    assert len(results) == 2
    assert "Birth date cannot be after the date of observation" in results[0]["msg"]
    assert "measurement_calculated_values" in results[1]


@pytest.mark.parametrize(
    "body",
    [
        {"sex": "male", "measurement_method": "height"},
        {"sex": "female", "measurement_method": "weight"},
    ],
)
def test_turner_chart_rejects_unsupported_sex_or_measurement(body):
    response = client.post(
        "/turner/chart-coordinates",
        json={
            **body,
            "is_sds": False,
            "centile_format": "cole-nine-centiles",
        },
    )

    assert response.status_code == 422
    assert response.json()["detail"][0]["msg"] == "Turner data only exists for height in girls."
