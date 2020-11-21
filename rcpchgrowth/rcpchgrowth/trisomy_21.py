import json
import pkg_resources
from .constants import *
from .global_functions import z_score, cubic_interpolation, linear_interpolation, centile, measurement_for_z, nearest_lowest_index, fetch_lms
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

T21_DATA = pkg_resources.resource_filename(__name__, "/data_tables/trisomy_21.json")
with open(T21_DATA) as json_file:
            T21_DATA = json.load(json_file)
            json_file.close()

def t21_sds_calculation(
    age: float,
    measurement_method: str,
    observation_value: float,
    sex: str,
    )->float:

    """
    The is the caller function to calculate an SDS for a child specifically using the Down's syndrome dataset.
    
    """

    try:
        selected_reference = T21_DATA
    except: # there is no reference for the age supplied
        return ValueError("The Down's syndrom reference cannot be found.")

    # Check that the measurement requested has reference data at that age
    if reference_data_absent(
        age=age, 
        measurement_method=measurement_method, 
        sex=sex):
        return ValueError("There is no reference data for this measurement at this age")

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = selected_reference["measurement"][measurement_method][sex]

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]
    ## calculate the SDS from the L, M and S values

    return z_score(l=l, m=m, s=s, observation=observation_value)

def reference_data_absent( 
        age: float,
        measurement_method: str,
        sex: str
    ) -> bool:
    """
    Helper function.
    Returns boolean
    Tests presence of valid reference data for a given measurement request

    Reference data is not complete for all ages/sexes/measurements.
     - There is only BMI reference data until 18.92y
     - Head circumference reference data is available until 18.0y
     - lowest threshold is 0 weeks, upper threshold is 20y
    """

    if age < 0: # lower threshold of T21 data
        return True
    
    if age > TWENTY_YEARS: # upper threshold of T21 data
        return True
        
    elif measurement_method == "bmi" and age > 18.82:
        return True
    
    elif measurement_method == "ofc":
        if age > EIGHTEEN_YEARS:
            return True
        else:
            return False
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
    lms_value_array_for_measurement = T21_DATA["measurement"][measurement_method][sex]

    # test reference data exists for age
    if reference_data_absent(age=age, measurement_method=measurement_method, sex=sex):
        return ValueError(f'There is no reference data for this measurement at {age} years.')
    else:
        # get LMS values from the reference: check for age match, interpolate if none
        lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
        l = lms["l"]
        m = lms["m"]
        s = lms["s"]

        observation_value = measurement_for_z(z=requested_sds, l=l, m=m, s=s)
        return observation_value