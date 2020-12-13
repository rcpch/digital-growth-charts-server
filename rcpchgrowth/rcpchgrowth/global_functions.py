import math
import scipy.stats as stats
from scipy.interpolate import interp1d
# from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method
from .uk_who import uk_who_lms_array_for_measurement_and_sex, select_reference_data_for_uk_who_chart
from .turner import turner_lms_array_for_measurement_and_sex, select_reference_data_for_turners
from .trisomy_21 import trisomy_21_lms_array_for_measurement_and_sex, select_reference_data_for_trisomy_21
from .constants.parameter_constants import *
import logging
import json


def cubic_interpolation(age: float, age_one_below: float, age_two_below: float, age_one_above: float, age_two_above: float, parameter_two_below: float, parameter_one_below: float, parameter_one_above: float, parameter_two_above: float) -> float:
    """
    See sds function. This method tests if the age of the child (either corrected for prematurity or chronological) is at a threshold of the reference data
    This method is specific to the UK-WHO data set.
    """

    cubic_interpolated_value = 0.0

    t = 0.0  # actual age ///This commented function is Tim Cole"s used in LMSGrowth to perform cubic interpolation - 50000000 loops, best of 5: 7.37 nsec per loop
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

    cubic_interpolated_value = parameter_two_below * tt1 * tt2 * tt3 / t01 / t02 / t03 - parameter_one_below * tt0 * tt2 * tt3 / t01 / \
        t12 / t13 + parameter_one_above * tt0 * tt1 * tt3 / t02 / t12 / \
        t23 - parameter_two_above * tt0 * tt1 * tt2 / t03 / t13 / t23

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


def linear_interpolation(age: float, age_one_below: float, age_one_above: float, parameter_one_below: float, parameter_one_above: float) -> float:
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
        sds = (((math.pow((observation / m), l)) - 1) / (l * s))
    else:
        sds = (math.log(observation / m) / s)
    return sds


def centile(z_score: float):
    """
    Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage
    """

    centile = (stats.norm.cdf(z_score) * 100)
    return centile


def measurement_for_z(z: float, l: float, m: float, s: float) -> float:
    """
    Returns a measurement for a z score, L, M and S
    """
    if l != 0.0:
        measurement_value = math.pow((1 + l * s * z), 1 / l) * m
    else:
        measurement_value = math.exp(s * z) * m
    return measurement_value


