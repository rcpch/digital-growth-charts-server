# from .measurement import Measurement
import pandas as pd
import os
import math
from scipy.interpolate import interp1d
from datetime import datetime, date
from dateutil.relativedelta import relativedelta
from random import uniform
from .measurement import Measurement
from .global_functions import measurement_from_sds
from .date_calculations import corrected_decimal_age

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
    parameter_list = []
    if len(measurements_array) < 2:
        return 'Not enough data'
    else:
        for measurement in measurements_array:
            if measurement:
                if parameter == measurement['child_observation_value']['measurement_method']:
                    parameter_list.append(measurement)
        if len(parameter_list) < 2:
            return f"There are not enough {parameter} values to calculate a velocity."
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            time_elapsed = last['measurement_dates']['chronological_decimal_age'] - \
                penultimate['measurement_dates']['chronological_decimal_age']
            parameter_difference = 0.0
            parameter_difference = last['child_observation_value']['observation_value'] - \
                penultimate['child_observation_value']['observation_value']
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
    parameter_list = []
    if len(measurements_array) < 3:
        return 'Not enough data'
    else:
        for measurement in measurements_array:
            if measurement:
                if parameter == measurement['child_observation_value']['measurement_method']:
                    parameter_list.append(measurement)
        if len(parameter_list) < 3:
            return f"There are not enough {parameter} values to calculate acceleration."
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            antepentultimate = parameter_list[-3]
            first_parameter_pair_time_elapsed = penultimate['measurement_dates']['chronological_decimal_age'] - \
                antepentultimate['measurement_dates']['chronological_decimal_age']
            last_parameter_pair_time_elapsed = last['measurement_dates']['chronological_decimal_age'] - \
                penultimate['measurement_dates']['chronological_decimal_age']
            first_parameter_pair_difference = 0.0
            last_parameter_pair_difference = 0.0

            last_parameter_pair_difference = last['child_observation_value']['observation_value'] - \
                penultimate['child_observation_value']['observation_value']
            first_parameter_pair_difference = penultimate['child_observation_value']['observation_value'] - \
                antepentultimate['child_observation_value']['observation_value']

            latest_velocity = last_parameter_pair_difference / last_parameter_pair_time_elapsed
            penultimate_velocity = first_parameter_pair_difference / \
                first_parameter_pair_time_elapsed
            accleration = (latest_velocity - penultimate_velocity) / \
                last_parameter_pair_time_elapsed
            return accleration


