import math
import data_tables
import statistics
import scipy.stats as stats
import numpy as np
from datetime import date
import json

"""
dob: date of birth
obs_date: date of observation
sex: sex (string, MALE or FEMALE)
decimal_age: chronological, decimal
corrected_age: corrected for prematurity, decimal
measurement: height, weight, bmi, ofc (decimal)
observation: value (float)
gestation_weeks: gestational age(weeks), integer
gestation_days: supplementary days of gestation
lms: L, M or S
"""

#load the reference data
with open('./data_tables/uk_who_0_20_preterm.json') as json_file:
            data = json.load(json_file)
            json_file.close()

decimal_ages=[-0.325804244,-0.306639288,-0.287474333,-0.268309377,-0.249144422,-0.229979466,-0.210814511,-0.191649555,-0.1724846,-0.153319644,-0.134154689,-0.114989733,-0.095824778,-0.076659822,-0.057494867,-0.038329911,-0.019164956,0,0.019164956,0.038329911,0.038329911,0.057494867,0.076659822,0.083333333,0.095824778,0.114989733,0.134154689,0.153319644,0.166666667,0.1724846,0.191649555,0.210814511,0.229979466,0.249144422,0.25,0.333333333,0.416666667,0.5,0.583333333,0.666666667,0.75,0.833333333,0.916666667,1.0,1.083333333,1.166666667,1.25,1.333333333,1.416666667,1.5,1.583333333,1.666666667,1.75,1.833333333,1.916666667,2.0,2.0,2.083333333,2.166666667,2.25,2.333333333,2.416666667,2.5,2.583333333,2.666666667,2.75,2.833333333,2.916666667,3.0,3.083333333,3.166666667,3.25,3.333333333,3.416666667,3.5,3.583333333,3.666666667,3.75,3.833333333,3.916666667,4.0,4.0,4.083,4.167,4.25,4.333,4.417,4.5,4.583,4.667,4.75,4.833,4.917,5.0,5.083,5.167,5.25,5.333,5.417,5.5,5.583,5.667,5.75,5.833,5.917,6.0,6.083,6.167,6.25,6.333,6.417,6.5,6.583,6.667,6.75,6.833,6.917,7.0,7.083,7.167,7.25,7.333,7.417,7.5,7.583,7.667,7.75,7.833,7.917,8.0,8.083,8.167,8.25,8.333,8.417,8.5,8.583,8.667,8.75,8.833,8.917,9.0,9.083,9.167,9.25,9.333,9.417,9.5,9.583,9.667,9.75,9.833,9.917,10.0,10.083,10.167,10.25,10.333,10.417,10.5,10.583,10.667,10.75,10.833,10.917,11.0,11.083,11.167,11.25,11.333,11.417,11.5,11.583,11.667,11.75,11.833,11.917,12.0,12.083,12.167,12.25,12.333,12.417,12.5,12.583,12.667,12.75,12.833,12.917,13.0,13.083,13.167,13.25,13.333,13.417,13.5,13.583,13.667,13.75,13.833,13.917,14.0,14.083,14.167,14.25,14.333,14.417,14.5,14.583,14.667,14.75,14.833,14.917,15.0,15.083,15.167,15.25,15.333,15.417,15.5,15.583,15.667,15.75,15.833,15.917,16.0,16.083,16.167,16.25,16.333,16.417,16.5,16.583,16.667,16.75,16.833,16.917,17.0,17.083,17.167,17.25,17.333,17.417,17.5,17.583,17.667,17.75,17.833,17.917,18.0,18.083,18.167,18.25,18.333,18.417,18.5,18.583,18.667,18.75,18.833,18.917,19,19.083,19.167,19.25,19.333,19.417,19.5,19.583,19.667,19.75,19.833,19.917,20.0]


def nearest_age_below_index(age: float)->int:
    # result = 0
    result_index = 0
    idx = np.searchsorted(decimal_ages, age, side="left")
    if idx > 0 and (idx == len(decimal_ages) or math.fabs(age - decimal_ages[idx-1]) < math.fabs(age - decimal_ages[idx])):
        result = decimal_ages[idx-1]
        result_index = idx-1
    else:
        result = decimal_ages[idx]
        result_index = idx
    if result < age:
        return result_index
    else:
        return result_index-1

def cubic_interpolation_possible(age: float):
    if age < decimal_ages[3] or age == 0.038329911 or age == 2.0 or age == 4.0 or age > 19.917:
        return False
    else:
        return True

