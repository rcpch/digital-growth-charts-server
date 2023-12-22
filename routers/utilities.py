"""
Utilities router
"""

# Third party imports
from fastapi import APIRouter

# RCPCH imports
from rcpchgrowth import mid_parental_height, sds_for_measurement, constants, centile
from rcpchgrowth.constants.reference_constants import UK_WHO
from rcpchgrowth.global_functions import measurement_from_sds
from rcpchgrowth.chart_functions import create_chart
from schemas import MidParentalHeightRequest, MidParentalHeightResponse

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

    height = mid_parental_height(
        mid_parental_height_request.height_paternal,
        mid_parental_height_request.height_maternal,
        mid_parental_height_request.sex,
    )

    """
    ## Calculate SDS and centile
    """
    mph_sds = None
    mph_centile = None
    upper_height = None
    lower_height = None
    mph_centile_data = None
    mph_lower_centile_data = None
    mph_upper_centile_data = None
    try:
        mph_sds = sds_for_measurement(
            reference=constants.UK_WHO,
            age=20.0,
            measurement_method=constants.HEIGHT,
            observation_value=height,
            sex=mid_parental_height_request.sex,
        )

    except Exception:
        print("It was not possible to calculate midparental SDS.")

    try:
        mph_centile = centile(mph_sds)
    except:
        print("It was not possible to calculate a centile from midparental height.")

    try:
        mph_centile_data = create_chart(
            reference=UK_WHO,
            centile_format=[mph_centile],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
        )
    except Exception as e:
        print(e)
        mph_centile_data = []

    try:
        lower_centile = centile(mph_sds - 2)
        mph_lower_centile_data = create_chart(
            reference=UK_WHO,
            centile_format=[lower_centile],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
        )

    except Exception as e:
        print(e)
        mph_lower_centile_data = []

    try:
        upper_centile = centile(mph_sds + 2)

        mph_upper_centile_data = create_chart(
            reference=UK_WHO,
            centile_format=[upper_centile],
            measurement_method=constants.HEIGHT,
            sex=mid_parental_height_request.sex,
        )

    except Exception as e:
        mph_upper_centile_data = []
        print(f"Error: {e}")

    try:
        upper_height = measurement_from_sds(
            reference=constants.UK_WHO,
            age=20,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=mph_sds + 2,
        )
        lower_height = measurement_from_sds(
            reference=constants.UK_WHO,
            age=20,
            sex=mid_parental_height_request.sex,
            measurement_method=constants.HEIGHT,
            requested_sds=mph_sds - 2,
        )
    except Exception as e:
        print(e)

    return {
        "mid_parental_height": height,
        "mid_parental_height_sds": mph_sds,
        "mid_parental_height_centile": mph_centile,
        "mid_parental_height_centile_data": mph_centile_data,
        "mid_parental_height_lower_centile_data": mph_lower_centile_data,
        "mid_parental_height_upper_centile_data": mph_upper_centile_data,
        "mid_parental_height_lower_value": lower_height,
        "mid_parental_height_upper_value": upper_height,
    }