def correlate_weight(measurements_array: list = []):
    """
    Weight velocity of the individual child cannot be predicted without comparison against reference data velocity
    since weight velocity is age dependent. This uses a uses a correlation matrix to look up values against which
    to compare the rate at which the child is gaining or losing weight.
    The formula for conditional weight gain is: (z2 – r x z1) / √1-r^2
    Conditional reference charts to assess weight gain in British infants, T J Cole, Archives of Disease in Childhood 1995; 73: 8-16
    """

    # test data
    """
    measurements = [{'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 25 Apr 1759 00:00:00 GMT', 'chronological_decimal_age': 0.038329911019849415, 'corrected_decimal_age': 0.038329911019849415, 'chronological_calendar_age': '2 weeks', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 4.111224921050807, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.0020115566532506, 'weight_centile': 84.18309943393204, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 09 May 1759 00:00:00 GMT', 'chronological_decimal_age': 0.07665982203969883, 'corrected_decimal_age': 0.07665982203969883, 'chronological_calendar_age': '4 weeks', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 4.699038339425533, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.002339620693291, 'weight_centile': 84.19102035307033, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 23 May 1759 00:00:00 GMT', 'chronological_decimal_age': 0.11498973305954825, 'corrected_decimal_age': 0.11498973305954825, 'chronological_calendar_age': '1 month, 1 week and 5 days', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 5.232213641808542, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.0045936184500082, 'weight_centile': 84.24537143099158, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 06 Jun 1759 00:00:00 GMT', 'chronological_decimal_age': 0.15331964407939766, 'corrected_decimal_age': 0.15331964407939766, 'chronological_calendar_age': '1 month, 3 weeks and 5 days', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 5.692927141647227, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.004963324529577, 'weight_centile': 84.25427448883711, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 20 Jun 1759 00:00:00 GMT', 'chronological_decimal_age': 0.19164955509924708, 'corrected_decimal_age': 0.19164955509924708, 'chronological_calendar_age': '2 months, 1 week and 2 days', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 6.099306464415924, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.007109988748447, 'weight_centile': 84.30590392040097, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 04 Jul 1759 00:00:00 GMT', 'chronological_decimal_age': 0.2299794661190965, 'corrected_decimal_age': 0.2299794661190965, 'chronological_calendar_age': '2 months, 3 weeks and 2 days', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 6.461379695081464, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.007475030461087, 'weight_centile': 84.31467244800477, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 18 Jul 1759 00:00:00 GMT', 'chronological_decimal_age': 0.2683093771389459, 'corrected_decimal_age': 0.2683093771389459, 'chronological_calendar_age': '3 months and 1 week', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 6.789203770743711, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.009650708766674, 'weight_centile': 84.36686671210703, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 01 Aug 1759 00:00:00 GMT', 'chronological_decimal_age': 0.3066392881587953, 'corrected_decimal_age': 0.3066392881587953, 'chronological_calendar_age': '3 months and 3 weeks', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 7.088501064489439, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.0108086749449121, 'weight_centile': 84.39459948388198, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 15 Aug 1759 00:00:00 GMT', 'chronological_decimal_age': 0.34496919917864477, 'corrected_decimal_age': 0.34496919917864477, 'chronological_calendar_age': '4 months', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 7.363720070832382, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.0126387519444007, 'weight_centile': 84.4383628580822, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}, {'birth_data': {'birth_date': 'Wed, 11 Apr 1759 00:00:00 GMT', 'gestation_weeks': 0, 'gestation_days': 0, 'estimated_date_delivery': 'None', 'estimated_date_delivery_string': '', 'sex': 'female'}, 'measurement_dates': {'observation_date': 'Wed, 29 Aug 1759 00:00:00 GMT', 'chronological_decimal_age': 0.38329911019849416, 'corrected_decimal_age': 0.38329911019849416, 'chronological_calendar_age': '4 months, 2 weeks and 4 days', 'corrected_calendar_age': '', 'corrected_gestational_age': {'corrected_gestation_weeks': None, 'corrected_gestation_days': None}, 'clinician_decimal_age_comment': 'Correction for gestational age is nolonger necessary after two years of age.', 'lay_decimal_age_comment': 'Your child is now old enough nolonger to need to take their prematurity into account when considering their growth.'}, 'child_measurement_value': {'height': None, 'weight': 7.614522747033926, 'bmi': 'None', 'ofc': None}, 'measurement_calculated_values': {'height_sds': 'None', 'height_centile': 'None', 'clinician_height_comment': '', 'lay_height_comment': '', 'weight_sds': 1.0139857964039922, 'weight_centile': 84.47052350872625, 'clinician_weight_comment': '', 'lay_weight_comment': '', 'bmi_sds': 'None', 'bmi_centile': 'None', 'clinician_bmi_comment': '', 'lay_bmi_comment': '', 'ofc_sds': 'None', 'ofc_centile': 'None', 'clinician_ofc_comment': '', 'lay_ofc_comment': ''}}]
    """

    # import the reference
    cwd = os.path.dirname(__file__)  # current location
    file_path = os.path.join(
        cwd, './data_tables/RCPCH weight correlation matrix by month.csv')
    data_frame = pd.read_csv(file_path)

    parameter_list = []

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
            penultimate_weight_sds_value = penultimate['measurement_calculated_values']['weight_sds']
            penultimate_decimal_age = penultimate['measurement_dates']['chronological_decimal_age']
            last_weight_sds_value = last['measurement_calculated_values']['weight_sds']
            last_decimal_age = last['measurement_dates']['chronological_decimal_age']

            # look up age
            # this is the formula: (z2 – r x z1) / √1-r^2 where z2 is the most recent value and z1 the penultimate
            # and r the correlation

            # rows are penultimate age, columns are last age. to get r we must look up the ages on
            # the correlation matrix
            z2 = last_weight_sds_value
            z1 = penultimate_weight_sds_value

            if penultimate_decimal_age.is_integer():
                final_row = penultimate_decimal_age
                if last_decimal_age.is_integer():
                    final_column = last_decimal_age
                    # we have both exact ages - can now look up r
                    r = data_frame.at(final_row, final_column)
                    # enough data to simplify formula
                    return r_for_age(z1, z2, r)
                else:
                    # no match - need to interpolate most recent age
                    last_age_age_below = math.floor(last_decimal_age)
                    last_age_age_above = math.ceil(last_decimal_age)
                    x_array = [last_age_age_below + 1, last_age_age_above + 1]

                    # ..and associated r values
                    last_r_below = data_frame.at[final_row,
                                                 last_age_age_below + 1]
                    last_r_above = data_frame.at[final_row,
                                                 last_age_age_above + 1]
                    y_array = [last_r_below, last_r_above]
                    interpolate = interp1d(x_array, y_array)
                    r = interpolate(last_decimal_age)
                    # enough data to simplify formula
                    return r_for_age(z1, z2, r)
            else:
                # no match in penultimate age - need to interpolate
                # get age below penultimate age
                penultimate_age_below = int(
                    math.floor(penultimate_decimal_age))
                penultimate_age_above = int(penultimate_age_below + 1)
                if last_decimal_age.is_integer():
                    # there is a match in last age
                    x_array = [penultimate_age_below, penultimate_age_above]
                    y_array = [data_frame.at[penultimate_age_below, last_decimal_age + 1],
                               data_frame.at[penultimate_age_above, last_decimal_age + 1]]
                    interpolate = interp1d(x_array, y_array)
                    r = (penultimate_decimal_age)
                    # enough data to simplify formula
                    return r_for_age(z1, z2, r)
                else:
                    # will need bilinear interpolation
                    last_age_below = int(math.floor(last_decimal_age))
                    last_age_above = int(math.ceil(last_decimal_age))
                    # ages between penultimate for lowest last age
                    x_array = [penultimate_age_below, penultimate_age_above]
                    y_array = [data_frame.iat[penultimate_age_below, last_age_below + 1],
                               data_frame.iat[penultimate_age_above, last_age_below + 1]]
                    interpolate = interp1d(x_array, y_array)
                    lower_r_between_penultimate_ages = interpolate(
                        penultimate_decimal_age)

                    ## ages between penultimate for highest last age##
                    y_array = [data_frame.iat[penultimate_age_below, last_age_above + 1],
                               data_frame.iat[penultimate_age_above, last_age_above + 1]]
                    interpolate = interp1d(x_array, y_array)
                    upper_r_between_penultimate_ages = interpolate(
                        penultimate_decimal_age)

                    # interpolate between r values against last_ages
                    x_array = [last_age_below, last_age_above]
                    y_array = [float(upper_r_between_penultimate_ages), float(
                        lower_r_between_penultimate_ages)]
                    interpolate = interp1d(x_array, y_array)
                    r = interpolate(last_decimal_age)

                    return r_for_age(z1, z2, r)


