import os
import json
from datetime import datetime

import pytest
from rcpchgrowth import Measurement

# the ACCURACY constant defines the accuracy of the test comparisons
# owing to variations in statistical calculations it's impossible to get exact
# agreement between R and Python, so our statistician feels we can set a tolerance
# within which we will accept a result as correct.

ACCURACY = 1e-3


def load_valid_data_set():
    """
    Loads in the testing data from JSON file
    """
    with open(os.path.abspath(os.path.dirname(__file__)) + "/test_measurement_class_values.json") as f:
        return json.load(f)


@pytest.mark.parametrize("line", load_valid_data_set())
def test_measurement_class_with_valid_data_set(line):
    print(line)
    """
    Test which iterates through a JSON file of fictional children and known calculated (TC via R)
      correct SDS values. Compares the output of the Measurement.measurement method with the known
      correct value.
    """

    measurement_object = Measurement(
        sex=str(line["sex"]),
        birth_date=datetime.strptime(line["birth_date"], "%Y-%m-%d"),
        observation_date=datetime.strptime(
            line["observation_date"], "%Y-%m-%d"),
        measurement_method=str(line["measurement_method"]),
        observation_value=float(line["observation_value"]),
        gestation_weeks=int(line["gestation_weeks"]),
        gestation_days=int(line["gestation_days"]),
        reference="uk-who"
    )

    rcpchgrowth_result = measurement_object.measurement["measurement_calculated_values"]['sds']
    tim_cole_r_result = line["SDS"]

    # comparison using absolute tolerance (not relative)
    assert rcpchgrowth_result == pytest.approx(tim_cole_r_result, abs=ACCURACY)


# def test_measurement_class_with_invalid_sex_type():
#     measurement_object = Measurement(
#         sex="males",
#         birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
#         observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
#         measurement_method="weight",
#         observation_value=5.0,
#         gestation_weeks=0,
#         gestation_days=40,
#         reference="uk-who"
#     )

    # Should raise a TypeError (sex must be a string)


# def test_measurement_class_with_invalid_sex_string():
#     measurement_object = Measurement(
#         sex="male",
#         birth_date=datetime.strptime("2020-04-01", "%Y-%m-%d"),
#         observation_date=datetime.strptime("2020-06-01", "%Y-%m-%d"),
#         measurement_method="weight",
#         observation_value=5.0,
#         gestation_weeks=0,
#         gestation_days=40,
#         reference="uk-who"
#     )

    # Should raise a ValueError (sex must be "male" OR "female")
