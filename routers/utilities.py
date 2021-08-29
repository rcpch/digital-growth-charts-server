"""
Utilities router
"""

# Third party imports
from fastapi import APIRouter

# RCPCH imports
from rcpchgrowth import mid_parental_height
from schemas import MidParentalHeightRequest

# set up the API router
utilities = APIRouter(
    prefix="/utilities",
)


@utilities.post('/mid-parental-height')
def mid_parental_height_endpoint(mid_parental_height_request: MidParentalHeightRequest):
    """
    ## Mid-parental-height Endpoint

    * Calculates mid-parental-height
    """
    height = mid_parental_height(mid_parental_height_request.height_paternal, 
                                 mid_parental_height_request.height_maternal, 
                                 mid_parental_height_request.sex)
    return height


