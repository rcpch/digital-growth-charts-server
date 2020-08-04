import pytest
from datetime import date
from ..sds_calculations import sds
from datetime import datetime
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery


# @pytest.mark.parametrize("test_input,expected", [("3+5", 8), ("2+4", 6), ("6*9", 42)])
# def test_eval(test_input, expected):
#    assert eval(test_input) == expected


@pytest.mark.parametrize("dec_age, measurement, measure, sex, expected", [(-0.095824778, 'height', 46.1415, 'male', 0), (0, 'height', 51, 'male', 0)])
def test_sds_calulations(dec_age, measurement, measure, sex, expected):
    assert sds(dec_age, measurement, measure, sex, expected) == expected
