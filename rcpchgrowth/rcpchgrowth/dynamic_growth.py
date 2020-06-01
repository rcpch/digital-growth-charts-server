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
                    print(f"bmi: {measurement['child_measurement_value']['bmi']}")
                    parameter_list.append(measurement)
                elif parameter == 'ofc' and measurement['child_measurement_value']['ofc'] is not None:
                    parameter_list.append(measurement)
        if len(parameter_list) < 2:
            return f"Not enough data for {parameter} to calculate a velocity"
        else:
            last = parameter_list[-1]
            penultimate = parameter_list[-2]
            time_elapsed = last['measurement_dates']['chronological_decimal_age'] - penultimate['measurement_dates']['chronological_decimal_age']
            parameter_difference = 0.0
            if parameter == 'height':
                parameter_difference = last['measurement_calculated_values']['height_sds'] - penultimate['measurement_calculated_values']['height_sds']
            elif parameter == 'weight':
                parameter_difference = last['measurement_calculated_values']['weight_sds'] - penultimate['measurement_calculated_values']['weight_sds']
            elif parameter == 'bmi':
                parameter_difference = last['measurement_calculated_values']['bmi_sds'] - penultimate['measurement_calculated_values']['bmi_sds']
            elif parameter == 'ofc':
                parameter_difference = last['measurement_calculated_values']['ofc_sds'] - penultimate['measurement_calculated_values']['ofc_sds']
            return parameter_difference / time_elapsed