import math
import statistics
import scipy.stats as stats
from scipy.interpolate import interp1d
from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method
import numpy as np
from datetime import date
import json
import pkg_resources
# from .constants import TWENTY_FOUR_WEEKS_GESTATION, TWENTY_FIVE_WEEKS_GESTATION, THIRTY_SEVEN_WEEKS_GESTATION, FORTY_TWO_WEEKS_GESTATION, TERM_LOWER_THRESHOLD_LENGTH_DAYS, DECIMAL_AGES, FORTY_TWO_WEEKS_GESTATION_INDEX, TWO_YEARS_LYING_INDEX, FOUR_YEARS_WHO_INDEX
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
"""

#load the reference data
data = pkg_resources.resource_filename(__name__, "/data_tables/uk_who_0_20_preterm.json")
with open(data) as json_file:
            data = json.load(json_file)
            json_file.close()
term_data = pkg_resources.resource_filename(__name__, "/data_tables/uk_who_0_20_term.json")
with open(term_data) as json_file:
            term_data = json.load(json_file)
            json_file.close()

UK90_DATA = pkg_resources.resource_filename(__name__, "/data_tables/uk90.json")
with open(data) as json_file:
            data = json.load(json_file)
            json_file.close()
UK90_TERM_DATA = pkg_resources.resource_filename(__name__, "/data_tables/uk90_term.json")
with open(data) as json_file:
            data = json.load(json_file)
            json_file.close()
WHO_INFANTS_DATA = pkg_resources.resource_filename(__name__, "/data_tables/who_infants.json")
with open(data) as json_file:
            data = json.load(json_file)
            json_file.close()
WHO_CHILD_DATA = pkg_resources.resource_filename(__name__, "/data_tables/who_children.json")
with open(data) as json_file:
            data = json.load(json_file)
            json_file.close()

# reference decimal ages - these are now all 9dp and moved to constants.py
# decimal_ages=[-0.325804244,-0.306639288,-0.287474333,-0.268309377,-0.249144422,-0.229979466,-0.210814511,-0.191649555,-0.1724846,-0.153319644,-0.134154689,-0.114989733,-0.095824778,-0.076659822,-0.057494867,-0.038329911,-0.019164956,0,0.019164956,0.038329911,0.038329911,0.057494867,0.076659822,0.083333333,0.095824778,0.114989733,0.134154689,0.153319644,0.166666667,0.1724846,0.191649555,0.210814511,0.229979466,0.249144422,0.25,0.333333333,0.416666667,0.5,0.583333333,0.666666667,0.75,0.833333333,0.916666667,1.0,1.083333333,1.166666667,1.25,1.333333333,1.416666667,1.5,1.583333333,1.666666667,1.75,1.833333333,1.916666667,2.0,2.0,2.083333333,2.166666667,2.25,2.333333333,2.416666667,2.5,2.583333333,2.666666667,2.75,2.833333333,2.916666667,3.0,3.083333333,3.166666667,3.25,3.333333333,3.416666667,3.5,3.583333333,3.666666667,3.75,3.833333333,3.916666667,4.0,4.0,4.083,4.167,4.25,4.333,4.417,4.5,4.583,4.667,4.75,4.833,4.917,5.0,5.083,5.167,5.25,5.333,5.417,5.5,5.583,5.667,5.75,5.833,5.917,6.0,6.083,6.167,6.25,6.333,6.417,6.5,6.583,6.667,6.75,6.833,6.917,7.0,7.083,7.167,7.25,7.333,7.417,7.5,7.583,7.667,7.75,7.833,7.917,8.0,8.083,8.167,8.25,8.333,8.417,8.5,8.583,8.667,8.75,8.833,8.917,9.0,9.083,9.167,9.25,9.333,9.417,9.5,9.583,9.667,9.75,9.833,9.917,10.0,10.083,10.167,10.25,10.333,10.417,10.5,10.583,10.667,10.75,10.833,10.917,11.0,11.083,11.167,11.25,11.333,11.417,11.5,11.583,11.667,11.75,11.833,11.917,12.0,12.083,12.167,12.25,12.333,12.417,12.5,12.583,12.667,12.75,12.833,12.917,13.0,13.083,13.167,13.25,13.333,13.417,13.5,13.583,13.667,13.75,13.833,13.917,14.0,14.083,14.167,14.25,14.333,14.417,14.5,14.583,14.667,14.75,14.833,14.917,15.0,15.083,15.167,15.25,15.333,15.417,15.5,15.583,15.667,15.75,15.833,15.917,16.0,16.083,16.167,16.25,16.333,16.417,16.5,16.583,16.667,16.75,16.833,16.917,17.0,17.083,17.167,17.25,17.333,17.417,17.5,17.583,17.667,17.75,17.833,17.917,18.0,18.083,18.167,18.25,18.333,18.417,18.5,18.583,18.667,18.75,18.833,18.917,19,19.083,19.167,19.25,19.333,19.417,19.5,19.583,19.667,19.75,19.833,19.917,20.0]


#public functions
def uk_who_sds_calculation():

    # Get the correct reference from the patchwork of references that make up UK-WHO
    # uk_who_reference()

    # uk_who_measurement_lms_data(
    # measurement_method: str,
    # sex: str,
    # reference_data): sds()

    # sds()

def uk_who_reference(age: float, measurement_method: str, sex: str, born_preterm: bool = False)->List:
    # the purpose of this function is to choose the correct reference for calculation, 
    # for the UK-WHO standard, which is an unusual case because it combines two different reference sources.
    #  UK90 reference runs from 23 weeks to 20 y
    #  WHO 2006 runs from 2 weeks to 4 years
    # Returns the appropriate reference file

    # CONSTANTS RELEVANT ONLY TO UK-WHO REFERENCE-SELECTION LOGIC
    # 23 weeks is the lowest decimal age available on the UK90 charts
    UK90_REFERENCE_LOWER_THRESHOLD = ((23 * 7) - 40) / 365.25  # 23 weeks as decimal age
    UK90_TERM_REFERENCE_LOWER_THRESHOLD = ((37 * 7) - 40) / 365.25  # 37 weeks as decimal age
    UK90_TERM_REFERENCE_UPPER_THRESHOLD = ((42 * 7) - 40) / 365.25  # 42 weeks as decimal age
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
        raise ValueError("There is no reference data below 23 weeks gestation")
    elif age < UK90_TERM_REFERENCE_LOWER_THRESHOLD:
        # Below 37 weeks, the UK90 preterm data is always used
        return UK90_PRETERM_DATA

    elif age < UK_90_HIGH_CUTOFF_TERM_REFERENCES:
        # Below 42 weeks
        if born_preterm:
            # Preterm children should continue to be plotted using the preterm references
            return UK90_PRETERM_DATA
        else:
            return UK90_TERM_DATA
    
    elif age < WHO_CHILD_LOWER_THRESHOLD:
        # Children beyond 2 weeks but below 2 years are measured lying down using WHO data
        return WHO_INFANTS_DATA
        
    elif age < WHO_CHILDREN_UPPER_THRESHOLD:
        # Children beyond 2 years but below 4 years are measured standing up using WHO data
        return WHO_CHILD_DATA
    
    elif age <= 20:
        # All children 4 years and above are measured using UK90 child data
        return UK90_PRETERM_DATA

    else:
        raise ValueError("There is no reference data above the age of 20 years.")

def uk_who_measurement_lms_data(
    measurement_method: str,
    sex: str,
    reference_data):
    
    """
    Helper function which handles obtaining the correct LMS values from the reference data it is passed.
    """
    if measurement_method == 'height':
        return reference_data['measurement']['height'][sex]
        
    if measurement_method == 'weight':
        return reference_data['measurement']['weight'][sex]

    if measurement_method == 'bmi':
        return reference_data['measurement']['bmi'][sex]

    if measurement_method == 'ofc':
        return reference_data['measurement']['ofc'][sex]

def sds(age: float, measurement_method: str, measurement_value: float, sex: str, default_to_youngest_reference: bool = False, born_preterm: bool = False)->float:
    """
    Public function
    Returns a standard deviation score. 
    Parameters are: 
    a decimal age (corrected or chronological), 
    a measurement_method (type of observation) ['height', 'weight', 'bmi', 'ofc']
    measurement_value (the value is standard units) [height and ofc are in cm, weight in kg bmi in kg/m²]
    sex (a standard string) ['male' or 'female']
    default_to_youngest_reference (boolean): defaults to True. For circumstances when the age exactly matches a join between two references (or moving from lying to standing at 2y) where there are 2 ages in the reference data to choose between. Defaults to the youngest reference unless the user selects false
    born_preterm (boolean): defaults to False. If a baby is 37-42 weeks, use the uk_who_0_20_term data by default. If a baby was born preterm, the UK90 gestation specific data is used up to 42 weeks

    This function is specific to the UK-WHO data set as this is actually a blend of UK-90 and WHO 2006 references and necessarily has duplicate values.

    SDS is generated by passing the interpolated L, M and S values for age through an equation.
    Cubic interpolation is used for most values, but where ages of children are at the extremes of the growth reference,
    linear interpolation is used instead. These are:
    1. 23 weeks gestation
    2. 42 weeks gestation or 2 weeks post term delivery - the reference data here changes from UK90 to WHO 2006
    3. 2 years - children at this age stop being measured lying down and are instead measured standing, leading to a small decrease
    4. 4 years - the reference data here changes back to UK90 data
    5. 20 years - the threshold of the reference data

    Other considerations
     - Length data is not available until 25 weeks gestation, though weight date is available from 23 weeks
     - There is only BMI reference data from 2 weeks of age to aged 20y
     - Head circumference reference data is available from 23 weeks gestation to 17y in girls and 18y in boys
    """
    
    # TODO Extremes of the chart should be handled from introspection of the 
    # reference table, not hard-coded
    if age < DECIMAL_AGES[TWENTY_THREE_WEEKS_GESTATION_INDEX] or age > DECIMAL_AGES[TWENTY_YEARS_INDEX]:
        # extremes of chart
        return None

    if measurement_method == 'height':
        if age < DECIMAL_AGES[TWENTY_FIVE_WEEKS_GESTATION_INDEX]:
            return None # There is no reference data for length below 25 weeks'
    
    if measurement_method == 'bmi':
        if age < DECIMAL_AGES[TWO_WEEKS_INDEX]:
            return None # There is no BMI reference data available for BMI below 2 weeks
    
    if measurement_method == 'ofc':
        if (sex == 'male' and age > DECIMAL_AGES[EIGHTEEN_YEARS_INDEX]) or (sex == 'female' and age > DECIMAL_AGES[SEVENTEEN_YEARS_INDEX]):
            return None # There is no head circumference data available in girls over 17y or boys over 18y

    ## if this is a baby now term, use the term data set unless the child was born preterm and is now term,
    ## in which case continue to use the preterm data set
    
    if age >= DECIMAL_AGES[THIRTY_SEVEN_WEEKS_GESTATION_INDEX]  and age < DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX] and born_preterm == False:
        lms = get_term_lms(measurement_method, sex)
    else:
        try:
            lms = get_lms(age, measurement_method, sex, default_to_youngest_reference)
        except:
            raise
        
    l = lms['l']
    m = lms ['m']
    s = lms ['s']

    print(f'l: {l} m:{m} s:{s}')

    sds = z_score(l, m, s, measurement_value)
    
    return sds

def centile(z_score: float):
    """
    Converts a Z Score to a p value (2-tailed) using the SciPy library, which it returns as a percentage
    """

    centile = (stats.norm.cdf(z_score) * 100)
    return centile

def percentage_median_bmi( age: float, actual_bmi: float, sex: str)->float:

    """
    public method
    This returns a child's BMI expressed as a percentage of the median value for age and sex.
    It is used widely in the assessment of malnutrition particularly in children and young people with eating disorders.
    """
    
    age_index_one_below = nearest_age_below_index(age)

    if cubic_interpolation_possible(age, 'bmi', sex):
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

def measurement_from_sds(measurement_method: str,  requested_sds: float,  sex: str,  decimal_age: float, default_to_youngest_reference: bool = False, born_preterm = False) -> float:
    """
    Public method
    Returns the measurement value from a given SDS.
    Parameters are: 
        measurement_method (type of observation) ['height', 'weight', 'bmi', 'ofc']
        decimal age (corrected or chronological),
        requested_sds
        sex (a standard string) ['male' or 'female']
        default_to_youngest_reference (boolean): in the event of an exact age match at the threshold of a chart,
            where it is possible to choose 2 references, default will pick the youngest reference (optional)
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

    measurement_value = 0.0
    try:
        if(decimal_age < DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX] and born_preterm):
            lms= get_lms(decimal_age, measurement_method, sex, default_to_youngest_reference)
        elif(decimal_age < DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX] and born_preterm==False):
            lms=get_term_lms(measurement_method=measurement_method, sex=sex)
        else:
            # the UK90 prematurity data file is continuous to 20y and confusingly named. Any children caught here
            # will be post term and will be calculated correctly on WHO data if < 4 or UK90 if >= 4y
            lms= get_lms(decimal_age, measurement_method, sex, default_to_youngest_reference)
    except:
        raise
    else:
        l = lms['l']
        m = lms['m']
        s = lms['s']

        if l != 0.0:
            measurement_value = math.pow((1+l*s*requested_sds),1/l)*m
        else:
            measurement_value = math.exp(s*requested_sds)*m
        return measurement_value

