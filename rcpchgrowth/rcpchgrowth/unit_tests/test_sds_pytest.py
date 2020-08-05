import pytest
from datetime import date
from ..sds_calculations import sds
from datetime import datetime
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery



#@pytest.mark.parametrize("dec_age, measurement, measure, sex, expected", [(-0.095824778, 'height', 46.1415, 'male', 0), (0, 'height', 51, 'male', 0)])
#def test_sds_calulations(dec_age, measurement, measure, sex, expected):
#   assert sds(dec_age, measurement, measure, sex, expected) == expected


@pytest.mark.parametrize(
    "dec_age, measurement, measure, sex, default_to_youngest, preterm, expected", 
    [
        pytest.param(
            -0.191649555, 'height', 40.48008, 'male', True, True, 0, id= "Height, Boy, 30Weeks"
         ), 
        pytest.param(
            -0.191649555, 'weight', 1.436, 'male', True, True, 0,  id= "Weight, Boy, 30Weeks"            
        ),
        pytest.param(
            0, 'height', 51, 'male', True, False,  0, id="Height, Boy, Term"
        ),
        pytest.param(
            5, 'height', 109.59, 'male', True, False, 0,  id="Height, Boy, 5 years"
        )
    ],
)



def test_sds_calulations(dec_age, measurement, measure, sex, default_to_youngest, preterm, expected):
    assert sds(dec_age, measurement, measure, sex, default_to_youngest, preterm) == expected
