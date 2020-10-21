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
            chronological_data_point = {
                "x": child_result["measurement_dates"]["chronological_decimal_age"], 
                "y": child_result["child_observation_value"]["measurement_value"],
                "label": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestational_weeks": child_result["corrected_gestational_age"]["corrected_gestational_weeks"],
                "corrected_gestational_days": child_result["corrected_gestational_age"]["corrected_gestational_days"]
            }
            corrected_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["child_observation_value"]["measurement_value"],
                "label": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["corrected_calendar_age"],
                "corrected_gestational_weeks": child_result["corrected_gestational_age"]["corrected_gestational_weeks"],
                "corrected_gestational_days": child_result["corrected_gestational_age"]["corrected_gestational_days"]
            }
            chronological_sds_data_point = {
                "x": child_result["measurement_dates"]["chronological_decimal_age"], 
                "y": child_result["measurement_calculated_values"]["sds"],
                "label": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestational_weeks": child_result["corrected_gestational_age"]["corrected_gestational_weeks"],
                "corrected_gestational_days": child_result["corrected_gestational_age"]["corrected_gestational_days"]
            }
            corrected_sds_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["measurement_calculated_values"]["sds"],
                "label": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestational_weeks": child_result["corrected_gestational_age"]["corrected_gestational_weeks"],
                "corrected_gestational_days": child_result["corrected_gestational_age"]["corrected_gestational_days"]
            }
            if(child_result["child_observation_value"]["measurement_method"] == "height"):
                child_height_data.append(corrected_data_point)
                child_height_data.append(chronological_data_point)
                child_height_sds_data.append(corrected_sds_data_point)
                child_height_sds_data.append(chronological_sds_data_point)
            elif(child_result["child_observation_value"]["measurement_method"] == "weight"):
                child_weight_data.append(corrected_data_point)
                child_weight_data.append(chronological_data_point)
                child_weight_sds_data.append(corrected_sds_data_point)
                child_weight_sds_data.append(chronological_sds_data_point)
            elif(child_result["child_observation_value"]["measurement_method"] == "bmi"):
                child_bmi_data.append(corrected_data_point)
                child_bmi_data.append(chronological_data_point)
                child_bmi_sds_data.append(corrected_sds_data_point)
                child_bmi_sds_data.append(chronological_sds_data_point)
            elif(child_result["child_observation_value"]["measurement_method"] == "ofc"):
                child_ofc_data.append(corrected_data_point)
                child_ofc_data.append(chronological_data_point)
                child_ofc_sds_data.append(corrected_sds_data_point)
                child_ofc_sds_data.append(chronological_sds_data_point)

        
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
                "label": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
            }
        ],
        height_sds: [
                x: 9.415, `this is the age of the child at date of measurement in decimal years
                y: 1.3 `this is the SDS value for SDS charts
                "label": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
        ],
        .... and so on for the other measurement_methods
        
    ]

    """