#private methods
def nearest_age_below_index(age: float)->int:
    """
    Returns the array index of the nearest (lowest) age (or a match) in the reference data below the calculated decimal age (either chronological or corrected for gestational age)
    Uses the NumPy library to do this quickly - identifies the first incidence of a value in a sorted array.
    """
    result_index = 0
    decimal_ages_as_np_array = np.asarray(DECIMAL_AGES)
    idx = np.searchsorted(decimal_ages_as_np_array, age, side="left")
    if idx > 0 and (idx == len(DECIMAL_AGES) or math.fabs(age - DECIMAL_AGES[idx-1]) < math.fabs(age - DECIMAL_AGES[idx])):
        result = DECIMAL_AGES[idx-1]
        result_index = idx-1
    else:
        result = DECIMAL_AGES[idx]
        result_index = idx
    if result <= age:
        return result_index
    else:
        return result_index-1

def cubic_interpolation_possible(age: float, measurement_method, sex):
    """
    See sds function. This method tests if the age of the child (either corrected for prematurity or chronological) is at a threshold of the reference data
    This method is specific to the UK-WHO data set.
    Thresholds wehere cubic interpolation is not possible:
    - Start of viability: [-0.325804244,-0.306639288....], indices are 0, 1
    - Threshold of UK90 term data and start of WHO data at 2 weeks of age (42 weeks): [...0,0.019164956,0.038329911,0.038329911,0.057494867...], indices are 17, 18, 19, 20, 21
    - Threshold at 2 years [1.916666667,2.0,2.0,2.083333333] - this is the same data set but children are measured standing not lying > 2y, indices 54, 55, 56, 57
    - Threshold of WHO 2006 data at 4y and reverts to UK90: [...3.916666667,4.0,4.0,4.083...], indices 79, 80, 81, 82
    - End of UK90 data set at 20y: [...19.917,20.0], indices 272, 273
    - Height in boys and girls below 27 weeks (no data below 25 weeks) [-0.2683093771] index 3
    - BMI in boys and girls below 4 weeks (no data below 2 weeks) [0.07665982204] index 22
    - OFC in boys > 17.917y index 248 (no data over 18y) or in girls > 16.917y index 236 (no data over 17y)
    """
    if (
        age <= DECIMAL_AGES[TWENTY_FOUR_WEEKS_GESTATION_INDEX] or 
        (age > DECIMAL_AGES[FORTY_ONE_WEEKS_GESTATION_INDEX] and age < DECIMAL_AGES[THREE_WEEKS_INDEX]) or 
        (age > DECIMAL_AGES[PENULTIMATE_TWO_YEARS_LYING_INDEX] and age < DECIMAL_AGES[SECOND_FOLLOWING_TWO_YEARS_STANDING_INDEX]) or 
        (age > DECIMAL_AGES[PENULTIMATE_FOUR_YEARS_WHO_INDEX] and age < DECIMAL_AGES[SECOND_FOLLOWING_FOUR_YEARS_UK90_INDEX]) or 
        age > DECIMAL_AGES[PENULTIMATE_TWENTY_YEARS_UK90_INDEX] or 
        (age < DECIMAL_AGES[TWENTY_SIX_WEEKS_GESTATION_INDEX] and measurement_method == 'height') or 
        (age < DECIMAL_AGES[THREE_WEEKS_INDEX] and measurement_method == 'bmi') or 
        (age > DECIMAL_AGES[PENULTIMATE_EIGHTEEN_YEARS_INDEX] and measurement_method == 'ofc' and sex=='male') or 
        (age > DECIMAL_AGES[PENULTIMATE_SEVENTEEN_YEARS_INDEX] and measurement_method == 'ofc' and sex=='female')
    ):
        return False
    else:
        return True

