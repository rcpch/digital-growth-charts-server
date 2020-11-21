import math
import scipy.stats as stats
from scipy.interpolate import interp1d
# from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method
from .uk_who import uk_who_lms_array_for_measurement_and_sex
from .turner import turner_lms_array_for_measurement_and_sex
from .trisomy_21 import trisomy_21_lms_array_for_measurement_and_sex
import logging

def cubic_interpolation( age: float, age_one_below: float, age_two_below: float, age_one_above: float, age_two_above: float, parameter_two_below: float, parameter_one_below: float, parameter_one_above: float, parameter_two_above: float) -> float:

    """
    See sds function. This method tests if the age of the child (either corrected for prematurity or chronological) is at a threshold of the reference data
    This method is specific to the UK-WHO data set.
    """

    cubic_interpolated_value = 0.0

    t = 0.0 #actual age ///This commented function is Tim Cole"s used in LMSGrowth to perform cubic interpolation - 50000000 loops, best of 5: 7.37 nsec per loop
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
    
    t = age

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

    # prerequisite arrays for either of below functions
    # xpoints = [age_two_below, age_one_below, age_one_above, age_two_above]
    # ypoints = [parameter_two_below, parameter_one_below, parameter_one_above, parameter_two_above]

    # this is the scipy cubic spline interpolation function...
    # cs = CubicSpline(xpoints,ypoints,bc_type="natural")
    # cubic_interpolated_value = cs(age) # this also works, but not as accurate: 50000000 loops, best of 5: 7.42 nsec per loop

    # this is the scipy splrep function
    # tck = interpolate.splrep(xpoints, ypoints)
    # cubic_interpolated_value = interpolate.splev(age, tck)   #Matches Tim Cole"s for accuracy but slower: speed - 50000000 loops, best of 5: 7.62 nsec per loop

    return cubic_interpolated_value

def linear_interpolation( age: float, age_one_below: float, age_one_above: float, parameter_one_below: float, parameter_one_above: float) -> float:

    """
    See sds function. This method is to do linear interpolation of L, M and S values for children whose ages are at the threshold of the reference data, making cubic interpolation impossible
    """
    
    linear_interpolated_value = 0.0

    # linear_interpolated_value = parameter_one_above + (((decimal_age - age_below)*parameter_one_above-parameter_one_below))/(age_above-age_below)
    x_array = [age_one_below, age_one_above]
    y_array = [parameter_one_below, parameter_one_above]
    intermediate = interp1d(x_array, y_array)
    linear_interpolated_value = intermediate(age)
    return linear_interpolated_value

def z_score(l: float, m: float, s: float, observation: float):

    """
    Converts the (age-specific) L, M and S parameters into a z-score
    """
    sds = 0.0
    if l != 0.0:
        sds = (((math.pow((observation / m), l))-1)/(l*s))
    else:
        sds = (math.log(observation / m)/s)
    return sds

def centile(z_score: float):
    """
    Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage
    """

    centile = (stats.norm.cdf(z_score) * 100)
    return centile

def measurement_for_z(z: float, l: float, m:float, s:float)->float:

    """
    Returns a measurement for a z score, L, M and S
    """
    if l != 0.0:
        measurement_value = math.pow((1+l*s*z),1/l)*m
    else:
        measurement_value = math.exp(s*z)*m
    return measurement_value


def nearest_lowest_index(
        lms_array:list, 
        age: float
    )->int:
    """
    loops through the array of LMS values and returns either 
    the index of an exact match or the lowest nearest decimal age
    """
    lowest_index=0
    for num, lms_element in enumerate(lms_array):
        if lms_element["decimal_age"]==age:
            lowest_index = num
            break
        else:
            if lms_element["decimal_age"] < age:
                lowest_index = num
    return lowest_index

