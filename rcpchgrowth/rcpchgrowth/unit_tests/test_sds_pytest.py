import pytest
from datetime import date
from ..sds_calculations import sds
from datetime import datetime
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery



#@pytest.mark.parametrize("dec_age, measurement, measure, sex, expected", [(-0.095824778, 'height', 46.1415, 'male', 0), (0, 'height', 51, 'male', 0)])
#def test_sds_calulations(dec_age, measurement, measure, sex, expected):
#   assert sds(dec_age, measurement, measure, sex, expected) == expected


@pytest.mark.parametrize(
    "dec_age, measurement, measure, sex, expected", 
    [
        pytest.param(
            -0.095824778, 'height', 46.1415, 'male', 0, id= "Height, Boy, 30Weeks"
        ), 
        pytest.param(
            0, 'height', 51, 'male', 0, id="Height, Boy, Term"
        ),
    ],
)



def test_sds_calulations(dec_age, measurement, measure, sex, expected):
    assert sds(dec_age, measurement, measure, sex, expected) == expected
