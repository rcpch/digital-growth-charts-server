import math
import scipy.stats as stats
from scipy.interpolate import interp1d
# from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method
from .uk_who import uk_who_lms_array_for_measurement_and_sex
from .turner import turner_lms_array_for_measurement_and_sex
from .trisomy_21 import trisomy_21_lms_array_for_measurement_and_sex
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
        age += (7/365.25) # weekly intervals
    return centile_measurements


def create_chart(reference: str, measurement_method: str, sex: str, born_preterm=False):
    ## creates a chart of 9 centiles
    nine_centile_array = [0.4, 2, 9, 25, 50, 75, 91, 98, 99.6]
    centile_array_experiment = [3, 25, 50, 75, 97 ]
    lms_value_array_list = []

    if reference == 'uk-who': 
        # The UK-WHO reference is made up of 4 separate references, so these each need fetching
        # Not all references are used for all measurement: eg bmi is not used in the preterm references
        # The references which are used are added to an array (lms_value_array_list), which is used to generate
        # the nine centiles

        #select the correct reference data and store it in a reference-specific variable as an array
        try:
            uk90_preterm_reference = uk_who_lms_array_for_measurement_and_sex(
                age=-0.01, 
                measurement_method=measurement_method, 
                sex=sex, 
                born_preterm=born_preterm)
        except:
            uk90_preterm_reference = []
        try:
            uk_who_infants_reference = uk_who_lms_array_for_measurement_and_sex(
                age=0.04, 
                measurement_method=measurement_method, 
                sex=sex, 
                born_preterm=born_preterm)
        except:
            uk_who_infants_reference = []
        try:
            uk_who_children_reference = uk_who_lms_array_for_measurement_and_sex(
                age=2.0, 
                measurement_method=measurement_method, 
                sex=sex, 
                born_preterm=born_preterm)
        except:
            uk_who_children_reference = []
        try:
            uk90_children_reference = uk_who_lms_array_for_measurement_and_sex(
                age=4.0, 
                measurement_method=measurement_method, 
                sex=sex, 
                born_preterm=born_preterm)
        except:
            uk90_children_reference=[]
        
        ## Build an array of all the references
        array_list = [{"reference_name": "uk90_preterm_data", "data": uk90_preterm_reference}, {"reference_name":"who_infant_data", "data": uk_who_infants_reference}, {"reference_name":"who_child_data", "data": uk_who_children_reference}, {"reference_name":"uk90_child_data", "data": uk90_children_reference}]

        ## Pare the array_list down to include only those references which have been selected. Store this as lms_value_array_list
        for element in array_list:
            if len(element["data"]) > 0:
                lms_value_array_list.append(element)
    else:
        try:
            # the Turner and T21 references are single references
            lms_value_array_for_measurement = lms_value_array_for_measurement_for_reference(
                reference=reference, age=1.0, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
            # store the lms data in lms_value_array_list
            lms_value_array_list = [{"reference_name": reference, "data": lms_value_array_for_measurement}]
            
        except LookupError as err:
            print(err)
            return
    
    nine_centiles = []
    for index, centile in enumerate(nine_centile_array):
        # iterate through the 9 centiles
        uk90_preterm, who_infants, who_children, uk90_children = [], [], [], []
        z = sds_value_for_centile_value(centile=centile)
        for index, reference_data in enumerate(lms_value_array_list):
            # each centile is made of difference references
            centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method, sex=sex, lms_array_for_measurement=reference_data["data"], reference=reference)
            if reference == 'uk-who':
                if reference_data['reference_name']==array_list[0]['reference_name']:
                    uk90_preterm = centile_data
                elif reference_data['reference_name']==array_list[1]['reference_name']:
                    who_infants = centile_data
                elif reference_data['reference_name']==array_list[2]['reference_name']:
                    who_children = centile_data
                elif reference_data['reference_name']==array_list[3]['reference_name']:
                    uk90_children = centile_data
                nine_centiles.append({"sds": z, "centile": centile, array_list[0]['reference_name']:uk90_preterm, array_list[1]['reference_name'] : who_infants, array_list[2]['reference_name']: who_children, array_list[3]['reference_name']:uk90_children})
            else:
                ## turner or T21 data
                nine_centiles.append({"sds": z, "centile": centile, reference_data["reference_name"]: centile_data})
        
    return_object = {"centile_data": { measurement_method: nine_centiles}}
    return return_object

def create_all_charts():
    sexes = ["male", "female"]
    references = ["trisomy-21", "turners-syndrome", 'uk-who']
    measurement_methods = ['height', 'weight', 'ofc', 'bmi']
    all_charts=[]
    for number, reference in enumerate(references):
        for index, sex in enumerate(sexes):
            for place, measurement_method in enumerate(measurement_methods):
                born_preterm = False
                if reference=="uk-who":
                    born_preterm = True
                try:
                    data = create_chart(reference=reference, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
                except:
                    data = []
                return_object = { f"{reference}-{measurement_method}-{sex}": }
                all_charts.append(data)
    return all_charts

    """
    structure:

    sex: {
        height: [{l: , x: , y: }, ....],
        weight: [{l: , x: , y: }, ....],
        ofc: [{l: , x: , y: }, ....],
        bmi: [{l: , x: , y: }, ....],
    },
    female: {
        height: [{l: , x: , y: }, ....],
        weight: [{l: , x: , y: }, ....],
        ofc: [{l: , x: , y: }, ....],
        bmi: [{l: , x: , y: }, ....],
    }

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

    heights: {"decimal_age": -0.3258042436687201, "interval": "weeks", "M": "", "L": "", "value": 23, "S": ""},
                {"decimal_age": -0.3066392881587953, "interval": "weeks", "M": "", "L": "", "value": 24, "S": ""},

    """
