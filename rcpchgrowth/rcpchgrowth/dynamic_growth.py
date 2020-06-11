# from .measurement import Measurement
import pandas as pd
import os
import math
from scipy.interpolate import interp2d

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
    The formula for conditional weight gain is: (z2 – r x z1) / √1-r^2
    Conditional reference charts to assess weight gain in British infants, T J Cole, Archives of Disease in Childhood 1995; 73: 8-16
    """

    #test data
    measurements = [{'birth_data': {'birth_date': 'Mon, 08 Jun 2020 00:00:00 GMT', 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'gestation_days': 0, 'gestation_weeks': 40, 'sex': 'male'}, 'child_measurement_value': {'bmi': 'None', 'height': None, 'ofc': None, 'weight': 3.5}, 'measurement_calculated_values': {'bmi_centile': 'None', 'bmi_sds': 'None', 'clinician_bmi_comment': '', 'clinician_height_comment': '', 'clinician_ofc_comment': '', 'clinician_weight_comment': 'On or below the 50th centile .', 'height_centile': 'None', 'height_sds': 'None', 'lay_bmi_comment': '', 'lay_height_comment': '', 'lay_ofc_comment': '', 'lay_weight_comment': 'Your child is on or just below the average weight of the population, compared with other children the same age and sex.', 'ofc_centile': 'None', 'ofc_sds': 'None', 'weight_centile': 50.0, 'weight_sds': 0.0}, 'measurement_dates': {'chronological_calendar_age': 'Happy Birthday', 'chronological_decimal_age': 0.0, 'clinician_decimal_age_comment': 'Born Term. No correction necessary.', 'corrected_calendar_age': '', 'corrected_decimal_age': 0.0, 'corrected_gestational_age': {'corrected_gestation_days': 0, 'corrected_gestation_weeks': 40}, 'lay_decimal_age_comment': 'At 40+0, your child is considered to have been born at term. No age adjustment is necessary.', 'obs_date': 'Mon, 08 Jun 2020 00:00:00 GMT'}},{'birth_data': {'birth_date': 'Mon, 01 Jun 2020 00:00:00 GMT', 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'gestation_days': 0, 'gestation_weeks': 40, 'sex': 'male'}, 'child_measurement_value': {'bmi': 'None', 'height': None, 'ofc': None, 'weight': 3.6}, 'measurement_calculated_values': {'bmi_centile': 'None', 'bmi_sds': 'None', 'clinician_bmi_comment': '', 'clinician_height_comment': '', 'clinician_ofc_comment': '', 'clinician_weight_comment': 'On or below the 91st centile. Consider reviewing trend.', 'height_centile': 'None', 'height_sds': 'None', 'lay_bmi_comment': '', 'lay_height_comment': '', 'lay_ofc_comment': '', 'lay_weight_comment': 'Your child is in the top 9 percent of children the same age and sex for their weight. This does not take account of their height.', 'ofc_centile': 'None', 'ofc_sds': 'None', 'weight_centile': 76.30277592692399, 'weight_sds': 0.7160759040458319}, 'measurement_dates': {'chronological_calendar_age': '1 week', 'chronological_decimal_age': 0.019164955509924708, 'clinician_decimal_age_comment': 'Born Term. No correction necessary.', 'corrected_calendar_age': '', 'corrected_decimal_age': 0.019164955509924708, 'corrected_gestational_age': {'corrected_gestation_days': 0, 'corrected_gestation_weeks': 41}, 'lay_decimal_age_comment': 'At 40+0, your child is considered to have been born at term. No age adjustment is necessary.', 'obs_date': 'Mon, 08 Jun 2020 00:00:00 GMT'}},{'birth_data': {'birth_date': 'Mon, 25 May 2020 00:00:00 GMT', 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'gestation_days': 0, 'gestation_weeks': 40, 'sex': 'male'}, 'child_measurement_value': {'bmi': 'None', 'height': None, 'ofc': None, 'weight': 3.65}, 'measurement_calculated_values': {'bmi_centile': 'None', 'bmi_sds': 'None', 'clinician_bmi_comment': '', 'clinician_height_comment': '', 'clinician_ofc_comment': '', 'clinician_weight_comment': 'On or below the 91st centile. Consider reviewing trend.', 'height_centile': 'None', 'height_sds': 'None', 'lay_bmi_comment': '', 'lay_height_comment': '', 'lay_ofc_comment': '', 'lay_weight_comment': 'Your child is in the top 9 percent of children the same age and sex for their weight. This does not take account of their height.', 'ofc_centile': 'None', 'ofc_sds': 'None', 'weight_centile': 85.86141724618928, 'weight_sds': 1.074113856068745}, 'measurement_dates': {'chronological_calendar_age': '2 weeks', 'chronological_decimal_age': 0.038329911019849415, 'clinician_decimal_age_comment': 'Born Term. No correction necessary.', 'corrected_calendar_age': '', 'corrected_decimal_age': 0.038329911019849415, 'corrected_gestational_age': {'corrected_gestation_days': None, 'corrected_gestation_weeks': None}, 'lay_decimal_age_comment': 'At 40+0, your child is considered to have been born at term. No age adjustment is necessary.', 'obs_date': 'Mon, 08 Jun 2020 00:00:00 GMT'}},{'birth_data': {'birth_date': 'Mon, 18 May 2020 00:00:00 GMT', 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'gestation_days': 0, 'gestation_weeks': 40, 'sex': 'male'}, 'child_measurement_value': {'bmi': 'None', 'height': None, 'ofc': None, 'weight': 4.1}, 'measurement_calculated_values': {'bmi_centile': 'None', 'bmi_sds': 'None', 'clinician_bmi_comment': '', 'clinician_height_comment': '', 'clinician_ofc_comment': '', 'clinician_weight_comment': 'On or below the 75th centile. Consider reviewing trend.', 'height_centile': 'None', 'height_sds': 'None', 'lay_bmi_comment': '', 'lay_height_comment': '', 'lay_ofc_comment': '', 'lay_weight_comment': 'Your child is below or the same as 75 percent of children the same age and sex. This does not take account of their height.', 'ofc_centile': 'None', 'ofc_sds': 'None', 'weight_centile': 52.812447858684855, 'weight_sds': 0.07055610953540369}, 'measurement_dates': {'chronological_calendar_age': '3 weeks', 'chronological_decimal_age': 0.057494866529774126, 'clinician_decimal_age_comment': 'Born Term. No correction necessary.', 'corrected_calendar_age': '', 'corrected_decimal_age': 0.057494866529774126, 'corrected_gestational_age': {'corrected_gestation_days': None, 'corrected_gestation_weeks': None}, 'lay_decimal_age_comment': 'At 40+0, your child is considered to have been born at term. No age adjustment is necessary.', 'obs_date': 'Mon, 08 Jun 2020 00:00:00 GMT'}}]
    
    # import the reference
    cwd = os.path.dirname(__file__) # current location
    file_path = os.path.join(cwd, './data_tables/RCPCH weight correlation matrix by month.csv')
    data_frame = pd.read_csv(file_path)

    parameter_list=[]

    if len(measurements) < 2:
        return 'Not enough data'
    else:
        for measurement in measurements:
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
            ## this is the formula: (z2 – r x z1) / √1-r^2 where z2 is the most recent value and z1 the penultimate
            ## and r the correlation 

            ## rows are penultimate age, columns are last age. to get r we must look up the ages on
            ## the correlation matrix 
            z2 = last_weight_sds_value
            z1 = penultimate_weight_sds_value
            
            if penultimate_decimal_age.is_integer():
                final_row = penultimate_decimal_age
                if last_decimal_age.is_integer():
                    final_column = last_decimal_age
                    ## we have both exact ages - can now look up r
                    r = data_frame.at(final_row, final_column)
                    ## enough data to simplify formula
                    return r_for_age(z1, z2, r)
                else:
                    #no match - need to interpolate most recent age
                    last_age_age_below = math.floor(last_decimal_age)
                    last_age_age_above = math.ceil(last_decimal_age)
                    x_array = [last_age_age_below, last_age_age_above]
                    
                    ## ..and associated r values
                    last_r_below = data_frame.at(final_row, last_age_age_below)
                    last_r_above = data_frame.at(final_row, last_age_age_above)
                    y_array = [last_r_below, last_r_above]
                    interpolate = interp1d(x_array, y_array)
                    r = interpolate(last_decimal_age)
                    ## enough data to simplify formula
                    return r_for_age(z1, z2, r)
            else:
                ## no match in penultimate age - need to interpolate
                ## get age below penultimate age
                penultimate_age_below = math.floor(penultimate_decimal_age)
                penultimate_age_above = penultimate_age_below + 1
                if last_decimal_age.is_integer():
                    ### there is a match in last age
                    x_array = [penultimate_age_below, penultimate_age_above]
                    y_array = [data_frame.at(penultimate_age_below, last_decimal_age), data_frame.at(penultimate_age_above, last_decimal_age)]
                    interpolate = interp1d(x_array, y_array)
                    r = (penultimate_decimal_age)
                    ## enough data to simplify formula
                    return r_for_age(z1, z2, r)
                else:
                    ## will need bilinear interpolation
                    last_age_below = math.floor(last_decimal_age)
                    last_age_above = math.ceil(last_decimal_age)
                    x_array = [penultimate_age_below, penultimate_age_above]
                    y_array = [last_age_below, last_age_above]
                    z_array = [[data_frame.at(penultimate_age_below, last_age_below), data_frame.at(penultimate_age_above, last_age_below)], [data_frame.at(penultimate_age_below, last_age_above), data_frame.at(penultimate_age_above, last_age_above)]]
                    interpolate = interp2d(x_array, y_array, z_array)
                    r = interpolate(penultimate_decimal_age,last_decimal_age)
                    return r_for_age(z1, z2, r)

def r_for_age(z1, z2, r):
    """
    The formula for conditional weight gain is: (z2 – r x z1) / √1-r^2
    Conditional reference charts to assess weight gain in British infants, T J Cole, Archives of Disease in Childhood 1995; 73: 8-16
    """
    conditional_weight_gain = (z2 - (z1 * r)) / math.sqrt(1 - pow(r, 2))
    return conditional_weight_gain