import math
import scipy.stats as stats
from scipy.interpolate import interp1d
# from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method
from datetime import date
import json
import pkg_resources
from .constants import *
# import timeit #see below, comment back in if timing functions in this module

"""
birth_date: date of birth
observation_date: date of observation
sex: sex (string, MALE or FEMALE)
decimal_age: chronological, decimal
corrected_age: corrected for prematurity, decimal
measurement_method: height, weight, bmi, ofc (decimal)
observation: value (float)
gestation_weeks: gestational age(weeks), integer
gestation_days: supplementary days of gestation
lms: L, M or S
reference: reference data
"""

#load the reference data

UK90_DATA = pkg_resources.resource_filename(__name__, "/data_tables/uk90.json")
with open(UK90_DATA) as json_file:
            UK90_DATA = json.load(json_file)
            json_file.close()
UK90_TERM_DATA = pkg_resources.resource_filename(__name__, "/data_tables/uk90_term.json")
with open(UK90_TERM_DATA) as json_file:
            UK90_TERM_DATA = json.load(json_file)
            json_file.close()
WHO_INFANTS_DATA = pkg_resources.resource_filename(__name__, "/data_tables/who_infants.json")
with open(WHO_INFANTS_DATA) as json_file:
            WHO_INFANTS_DATA = json.load(json_file)
            json_file.close()
WHO_CHILD_DATA = pkg_resources.resource_filename(__name__, "/data_tables/who_children.json")
with open(WHO_CHILD_DATA) as json_file:
            WHO_CHILD_DATA = json.load(json_file)
            json_file.close()

#public functions
def uk_who_sds_calculation(
        age: float,
        measurement_method: str,
        measurement_value: float,
        sex: str,
        born_preterm: bool = False
    )->float:

    """
    The is the caller function to calculate an SDS for a child specifically using the UK-WHO dataset(s).
    
    """

    # Get the correct reference from the patchwork of references that make up UK-WHO
    try:
        selected_reference = uk_who_reference(age=age, born_preterm=born_preterm)
    except: # there is no reference for the age supplied
        return ValueError("There is no reference for the age supplied.")

    # Check that the measurement requested has reference data at that age
    if reference_data_absent(
        age=age, 
        reference=selected_reference, 
        measurement_method=measurement_method, 
        sex=sex):
        return ValueError("There is no reference data for this measurement at this age")

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = selected_reference["measurement"][measurement_method][sex]

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, born_preterm=born_preterm, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]
    ## calculate the SDS from the L, M and S values

    return z_score(l=l, m=m, s=s, observation=measurement_value)

def fetch_lms(age: float, born_preterm: bool, lms_value_array_for_measurement: list):
    """
    Retuns the LMS 
    """
    # Define if there is a match for this age in the reference selected.
    # Note: if the child is 37-42 weeks and not born preterm, no interpolation is required
    # as reference data only have one L, M and S
    if age >= THIRTY_SEVEN_WEEKS_GESTATION and age < FORTY_TWO_WEEKS_GESTATION and (born_preterm is False):
        l = lms_value_array_for_measurement[0]["L"]
        m = lms_value_array_for_measurement[0]["M"]
        s = lms_value_array_for_measurement[0]["S"]
    else:
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
            # needs to be a value below that, and two values above, 
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

