import math
import scipy.stats as stats
from scipy.interpolate import interp1d
# from scipy import interpolate  #see below, comment back in if swapping interpolation method
# from scipy.interpolate import CubicSpline #see below, comment back in if swapping interpolation method

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
    if l != 0.0:
        measurement_value = math.pow((1+l*s*z),1/l)*m
    else:
        measurement_value = math.exp(s*z)*m
    return measurement_value
    