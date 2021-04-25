import math

"""
functions to manipulate BMI
"""

#exposed functions

"""
PARAMETERS
weight
height
bmi
ofc
"""

# public functions

def bmi_from_height_weight( height: float,  weight: float) -> float:
    """
    Returns a BMI in kg/m² from a height in cm and a weight in kg
    Does not depend on the age or sex of the child.
    Note does not test for incorrect parameters (eg height mistakenly 
    supplied in metres)
    """
    bmi = weight/math.pow(height/100, 2)
    return bmi

def weight_for_bmi_height( height: float,  bmi: float) -> float:
    """
    Returns a weight in kg from a height in cm and a BMI in kg/m²
    Does not depend on the age or sex of the child.
    Does not test for incorrect parameter values
    """
    return_weight = 0.0
    return_weight = bmi*math.pow(height/100, 2)
    return return_weight