def nearest_lowest_index(
    lms_array: list,
    age: float
) -> int:
    """
    loops through the array of LMS values and returns either 
    the index of an exact match or the lowest nearest decimal age
    """
    lowest_index = 0
    for num, lms_element in enumerate(lms_array):
        reference_age = lms_element["decimal_age"]
        if round(reference_age, 16) == round(age, 16):
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
    age_matched_index = nearest_lowest_index(
        lms_value_array_for_measurement, age)  # returns nearest LMS for age
    if round(lms_value_array_for_measurement[age_matched_index]["decimal_age"], 16) == round(age, 16):
        # there is an exact match in the data with the requested age
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
        age_one_above = lms_value_array_for_measurement[age_matched_index + 1]["decimal_age"]
        parameter_one_below = lms_value_array_for_measurement[age_matched_index]
        parameter_one_above = lms_value_array_for_measurement[age_matched_index + 1]

        if age_matched_index >= 1 and age_matched_index < len(lms_value_array_for_measurement) - 2:
            # cubic interpolation is possible
            age_two_below = lms_value_array_for_measurement[age_matched_index - 1]["decimal_age"]
            age_two_above = lms_value_array_for_measurement[age_matched_index + 2]["decimal_age"]
            parameter_two_below = lms_value_array_for_measurement[age_matched_index - 1]
            parameter_two_above = lms_value_array_for_measurement[age_matched_index + 2]
            
            l = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above,
                                    parameter_two_below=parameter_two_below["L"], parameter_one_below=parameter_one_below["L"], parameter_one_above=parameter_one_above["L"], parameter_two_above=parameter_two_above["L"])
            m = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above,
                                    parameter_two_below=parameter_two_below["M"], parameter_one_below=parameter_one_below["M"], parameter_one_above=parameter_one_above["M"], parameter_two_above=parameter_two_above["M"])
            s = cubic_interpolation(age=age, age_one_below=age_one_below, age_two_below=age_two_below, age_one_above=age_one_above, age_two_above=age_two_above,
                                    parameter_two_below=parameter_two_below["S"], parameter_one_below=parameter_one_below["S"], parameter_one_above=parameter_one_above["S"], parameter_two_above=parameter_two_above["S"])
        else:
            # we are at the thresholds of this reference. Only linear interpolation is possible
            l = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above,
                                     parameter_one_below=parameter_one_below["L"], parameter_one_above=parameter_one_above["L"])
            m = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above,
                                     parameter_one_below=parameter_one_below["M"], parameter_one_above=parameter_one_above["M"])
            s = linear_interpolation(age=age, age_one_below=age_one_below, age_one_above=age_one_above,
                                     parameter_one_below=parameter_one_below["S"], parameter_one_above=parameter_one_above["S"])

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
    born_preterm: bool = False
) -> float:

    try:
        lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(
            reference=reference, age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(
        age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
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
) -> float:

    try:
        lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(
            reference=reference, age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(
        age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]

    return z_score(l=l, m=m, s=s, observation=observation_value)


def percentage_median_bmi(reference: str, age: float, actual_bmi: float, sex: str, born_preterm=False) -> float:
    """
    public method
    This returns a child"s BMI expressed as a percentage of the median value for age and sex.
    It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders.
    It accepts the reference ('uk-who', 'turners-syndrome' or 'trisomy-21')
    """

    # fetch the LMS values for the requested measurement
    try:
        lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(
            reference=reference, measurement_method="bmi", sex=sex, age=age, born_preterm=born_preterm)
    except LookupError as err:
        print(err)
        return None

    # get LMS values from the reference: check for age match, interpolate if none
    try:
        lms = fetch_lms(
            age=age, lms_value_array_for_measurement=lms_value_array_for_measurement)
    except LookupError as err:
        print(err)
        return None

    m = lms["m"]  # this is the median BMI

    percent_median_bmi = (actual_bmi / m) * 100.0
    return percent_median_bmi


def lms_value_array_for_measurement_for_reference(
    reference: str,
    age: float,
    measurement_method: str,
    sex: str,
    born_preterm: bool
) -> list:
    """
    This is a private function which returns the LMS array for measurement_method and sex and reference
    It accepts the reference ('uk-who', 'turners-syndrome' or 'trisomy-21')
    """

    if reference == "uk-who":
        lms_value_array_for_measurement = uk_who_lms_array_for_measurement_and_sex(
            age=age, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
    elif reference == "turners-syndrome":
        lms_value_array_for_measurement = turner_lms_array_for_measurement_and_sex(
            measurement_method=measurement_method, sex=sex, age=age)
    elif reference == "trisomy-21":
        lms_value_array_for_measurement = trisomy_21_lms_array_for_measurement_and_sex(
            measurement_method=measurement_method, sex=sex, age=age)
    else:
        raise ValueError("Incorrect reference supplied")
    return lms_value_array_for_measurement


def generate_centile(z: float, centile: float, measurement_method: str, sex: str, lms_array_for_measurement: list, reference: str) -> list:
    """
    Generates a centile curve for a given reference. 
    Takes the z-score equivalent of the centile, the centile to be used as a label, the sex and measurement method.
    """

    min_age = lms_array_for_measurement[0]["decimal_age"]
    max_age = lms_array_for_measurement[-1]["decimal_age"]

    centile_measurements = []
    age = min_age
    while age <= max_age:
        # loop through the reference in steps of 0.1y
        try:
            measurement = measurement_from_sds(
                reference=reference, measurement_method=measurement_method, requested_sds=z, sex=sex, age=age, born_preterm=True)
        except ValueError as err:
            print(err)
            measurement = None
        # creates a data point
        if measurement is not None:
            rounded = round(measurement, 4)
        else:
            rounded = None
        value = {
            "l": centile,
            "x": round(age,4),
            "y": rounded
        }
        centile_measurements.append(value)

        ## weekly intervals until 2 y, then monthly 
        if age <=2:
            age += (7/365.25) # weekly intervals
        else:
            age += 1/12 # monthly intervals

        # Although it is preferable to have weekly data points, it generates files of ~2.5 MB
        # even after minifying, which are not practical. Weekly values makes plotting easier.
        # Here we have used weekly points from preterm to 2 y, monthly values after.    
        # age += (7/365.25) # weekly intervals
    return centile_measurements

def create_uk_who_chart(centile_selection: str=COLE_TWO_THIRDS_SDS_NINE_CENTILES):

    ## user selects which centile collection they want
    ## If the Cole method is selected, conversion between centile and SDS
    ## is different as SDS is rounded to the nearest 2/3
    ## Cole method selection is stored in the cole_method flag.
    ## If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False
    
    ##
    # iterate through the 4 references that make up UK-WHO
    # There will be a list for each one
    ##
    
    reference_data = [] # all data for a given reference are stored here: this is returned to the user

    for reference_index, reference in enumerate(UK_WHO_REFERENCES):
        sex_list: dict = {} # all the data for a given sex are stored here
        ## For each reference we have 2 sexes
        for sex_index, sex in enumerate(SEXES):
            ##For each sex we have 4 measurement_methods

            measurements: dict = {} # all the data for a given measurement_method are stored here

            for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
                ## for every measurement method we have as many centiles
                ## as have been requested

                centiles=[] # all generated centiles for a selected centile collection are stored here

                for centile_index, centile in enumerate(centile_collection):
                    ## we must create a z for each requested centile
                    ## if the Cole 9 centiles were selected, these are rounded,
                    ## so conversion to SDS is different
                    ## Otherwise standard conversation of centile to z is used
                    if cole_method:
                        z = rounded_sds_for_centile(centile)
                    else:
                        z = sds_for_centile(centile)
                    
                    ## Collect the LMS values from the correct reference
                    lms_array_for_measurement=select_reference_data_for_uk_who_chart(uk_who_reference=reference, measurement_method=measurement_method, sex=sex)
                    
                    ## Generate a centile. there will be nine of these if Cole method selected.
                    ## Some data does not exist at all ages, so any error reflects missing data.
                    ## If this happens, an empty list is returned.
                    try:
                        centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method, sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference="uk-who")
                    except:
                        print(f"There is no data for {measurement_method} at this age.")
                        centile_data = []

                    ## Store this centile for a given measurement
                    centiles.append({"sds": round(z*100)/100, "centile": centile, "data": centile_data})
                    
                ## this is the end of the centile_collection for loop
                ## All the centiles for this measurement, sex and reference are added to the measurements list
                measurements.update({measurement_method: centiles})
            
            ## this is the end of the measurement_methods loop
            ## All data for all measurement_methods for this sex are added to the sex_list list

            sex_list.update({sex: measurements})
                
        ## all data can now be tagged by reference_name and added to reference_data
        reference_data.append({reference: sex_list})
        
    ## returns a list of 4 references, each containing 2 lists for each sex, 
    ## each sex in turn containing 4 datasets for each measurement_method
    return reference_data

    """

    structure:

    UK_WHO generates 4 json objects, each structure as below

    uk90_preterm: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }

    uk_who_infant: {...}
    uk_who_child:{...}
    uk90_child: {...}

    and for the specialist references:

    trisomy_21: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }

    """
def create_trisomy_21_chart(centile_selection: str):
   ## user selects which centile collection they want
    ## If the Cole method is selected, conversion between centile and SDS
    ## is different as SDS is rounded to the nearest 2/3
    ## Cole method selection is stored in the cole_method flag.
    ## If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False
    
    reference_data = [] # all data for a the reference are stored here: this is returned to the user 
    sex_list: dict = {}

    for sex_index, sex in enumerate(SEXES):
            ##For each sex we have 4 measurement_methods

        measurements: dict = {} # all the data for a given measurement_method are stored here

        for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
            ## for every measurement method we have as many centiles
            ## as have been requested

            centiles=[] # all generated centiles for a selected centile collection are stored here

            for centile_index, centile in enumerate(centile_collection):
                ## we must create a z for each requested centile
                ## if the Cole 9 centiles were selected, these are rounded,
                ## so conversion to SDS is different
                ## Otherwise standard conversation of centile to z is used
                if cole_method:
                    z = rounded_sds_for_centile(centile)
                else:
                    z = sds_for_centile(centile)
                
                ## Collect the LMS values from the correct reference
                lms_array_for_measurement=select_reference_data_for_trisomy_21(measurement_method=measurement_method, sex=sex)
                
                ## Generate a centile. there will be nine of these if Cole method selected.
                ## Some data does not exist at all ages, so any error reflects missing data.
                ## If this happens, an empty list is returned.
                try:
                    centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method, sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference=TRISOMY_21)
                except:
                    print(f"There is no data for {measurement_method} at this age.")
                    centile_data = []

                ## Store this centile for a given measurement
                centiles.append({"sds": round(z*100)/100, "centile": centile, "data": centile_data})
                
            ## this is the end of the centile_collection for loop
            ## All the centiles for this measurement, sex and reference are added to the measurements list
            measurements.update({measurement_method: centiles})
            
            ## this is the end of the measurement_methods loop
            ## All data for all measurement_methods for this sex are added to the sex_list list

            sex_list.update({sex: measurements})
                
    ## all data can now be tagged by reference_name and added to reference_data
    reference_data.append({TRISOMY_21: sex_list})
    return reference_data

def create_turner_chart(centile_selection: str):
   ## user selects which centile collection they want
    ## If the Cole method is selected, conversion between centile and SDS
    ## is different as SDS is rounded to the nearest 2/3
    ## Cole method selection is stored in the cole_method flag.
    ## If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False
    
    reference_data = [] # all data for a the reference are stored here: this is returned to the user 
    sex_list: dict = {}

    for sex_index, sex in enumerate(SEXES):
            ##For each sex we have 4 measurement_methods
            ## Turner is female only, but we will generate empty arrays for male
            ## data to keep all objects the same

        measurements: dict = {} # all the data for a given measurement_method are stored here

        for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
            ## for every measurement method we have as many centiles
            ## as have been requested

            centiles=[] # all generated centiles for a selected centile collection are stored here

            for centile_index, centile in enumerate(centile_collection):
                ## we must create a z for each requested centile
                ## if the Cole 9 centiles were selected, these are rounded,
                ## so conversion to SDS is different
                ## Otherwise standard conversation of centile to z is used
                if cole_method:
                    z = rounded_sds_for_centile(centile)
                else:
                    z = sds_for_centile(centile)
                
                ## Collect the LMS values from the correct reference
                try:
                    lms_array_for_measurement=select_reference_data_for_turners(measurement_method=measurement_method, sex=sex)
                except LookupError:
                    # there is no data in the reference
                    lms_array_for_measurement=[]
                
                ## Generate a centile. there will be nine of these if Cole method selected.
                ## Some data does not exist at all ages, so any error reflects missing data.
                ## If this happens, an empty list is returned.
                try:
                    centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method, sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference=TRISOMY_21)
                except:
                    print(f"There is no data for {measurement_method} at this age.")
                    centile_data = []

                ## Store this centile for a given measurement
                centiles.append({"sds": round(z*100)/100, "centile": centile, "data": centile_data})
                
            ## this is the end of the centile_collection for loop
            ## All the centiles for this measurement, sex and reference are added to the measurements list
            measurements.update({measurement_method: centiles})
            
            ## this is the end of the measurement_methods loop
            ## All data for all measurement_methods for this sex are added to the sex_list list

            sex_list.update({sex: measurements})
                
    ## all data can now be tagged by reference_name and added to reference_data
    reference_data.append({TURNERS: sex_list})
    return reference_data



def rounded_sds_for_centile(centile:float)->float:
    """
    converts a centile (supplied as a percentage) using the scipy package to the nearest 2/3 SDS.
    """
    sds = stats.norm.ppf(centile/100)
    if sds == 0:
        return sds
    else:
        rounded_to_nearest_two_thirds = round(sds/(2/3))
        return rounded_to_nearest_two_thirds*(2/3)

def sds_for_centile(centile: float)->float:
    """
    converts a centile (supplied as a percentage) using the scipy package to an SDS.
    """
    sds = stats.norm.ppf(centile/100)
    return sds


def sds_value_for_centile_value(centile: float):
    ## to be deprecated

    if centile == 0.4:
        return -2.0 - (2 / 3)
    elif centile == 2:
        return -2.0
    elif centile == 9:
        return -1 - (1 / 3)
    elif centile == 25:
        return 0 - (2 / 3)
    elif centile == 50:
        return 0
    elif centile == 75:
        return 2 / 3
    elif centile == 91:
        return 1 + (1 / 3)
    elif centile == 98:
        return 2.0
    elif centile == 99.6:
        return 2 + (2 / 3)
    else:
        # error
        raise LookupError("SDS could not be calculated from Centile supplied")

