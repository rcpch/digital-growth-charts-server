import pytest
from datetime import date
from ..sds_calculations import sds
from datetime import datetime
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery
from pytest import approx


#@pytest.mark.parametrize("dec_age, measurement, measure, sex, expected", [(-0.095824778, 'height', 46.1415, 'male', 0), (0, 'height', 51, 'male', 0)])
#def test_sds_calulations(dec_age, measurement, measure, sex, expected):
#   assert sds(dec_age, measurement, measure, sex, expected) == expected
accuracy = 1e-4

@pytest.mark.parametrize(
    "dec_age, measurement, measure, sex, default_to_youngest, preterm, expected", 
    [
        pytest.param(
            -0.191649555, 'height', 40.48008, 'male', True, True, approx(0, abs=accuracy), id= "Height, Boy, 30Weeks"
         ), 
        pytest.param(
            -0.191649555, 'weight', 1.436, 'male', True, True, approx(0, abs=accuracy),  id= "Weight, Boy, 30Weeks"            
        ),
        pytest.param(
            -0.191649555, 'ofc', 28.48013, 'male', True, True, approx(0, abs=accuracy),  id= "OFC, Boy, 30Weeks"            
        ),
        pytest.param(
            -0.191649555, 'height', 39.94117, 'female', True, True, approx(0, abs=accuracy), id= "Height, Girl, 30Weeks"
         ), 
        pytest.param(
            -0.191649555, 'weight', 1.3593, 'female', True, True, approx(0, abs=accuracy),  id= "Weight, Girl, 30Weeks"            
        ),
        pytest.param(
            -0.191649555, 'ofc', 28.15286, 'female', True, True, approx(0, abs=accuracy),  id= "OFC, Girl, 30Weeks"            
        ),
        pytest.param(
            0, 'height', 51, 'male', True, False,  approx(0, abs=accuracy), id="Height, Boy, Term"
        ),
        pytest.param(
            0, 'weight',3.5, 'male', True, False,  approx(0, abs=accuracy), id="Weight, Boy, Term"
        ),
 #       pytest.param(
 #           0, 'bmi', 51, 'male', True, False,  approx(0, abs=accuracy), id="BMI, Boy, Term"
 #       ),
        pytest.param(
            0, 'ofc', 35, 'male', True, False,  approx(0, abs=accuracy), id="OFC, Boy, Term"
        ),
        pytest.param(
            0, 'height', 50, 'female', True, False,  approx(0, abs=accuracy), id="Height, Girl, Term"
        ),
        pytest.param(
            0, 'weight', 3.36 , 'female', True, False,  approx(0, abs=accuracy), id="Weight, Girl, Term"
        ),
#        pytest.param(
#            0, 'bmi', 51, 'female', True, False,  approx(0, abs=accuracy), id="BMI, Girl, Term"
#        ),
        pytest.param(
            0, 'ofc', 34, 'female', True, False,  approx(0, abs=accuracy), id="OFC, Girl, Term"
        ),
        pytest.param(
            5, 'height', 109.59, 'male', True, False, approx(0, abs=accuracy),  id="Height, Boy, 5 years"
        ),
        pytest.param(
            5, 'weight', 18.633, 'male', True, False, approx(0, abs=accuracy),  id="Weight, Boy, 5 years"
        ),
        pytest.param(
            5, 'bmi', 15.547, 'male', True, False, approx(0, abs=accuracy),  id="BMI, Boy, 5 years"
        ),
        pytest.param(
            5, 'ofc', 52.747, 'male', True, False, approx(0, abs=accuracy),  id="OFC, Boy, 5 years"
        ),
        pytest.param(
            5, 'height', 108.86, 'female', True, False, approx(0, abs=accuracy),  id="Height, Girl, 5 years"
        ),
        pytest.param(
            5, 'weight', 18.299, 'female', True, False, approx(0, abs=accuracy),  id="Weight, Girl, 5 years"
        ),
        pytest.param(
            5, 'bmi',15.483, 'female', True, False, approx(0, abs=accuracy),  id="BMI, Girl, 5 years"
        ),
        pytest.param(
            5, 'ofc', 51.681, 'female', True, False, approx(0, abs=accuracy),  id="OFC, Girl, 5 years"
        ),
        pytest.param(
            1, 'height', 71.12, 'male', True, False, approx(-1.95, abs=accuracy),  id="Height, Boy, 1 years"
        ),
        pytest.param(
            1, 'height', 68.58, 'female', True, False, approx(-2.11, abs=accuracy),  id="Height, Girl, 1 years"
        ),
        pytest.param(
            1, 'weight', 9.5, 'male', True, False, approx(0, abs=accuracy),  id="OFC, Boy, 1 years"
        ),
        pytest.param(
            1, 'weight', 7.7, 'female', True, False, approx(0, abs=accuracy),  id="Weight, Girl, 1 years"
        ),
        pytest.param(
            5, 'ofc', 51.681, 'female', True, False, approx(0, abs=accuracy),  id="OFC, Girl, 5 years"
        ),
        pytest.param(
            5, 'ofc', 51.681, 'female', True, False, approx(0, abs=accuracy),  id="OFC, Girl, 5 years"
        ),
        pytest.param(
            5, 'ofc', 51.681, 'female', True, False, approx(0, abs=accuracy),  id="OFC, Girl, 5 years"
        )
    ],
)



def test_sds_calulations(dec_age, measurement, measure, sex, default_to_youngest, preterm, expected):
    assert sds(dec_age, measurement, measure, sex, default_to_youngest, preterm) == expected