def r_for_age(z1, z2, r):
    """
    The formula for conditional weight gain is: (z2 – r x z1) / √1-r^2
    Conditional reference charts to assess weight gain in British infants, T J Cole, Archives of Disease in Childhood 1995; 73: 8-16
    """
    conditional_weight_gain = (z2 - (z1 * r)) / math.sqrt(1 - pow(r, 2))
    return conditional_weight_gain


def create_fictional_child(
        sex: str,
        measurement_method: str,
        requested_sds: float,
        number_of_measurements: int,
        starting_decimal_age: float,
        measurement_interval_value: int,
        measurement_interval_type: str,
        gestation_weeks=0,
        gestation_days=0,
        drift: bool = False,
        drift_sds_range: float = 0.0,
        reference: str = "uk-who"):
    """
    this function will ultimately become a class method
    It's purpose is to generate an array of Measurement objects that mimic the growth of a child
    Mandatory params:
    sex: a string ['male', 'female'] (lower case)
    measurement_method: a string ['height', 'weight', 'ofc', 'bmi'] (lower case)
    requested_sds: float value relating to start value of array
    number_of_measurements: integer - number of growth points requested
    starting_decimal_age: float - age from which growth data should start
    measurement_interval_type: string - accepts parameters ['d', 'day', 'days', 'weeks', 'm', 'month', 'months', 'y', 'year', 'years']
    measurement_interval_value: float - number relating to measurement_interval_type
    Optional params
    gestation_weeks: integer - specify weeks of gestation. The final age will be subject to correction depending on the chronological age
    gestation_days: integer - specify supplementary days of gestation. The final age will be subject to correction depending on the chronological age
    drift: a boolean value - user can request if values deviate at random from the starting SDS
    drift_sds_range: float value, degree to which values can drift from starting SDS. May be positive or negative
    """

    fictional_child = []

    """
    This is an unnecessary piece of growth chart trivia included for entertainment. The first published 
    growth chart is that of the son of Count Philibert de Montbeillard (1720-1785), François Guéneau de Montbeillard.
    The date of birth used here is that of Francois.
    Acknowledgement:
    The development of growth references and growth charts, T J Cole, Ann Hum Biol. 2012 Sep; 39(5): 382–394.
    Wikipedia: https://en.wikipedia.org/wiki/Philippe_Gu%C3%A9neau_de_Montbeillard
    """
    birth_date = date(1759, 4, 11)  # YYYY m d

    born_preterm = False

    if gestation_weeks == 0:
        gestation_weeks = 40
    if gestation_weeks < 37:
        born_preterm = True

    i = 0

    while i < number_of_measurements:

        if measurement_interval_type in ['d', 'day', 'days']:
            observation_date = birth_date + \
                relativedelta(days=(measurement_interval_value * i))
        elif measurement_interval_type in ['w', 'week', 'weeks']:
            observation_date = birth_date + \
                relativedelta(weeks=(measurement_interval_value * i))
        elif measurement_interval_type in ['m', 'month', 'months']:
            observation_date = birth_date + \
                relativedelta(months=(measurement_interval_value * i))
        elif measurement_interval_type in ['y', 'year', 'years']:
            observation_date = birth_date + \
                relativedelta(years=(measurement_interval_value * i))
        else:
            raise ValueError(
                "parameters must be one of 'd', 'day', 'days', 'w', 'week', 'weeks', 'm', 'month', 'months', 'y', 'year' or 'years'")

        # generate random sds in a range requested if drift specified
        if drift:
            requested_sds = requested_sds + uniform(0, drift_sds_range)

        # calculate age at new measurement
        child_age_at_measurement_date = corrected_decimal_age(
            birth_date=birth_date, observation_date=observation_date, gestation_weeks=gestation_weeks, gestation_days=gestation_days)
        # calculate observation_value back from new SDS
        new_measurement_value = measurement_from_sds(reference=reference, measurement_method=measurement_method,
                                                     requested_sds=requested_sds, sex=sex, age=child_age_at_measurement_date, born_preterm=born_preterm)

        # create Measurement object with dates
        new_measurement = Measurement(
            sex=sex,
            birth_date=birth_date,
            observation_date=observation_date,
            measurement_method=measurement_method,
            observation_value=new_measurement_value,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days,
            reference="uk-who"
        )

        #store in array
        fictional_child.append(new_measurement.measurement)

        # and round we go again until number of requested data points reached
        i += 1
    return fictional_child