def nearest_lowest_index(
        lms_array:list, 
        age: float
    )->int:
    """
    loops through the array of LMS values and returns either 
    thie index of an exact match or the lowest nearest decimal age
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


def reference_data_absent( 
        age: float,
        reference: json,
        measurement_method: str,
        sex: str
    ) -> bool:
    """
    Helper function.
    Returns boolean
    Tests presence of valid reference data for a given measurement request

    Reference data is not complete for all ages/sexes/measurements.
     - Length data is not available until 25 weeks gestation, though weight date is available from 23 weeks
     - There is only BMI reference data from 2 weeks of age to aged 20y
     - Head circumference reference data is available from 23 weeks gestation to 17y in girls and 18y in boys
     - lowest threshold is 23 weeks, upper threshold is 20y
    """

    if age < TWENTY_THREE_WEEKS_GESTATION: # lower threshold of UK90 data
        return True
    
    if age > TWENTY_YEARS: # upper threshold of UK90 data
        return True

    if measurement_method == "height" and age < TWENTY_FIVE_WEEKS_GESTATION:
        return True
        
    elif measurement_method == "bmi" and age < FORTY_TWO_WEEKS_GESTATION:
        return True
    
    elif measurement_method == "ofc":
        if (sex == "male" and age > EIGHTEEN_YEARS) or (sex == "female" and age > SEVENTEEN_YEARS):
            return True
        else:
            return False
    else:
        return False

def uk_who_reference(
        age: float, 
        born_preterm: bool = False
    ) -> json:
    """
    The purpose of this function is to choose the correct reference for calculation.
    The UK-WHO standard is an unusual case because it combines two different reference sources.
    - UK90 reference runs from 23 weeks to 20 y
    - WHO 2006 runs from 2 weeks to 4 years
    - UK90 then resumes from 4 years to 20 years
    The function return the appropriate reference file as json
    """

    # CONSTANTS RELEVANT ONLY TO UK-WHO REFERENCE-SELECTION LOGIC
    # 23 weeks is the lowest decimal age available on the UK90 charts
    UK90_REFERENCE_LOWER_THRESHOLD = ((23 * 7) - (40*7)) / 365.25  # 23 weeks as decimal age
    UK90_TERM_REFERENCE_LOWER_THRESHOLD = ((37 * 7) - (40*7)) / 365.25  # 37 weeks as decimal age
    UK90_TERM_REFERENCE_UPPER_THRESHOLD = ((42 * 7) - (40*7)) / 365.25  # 42 weeks as decimal age
    # The WHO references change from measuring infants in the lying position to measuring children in the standing position at 2.0 years.
    WHO_CHILD_LOWER_THRESHOLD = 2.0  # 2 years as decimal age
    # The UK-WHO standard is complicated because it switches from the WHO references to UK90 references
    #  at the age of 4.0 years. This is because it was felt the reference data from breast fed infants
    #  from the WHO cohorts were more accurate than the UK90 cohorts for this age group.
    WHO_CHILDREN_UPPER_THRESHOLD = 4.0
    UK90_UPPER_THRESHOLD = 20

    #These conditionals are to select the correct reference
    if age < UK90_REFERENCE_LOWER_THRESHOLD:
        # Below the range for which we have reference data, we can't provide a calculation.
        return ValueError("There is no reference data below 23 weeks gestation")
    elif age < UK90_TERM_REFERENCE_LOWER_THRESHOLD:
        # Below 37 weeks, the UK90 preterm data is always used
        return UK90_DATA

    elif age < UK90_TERM_REFERENCE_UPPER_THRESHOLD:
        # Below 42 weeks
        if born_preterm:
            # Preterm children should continue to be plotted using the preterm references
            return UK90_DATA
        else:
            return UK90_TERM_DATA
    
    elif age < WHO_CHILD_LOWER_THRESHOLD:
        # Children beyond 2 weeks but below 2 years are measured lying down using WHO data
        return WHO_INFANTS_DATA
        
    elif age < WHO_CHILDREN_UPPER_THRESHOLD:
        # Children beyond 2 years but below 4 years are measured standing up using WHO data
        return WHO_CHILD_DATA
    
    elif age <= UK90_UPPER_THRESHOLD:
        # All children 4 years and above are measured using UK90 child data
        return UK90_DATA

    else:
        return ValueError("There is no reference data above the age of 20 years.")

def centile(z_score: float):
    """
    Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage
    """

    centile = (stats.norm.cdf(z_score) * 100)
    return centile

def percentage_median_bmi( age: float, actual_bmi: float, sex: str, born_preterm=False)->float:

    """
    public method
    This returns a child"s BMI expressed as a percentage of the median value for age and sex.
    It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders.
    """
    
    # Get the correct reference from the patchwork of references that make up UK-WHO
    try:
        selected_reference = uk_who_reference(age=age, born_preterm=born_preterm)
    except: # there is no reference for the age supplied
        return ValueError("There is no reference for the age supplied.")

    # Check that the measurement requested has reference data at that age
    if reference_data_absent(
        age=age, 
        reference=selected_reference, 
        measurement_method="bmi", 
        sex=sex):
        return ValueError("There is no reference data for BMI at this age")

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = selected_reference["measurement"]['bmi'][sex]

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, born_preterm=born_preterm, lms_value_array_for_measurement=lms_value_array_for_measurement)
    
    m = lms["m"] # this is the median BMI
    
    percent_median_bmi = (actual_bmi/m)*100.0
    return percent_median_bmi

def measurement_from_sds(
    measurement_method: str,  
    requested_sds: float,  
    sex: str,  
    age: float, 
    born_preterm = False) -> float:
    """
    Public method
    Returns the measurement value from a given SDS.
    Parameters are: 
        measurement_method (type of observation) ["height", "weight", "bmi", "ofc"]
        decimal age (corrected or chronological),
        requested_sds
        sex (a standard string) ["male" or "female"]
        born_preterm: a boolean flag to track whether to use UK90 premature data or UK90-WHO term data for 37-42 weeks

    Centile to SDS Conversion for Chart lines (2/3 of an SDS)
    0.4th -2.67
    2nd -2.00
    9th -1.33
    25th -0.67
    50th 0
    75th 0.67
    91st 1.33
    98th 2.00
    99.6th 2.67
    """

    # Get the correct reference from the patchwork of references that make up UK-WHO
    try:
        selected_reference = uk_who_reference(age=age, born_preterm=born_preterm)
    except: # there is no reference for the age supplied
        return ValueError("There is no reference for the age supplied.")

    # Check that the measurement requested has reference data at that age
    if reference_data_absent(
        age=age, 
        reference=selected_reference, 
        measurement_method=measurement_method, 
        sex=sex):
        return ValueError("There is no reference data for this measurement at this age")

    # fetch the LMS values for the requested measurement
    lms_value_array_for_measurement = selected_reference["measurement"][measurement_method][sex]

    # get LMS values from the reference: check for age match, interpolate if none
    lms = fetch_lms(age=age, born_preterm=born_preterm, lms_value_array_for_measurement=lms_value_array_for_measurement)
    l = lms["l"]
    m = lms["m"]
    s = lms["s"]

    if l != 0.0:
        measurement_value = math.pow((1+l*s*requested_sds),1/l)*m
    else:
        measurement_value = math.exp(s*requested_sds)*m
    return measurement_value

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

"""
These functions are for testing accuracy.
Commented out but left for documentation to show process behind evaluation of each interpolation method
# """                                                                                    
# def tim_tests():
#     """
#         function to run growth data on 76 hypothetical children to test algorithm against gold standard (LMSGrowth and LMS2z function from Tim Cole R package Sitar)
#     """
#     # child_decimal_ages = [-0.249144422,-0.202600958,1.013004791,1.303216975,3.983572895,0.161533196,0.161533196,0,0.251882272,0.303901437,0.303901437,0.323066393,0.331279945,0.895277207,2.288843258,2.587268994,3.271731691,3.504449008,3.808350445,4.462696783,1.013004791,3.271731691,3.504449008,3.808350445,4.462696783,-0.095824778,0.396988364,0.793976728,1.065023956,1.330595483,1.492128679,2.280629706,2.565366188,0.396988364,0.793976728,1.065023956,0.323066393,0.380561259,0.41889117,0.676249144,0.887063655,0.898015058,1.095140315,1.45927447,1.535934292,1.708418891,1.919233402,0.380561259,0.676249144,0.887063655,1.095140315,1.45927447,1.535934292,1.708418891,1.919233402,1.327857632,1.984941821,2.691307324,2.746064339,3.244353183,3.422313484,4.164271047,4.878850103,4.955509925,5.032169747,5.278576318,5.708418891,5.935660507,6.127310062,6.412046543,1.327857632,2.691307324,4.164271047,4.878850103,5.708418891,5.935660507,6.127310062]
#     # child_sexes = ["female","female","female","female","female","male","male","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","male","male","male","male","male","male","male","male","male","male","male","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","female","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male","male"]
#     # child_measurements = ["weight","weight","height","height","height","weight","height","weight","weight","weight","height","height","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","height","height","height","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","height","height"]
#     # child_observations = [1.21,1.5,81,84.5,100.5,4.17,54.8,2.7,4.57,4.48,57,59,8.2,10.7,12.4,12.5,13.8,13.6,14.1,15.36,81,96,98,99.5,100.8,3.09,5.23,5.85,6.62,7.41,7.25,9.96,10.84,61.7,65,68.2,4.67,5.42,5.63,6.3,7.1,7.1,7.26,8.08,8.11,8.1,8.98,60,66,70.5,73.6,75.9,79.1,78.2,78.9,12.2,13.8,12.5,12.5,13.5,14.3,16,20.05,20.5,19.85,20.5,21.9,22.8,22.3,24,79.6,88,99,102.7,110,109.5,109]
#     # child_gestational_ages = [27,27,27,27,27,35,35,40,40,40,40,40,27,27,27,27,27,27,27,27,27,27,27,27,27,35,35,35,35,35,35,35,35,35,35,35,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40,40]