def fetch_lms(age: float, lms_value_array_for_measurement: list):
    """
    Retuns the LMS for a given age. If there is no exact match in the reference
    an interpolated LMS is returned. Cubic interpolation is used except at the fringes of the 
    reference where linear interpolation is used.
    It accepts the age and a python list of the LMS values for that measurement_method and sex.
    """
    age_matched_index = nearest_lowest_index(lms_value_array_for_measurement, age) # returns nearest LMS for age
    if lms_value_array_for_measurement[age_matched_index]["decimal_age"] == age:
        ## there is an exact match in the data with the requested age
        l = lms_value_array_for_measurement[age_matched_index]["L"]
        m = lms_value_array_for_measurement[age_matched_index]["M"]
        s = lms_value_array_for_measurement[age_matched_index]["S"]
    else:
        # there has not been an exact match in the reference data
        # Interpolation will be required. 
        # The age_matched_index is one below the age supplied. There
        # needs to be a value below that, and two values above the supplied age, 
        # for cubic interpolation to be possible.
        age_one_below = lms_value_array_for_measurement[age_matched_index]["decimal_age"]
        age_one_above = lms_value_array_for_measurement[age_matched_index+1]["decimal_age"]
        parameter_one_below = lms_value_array_for_measurement[age_matched_index]
        parameter_one_above = lms_value_array_for_measurement[age_matched_index+1]

        if age_matched_index >= 1 and age_matched_index < len(lms_value_array_for_measurement)-2:
            # cubic interpolation is possible
            age_two_below = lms_value_array_for_measurement[age_matched_index-1]["decimal_age"]
            age_two_above = lms_value_array_for_measurement[age_matched_index+2]["decimal_age"]
            parameter_two_below = lms_value_array_for_measurement[age_matched_index-1]
            parameter_two_above = lms_value_array_for_measurement[age_matched_index+2]
            l = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above, parameter_two_below=parameter_two_below["L"], parameter_one_below=parameter_one_below["L"], parameter_one_above=parameter_one_above["L"], parameter_two_above=parameter_two_above["L"])
            m = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above, parameter_two_below=parameter_two_below["M"], parameter_one_below=parameter_one_below["M"], parameter_one_above=parameter_one_above["M"], parameter_two_above=parameter_two_above["M"])
            s = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above, parameter_two_below=parameter_two_below["S"], parameter_one_below=parameter_one_below["S"], parameter_one_above=parameter_one_above["S"], parameter_two_above=parameter_two_above["S"])
        else:
            # we are at the thresholds of this reference. Only linear interpolation is possible
            l = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above, parameter_one_below=parameter_one_below["L"], parameter_one_above=parameter_one_above["L"])
            m = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above, parameter_one_below=parameter_one_below["M"], parameter_one_above=parameter_one_above["M"])
            s = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above, parameter_one_below=parameter_one_below["S"], parameter_one_above=parameter_one_above["S"])
            
    return {
        "l": l,
        "m": m,
        "s": s
    }

def measurement_from_sds(
        reference: str,  
        requested_sds: float,
        measurement_method: str,  
        sex: str,  
        age: float,
        born_preterm: bool=False
    )->float:

    try:
        lms_value_array_for_measurement=lms_value_array_for_measurement_for_reference(reference=reference, age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None
    
    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]

    observation_value = measurement_for_z(z=requested_sds, l=l, m=m, s=s)
    return observation_value


def sds_for_measurement(
        reference: str,
        age: float,
        measurement_method: str,
        observation_value: float,
        sex: str,
        born_preterm: bool = False
    )->float:

    try:
        lms_value_array_for_measurement=lms_value_array_for_measurement_for_reference(reference=reference, age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None
    
    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]

    return z_score(l=l, m=m, s=s, observation=observation_value)

