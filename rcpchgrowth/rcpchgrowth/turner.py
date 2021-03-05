import json
import pkg_resources
from .constants import *
# import timeit #see below, comment back in if timing functions in this module

"""
birth_date: date of birth
observation_date: date of observation
sex: sex (string, MALE or FEMALE)
decimal_age: chronological, decimal
corrected_age: corrected for prematurity, decimal
measurement_method: height, weight, bmi, ofc (decimal)
observation: value (float)
gestation_weeks: gestational age(weeks), integer
gestation_days: supplementary days of gestation
lms: L, M or S
reference: reference data
"""

#load the reference data

TURNER_DATA = pkg_resources.resource_filename(__name__, "/data_tables/turner.json")
with open(TURNER_DATA) as json_file:
            TURNER_DATA = json.load(json_file)
            json_file.close()

def turner_lms_array_for_measurement_and_sex(
        measurement_method: str,    
        sex: str,  
        age: float
    ):

    invalid_data, data_error = reference_data_absent(age=age, measurement_method=measurement_method, sex=sex)

    if invalid_data:
        raise LookupError(data_error)

    # Get the Turner reference data
    try:
        return TURNER_DATA["measurement"][measurement_method][sex]
    except: # there is no reference for the age supplied
        raise LookupError("The Turner's syndrome reference cannot be found.")
    

def reference_data_absent( 
        age: float,
        measurement_method: str,
        sex: str
    ):
    """
    Helper function.
    Returns boolean
    Tests presence of valid reference data for a given measurement request

    Turners syndrome
    Data are available for girls heights at year intervals from 1-20y
    No other reference data are available
    """

    if age < 1: # lower threshold of Turner data
        return True, 'There is no reference data below 1 year.'
    elif age > TWENTY_YEARS: # upper threshold of Turner data
        return True, "There is no reference data above 20 years."
    elif measurement_method=="weight" or measurement_method=="bmi" or measurement_method=="ofc":
        text_string = measurement_method
        if measurement_method == "bmi":
            text_string = "BMI (body mass index)"
        elif measurement_method == "ofc":
            text_string = "head circumference"
        return True, f"There is no reference data for {text_string}."
    elif sex == "male":
        return True, f"Turner's syndrome only affects girls and women."
    else:
        return False, "Valid Data"

def select_reference_data_for_turner(measurement_method: str, sex: str):
    return turner_lms_array_for_measurement_and_sex(measurement_method=measurement_method, sex=sex, age=1.0)