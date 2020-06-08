# from .measurement import Measurement
import pandas as pd
import os
import math

"""
These functions are experimental
Height, weight, BMI or OFC in terms of SDS / Centile are snapshots in time and tell
us actually very little about growth, which is a dynamic measure. In order to make 
predictions, we need to look at change in parameter measured over time (velocity)
which requires 2 measurements over a known time interval, or change in velocity (acceleration/deceleration)
which requires three measurements. 

From these measurements predictions can be made about speed of growth, or rate of slowing (catch down)
or acceleration (catch up). The normative data against which to compare the index child are 
thrive lines, generated here.

"""

def velocity(parameter: str, measurements_array):
    """
    This is an experimental function and not to be used clinically because velocity is not constant
    and is age dependent.
    Velocity needs at least 2 measurements from 2 consecutive time points.
    This takes an array of Measurement objects of the same child, removes the last 2 values of the same
    measurement and calculates the velocity in units/y.
    """
    parameter_list=[]
    if len(measurements_array) < 2:
        return 'Not enough data'
    else:
        for measurement in measurements_array:
            if measurement:
                if parameter == 'height' and measurement['child_measurement_value']['height'] is not None:
                    parameter_list.append(measurement)
                elif parameter == 'weight' and measurement['child_measurement_value']['weight'] is not None:
                    parameter_list.append(measurement)
                elif parameter == 'bmi' and measurement['child_measurement_value']['bmi'] != "None":
                    parameter_list.append(measurement)
                elif parameter == 'ofc' and measurement['child_measurement_value']['ofc'] is not None:
                    parameter_list.append(measurement)
        if len(parameter_list) < 2:
            return f"There are not enough {parameter} values to calculate a velocity."
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            time_elapsed = last['measurement_dates']['chronological_decimal_age'] - penultimate['measurement_dates']['chronological_decimal_age']
            parameter_difference = 0.0
            if parameter == 'height':
                parameter_difference = last['child_measurement_value']['height'] - penultimate['child_measurement_value']['height']
            elif parameter == 'weight':
                parameter_difference = last['child_measurement_value']['weight'] - penultimate['child_measurement_value']['weight']
            elif parameter == 'bmi':
                parameter_difference = last['child_measurement_value']['bmi'] - penultimate['child_measurement_value']['bmi']
            elif parameter == 'ofc':
                parameter_difference = last['child_measurement_value']['ofc'] - penultimate['child_measurement_value']['ofc']
            return parameter_difference / time_elapsed

def acceleration(parameter: str, measurements_array):
    """
    This is an experimental function and not to be used clinically because acceleration is not constant
    and is age dependent.
    Accelaration needs at least 3 measurements over 3 consecutive time points in order to compare the velocity
    change between the first pair and the last pair.
    This takes an array of Measurement objects of the same child, removes the last 3 values of the same
    measurement and calculates the acceleration.
    The parameter in question is one of 'height', 'weight', 'bmi', 'ofc'
    """
    parameter_list=[]
    if len(measurements_array) < 3:
        return 'Not enough data'
    else:
        for measurement in measurements_array:
            if measurement:
                if parameter == 'height' and measurement['child_measurement_value']['height'] is not None:
                    parameter_list.append(measurement)
                elif parameter == 'weight' and measurement['child_measurement_value']['weight'] is not None:
                    parameter_list.append(measurement)
                elif parameter == 'bmi' and measurement['child_measurement_value']['bmi'] != "None":
                    parameter_list.append(measurement)
                elif parameter == 'ofc' and measurement['child_measurement_value']['ofc'] is not None:
                    parameter_list.append(measurement)
        if len(parameter_list) < 3:
            return f"There are not enough {parameter} values to calculate acceleration."
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            antepentultimate = parameter_list[-3]
            first_parameter_pair_time_elapsed = penultimate['measurement_dates']['chronological_decimal_age'] - antepentultimate['measurement_dates']['chronological_decimal_age']
            last_parameter_pair_time_elapsed = last['measurement_dates']['chronological_decimal_age'] - penultimate['measurement_dates']['chronological_decimal_age']
            first_parameter_pair_difference = 0.0
            last_parameter_pair_difference = 0.0
            if parameter == 'height':
                last_parameter_pair_difference = last['child_measurement_value']['height'] - penultimate['child_measurement_value']['height']
                first_parameter_pair_difference = penultimate['child_measurement_value']['height'] - antepentultimate['child_measurement_value']['height']
            elif parameter == 'weight':
                last_parameter_pair_difference = last['child_measurement_value']['weight'] - penultimate['child_measurement_value']['weight']
                first_parameter_pair_difference = penultimate['child_measurement_value']['weight'] - antepentultimate['child_measurement_value']['weight']
            elif parameter == 'bmi':
                last_parameter_pair_difference = last['child_measurement_value']['bmi'] - penultimate['child_measurement_value']['bmi']
                first_parameter_pair_difference = penultimate['child_measurement_value']['bmi'] - antepentultimate['child_measurement_value']['bmi']
            elif parameter == 'ofc':
                last_parameter_pair_difference = last['child_measurement_value']['ofc'] - penultimate['child_measurement_value']['ofc']
                first_parameter_pair_difference = penultimate['child_measurement_value']['ofc'] - antepentultimate['child_measurement_value']['ofc']
            
            latest_velocity = last_parameter_pair_difference / last_parameter_pair_time_elapsed
            penultimate_velocity = first_parameter_pair_difference / first_parameter_pair_time_elapsed
            accleration = (latest_velocity - penultimate_velocity)/last_parameter_pair_time_elapsed
            return accleration