def percentage_median_bmi(reference: str, age: float, actual_bmi: float, sex: str, born_preterm=False)->float:

    """
    public method
    This returns a child"s BMI expressed as a percentage of the median value for age and sex.
    It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders.
    It accepts the reference ('UKWHO', 'TURNER' or 'TRISOMY_21')
    """

    # fetch the LMS values for the requested measurement
    try:
        lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(reference=reference, measurement_method="bmi", sex=sex, age=age, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None

    # get LMS values from the reference: check for age match, interpolate if none
    try:
        lms = fetch_lms(age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    except LookupError as err:
        print(err)
        return None
    
    m = lms["m"] # this is the median BMI
    
    percent_median_bmi = (actual_bmi/m)*100.0
    return percent_median_bmi

def lms_value_array_for_measurement_for_reference(
        reference: str,
        age: float,
        measurement_method: str,
        sex: str,
        born_preterm: bool
    )->list:

    """
    This is a private function which returns the LMS array for measurement_method and sex and reference
    It accepts the reference ('UKWHO', 'TURNER' or 'TRISOMY_21')
    """

    if reference == "UKWHO":
        lms_value_array_for_measurement=uk_who_lms_array_for_measurement_and_sex(age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    elif reference == "TURNER":
        lms_value_array_for_measurement=turner_lms_array_for_measurement_and_sex(measurement_method=measurement_method, sex=sex, age=age)
    elif reference == "T21":
        lms_value_array_for_measurement=trisomy_21_lms_array_for_measurement_and_sex(measurement_method=measurement_method, sex=sex, age=age)
    else:
        raise ValueError("Incorrect reference supplied")
    return lms_value_array_for_measurement


def generate_centile(z: float, centile: float, measurement_method: str, sex:str, lms_array_for_measurement: list, reference: str)->list:

    """
    Generates a centile curve for a given reference. 
    Takes the z-score equivalent of the centile, the centile to be used as a label, the sex and measurement method.
    """

    min_age = lms_array_for_measurement[0]["decimal_age"]
    max_age = lms_array_for_measurement[-1]["decimal_age"]

    # ages=[1.0, 1.2, 1.4, 1.6, 1.8, 2.0, 2.2, 2.4, 2.6, 2.8, 3.0, 3.2, 3.4, 3.6, 3.8, 4.0, 4.2, 4.4, 4.6, 4.8, 5.0, 5.2, 5.4, 5.6, 5.8, 6.0, 6.2, 6.4, 6.6, 6.8, 7.0, 7.2, 7.4, 7.6, 7.8, 8.0, 8.2, 8.4, 8.6, 8.8, 9.0, 9.2, 9.4, 9.6, 9.8, 10.0, 10.2, 10.4, 10.6, 10.8, 11.0, 11.2, 11.4, 11.6, 11.8, 12.0, 12.2, 12.4, 12.6, 12.8, 13.0, 13.2, 13.4, 13.6, 13.8, 14.0, 14.2, 14.4, 14.6, 14.8, 15.0, 15.2, 15.4, 15.6, 15.8, 16.0, 16.2, 16.4, 16.6, 16.8, 17.0, 17.2, 17.4, 17.6, 17.8, 18.0, 18.2, 18.4, 18.6, 18.8, 19.0, 19.2, 19.4, 19.6, 19.8]
    centile_measurements=[]
    age = min_age
    while age < max_age:
        # loop through the reference in steps of 0.1y
        measurement = measurement_from_sds(reference=reference, measurement_method=measurement_method, requested_sds=z, sex=sex, age=age)
        ## creates a data point
        value = {
            "label": centile,
            "x": age,
            "y": measurement
        }
        centile_measurements.append(value)
        age += 0.1
    return {
        "sds": z,
        "centile": centile,
        "turner_data": centile_measurements
    }

def create_chart(reference: str, measurement_method:str, sex: str, age: float, born_preterm=False):
    centile_array = [0.4, 2, 9, 25, 50, 75, 91, 98, 99.6]
    try:
        lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(reference=reference, age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return
    chart_values=[]
    for index, centile in enumerate(centile_array):
        z=sds_value_for_centile_value(centile=centile)
        centile_line = generate_centile(z=z, centile=centile, measurement_method=measurement_method, sex=sex, lms_array_for_measurement=lms_value_array_for_measurement, reference=reference)
        chart_values.append(centile_line)
    return {"data": chart_values, "key": measurement_method}

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