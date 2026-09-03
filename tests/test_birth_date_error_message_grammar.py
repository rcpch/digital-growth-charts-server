"""
Regression test for an incongruous error-message sentence.

`chronological_calendar_age()` returns the standalone label "Birth date"
for an observation taken on the day of birth, rather than a noun phrase
such as "3 years, 2 months". validate_observation_value.py used to
interpolate that label directly into a sentence built for a noun phrase,
producing:

    "A height of 100.0 cm in a boy of Birth date is more than +8 SD.
     Please recheck the measurement and date of birth."

This asserts the corrected phrasing for both the +8 SD and -8 SD paths, on
the day of birth specifically (age zero, the only case that triggers the
"Birth date" label), and that the ordinary non-zero-age phrasing is
unaffected.
"""

from fastapi.testclient import TestClient

from main import app

client = TestClient(app)


def test_extreme_high_measurement_on_day_of_birth_has_grammatical_message():
    response = client.post(
        "/uk-who/calculation",
        json={
            "birth_date": "2024-01-01",
            "observation_date": "2024-01-01",
            "observation_value": 100.0,
            "sex": "male",
            "measurement_method": "height",
        },
    )
    assert response.status_code == 422
    msg = response.json()["detail"][0]["msg"]
    assert "at birth" in msg
    assert "of Birth date" not in msg
    assert msg == (
        "A height of 100.0 cm in a boy at birth is more than +8 SD. "
        "Please recheck the measurement and date of birth."
    )


def test_extreme_low_measurement_on_day_of_birth_has_grammatical_message():
    response = client.post(
        "/uk-who/calculation",
        json={
            "birth_date": "2024-01-01",
            "observation_date": "2024-01-01",
            "observation_value": 5.0,
            "sex": "female",
            "measurement_method": "height",
        },
    )
    assert response.status_code == 422
    msg = response.json()["detail"][0]["msg"]
    assert "at birth" in msg
    assert "of Birth date" not in msg
    assert msg == (
        "A height of 5.0 cm in a girl at birth is less than -8 SD. "
        "Please recheck the measurement and date of birth."
    )


def test_extreme_measurement_at_a_non_zero_age_is_unaffected():
    response = client.post(
        "/uk-who/calculation",
        json={
            "birth_date": "2020-01-01",
            "observation_date": "2024-01-01",
            "observation_value": 300.0,
            "sex": "male",
            "measurement_method": "height",
        },
    )
    assert response.status_code == 422
    msg = response.json()["detail"][0]["msg"]
    assert "at birth" not in msg
    assert " of " in msg
    assert "4 years" in msg
