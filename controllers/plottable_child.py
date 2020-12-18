def create_plottable_child_data(child_results_array):
    child_height_data = []
    child_weight_data = []
    child_bmi_data = []
    child_ofc_data = []
    child_height_sds_data = []
    child_weight_sds_data = []
    child_bmi_sds_data = []
    child_ofc_sds_data = []
    for count, child_result in enumerate(child_results_array):
        if(child_result):

            ## create 4 plottable return objects for each measurement: one for each corrected and chronological age
            ## per measurement and per SDS score
            ## These measurement pairs and SDS pairs are stored in a 2 2-value arrays, so that each measurement/SDS
            ## can be plotted as a series in the charts.
            ## If there are multiple values to plot, the return array will be a string of arrays of paired values,
            ## which allows them to be plotted as pairs: this is because corrected and chronological values should be
            ## linked by a line, the chronological value denotes as a dot, the corrected value as a cross.

            chronological_data_point = {
                "x": child_result["measurement_dates"]["chronological_decimal_age"], 
                "y": child_result["child_observation_value"]["observation_value"],
                "centile_band": child_result["measurement_calculated_values"]["centile_band"],
                "centile_value": child_result["measurement_calculated_values"]["centile"],
                "age_type": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"]
            }
            corrected_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["child_observation_value"]["observation_value"],
                "centile_band": child_result["measurement_calculated_values"]["centile_band"],
                "centile_value": child_result["measurement_calculated_values"]["centile"],
                "age_type": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["corrected_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"]
            }
            chronological_sds_data_point = {
                "x": child_result["measurement_dates"]["chronological_decimal_age"], 
                "y": child_result["measurement_calculated_values"]["sds"],
                "age_type": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"]
            }
            corrected_sds_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["measurement_calculated_values"]["sds"],
                "age_type": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"]
            }

            measurement_data_points=[corrected_data_point, chronological_data_point]
            measurement_sds_data_points=[corrected_sds_data_point, chronological_sds_data_point]

            if(child_result["child_observation_value"]["measurement_method"] == "height"):
                child_height_data.append(measurement_data_points)
                child_height_sds_data.append(measurement_sds_data_points)
            elif(child_result["child_observation_value"]["measurement_method"] == "weight"):
                child_weight_data.append(measurement_data_points)
                child_weight_sds_data.append(measurement_sds_data_points)
            elif(child_result["child_observation_value"]["measurement_method"] == "bmi"):
                child_bmi_data.append(measurement_data_points)
                child_bmi_sds_data.append(measurement_sds_data_points)
            elif(child_result["child_observation_value"]["measurement_method"] == "ofc"):
                child_ofc_data.append(measurement_data_points)
                child_ofc_sds_data.append(measurement_sds_data_points)

    result = {
        "heights": child_height_data,
        "height_sds": child_height_sds_data,
        "weights": child_weight_data,
        "weight_sds": child_weight_sds_data,
        "bmis": child_bmi_data,
        "bmi_sds": child_bmi_sds_data,
        "ofcs": child_ofc_data,
        "ofc_sds": child_ofc_sds_data
    }

    return result



def sds_value_for_centile_value(centile: float):

    if centile == 0.4:
        return -2.0 - (2/3)
    elif centile == 2:
        return -2.0
    elif centile == 9:
        return -1 - (1/3)
    elif centile == 25:
        return 0 - (2/3)
    elif centile == 50:
        return 0
    elif centile == 75:
        return 2/3
    elif centile == 91:
        return 1 + (1/3)
    elif centile == 98:
        return 2.0
    elif centile == 99.6:
        return 2 + (2/3)
    else:
        #error
        raise LookupError("SDS could not be calculated from Centile supplied")

    """
    Return object structure

    [
        heights: [
            {
                x: 9.415, `this is the age of the child at date of measurement in decimal years
                y: 120 `this is the observation value - the units will be added in the client
                "centile_band": 'You childs height is between the 75th and 91st centiles' `a text advice string for labelling,
                "centile_value": 86 `centile number value - reported but not used: the project board do not like exact centile numbers,
                "age_type": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
            }
        ],
        height_sds: [
                x: 9.415, `this is the age of the child at date of measurement in decimal years
                y: 1.3 `this is the SDS value for SDS charts
                "age_type": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
        ],
        .... and so on for the other measurement_methods
        
    ]

    """