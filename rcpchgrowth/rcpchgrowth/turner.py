import json
import pkg_resources
from .constants import *
from .global_functions import z_score, fetch_lms, measurement_for_z
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

TURNER_DATA = pkg_resources.resource_filename(__name__, "/data_tables/uk90.json")
with open(TURNER_DATA) as json_file:
            TURNER_DATA = json.load(json_file)
            json_file.close()

def turner_sds_calculation(
    age: float,
    measurement_method: str,
    measurement_value: float,
    sex: str,
    )->float:

    """
    The is the caller function to calculate an SDS for a child specifically using the Turner"s syndrome dataset.
    
    """

    # Get the correct reference from the patchwork of references that make up UK-WHO
    try:
        selected_reference = TURNER_DATA
    except: # there is no reference for the age supplied
        return ValueError("The Turner's syndrome reference cannot be found.")

    # Check that the measurement requested has reference data at that age
    if reference_data_absent(
        age=age, 
        measurement_method=measurement_method, 
        sex=sex):
        return ValueError("There is no reference data for this measurement.")

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = selected_reference["measurement"][measurement_method][sex]

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]
    ## calculate the SDS from the L, M and S values

    return z_score(l=l, m=m, s=s, observation=measurement_value)

def reference_data_absent( 
        age: float,
        measurement_method: str,
        sex: str
    ) -> bool:
    """
    Helper function.
    Returns boolean
    Tests presence of valid reference data for a given measurement request

    Turners syndrome
    Data are available for girls heights at year intervals from 1-20y
    No other reference data are available
    """

    if age < 1: # lower threshold of Turner data
        return True
    elif age > TWENTY_YEARS: # upper threshold of Turner data
        return True
    elif measurement_method=="weight" or measurement_method=="bmi" or measurement_method=="ofc":
        return True
    elif sex == "male":
        return True
    else:
        return False

def measurement_from_sds(
    measurement_method: str,  
    requested_sds: float,  
    sex: str,  
    age: float,
    ) -> float:
    """
    Public method
    Returns the measurement value from a given SDS.
    Parameters are: 
        measurement_method (type of observation) ["height", "weight", "bmi", "ofc"]
        decimal age (corrected or chronological),
        requested_sds
        sex (a standard string) ["male" or "female"]
        born_preterm: a boolean flag to track whether to use UK90 premature data or UK90-WHO term data for 37-42 weeks

    Centile to SDS Conversion for Chart lines (2/3 of an SDS)
    0.4th -2.67
    2nd -2.00
    9th -1.33
    25th -0.67
    50th 0
    75th 0.67
    91st 1.33
    98th 2.00
    99.6th 2.67
    """

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = TURNER_DATA["measurement"][measurement_method][sex]

    # test reference data exists for age
    if reference_data_absent(age=age, measurement_method=measurement_method, sex=sex):
        return ValueError(f"There is no reference data for this measurement at {age} years.")
    else:
        # get LMS values from the reference: check for age match, interpolate if none
        lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
        l = lms["l"]
        m = lms["m"]
        s = lms["s"]

        measurement_value = measurement_for_z(z=requested_sds, l=l, m=m, s=s)
        return measurement_value