def get_term_lms(measurement_method: str, sex: str):
    """
    For babies at 37-42 weeks not preterm, L, M, S are averaged across the 5 weeks. For babies born preterm
    but are now term gestation, this method is not called and the UK90 preterm data is used upto 42 weeks
    """
    l = term_data['measurement'][measurement_method][sex][0]["L"]
    m = term_data['measurement'][measurement_method][sex][0]["M"]
    s = term_data['measurement'][measurement_method][sex][0]["S"]

    lms = {
            'l': l,
            'm': m,
            's': s
        }
    return lms


def get_lms(age: float, measurement_method: str, sex: str, default_to_youngest_reference: bool = False)->list:
    """
    Returns an interpolated L, M and S value as an array [l, m, s] against a decimal age, sex and measurement_method

    default_to_youngest_reference (boolean): in the event of an exact age match at the threshold of a chart,
            where it is possible to choose 2 references, default will pick the oldest reference (optional)
            eg at exactly 2 y, the function will therefore always select UK-WHO child and not infant data, unless
            this flag specifies otherwise
    """
    
    try:
        #this child is < or > the extremes of the chart
        assert (age >= DECIMAL_AGES[0] or age <= DECIMAL_AGES[-1]), 'Cannot be younger than 23 weeks or older than 20y'
    except IndexError as chart_extremes_msg:
        print(chart_extremes_msg)
    
    if measurement_method == 'height':
        if age < DECIMAL_AGES[TWENTY_FIVE_WEEKS_GESTATION_INDEX]:
            raise ValueError(f'There is no reference data for length below 25 weeks ({DECIMAL_AGES[TWENTY_FIVE_WEEKS_GESTATION_INDEX]} y)')
    
    if measurement_method == 'bmi':
        if age < DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX]:
            raise ValueError(f'There is no BMI reference data available for BMI below 2 weeks ({DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX]} y)')
    
    if measurement_method == 'ofc':
        if (sex == 'male' and age > DECIMAL_AGES[EIGHTEEN_YEARS_INDEX]) or (sex == 'female' and age > DECIMAL_AGES[SEVENTEEN_YEARS_INDEX]):
            raise ValueError('There is no head circumference data available in girls over 17y or boys over 18y')

    age_index_one_below = nearest_age_below_index(age)
    if age == DECIMAL_AGES[age_index_one_below]:
        """
        child's age matches a reference age - no interpolation necessary
        defaults to the highest reference if at reference threshold
        unless default_to_youngest_reference is false
        or bmi at 2 weeks of age is requested as no data at 42 weeks gestation
        """

        # age_matches = [0.038329911, 2.0, 4.0]
        lower_index = [FORTY_TWO_WEEKS_GESTATION_INDEX, TWO_YEARS_LYING_INDEX, FOUR_YEARS_WHO_INDEX]
        # upper_index = [20, 56, 81]

        if (age_index_one_below in lower_index) and (default_to_youngest_reference == False):
            age_index_one_below = age_index_one_below + 1


        """
        NB: if age == 0.038329911 (2 weeks of age) and we are requesting BMI, must start at 
        WHO ref data. This is index 20, not 19
        """
        if measurement_method == 'bmi' and age_index_one_below == 19:
            age_index_one_below = 20

        l = data['measurement'][measurement_method][sex][age_index_one_below]["L"]
        m = data['measurement'][measurement_method][sex][age_index_one_below]["M"]
        s = data['measurement'][measurement_method][sex][age_index_one_below]["S"]
        lms = {
            'l': l,
            'm': m,
            's': s
        }
        return lms
        

    if cubic_interpolation_possible(age, measurement_method, sex):
        #collect all L, M and S above and below lower age index for cubic interpolation
        l_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["L"]
        m_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["M"]
        s_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["S"]

        l_two_below = data['measurement'][measurement_method][sex][age_index_one_below-1]["L"]
        m_two_below = data['measurement'][measurement_method][sex][age_index_one_below-1]["M"]
        s_two_below = data['measurement'][measurement_method][sex][age_index_one_below-1]["S"]

        l_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["L"]
        m_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["M"]
        s_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["S"]

        l_two_above = data['measurement'][measurement_method][sex][age_index_one_below+2]["L"]
        m_two_above = data['measurement'][measurement_method][sex][age_index_one_below+2]["M"]
        s_two_above = data['measurement'][measurement_method][sex][age_index_one_below+2]["S"]
        
        l = cubic_interpolation(age, age_index_one_below, l_two_below, l_one_below, l_one_above, l_two_above)
        m = cubic_interpolation(age, age_index_one_below, m_two_below, m_one_below, m_one_above, m_two_above)
        s = cubic_interpolation(age, age_index_one_below, s_two_below, s_one_below, s_one_above, s_two_above)
    else:
        #a chart threshold: collect one L, M and S above and below lower age index for linear interpolation
        l_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["L"]
        m_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["M"]
        s_one_below = data['measurement'][measurement_method][sex][age_index_one_below]["S"]

        l_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["L"]
        m_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["M"]
        s_one_above = data['measurement'][measurement_method][sex][age_index_one_below+1]["S"]

        l = linear_interpolation(age, age_index_one_below, l_one_below, l_one_above)
        m = linear_interpolation(age, age_index_one_below, m_one_below, m_one_above)
        s = linear_interpolation(age, age_index_one_below, s_one_below, s_one_above)
    # print(f"actual age: {age} l,m,s interpolated: {l} {m} {s} ") #debugging as accuracy currently uncertain 
    # print(f"2 lower: {l_two_below} {m_two_below} {s_two_below}")
    # print(f"1 lower: {l_one_below} {m_one_below} {s_one_below}")
    # print(f"1 above: l: {l_one_above} m:{m_one_above} s:{s_one_above}")
    # print(f"2 above: l: {l_two_above} m:{m_two_above} s:{s_two_above}")
    # print(f"{l}, {m}, {s}")
    lms = {
        'l': l,
        'm': m,
        's': s
        }
    return lms