def sds(age: float, measurement: str, observation: float, sex: str)->float:

    age_index_one_below = nearest_age_below_index(age)

    if cubic_interpolation_possible(age):
        l_one_below = data['measurement'][measurement][sex][age_index_one_below]["L"]
        m_one_below = data['measurement'][measurement][sex][age_index_one_below]["M"]
        s_one_below = data['measurement'][measurement][sex][age_index_one_below]["S"]

        l_two_below = data['measurement'][measurement][sex][age_index_one_below-1]["L"]
        m_two_below = data['measurement'][measurement][sex][age_index_one_below-1]["M"]
        s_two_below = data['measurement'][measurement][sex][age_index_one_below-1]["S"]

        l_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["L"]
        m_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["M"]
        s_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["S"]

        l_two_above = data['measurement'][measurement][sex][age_index_one_below+2]["L"]
        m_two_above = data['measurement'][measurement][sex][age_index_one_below+2]["M"]
        s_two_above = data['measurement'][measurement][sex][age_index_one_below+2]["S"]
        
        l = cubic_interpolation(age, age_index_one_below, l_two_below, l_one_below, l_one_above, l_two_above)
        m = cubic_interpolation(age, age_index_one_below, m_two_below, m_one_below, m_one_above, m_two_above)
        s = cubic_interpolation(age, age_index_one_below, s_two_below, s_one_below, s_one_above, s_two_above)
    else:
        l_one_below = data['measurement'][measurement][sex][age_index_one_below]["L"]
        m_one_below = data['measurement'][measurement][sex][age_index_one_below]["M"]
        s_one_below = data['measurement'][measurement][sex][age_index_one_below]["S"]

        l_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["L"]
        m_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["M"]
        s_one_above = data['measurement'][measurement][sex][age_index_one_below+1]["S"]

        l = linear_interpolation(age, age_index_one_below, l_one_below, l_one_above)
        m = linear_interpolation(age, age_index_one_below, m_one_below, m_one_above)
        s = linear_interpolation(age, age_index_one_below, s_one_below, s_one_above)
    print(f"actual age: {round(age, 9)} l,m,s interpolated: {l} {m} {s} lower: {l_one_below} {m_one_below} {s_one_below}")
    sds = z_score(l, m, s, observation)
    return sds


def cubic_interpolation( age: float, age_index_below: int, parameter_two_below: float, parameter_one_below: float, parameter_one_above: float, parameter_two_above: float) -> float:

    cubic_interpolated_value = 0.0

    t = 0.0 #actual age
    tt0 = 0.0
    tt1 = 0.0
    tt2 = 0.0
    tt3 = 0.0

    t01 = 0.0
    t02 = 0.0
    t03 = 0.0
    t12 = 0.0
    t13 = 0.0
    t23 = 0.0

    age_two_below = decimal_ages[age_index_below-1]
    age_one_below = decimal_ages[age_index_below]
    age_one_above = decimal_ages[age_index_below+1]
    age_two_above = decimal_ages[age_index_below+2]
    
    t = round(age, 9)

    tt0 = t - age_two_below
    tt1 = t - age_one_below
    tt2 = t - age_one_above
    tt3 = t - age_two_above

    t01 = age_two_below - age_one_below
    t02 = age_two_below - age_one_above
    t03 = age_two_below - age_two_above

    t12 = age_one_below - age_one_above
    t13 = age_one_below - age_two_above
    t23 = age_one_above - age_two_above

    cubic_interpolated_value = parameter_two_below * tt1 * tt2 * tt3 /t01 / t02 / t03 - parameter_one_below * tt0 * tt2 * tt3 / t01 / t12 /t13 + parameter_one_above * tt0 * tt1 * tt3 / t02/ t12 / t23 - parameter_two_above * tt0 * tt1 * tt2 / t03 / t13 / t23

    return cubic_interpolated_value

def linear_interpolation( decimal_age: float, age_index_below: int, parameter_one_below: int, parameter_one_above: int) -> float:
    linear_interpolated_value = 0.0
    
    age_below = decimal_ages[age_index_below]
    age_above = decimal_ages[age_index_below+1]
    linear_interpolated_value = parameter_one_above + (((decimal_age - age_below)*parameter_one_above-parameter_one_below))/(age_above-age_below)
    return linear_interpolated_value

def z_score(l: float, m: float, s: float, observation: float):
    sds = 0.0
    if round(l, 1) != 0.0:
        sds = (((math.pow((observation / m), l))-1)/(l*s))
    else:
        sds = (math.log(observation / m)/s)
    return sds

def centile(z_score: float):
    #convert z_score to p value
    p = stats.norm.sf(abs(z_score))*2 #twosided
    centile = p*100.0
    if centile >99.6:
        centile = 'above 99.6th centile'
    if centile < 0.04:
        centile = 'below 0.04th centile'
    return centile

def percentage_median_bmi( age: float, actual_bmi: float, sex: str)->float:
    
    age_index_one_below = nearest_age_below_index(age)

    if cubic_interpolation_possible(age):
        m_one_below = data['measurement']["bmi"][sex][age_index_one_below]["M"]
        m_two_below = data['measurement']["bmi"][sex][age_index_one_below-1]["M"]
        m_one_above = data['measurement']["bmi"][sex][age_index_one_below+1]["M"]
        m_two_above = data['measurement']["bmi"][sex][age_index_one_below+2]["M"]
        
        m = cubic_interpolation(age, age_index_one_below, m_two_below, m_one_below, m_one_above, m_two_above)
    else:
        m_one_below = data['measurement']["bmi"][sex][age_index_one_below]["M"]
        m_one_above = data['measurement']["bmi"][sex][age_index_one_below+1]["M"]
        
        m = linear_interpolation(age, age_index_one_below, m_one_below, m_one_above)
    
    percent_median_bmi = (actual_bmi/m)*100.0
    return percent_median_bmi