#     # these ages are from November 2020
#     child_decimal_ages = [5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,5.921971253,1.034907598,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283,15.39767283]
#     child_sexes = ["weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi"]
#     child_observations = [20.45,47.7,37.64,27.1,10.99,11.68,25.1,26.19,14.87,46.71,15.56,15.97,20.59,15.36,78.28,18.58,24.62,35.72,18.17,13.18,38.58,11.92,58.87,20.6,23.77,70.45,24.89,59.29,16.34,25.11,7.95,10.62,28.19,89.81,6.76,33.15,19.17,35.27,59.01,6.81,24.06,43.32,10.02,25.48,10.35,49.58,56.29,23.98,34.33,7.16,9.81,23.66,15.04,29.69,5.57,28.69,13.26,45.54,11.01,46.35,44.6,44.88,16.8,39.27,55.87,42.28,29.91,19.17,68.29,31.01,10.18,22.14,30.34,37.77,19.02,26.96,16.85,66.81,31.23,56.21,16.26,9.31,48,49.58,65.69,23.68,41.17,34.93,23.35,22.39,44.65,17.22,36.45,54.68,20.24,11.64,23.03,12.83,7.61,45.27,113.9,156.9,147.5,131.8,85.3,87,128.6,129,99.9,155.9,104,101.1,115.5,103.2,185.1,111.6,126.1,145.3,105.7,89,149.7,89.6,171.7,116.5,125.2,178.6,127.3,171,106.8,123.3,66.1,78,132.9,190.9,63.9,141.3,104.9,143.1,172,63.1,124.8,156.6,82.2,129.4,82.9,159.2,164.2,121.4,142.3,64.8,82.1,121.6,98,133.9,58.4,135.4,92.4,155.7,77.9,155.3,154.2,154.9,106.2,149.5,163.9,152.5,135.2,112.8,178.9,139.4,78.9,121.7,136.5,147.4,113.1,131.6,104.9,176.3,136.8,162.3,106.7,75.1,155,157.5,176.3,124.6,143.6,144.4,123,119.7,154,105.8,142.3,162,117.2,91,123.5,88.9,65.7,159.6,15.76325226,19.37637329,17.30077553,15.60049915,15.10426617,15.43136501,15.17720413,15.73823834,14.89978409,19.21841812,14.386096,15.62437248,15.43449402,14.42221165,22.84746361,14.9182291,15.48309803,16.91921806,16.2631588,16.63931465,17.21546173,14.84773541,19.96886826,15.17803001,15.16423607,22.08605003,15.3591814,20.27632332,14.32549286,16.51659584,18.19550705,17.45562172,15.96045017,24.64409065,16.55560303,16.60348511,17.42092133,17.22369003,19.94659233,17.10363388,15.44779205,17.66464615,14.82941723,15.21706295,15.06021977,19.56232262,20.87781143,16.27090836,16.95368195,17.05151558,14.5540123,16.00101852,15.66014099,16.55957031,16.33163071,15.64923954,15.53100491,18.78519821,18.14313889,19.21793938,18.75711632,18.70466805,14.89567566,17.57027245,20.79796028,18.18005943,16.36300278,15.06620598,21.33715057,15.95791626,16.35286331,14.94845963,16.28359413,17.38409233,14.8691206,15.56711388,15.31259918,21.49496841,16.68782616,21.33912087,14.28208733,16.50706482,19.97918892,19.98689842,21.1346302,15.2526598,19.96512222,16.75190544,15.43393421,15.62664509,18.82695389,15.38373566,18.00063133,20.83523941,14.73517323,14.05627346,15.09941196,16.23390961,17.63006592,17.7723465,52.4,53.9,52.3,52.5,46.7,47.2,52.6,53.9,49.2,53.7,48.5,51,52.2,49.9,59.1,51.7,52.5,53.2,50.7,48.8,54.7,47.1,56.8,52,52.1,52.3,57.3,50.2,53.5,42.8,47.2,52.9,60.6,41.3,54.6,52.8,55.4,56.1,41.2,52.4,52.8,45.6,51.9,46.1,54.6,55.5,53.2,55.1,42,45.2,54.3,49.9,55,39,52.3,48.3,54.1,47.6,55.2,53.3,54.5,51.1,53.4,55.8,53.3,53.3,52.2,57.7,52.2,46.3,52.3,53.2,55.3,51.7,53.4,51.1,58.3,53.6,50.1,45.3,57,52.2,57.5,54.5,53.4,52.6,54.9,51.3,56.2,55.1,51.5,46.2,52.7,49,42.5,54,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439,17.77234439]