def correlate_weight(measurements_array: list):
    """
    Weight velocity of the individual child cannot be predicted without comparison against reference data velocity
    since weight velocity is age dependent. This uses a uses a correlation matrix to look up values against which
    to compare the rate at which the child is gaining or losing weight.
    The formula for conditional weight gain is: (z2 – r x z1) / √1-r2
    """

    # import the reference
    cwd = os.path.dirname(__file__) # current location
    file_path = os.path.join(cwd, './data_tables/RCPCH weight correlation matrix by month.csv')
    data_frame = pd.read_csv(file_path)

    parameter_list=[]

    if len(measurements_array) < 2:
        return 'Not enough data'
    else:
        for measurement in measurements_array:
            if measurement:
                if measurement['child_measurement_value']['weight'] is not None:
                    parameter_list.append(measurement)

        if len(parameter_list) < 2:
            return f"There are not enough weight values to calculate a velocity."
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            penultimate_weight_sds_value = penultimate['child_measurement_value']['weight_sds']
            penultimate_decimal_age = penultimate['measurement_dates']['chronological_decimal_age']
            last_weight_sds_value = last['child_measurement_value']['weight_sds']
            last_decimal_age = last['measurement_dates']['chronological_decimal_age']
            
            ## look up age
            ## this is the formula: (z2 – r x z1) / √1-r2
            z2 = last_weight_sds_value
            z1 = penultimate_weight_sds_value

            ## get age above penultimate age
            if penultimate_decimal_age.is_integer():
                ## match - look up correlation
                r = r_for_age(penultimate_decimal_age)
            else:
                ## no match - get nearest age below
                correlation_age_below = nearest_age(penultimate_decimal_age)
                r_below = r_for_age(correlation_age_below)
                r_above = r_for_age(correlation_age_below + 1)
                r = interpolate(r_below, r_above, correlation_age_below, correlation_age_below + 1)

            if last_decimal_age.is_integer():
                ## match - look up correlation
                r2 = r_for_age(last_decimal_age)
            else:
                correlation_age_below = nearest_age(last_decimal_age)
                r_below = r_for_age(correlation_age_below)
                r_above = r_for_age(correlation_age_below + 1)
                r2 = interpolate(r_below, r_above, correlation_age_below, correlation_age_below + 1)

            ## simplify
            conditional_weight_gain = (z2 - (z1 * r)) / math.sqrt(1 - r2)
            
            return conditional_weight_gain


def nearest_age(decimal_age)->float:
    nearest_age = int(round(decimal_age))
    age_above = 0.0
    age_below = 0.0
    if nearest_age > decimal_age:
        return nearest_age - 1
    else:
        return nearest_age
    
