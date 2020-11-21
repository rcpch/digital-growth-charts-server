from rcpchgrowth.rcpchgrowth import measurement_from_sds
from datetime import datetime


def create_centile_values(reference: str, sex: str, born_preterm=False):
    """
    creates centiles for height/weight/bmi/ofc
    Accepts a sex as a string ['male', 'female']
    Accepts born_preterm, boolean flag. If Born term, reference data for birth should reflect UK-WHO term data.
    """

    # sds_array = [-2.67, -2.0, -1.33, -0.67, 0.0, 0.67, 1.33, 2.0, 2.67]  #
    centile_array = [0.4, 2, 9, 25, 50, 75, 91, 98, 99.6]
    # measurements = ["height", "weight", "bmi", "ofc"]
    
    height_sds = []
    weight_sds = []
    bmi_sds = []
    ofc_sds = []
    
    for centile in centile_array:

        # Each centile is 2/3 of an SDS - to supply this as accurately as possible it is calculated
        sds_value = sds_value_for_centile_value(centile)

        length_sds = []
        weight_sds = []
        bmi_sds = []
        ofc_sds = []
        
        for index, age in enumerate(decimal_ages, 0):
            
            if index <= UK90_TERM_UPPER_THRESHOLD_INDEX:
                # at 2 weeks choose UK90 preterm data (lower reference as default)
                # with exception of BMI as there is no BMI reference data below 2 weeks
                
                if (born_preterm):
                    if index < 2: # there is no height data below 25 weeks
                        length_for_z = None
                    else:
                        length_for_z = measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, decimal_age=age, default_to_youngest_reference=True, born_preterm=born_preterm)
                    weight_for_z = measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, decimal_age=age, default_to_youngest_reference=True, born_preterm=born_preterm)
                    ofc_for_z = measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, decimal_age=age, default_to_youngest_reference=True, born_preterm=born_preterm)
                    bmi_for_z = None # there is no UK90 preterm BMI data

                    uk90_preterm_length_sds.append({"label": centile, "x": age, "y": length_for_z})
                    uk90_preterm_weight_sds.append({"label": centile, "x": age, "y": weight_for_z})
                    uk90_preterm_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                    uk90_preterm_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z})
                else:
                    ## centile curves are unwanted in term babies up to 2 weeks - age should start at 0
                    length_for_z = None
                    weight_for_z = None
                    bmi_for_z = None
                    ofc_for_z = None

                    uk90_preterm_length_sds=[]
                    uk90_preterm_weight_sds=[]
                    uk90_preterm_bmi_sds=[]
                    uk90_preterm_ofc_sds=[]

            elif index <= WHO_2006_LENGTH_THRESHOLD_INDEX:
                # at 2 weeks choose WHO child lying data (upper reference as default)
                try:
                    length_for_z = measurement_from_sds("height", sds_value, sex, age, False, born_preterm=born_preterm)
                except:
                    length_for_z = None
                try:
                    weight_for_z = measurement_from_sds("weight", sds_value, sex, age, False, born_preterm=born_preterm)
                except:
                    weight_for_z = None
                try:
                    bmi_for_z = measurement_from_sds("bmi", sds_value, sex, age, False, born_preterm=born_preterm)
                except:
                    bmi_for_z = None
                try:
                    ofc_for_z = measurement_from_sds("ofc", sds_value, sex, age, False, born_preterm=born_preterm)
                except:
                    ofc_for_z = None

                if index == WHO_2006_LENGTH_THRESHOLD_INDEX:
                    # at 2 years choose WHO child lying data (lower reference as default)
                    length_for_z = measurement_from_sds("height", sds_value, sex, age, True, born_preterm=born_preterm)
                    weight_for_z = measurement_from_sds("weight", sds_value, sex, age, True, born_preterm=born_preterm)
                    bmi_for_z = measurement_from_sds("bmi", sds_value, sex, age, True, born_preterm=born_preterm)
                    ofc_for_z = measurement_from_sds("ofc", sds_value, sex, age, True, born_preterm=born_preterm)

                who_infant_length_sds.append({"label": centile, "x": age, "y": length_for_z})
                who_infant_weight_sds.append({"label": centile, "x": age, "y": weight_for_z})
                who_infant_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                who_infant_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z})

            elif index <= WHO_2006_UPPER_THRESHOLD_INDEX:
                # at 2y choose WHO child standing data (upper reference as default)
                length_for_z = measurement_from_sds("height", sds_value, sex, age, False, born_preterm=born_preterm)
                weight_for_z = measurement_from_sds("weight", sds_value, sex, age, False, born_preterm=born_preterm)
                bmi_for_z = measurement_from_sds("bmi", sds_value, sex, age, False, born_preterm=born_preterm)
                ofc_for_z = measurement_from_sds("ofc", sds_value, sex, age, False, born_preterm=born_preterm)

                # at 4y choose WHO child standing data, not UK90 child standing data (lower reference as default)
                if index == WHO_2006_UPPER_THRESHOLD_INDEX:
                    length_for_z = measurement_from_sds("height", sds_value, sex, age, True, born_preterm=born_preterm)
                    weight_for_z = measurement_from_sds("weight", sds_value, sex, age, True, born_preterm=born_preterm)
                    bmi_for_z = measurement_from_sds("bmi", sds_value, sex, age, True, born_preterm=born_preterm)
                    ofc_for_z = measurement_from_sds("ofc", sds_value, sex, age, True, born_preterm=born_preterm)

                who_child_height_sds.append({"label": centile, "x": age, "y": length_for_z})
                who_child_weight_sds.append({"label": centile, "x": age, "y": weight_for_z})
                who_child_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                who_child_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z})
            else:
                #choose upper reference by default - no duplicate ages in this dataset
                length_for_z = measurement_from_sds("height", sds_value, sex, age, False, born_preterm=born_preterm)
                weight_for_z = measurement_from_sds("weight", sds_value, sex, age, False, born_preterm=born_preterm)
                bmi_for_z = measurement_from_sds("bmi", sds_value, sex, age, False, born_preterm=born_preterm)
                
                if (index <= 237 and sex=="female") or (index <= 249 and sex=="male"):
                    # there is no OFC data > 17y in girls or > 18y in boys
                    ofc_for_z = measurement_from_sds("ofc", sds_value, sex, age, False, born_preterm=born_preterm)
                else:
                    ofc_for_z = None

                uk90_child_height_sds.append({"label": centile, "x": age, "y": length_for_z}) 
                uk90_child_weight_sds.append({"label": centile, "x": age, "y": weight_for_z}) 
                uk90_child_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                uk90_child_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z}) 
            
        height_sds.append({"sds": sds_value, "centile": centile, "uk90_preterm_data": uk90_preterm_length_sds, "who_infant_data": who_infant_length_sds, "who_child_data": who_child_height_sds, "uk90_child_data": uk90_child_height_sds})
        weight_sds.append({"sds": sds_value, "centile": centile, "uk90_preterm_data": uk90_preterm_weight_sds, "who_infant_data": who_infant_weight_sds, "who_child_data": who_child_weight_sds, "uk90_child_data": uk90_child_weight_sds})
        bmi_sds.append({"sds": sds_value, "centile": centile, "uk90_preterm_data": uk90_preterm_bmi_sds, "who_infant_data": who_infant_bmi_sds, "who_child_data": who_child_bmi_sds, "uk90_child_data": uk90_child_bmi_sds})
        ofc_sds.append({"sds": sds_value, "centile": centile, "uk90_preterm_data": uk90_preterm_ofc_sds, "who_infant_data": who_infant_ofc_sds, "who_child_data": who_child_ofc_sds, "uk90_child_data": uk90_child_ofc_sds})
    
    centiles = {"height": height_sds, "weight": weight_sds, "bmi": bmi_sds, "ofc": ofc_sds}
    return centiles

def create_data_plots(child_results_array):
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
                    "y": child_result["child_observation_value"]["measurement_value"]
                }
            corrected_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["child_observation_value"]["measurement_value"]
            }
            chronological_sds_data_point = {
                    "x": child_result["measurement_dates"]["chronological_decimal_age"], 
                    "y": child_result["measurement_calculated_values"]["sds"]
                }
            corrected_sds_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["measurement_calculated_values"]["sds"]
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
        {
            childData: [
                {
                    x: 9.415, `this is the age of the child at date of measurement
                    y: 120 `this is the observation value
                }

            ],
            data: [
                {
                    sds: -2.666666,
                    uk90_child_data:[.....],
                    uk90_preterm_data: [...],
                    who_child_data: [...],
                    who_infant_data: [
                        {
                            label: 0.4, `this is the centile
                            x: 4, `this is the decimal age
                            y: 91.535  `this is the measurement
                        }
                    ]
                }
            ],
            key: "height"
        },
        ... repeat for weight, bmi, ofc, based on which measurements supplied. If only height data supplied, only height centile data returned
    ]

    """