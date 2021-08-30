"""
Utilities router
"""

# Third party imports
from fastapi import APIRouter

# RCPCH imports
from rcpchgrowth import mid_parental_height, sds_for_measurement, constants, centile
from schemas import MidParentalHeightRequest

# set up the API router
utilities = APIRouter(
    prefix="/utilities",
)


@utilities.post('/mid-parental-height', tags=['utilities'])
def mid_parental_height_endpoint(mid_parental_height_request: MidParentalHeightRequest):
    """
    ## Mid-parental-height Endpoint

    * Calculates mid-parental-height
    """
    height = mid_parental_height(mid_parental_height_request.height_paternal, 
                                 mid_parental_height_request.height_maternal, 
                                 mid_parental_height_request.sex)

    
    """
    ## Calculate SDS and centile
    """
    mph_sds = None
    mph_centile = None
    try:
        mph_sds = sds_for_measurement(
                reference=constants.UK_WHO,
                age=20.0,
                measurement_method=constants.HEIGHT, 
                observation_value=height, 
                sex=mid_parental_height_request.sex
            )
    except Exception:
        print("It was not possible to calculate midparental SDS.")

    try:
        mph_centile = centile(mph_sds)
    except:
        print("It was not possible to calculate a centile from midparental height.")

    return {
        "mid_parental_height": height,
        "mid_parental_height_sds": mph_sds,
        "mid_parental_height_centile": mph_centile
    }