#     final_z_list=[]
#     final_uncorrected = []
#     for i in range(len(child_decimal_ages)):
#         z = sds(child_decimal_ages[i], child_measurements[i], child_observations[i], child_sexes[i])
#         final_z_list.append(z)
#     return final_z_list

# def time_functions():
#     Used to test function run time. Needs timeit package importing also
#     return sds(-0.249144422,"weight",1.21,"female")

# def test_data():
#     array_to_add=[]
#     decimal_ages=[0.021902806,0.021902806,0.021902806,0.186173854,0.353182752,0.52019165,0.689938398,0.856947296,1.023956194,1.185489391,1.352498289,1.519507187,1.689253936,1.856262834,2.023271732,2.184804928,2.351813826,2.518822724,2.688569473,2.855578371,3.022587269,3.184120465,3.351129363,3.518138261,3.68788501,3.854893908,4.021902806,4.186173854,4.353182752,4.52019165,4.689938398,4.856947296,5.023956194,5.185489391,5.352498289,5.519507187,5.689253936,5.856262834,6.023271732,6.184804928]
#     measurement_types=["height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height"]
#     for i in range(len(decimal_ages)):
#         value = measurement_from_sds(measurement_types[i], 0.67, "male", decimal_ages[i])
#         array_to_add.append(value)
#     return array_to_add