def cubic_interpolation( age: float, age_index_below: int, parameter_two_below: float, parameter_one_below: float, parameter_one_above: float, parameter_two_above: float) -> float:

    """
    See sds function. This method tests if the age of the child (either corrected for prematurity or chronological) is at a threshold of the reference data
    This method is specific to the UK-WHO data set.
    """

    cubic_interpolated_value = 0.0

    t = 0.0 #actual age ///This commented function is Tim Cole's used in LMSGrowth to perform cubic interpolation - 50000000 loops, best of 5: 7.37 nsec per loop
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

    age_two_below = DECIMAL_AGES[age_index_below-1]
    age_one_below = DECIMAL_AGES[age_index_below]
    age_one_above = DECIMAL_AGES[age_index_below+1]
    age_two_above = DECIMAL_AGES[age_index_below+2]
    
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
    # xpoints = [DECIMAL_AGES[age_index_below-1], DECIMAL_AGES[age_index_below], DECIMAL_AGES[age_index_below+1], DECIMAL_AGES[age_index_below+2]]
    # ypoints = [parameter_two_below, parameter_one_below, parameter_one_above, parameter_two_above]

    # this is the scipy cubic spline interpolation function...
    # cs = CubicSpline(xpoints,ypoints,bc_type='natural')
    # cubic_interpolated_value = cs(age) # this also works, but not as accurate: 50000000 loops, best of 5: 7.42 nsec per loop

    # this is the scipy splrep function
    # tck = interpolate.splrep(xpoints, ypoints)
    # cubic_interpolated_value = interpolate.splev(age, tck)   #Matches Tim Cole's for accuracy but slower: speed - 50000000 loops, best of 5: 7.62 nsec per loop

    return cubic_interpolated_value

