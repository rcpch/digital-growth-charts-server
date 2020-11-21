import json
import pkg_resources
from .constants import *
# from .global_functions import z_score, fetch_lms, measurement_for_z, sds_value_for_centile_value
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
    ) -> (bool, str):
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

# def generate_centile(z: float, centile: float, measurement_method: str, sex='female'):
#     ages=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 10.0, 10.2, 10.4, 10.6, 10.8, 11.0, 11.2, 11.4, 11.6, 11.8, 12.0, 12.2, 12.4, 12.6, 12.8, 13.0, 13.2, 13.4, 13.6, 13.8, 14.0, 14.2, 14.4, 14.6, 14.8, 15.0, 15.2, 15.4, 15.6, 15.8, 16.0, 16.2, 16.4, 16.6, 16.8, 17.0, 17.2, 17.4, 17.6, 17.8, 18.0, 18.2, 18.4, 18.6, 18.8, 19.0, 19.2, 19.4, 19.6, 19.8]
#     plottable_measurements=[]
#     for num, age in enumerate(ages):
#         measurement = measurement_from_sds(measurement_method=measurement_method, requested_sds=z, sex=sex, age=age)
#         value = {
#             "label": centile,
#             "x": age,
#             "y": measurement
#         }
#         plottable_measurements.append(value)
#     return {
#         "sds": z,
#         "centile": centile,
#         "turner": plottable_measurements
#     }