"""
Utilities router
"""
# standard library imports

# Third party imports
from fastapi import APIRouter, HTTPException

# RCPCH imports
from rcpchgrowth import sds_for_measurement, constants, centile
from rcpchgrowth.global_functions import measurement_from_sds
from rcpchgrowth.chart_functions import create_chart
from rcpchgrowth import lower_and_upper_limits_of_expected_height_z, mid_parental_height_z
from schemas import MidParentalHeightRequest, MidParentalHeightResponse
from .utils import format_error

# set up the API router
utilities = APIRouter(
    prefix="/utilities",
)


@utilities.post(
    "/mid-parental-height", tags=["utilities"], response_model=MidParentalHeightResponse
)
def mid_parental_height_endpoint(mid_parental_height_request: MidParentalHeightRequest):
    """
    ## Mid-parental-height Endpoint

    * Calculates mid-parental-height
    * Returns mid-parental centile and SDS, as well as centile lines for mid-parental height
    * and +2 SD and -SD

    Note any paternal height above 253cm or maternal height above 250cm in a boy or
    any maternal height above 237 cm or any paternal height above 249 cm in a girl will return
    a midparental height whose centile is 100 which generates an error when calculating a plottable centile
    (since 100% is not technically plottable)
    Given that the tallest woman ever to live is Rumeysa Gelgi (born 1979) is 215.16 cm
    and the tallest man was 272 cm it seems reasonable to cap the upper limit for validation purposes
    to 245 cm in either parent (which is over 8 foot).

    if this function is called outside of the API and heights above those detailed above are higher,
    an empty array for that centile is returned. This is likely not compatible with the charting component
    as it will not be possible to render the area between the centiles if one is empty.
    """

    reference = mid_parental_height_request.reference
    adult_age = 20
    if reference == constants.WHO:
        adult_age = 19

    """
    ## Calculate SDS and centile
    """
    mph = None
    mph_sds = None
    mph_centile = None
    upper_height = None
    lower_height = None
    mph_centile_data = None
    mph_lower_centile_data = None
    mph_upper_centile_data = None

    try:
        maternal_height_sds = sds_for_measurement(age=20, measurement_method=constants.HEIGHT, observation_value=mid_parental_height_request.height_maternal, sex='female', reference=mid_parental_height_request.reference)
        paternal_height_sds = sds_for_measurement(age=20, measurement_method=constants.HEIGHT, observation_value=mid_parental_height_request.height_paternal, sex='male', reference=mid_parental_height_request.reference)
    except Exception as e:
        raise Exception(f"Error: {e}")
    
    if paternal_height_sds < -8 or maternal_height_sds < -8 or paternal_height_sds > 8 or maternal_height_sds > 8:
        errors = []
        if paternal_height_sds < -8:
            err = ("Error: The paternal height is < -8 SD. Please check the accuracy of the paternal height and try again.")
            field = "height_paternal"
            errors.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input=field))
        if maternal_height_sds < -8:
            err = ("Error: The maternal height is < -8 SD. Please check the accuracy of the maternal height and try again.")
            field = "height_maternal"
            errors.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input=field))
        if paternal_height_sds > 8:
            err = ("Error: The paternal height is > 8 SD. Please check the accuracy of the paternal height and try again.")
            field = "height_paternal"
            errors.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input=field))
        if maternal_height_sds > 8:
            err = ("Error: The maternal height is > 8 SD. Please check the accuracy of the maternal height and try again.")
            field = "height_maternal"
            errors.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input=field))
        
        raise HTTPException(status_code=422, detail=errors)

    try:
        mph_sds = mid_parental_height_z(paternal_height=mid_parental_height_request.height_paternal, maternal_height=mid_parental_height_request.height_maternal, reference=reference)
    except Exception as e:
        e = f"It was not possible to calculate a centile from the midparental height SDS: {e}"
        errors.append(format_error(loc=["body"], msg=str(e), error_type="value_error", input='height_paternal'))
        errors.append(format_error(loc=["body"], msg=str(e), error_type="value_error", input='height_maternal'))
        raise HTTPException(status_code=422, detail=f"Error: {e}")

    try:
        mph_centile = round(centile(mph_sds),3)
    except Exception as e:
        e = f"It was not possible to calculate a centile from the midparental height SDS: {e}"
        errors.append(format_error(loc=["body"], msg=str(e), error_type="value_error", input='height_paternal'))
        errors.append(format_error(loc=["body"], msg=str(e), error_type="value_error", input='height_maternal'))
        raise HTTPException(status_code=422, detail=f"Error: {e}")

    try:
        mph_centile_data = create_chart(
            reference=reference,
            centile_format=[mph_sds],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
            is_sds=True,
        )
    except Exception as e:
        print(e)
        mph_centile_data = []

    lower, upper = lower_and_upper_limits_of_expected_height_z(mid_parental_height_z=mph_sds)

    try:
        mph_lower_centile_data = create_chart(
            reference=reference,
            centile_format=[lower],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
            is_sds=True,
        )
    except Exception as e:
        # if the centile is not plottable, return an empty array
        print(f"Error: {e}")
        mph_lower_centile_data = []

    try:
        mph_upper_centile_data = create_chart(
            reference=reference,
            centile_format=[upper],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
            is_sds=True,
        )
    except Exception as e:
        mph_upper_centile_data = []
        print(f"Error: {e}")

    try:
        upper_height = measurement_from_sds(
            reference=reference,
            age=adult_age,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=upper,
        )
        lower_height = measurement_from_sds(
            reference=reference,
            age=adult_age,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=lower,
        )
    except Exception as e:
        print(e)
    
    # This is not quite the same as mid-parental height, but it is the target height for the child, and is related to mid-parental height sds * 0.5 and then converted to a measurement
    # It is present in the package but not included in the API response as it might break the charting component and so shoudl be included in future versions of the API and the charting component
    target_height = measurement_from_sds( 
            reference=reference,
            age=adult_age,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=mph_sds,
        )
    # Note this is not the same as the mid-parental height as calculated in the standard way (i.e. the mean of the parents' heights), but instead 
    # takes the means of the z-scores of the parents' heights and applies the regression coefficient of 0.5 - simplifed: (MatHtz +PatHtz)/4. This is then converted to a measurement
    # It has the effect of correcting for the fact that the children of taller parents are not as tall as their parents, and the children of  shorter parents are not as short as their parents, but regress to the mean.
    mph = measurement_from_sds(
            reference=reference,
            age=adult_age,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=mph_sds,
        )

    return {
        "mid_parental_height": mph,
        "mid_parental_height_sds": mph_sds,
        "mid_parental_height_centile": mph_centile,
        "mid_parental_height_centile_data": mph_centile_data,
        "mid_parental_height_lower_centile_data": mph_lower_centile_data,
        "mid_parental_height_upper_centile_data": mph_upper_centile_data,
        "mid_parental_height_lower_value": round(lower_height, 2),
        "mid_parental_height_upper_value": round(upper_height, 2),
    }
