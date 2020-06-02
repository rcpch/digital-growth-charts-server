from .measurement import Measurement

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