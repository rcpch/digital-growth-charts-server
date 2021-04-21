"""
Tests the validation of the inputs to Measurement class at instantiation
"""

# standard imports
from datetime import datetime
import pytest

# third-party imports
from marshmallow import exceptions

# rcpch imports
from rcpchgrowth import Measurement


def test_measurement_class_with_invalid_sex_type():
    """
    Should raise a Marshmallow ValidationError (sex must be a string)
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex=0,
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="weight",
            observation_value=5.0,
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who"
        )
    assert "{'sex': ['Not a valid string.']}" in (str(error_info.value))


def test_measurement_class_with_invalid_sex_string():
    """
    Should raise a ValueError (sex must be "male" OR "female")
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="maleS",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="weight",
            observation_value=5.0,
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who"
        )
    assert "{'sex': ['Must be one of: male, female.']}" in (
        str(error_info.value))


def test_measurement_class_with_invalid_birth_date_type():
    """
    Should raise an AttributeError during date -> str conversion (date must be a Python datetime object)
    """
    with pytest.raises(AttributeError) as error_info:
        Measurement(
            sex="male",
            birth_date="Date strings are not valid!",
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="weight",
            observation_value=5.0,
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who"
        )
    assert "'str' object has no attribute 'strftime'" in str(error_info.value)


def test_measurement_class_with_invalid_birth_data():
    """
    Should raise an (observation_date must be after birth_date)
    """
    m = Measurement(
        sex="male",
        birth_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
        observation_date=datetime.strptime("2020-05-01", "%Y-%m-%d"),
        measurement_method="weight",
        observation_value=5.0,
        gestation_weeks=0,
        gestation_days=40,
        reference="uk-who"
    ).measurement

    # This assertion may change once issues #155 and #157 are closed
    assert m["measurement_dates"]["chronological_decimal_age_error"] == "Chronological age calculation error."
