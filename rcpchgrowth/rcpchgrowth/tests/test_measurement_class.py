# standard imports
from datetime import datetime
import json
import os

# third-party imports
from marshmallow import exceptions
import pytest

# rcpch imports
from rcpchgrowth import Measurement, global_functions

# the ACCURACY constant defines the accuracy of the test comparisons
# owing to variations in statistical calculations it's impossible to get exact
# agreement between R and Python, so our statistician feels we can set a tolerance
# within which we will accept a result as correct.

ACCURACY = 1e-3


def load_valid_data_set():
    """
    Loads in the testing data from JSON file
    """
    with open(os.path.abspath(os.path.dirname(__file__)) + "/validation_sds-2021.json") as f:
        return json.load(f)


# @pytest.mark.parametrize("line", load_valid_data_set())
# def test_measurement_class_with_valid_data_set(line):
#     print(line)
#     """
#     Test which iterates through a JSON file of fictional children and known calculated (TC via R)
#       correct SDS values. Compares the output of the Measurement.measurement method with the known
#       correct value.
#     """

#     measurement_object = Measurement(
#         sex=str(line["sex"]),
#         birth_date=datetime.strptime(line["birth_date"], "%Y-%m-%d"),
#         observation_date=datetime.strptime(
#             line["observation_date"], "%Y-%m-%d"),
#         measurement_method=str(line["measurement_method"]),
#         observation_value=float(line["observation_value"]),
#         gestation_weeks=int(line["gestation_weeks"]),
#         gestation_days=int(line["gestation_days"]),
#         reference="uk-who"
#     )

#     rcpchgrowth_result = measurement_object.measurement["measurement_calculated_values"]['corrected_sds']
#     tim_cole_r_result = line["SDS"]

#     # comparison using absolute tolerance (not relative)
#     assert rcpchgrowth_result == pytest.approx(tim_cole_r_result, abs=ACCURACY)

@pytest.mark.parametrize("line", load_valid_data_set())
def test_sds_calculation(line):
    if line["observation_value"] == None or line["SDS"] == None:
        return
    sds = global_functions.sds_for_measurement("uk-who", float(line["corrected_age"]), str(
        line["measurement_method"]), float(line["observation_value"]), str(line["sex"]), False)
    tim_sds = float(line["SDS"])
    assert sds == pytest.approx(tim_sds, abs=ACCURACY)


def test_measurement_class_with_invalid_sex_type():
    """
    Should raise a Marshmallow error (sex must be a string)
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


def test_measurement_class_with_invalid_date_type():
    """
    Should raise a ValueError (sex must be "male" OR "female")
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