# def run_lms_test():
#     sexes = ["female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male"]
#     ages = ages = [5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,5.921971253,1.034907598,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283]
#     measurements = ["weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc"]
#     values = [20.45,47.7,37.64,27.1,10.99,11.68,25.1,26.19,14.87,46.71,15.56,15.97,20.59,15.36,78.28,18.58,24.62,35.72,18.17,13.18,38.58,11.92,58.87,20.6,23.77,70.45,24.89,59.29,16.34,25.11,7.95,10.62,28.19,89.81,6.76,33.15,19.17,35.27,59.01,6.81,24.06,43.32,10.02,25.48,10.35,49.58,56.29,23.98,34.33,7.16,9.81,23.66,15.04,29.69,5.57,28.69,13.26,45.54,11.01,46.35,44.6,44.88,16.8,39.27,55.87,42.28,29.91,19.17,68.29,31.01,10.18,22.14,30.34,37.77,19.02,26.96,16.85,66.81,31.23,56.21,16.26,9.31,48,49.58,65.69,23.68,41.17,34.93,23.35,22.39,44.65,17.22,36.45,54.68,20.24,11.64,23.03,12.83,7.61,45.27,113.9,156.9,147.5,131.8,85.3,87,128.6,129,99.9,155.9,104,101.1,115.5,103.2,185.1,111.6,126.1,145.3,105.7,89,149.7,89.6,171.7,116.5,125.2,178.6,127.3,171,106.8,123.3,66.1,78,132.9,190.9,63.9,141.3,104.9,143.1,172,63.1,124.8,156.6,82.2,129.4,82.9,159.2,164.2,121.4,142.3,64.8,82.1,121.6,98,133.9,58.4,135.4,92.4,155.7,77.9,155.3,154.2,154.9,106.2,149.5,163.9,152.5,135.2,112.8,178.9,139.4,78.9,121.7,136.5,147.4,113.1,131.6,104.9,176.3,136.8,162.3,106.7,75.1,155,157.5,176.3,124.6,143.6,144.4,123,119.7,154,105.8,142.3,162,117.2,91,123.5,88.9,65.7,159.6,15.76325226,19.37637329,17.30077553,15.60049915,15.10426617,15.43136501,15.17720413,15.73823834,14.89978409,19.21841812,14.386096,15.62437248,15.43449402,14.42221165,22.84746361,14.9182291,15.48309803,16.91921806,16.2631588,16.63931465,17.21546173,14.84773541,19.96886826,15.17803001,15.16423607,22.08605003,15.3591814,20.27632332,14.32549286,16.51659584,18.19550705,17.45562172,15.96045017,24.64409065,16.55560303,16.60348511,17.42092133,17.22369003,19.94659233,17.10363388,15.44779205,17.66464615,14.82941723,15.21706295,15.06021977,19.56232262,20.87781143,16.27090836,16.95368195,17.05151558,14.5540123,16.00101852,15.66014099,16.55957031,15.64923954,15.53100491,18.78519821,18.14313889,19.21793938,18.75711632,18.70466805,14.89567566,17.57027245,20.79796028,18.18005943,16.36300278,15.06620598,21.33715057,15.95791626,16.35286331,14.94845963,16.28359413,17.38409233,14.8691206,15.56711388,15.31259918,21.49496841,16.68782616,21.33912087,14.28208733,16.50706482,19.97918892,19.98689842,21.1346302,15.2526598,19.96512222,16.75190544,15.43393421,15.62664509,18.82695389,15.38373566,18.00063133,20.83523941,14.73517323,14.05627346,15.09941196,16.23390961,17.63006592,17.7723465,52.4,53.9,52.3,52.5,46.7,47.2,52.6,53.9,49.2,53.7,48.5,51,52.2,49.9,59.1,51.7,52.5,53.2,50.7,48.8,54.7,47.1,56.8,52,52.1,52.3,57.3,50.2,53.5,42.8,47.2,52.9,60.6,41.3,54.6,52.8,55.4,56.1,41.2,52.4,52.8,45.6,51.9,46.1,54.6,55.5,53.2,55.1,42,45.2,54.3,49.9,55,39,52.3,48.3,54.1,47.6,55.2,53.3,54.5,51.1,53.4,55.8,53.3,53.3,52.2,57.7,52.2,46.3,52.3,53.2,55.3,51.7,53.4,51.1,58.3,53.6,50.1,45.3,57,52.2,57.5,54.5,53.4,52.6,54.9,51.3,56.2,55.1,51.5,46.2,52.7,49,42.5,54]
#     ls = []
#     ms = []
#     ss = []
#     sdss = []
#     for num, age in enumerate(ages):
#         lms = get_lms(age, measurements[num], sexes[num], False)
#         calc_sds = sds(age, measurements[num], values[num], sexes[num], False)
#         ls.append(lms["l"])
#         ms.append(lms["m"])
#         ss.append(lms["s"])
#         sdss.append(calc_sds)
#     print("ls: ")
#     print(ls)
#     print("ms: ")
#     print(ms)
#     print("ss: ")
#     print(ss)
#     print(sdss)