def linear_interpolation( decimal_age: float, age_index_below: int, parameter_one_below: float, parameter_one_above: float) -> float:

    """
    See sds function. This method is to do linear interpolation of L, M and S values for children whose ages are at the threshold of the reference data, making cubic interpolation impossible
    """
    
    linear_interpolated_value = 0.0
    age_below = DECIMAL_AGES[age_index_below]
    age_above = DECIMAL_AGES[age_index_below+1]
    # linear_interpolated_value = parameter_one_above + (((decimal_age - age_below)*parameter_one_above-parameter_one_below))/(age_above-age_below)
    x_array = [age_below, age_above]
    y_array = [parameter_one_below, parameter_one_above]
    intermediate = interp1d(x_array, y_array)
    linear_interpolated_value = intermediate(decimal_age)
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
#     return sds(-0.249144422,'weight',1.21,'female')

# def test_data():
#     array_to_add=[]
#     decimal_ages=[0.021902806,0.021902806,0.021902806,0.186173854,0.353182752,0.52019165,0.689938398,0.856947296,1.023956194,1.185489391,1.352498289,1.519507187,1.689253936,1.856262834,2.023271732,2.184804928,2.351813826,2.518822724,2.688569473,2.855578371,3.022587269,3.184120465,3.351129363,3.518138261,3.68788501,3.854893908,4.021902806,4.186173854,4.353182752,4.52019165,4.689938398,4.856947296,5.023956194,5.185489391,5.352498289,5.519507187,5.689253936,5.856262834,6.023271732,6.184804928]
#     measurement_types=["height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height","weight","ofc","height"]
#     for i in range(len(decimal_ages)):
#         value = measurement_from_sds(measurement_types[i], 0.67, 'male', decimal_ages[i])
#         array_to_add.append(value)
#     return array_to_add

