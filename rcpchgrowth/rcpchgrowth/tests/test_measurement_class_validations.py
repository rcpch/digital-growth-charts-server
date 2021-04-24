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

def test_measurement_class_with_invalid_observation_date_type():
    """
    Should raise an AttributeError during date -> str conversion (date must be a Python datetime object)
    """
    with pytest.raises(AttributeError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            observation_date="Date strings are not valid!",
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

def test_measurement_class_with_invalid_measurement_method():
    """
    Should raise a ValueError (value should be one of [height, weight, bmi, ofc.])
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="length",
            observation_value=5.0,
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who")

    assert "{'measurement_method': ['Must be one of: height, weight, bmi, ofc.']}" in (str(error_info.value))

def test_measurement_class_with_invalid_measurement_method_type():
    """
    Should raise a ValidationError as measurement_method must be a str
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method=25,
            observation_value=5.0,
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who")

    assert "{'measurement_method': ['Not a valid string.']}" in (str(error_info.value))

def test_measurement_class_with_invalid_observation_value_type():
    """
    Should raise a ValidationError as measurement_method must be a float
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="height",
            observation_value="tall",
            gestation_weeks=0,
            gestation_days=40,
            reference="uk-who")

    assert "{'observation_value': ['Not a valid number.']}" in (str(error_info.value))


def test_measurement_class_with_invalid_observation_value_weight_high():
    """
    Should raise an (too high value error)
    """
    m = Measurement(
        sex="male",
        birth_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
        observation_date=datetime.strptime("2020-07-01", "%Y-%m-%d"),
        measurement_method="weight",
        observation_value=1000,
        gestation_weeks=0,
        gestation_days=40,
        reference="uk-who"
    ).measurement

    # This assertion may change once issues #155 and #157 are closed
    assert m["child_observation_value"]["observation_value_error"] == "1000 kilograms is very high. Weight must be passed in kilograms."

def test_measurement_class_with_invalid_observation_value_height_low():
    """
    Should raise an (height should be cm not metres error)
    """
    m = Measurement(
        sex="male",
        birth_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
        observation_date=datetime.strptime("2020-07-01", "%Y-%m-%d"),
        measurement_method="height",
        observation_value=1,
        gestation_weeks=0,
        gestation_days=40,
        reference="uk-who"
    ).measurement


    assert m["child_observation_value"]["observation_value_error"] == "Height/length must be passed in cm, not metres"

# def test_measurement_class_with_invalid_observation_value_gestation_weeks_low():
#     """
#     Should raise an (gestation_weeks range error)
#     """
#     m = Measurement(
#         sex="male",
#         birth_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
#         observation_date=datetime.strptime("2020-07-01", "%Y-%m-%d"),
#         measurement_method="height",
#         observation_value=53,
#         gestation_weeks=21,
#         gestation_days=2,
#         reference="uk-who"
#     ).measurement

#     assert m["child_observation_value"]["observation_value_error"] == "Height/length must be passed in cm, not metres" - returns {"gestation_weeks": ["Must be greater than or equal to 22 and less than or equal to 44."]} on the API?

def test_measurement_class_with_invalid_gestation_weeks_type():
    """
    Should raise a ValidationError as gestation_weeks must be a float
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="height",
            observation_value=53,
            gestation_weeks="two",
            gestation_days=40,
            reference="uk-who")

    assert "{'gestation_weeks': ['Not a valid number.']}" in (str(error_info.value))

def test_measurement_class_with_invalid_gestation_days_type():
    """
    Should raise a ValidationError as gestation_days must be a float
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="height",
            observation_value=53,
            gestation_weeks=40,
            gestation_days="three",
            reference="uk-who")

    assert "{'gestation_days': ['Not a valid number.']}" in (str(error_info.value))

def test_measurement_class_with_invalid_reference_type():
    """
    Should raise a ValidationError as reference must be a str
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="height",
            observation_value=53,
            gestation_weeks=40,
            gestation_days=3,
            reference=123)

    assert "{'reference': ['Not a valid string.']}" in (str(error_info.value))


def test_measurement_class_with_invalid_reference():
    """
    Should raise a ValidationError as reference must be one of ["uk-who", "turners-syndrome", "trisomy-21"]
    """
    with pytest.raises(exceptions.ValidationError) as error_info:
        Measurement(
            sex="male",
            birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
            observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
            measurement_method="height",
            observation_value=53,
            gestation_weeks=40,
            gestation_days=3,
            reference="who")

    assert "{'reference': ['Must be one of: uk-who, turners-syndrome, trisomy-21.']}" in (str(error_info.value))