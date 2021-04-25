"""
Tests for the global functions which perform lower-level intermediate calculations
"""

# standard imports
from datetime import datetime
import json
import os

# third-party imports
import pytest

# rcpch imports
from rcpchgrowth import global_functions, date_calculations

# The ACCURACY constant defines the level of accuracy required.
# Statistical functions in R (used by Tim Cole to create the input data we are testing against)
#   differ minutely from statistical function in Python. This is expected, and we use the ACCURACY
#   constant to account for this
ACCURACY = 1e-3


def load_valid_data_set():
    """
    Loads in the testing data from JSON file
    """
    # with open(os.path.abspath(os.path.dirname(__file__)) + "/validation_sds-2021.json") as f:
    with open(os.path.abspath(os.path.dirname(__file__)) + "/sds_age_validation_2021.json") as f:
        return json.load(f)


# date_calculations
@pytest.mark.parametrize("line", load_valid_data_set())
def test_chronological_decimal_age(line):
    """
    Tests the function which calculates chronological decimal age
        from birth_date and observation_date
    """
    if line["birth_date"] is None or line["observation_date"] is None:
        return
    birth_date = datetime.strptime(line["birth_date"], "%d/%m/%Y").date()
    observation_date = datetime.strptime(
        line["observation_date"], "%d/%m/%Y").date()
    age = date_calculations.chronological_decimal_age(
        birth_date, observation_date)
    tim_age = float(line["chronological_age"])
    assert age == pytest.approx(tim_age, abs=ACCURACY)


@pytest.mark.parametrize("line", load_valid_data_set())
def test_corrected_decimal_age(line):
    """
    Tests the function which calculates **corrected** decimal age
    """
    if line["birth_date"] is None or line["observation_date"] is None:
        return
    birth_date = datetime.strptime(line["birth_date"], "%d/%m/%Y").date()
    observation_date = datetime.strptime(
        line["observation_date"], "%d/%m/%Y").date()
    age = date_calculations.corrected_decimal_age(birth_date, observation_date, int(
        line["gestation_weeks"]), int(line["gestation_days"]))
    tim_age = float(line["corrected_age"])
    assert age == pytest.approx(tim_age, abs=ACCURACY)


# SDS calculation tests
@pytest.mark.parametrize("line", load_valid_data_set())
def test_sds_for_measurement_corrected(line):
    """
    Tests the function with calculates SDS from gestationally-corrected measurements
    """
    if line["observation_value"] is None or line["corrected_sds"] is None:
        return
    sds = global_functions.sds_for_measurement("uk-who", float(line["corrected_age"]), str(
        line["measurement_method"]), float(line["observation_value"]), str(line["sex"]), False)
    tim_sds = float(line["corrected_sds"])
    assert sds == pytest.approx(tim_sds, abs=ACCURACY)


@pytest.mark.parametrize("line", load_valid_data_set())
def test_sds_for_measurement_chronological(line):
    """
    Tests the function with calculates SDS from uncorrected measurements
    """
    if line["observation_value"] is None or line["chronological_sds"] is None:
        return
    sds = global_functions.sds_for_measurement("uk-who", float(line["chronological_age"]), str(
        line["measurement_method"]), float(line["observation_value"]), str(line["sex"]), False)
    tim_sds = float(line["chronological_sds"])
    assert sds == pytest.approx(tim_sds, abs=ACCURACY)
