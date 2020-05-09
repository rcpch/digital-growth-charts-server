import math

"""
functions to manipulate BMI
"""

#exposed functions

"""
PARAMETERS
weight
height
BMI
OFC
"""

def bmi_from_height_weight( height: float,  weight: float) -> float:
    bmi = weight/math.pow(height/100, 2)
    return bmi

def weight_for_bmi_height( height: float,  bmi: float) -> float:
    return_weight = 0.0
    return_weight = bmi*math.pow(height/100, 2)
    return return_weight