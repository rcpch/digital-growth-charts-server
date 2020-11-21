import rcpchgrowth.rcpchgrowth as rcpchgrowth
# from .calculations import create_measurement_object
import numpy as np
import os 
from datetime import datetime
from flask import jsonify

UK90_PREMATURITY_LOWER_THRESHOLD_INDEX = 0 # -0.268309377y or 24 weeks
UK90_TERM_UPPER_THRESHOLD_INDEX = 19 # 42 weeks 0.03833
WHO_2006_LOWER_THRESHOLD_INDEX = 20
WHO_2006_LENGTH_THRESHOLD_INDEX = 55 # 2 y
WHO_2006_HEIGHT_LOWER_THRESHOLD_INDEX = 56 # 2y
WHO_2006_UPPER_THRESHOLD_INDEX = 80 # 4y
UK90_LOWER_THRESHOLD_INDEX = 81 # 4y

def create_centile_values(sex: str, born_preterm=False):
    """
    creates centiles for height/weight/bmi/ofc
    Accepts a sex as a string ['male', 'female']
    Accepts born_preterm, boolean flag. If Born term, reference data for birth should reflect UK-WHO term data.
    """
    
    # sds_array = [-2.67, -2.0, -1.33, -0.67, 0.0, 0.67, 1.33, 2.0, 2.67]  #
    centile_array = [0.4, 2, 9, 25, 50, 75, 91, 98, 99.6]
    # measurements = ["height", "weight", "bmi", "ofc"]
    # datasets = ["uk_90_preterm", "who_infants" , "who_children", "uk90_children"]
    
    height_sds = []
    weight_sds = []
    bmi_sds = []
    ofc_sds = []
    
    for centile in centile_array:

        # Each centile is 2/3 of an SDS - to supply this as accurately as possible it is calculated
        sds_value = sds_value_for_centile_value(centile)

        uk90_preterm_length_sds = []
        who_infant_length_sds = []
        who_child_height_sds = []
        uk90_child_height_sds = []
        uk90_preterm_weight_sds = []
        who_infant_weight_sds = []
        who_child_weight_sds = []
        uk90_child_weight_sds = []
        uk90_preterm_bmi_sds = []
        who_infant_bmi_sds = []
        who_child_bmi_sds = []
        uk90_child_bmi_sds = []
        uk90_preterm_ofc_sds = []
        who_infant_ofc_sds = []
        who_child_ofc_sds = []
        uk90_child_ofc_sds = []

        DECIMAL_AGES=[-0.325804244,-0.306639288,-0.287474333,-0.268309377,-0.249144422,-0.229979466,-0.210814511,-0.191649555,-0.1724846,-0.153319644,-0.134154689,-0.114989733,-0.095824778,-0.076659822,-0.057494867,-0.038329911,-0.019164956,0,0.019164956,0.038329911,0.038329911,0.057494867,0.076659822,0.083333333,0.095824778,0.114989733,0.134154689,0.153319644,0.166666667,0.1724846,0.191649555,0.210814511,0.229979466,0.249144422,0.25,0.333333333,0.416666667,0.5,0.583333333,0.666666667,0.75,0.833333333,0.916666667,1.0,1.083333333,1.166666667,1.25,1.333333333,1.416666667,1.5,1.583333333,1.666666667,1.75,1.833333333,1.916666667,2.0,2.0,2.083333333,2.166666667,2.25,2.333333333,2.416666667,2.5,2.583333333,2.666666667,2.75,2.833333333,2.916666667,3.0,3.083333333,3.166666667,3.25,3.333333333,3.416666667,3.5,3.583333333,3.666666667,3.75,3.833333333,3.916666667,4.0,4.0,4.083333333, 4.166666667, 4.25, 4.333333333, 4.416666667, 4.5, 4.583333333, 4.666666667, 4.75, 4.833333333, 4.916666667, 5.0, 5.083333333, 5.166666667, 5.25, 5.333333333, 5.416666667, 5.5, 5.583333333, 5.666666667, 5.75, 5.833333333, 5.916666667, 6.0, 6.083333333, 6.166666667, 6.25, 6.333333333, 6.416666667, 6.5, 6.583333333, 6.666666667, 6.75, 6.833333333, 6.916666667, 7.0, 7.083333333, 7.166666667, 7.25, 7.333333333, 7.416666667, 7.5, 7.583333333, 7.666666667, 7.75, 7.833333333, 7.916666667, 8.0, 8.083333333, 8.166666667, 8.25, 8.333333333, 8.416666667, 8.5, 8.583333333, 8.666666667, 8.75, 8.833333333, 8.916666667, 9.0, 9.083333333, 9.166666667, 9.25, 9.333333333, 9.416666667, 9.5, 9.583333333, 9.666666667, 9.75, 9.833333333, 9.916666667, 10.0, 10.083333333, 10.166666667, 10.25, 10.333333333, 10.416666667, 10.5, 10.583333333, 10.666666667, 10.75, 10.833333333, 10.916666667, 11.0, 11.083333333, 11.166666667, 11.25, 11.333333333, 11.416666667, 11.5, 11.583333333, 11.666666667, 11.75, 11.833333333, 11.916666667, 12.0, 12.083333333, 12.166666667, 12.25, 12.333333333, 12.416666667, 12.5, 12.583333333, 12.666666667, 12.75, 12.833333333, 12.916666667, 13.0, 13.083333333, 13.166666667, 13.25, 13.333333333, 13.416666667, 13.5, 13.583333333, 13.666666667, 13.75, 13.833333333, 13.916666667, 14.0, 14.083333333, 14.166666667, 14.25, 14.333333333, 14.416666667, 14.5, 14.583333333, 14.666666667, 14.75, 14.833333333, 14.916666667, 15.0, 15.083333333, 15.166666667, 15.25, 15.333333333, 15.416666667, 15.5, 15.583333333, 15.666666667, 15.75, 15.833333333, 15.916666667, 16.0, 16.083333333, 16.166666667, 16.25, 16.333333333, 16.416666667, 16.5, 16.583333333, 16.666666667, 16.75, 16.833333333, 16.916666667, 17.0, 17.083333333, 17.166666667, 17.25, 17.333333333, 17.416666667, 17.5, 17.583333333, 17.666666667, 17.75, 17.833333333, 17.916666667, 18.0, 18.083333333, 18.166666667, 18.25, 18.333333333, 18.416666667, 18.5, 18.583333333, 18.666666667, 18.75, 18.833333333, 18.916666667, 19.0, 19.083333333, 19.166666667, 19.25, 19.333333333, 19.416666667, 19.5, 19.583333333, 19.666666667, 19.75, 19.833333333, 19.916666667, 20.0]

        for index, age in enumerate(DECIMAL_AGES, 0):
            
            if index <= UK90_TERM_UPPER_THRESHOLD_INDEX:
                # at 2 weeks choose UK90 preterm data (lower reference as default)
                # with exception of BMI as there is no BMI reference data below 2 weeks
                
                if (born_preterm):
                    if index < 2: # there is no height data below 25 weeks
                        length_for_z = None
                    else:
                        length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
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
                    length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                except:
                    length_for_z = None
                try:
                    weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                except:
                    weight_for_z = None
                try:
                    bmi_for_z = rcpchgrowth.measurement_from_sds(measurement_method="bmi", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                except:
                    bmi_for_z = None
                try:
                    ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                except:
                    ofc_for_z = None

                if index == WHO_2006_LENGTH_THRESHOLD_INDEX:
                    # at 2 years choose WHO child lying data (lower reference as default)
                    length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    bmi_for_z = rcpchgrowth.measurement_from_sds(measurement_method="bmi", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)

                who_infant_length_sds.append({"label": centile, "x": age, "y": length_for_z})
                who_infant_weight_sds.append({"label": centile, "x": age, "y": weight_for_z})
                who_infant_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                who_infant_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z})

            elif index <= WHO_2006_UPPER_THRESHOLD_INDEX:
                # at 2y choose WHO child standing data (upper reference as default)
                length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                bmi_for_z = rcpchgrowth.measurement_from_sds(measurement_method="bmi", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)

                # at 4y choose WHO child standing data, not UK90 child standing data (lower reference as default)
                if index == WHO_2006_UPPER_THRESHOLD_INDEX:
                    length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    bmi_for_z = rcpchgrowth.measurement_from_sds(measurement_method="bmi", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                    ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)

                who_child_height_sds.append({"label": centile, "x": age, "y": length_for_z})
                who_child_weight_sds.append({"label": centile, "x": age, "y": weight_for_z})
                who_child_bmi_sds.append({"label": centile, "x": age, "y": bmi_for_z})
                who_child_ofc_sds.append({"label": centile, "x": age, "y": ofc_for_z})
            else:
                #choose upper reference by default - no duplicate ages in this dataset
                length_for_z = rcpchgrowth.measurement_from_sds(measurement_method="height", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                weight_for_z = rcpchgrowth.measurement_from_sds(measurement_method="weight", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                bmi_for_z = rcpchgrowth.measurement_from_sds(measurement_method="bmi", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
                
                if (index <= 237 and sex=="female") or (index <= 249 and sex=="male"):
                    # there is no OFC data > 17y in girls or > 18y in boys
                    ofc_for_z = rcpchgrowth.measurement_from_sds(measurement_method="ofc", requested_sds=sds_value, sex=sex, age=age, born_preterm=born_preterm)
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
                    "y": child_result["child_observation_value"]["observation_value"]
                }
            corrected_data_point = {
                "x": child_result["measurement_dates"]["corrected_decimal_age"], 
                "y": child_result["child_observation_value"]["observation_value"]
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