import pytest
import json
from datetime import date
from rcpchgrowth import Measurement
from datetime import datetime
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery
from pytest import approx


accuracy = 1e-4

""""@pytest.mark.parametrize(
    "birth_date', 'observation_date', 'gestation_weeks', 'gestation_days', 'sex', 'measurement_type', 'measurement_value, expected", 
    [
        pytest.param(
            '2020-01-01', '2020-01-01', 'height', 40.48008, 'male', True, True, approx(0, abs=accuracy), id= "Height, Boy, 30Weeks"
         )
    ],
)
"""



""" def load_params_from_json(json_load):
    with open("rcpchgrowth/rcpchgrowth/unit_tests/test_values.json") as f:
        return json.load(f)
def pytest_generate_tests(metafunc):
    with open("rcpchgrowth/rcpchgrowth/unit_tests/test_values.json",'r') as f:
        obj = json.load(f)
        metafunc.parametrize("param", obj)
 """

@pytest.mark.parametrize(
    "birth_date, observation_date, gestation_weeks, gestation_days, sex, measurement_method, observation_value, expected", 
    [
        pytest.param(
            date(2015, 12, 7), date(2016,11,16), 27, 2, 'female', 'weight', 7.27, 0 , id= "Height, Boy, 30Weeks"

        )
    ]
)


def test_measurement(birth_date, observation_date, gestation_weeks, gestation_days, sex, measurement_method, observation_value, expected):
    measurement_object = Measurement(
        sex=sex,
        birth_date=birth_date,
        observation_date=observation_date,
        measurement_method=measurement_method,
        observation_value=float(observation_value),
        gestation_weeks=gestation_weeks,
        gestation_days=gestation_days,
        default_to_youngest_reference=False
    )

    assert measurement_object.measurement == expected