def run_lms_test():
    sexes = ["female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","male","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male","female","female","female","female","female","female","male","male","male","female","male","female","female","female","male","male","female","female","female","female","male","female","male","female","female","female","male","female","female","female","male","female","male","female","male","male","male","male","male","female","male","female","female","female","female","female","female","male","male","female","male","male","male","female","female","female","female","male","female","female","female","male","female","female","female","female","male","male","female","female","male","female","male","male","male","female","male","female","female","female","male","female","male","male","male","female","female","female","male","female","male","female","male","male","female","male"]
    ages = ages = [5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,19.14579055,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,19.33196441,5.921971253,1.034907598,19.86036961,17.01848049,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283,5.467488022,15.61396304,14.14921287,9.921971253,1.700205339,2.168377823,9.344284736,8.216290212,3.906913073,15.69062286,6.674880219,4.005475702,5.976728268,5.25119781,17.26214921,6.045174538,8.281998631,12.38877481,3.764544832,1.593429158,12.70362765,2.694045175,15.00616016,6.477754962,8.531143053,8.810403833,14.23134839,5.864476386,6.6091718,0.366872005,1.013004791,9.59890486,17.93839836,0.443531828,10.57357974,3.017111567,10.28610541,16.40520192,0.298425736,7.997262149,16.13141684,2.034223135,10.01505818,1.568788501,14.52429843,15.27994524,6.390143737,10.40383299,0.394250513,2.165639973,6.40109514,3.126625599,8.429842574,-0.016427105,11.14579055,2.622861054,13.99315537,0.709103354,12.22176591,15.33196441,13.02395619,5.297741273,13.2019165,13.83983573,14.28062971,9.727583847,6.01779603,16.55578371,12.37508556,1.267624914,7.822039699,10.22039699,11.54551677,6.36550308,9.273100616,4.643394935,14.33538672,9.744010951,5.921971253,1.034907598,17.95208761,8.194387406,8.574948665,11.72073922,7.318275154,6.631074606,12.33675565,4.700889802,9.368925394,16.78302533,7.441478439,3.466119097,7.92881588,1.932922656,0.405201916,15.39767283]
    measurements = ["weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","weight","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","height","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","bmi","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc","ofc"]
    values = [20.45,47.7,37.64,27.1,10.99,11.68,25.1,26.19,14.87,46.71,15.56,15.97,20.59,15.36,78.28,18.58,24.62,35.72,18.17,13.18,38.58,11.92,58.87,20.6,23.77,70.45,24.89,59.29,16.34,25.11,7.95,10.62,28.19,89.81,6.76,33.15,19.17,35.27,59.01,6.81,24.06,43.32,10.02,25.48,10.35,49.58,56.29,23.98,34.33,7.16,9.81,23.66,15.04,29.69,5.57,28.69,13.26,45.54,11.01,46.35,44.6,44.88,16.8,39.27,55.87,42.28,29.91,19.17,68.29,31.01,10.18,22.14,30.34,37.77,19.02,26.96,16.85,66.81,31.23,56.21,16.26,9.31,48,49.58,65.69,23.68,41.17,34.93,23.35,22.39,44.65,17.22,36.45,54.68,20.24,11.64,23.03,12.83,7.61,45.27,113.9,156.9,147.5,131.8,85.3,87,128.6,129,99.9,155.9,104,101.1,115.5,103.2,185.1,111.6,126.1,145.3,105.7,89,149.7,89.6,171.7,116.5,125.2,178.6,127.3,171,106.8,123.3,66.1,78,132.9,190.9,63.9,141.3,104.9,143.1,172,63.1,124.8,156.6,82.2,129.4,82.9,159.2,164.2,121.4,142.3,64.8,82.1,121.6,98,133.9,58.4,135.4,92.4,155.7,77.9,155.3,154.2,154.9,106.2,149.5,163.9,152.5,135.2,112.8,178.9,139.4,78.9,121.7,136.5,147.4,113.1,131.6,104.9,176.3,136.8,162.3,106.7,75.1,155,157.5,176.3,124.6,143.6,144.4,123,119.7,154,105.8,142.3,162,117.2,91,123.5,88.9,65.7,159.6,15.76325226,19.37637329,17.30077553,15.60049915,15.10426617,15.43136501,15.17720413,15.73823834,14.89978409,19.21841812,14.386096,15.62437248,15.43449402,14.42221165,22.84746361,14.9182291,15.48309803,16.91921806,16.2631588,16.63931465,17.21546173,14.84773541,19.96886826,15.17803001,15.16423607,22.08605003,15.3591814,20.27632332,14.32549286,16.51659584,18.19550705,17.45562172,15.96045017,24.64409065,16.55560303,16.60348511,17.42092133,17.22369003,19.94659233,17.10363388,15.44779205,17.66464615,14.82941723,15.21706295,15.06021977,19.56232262,20.87781143,16.27090836,16.95368195,17.05151558,14.5540123,16.00101852,15.66014099,16.55957031,15.64923954,15.53100491,18.78519821,18.14313889,19.21793938,18.75711632,18.70466805,14.89567566,17.57027245,20.79796028,18.18005943,16.36300278,15.06620598,21.33715057,15.95791626,16.35286331,14.94845963,16.28359413,17.38409233,14.8691206,15.56711388,15.31259918,21.49496841,16.68782616,21.33912087,14.28208733,16.50706482,19.97918892,19.98689842,21.1346302,15.2526598,19.96512222,16.75190544,15.43393421,15.62664509,18.82695389,15.38373566,18.00063133,20.83523941,14.73517323,14.05627346,15.09941196,16.23390961,17.63006592,17.7723465,52.4,53.9,52.3,52.5,46.7,47.2,52.6,53.9,49.2,53.7,48.5,51,52.2,49.9,59.1,51.7,52.5,53.2,50.7,48.8,54.7,47.1,56.8,52,52.1,52.3,57.3,50.2,53.5,42.8,47.2,52.9,60.6,41.3,54.6,52.8,55.4,56.1,41.2,52.4,52.8,45.6,51.9,46.1,54.6,55.5,53.2,55.1,42,45.2,54.3,49.9,55,39,52.3,48.3,54.1,47.6,55.2,53.3,54.5,51.1,53.4,55.8,53.3,53.3,52.2,57.7,52.2,46.3,52.3,53.2,55.3,51.7,53.4,51.1,58.3,53.6,50.1,45.3,57,52.2,57.5,54.5,53.4,52.6,54.9,51.3,56.2,55.1,51.5,46.2,52.7,49,42.5,54]
    ls = []
    ms = []
    ss = []
    sdss = []
    for num, age in enumerate(ages):
        lms = get_lms(age, measurements[num], sexes[num], False)
        calc_sds = sds(age, measurements[num], values[num], sexes[num], False)
        ls.append(lms['l'])
        ms.append(lms['m'])
        ss.append(lms['s'])
        sdss.append(calc_sds)
    print('ls: ')
    print(ls)
    print('ms: ')
    print(ms)
    print('ss: ')
    print(ss)
    print(sdss)

