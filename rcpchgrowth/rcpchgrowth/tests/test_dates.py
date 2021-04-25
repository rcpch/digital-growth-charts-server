"""
Date processing tests
"""

# standard imports
from datetime import date

# third party imports
import pytest

# rcpch imports
from ..date_calculations import (chronological_decimal_age,
                                 corrected_decimal_age, estimated_date_delivery)


@pytest.mark.parametrize("birth_date,observation_date,expected_decimal_age",
                         [
                             pytest.param(date(2009, 4, 1), date(
                                 2010, 2, 19), 0.8870636550308009,
                                 id="baby under a year born at term"),
                             pytest.param(date(2009, 1, 3), date(
                                 2011, 10, 3), 2.746064339493498,
                                 id="child over two born at term"),
                             pytest.param(date(2009, 1, 3), date(
                                 2013, 11, 20), 4.878850102669404,
                                 id="child over four born at term"),
                             pytest.param(date(2010, 12, 3), date(
                                 2010, 12, 20), 0.04654346338124572,
                                 id="baby over 32 weeks not yet term"),
                         ])
def test_chronological_decimal_age(birth_date, observation_date, expected_decimal_age):
    assert chronological_decimal_age(
        birth_date, observation_date) == expected_decimal_age


@pytest.mark.parametrize("birth_date,observation_date,gestation_weeks,gestation_days,expected_decimal_age",
                         [
                             pytest.param(date(2010, 12, 3), date(
                                 2010, 12, 20), 27, 0, -0.2026009582477755,
                                 id="baby under 32 weeks not yet term"),
                         ])
def test_corrected_decimal_age_premature_baby(birth_date, observation_date, gestation_weeks, gestation_days,
                                              expected_decimal_age):
    assert corrected_decimal_age(
        birth_date, observation_date, gestation_weeks, gestation_days) == expected_decimal_age


@pytest.mark.parametrize("birth_date,gestation_weeks,gestation_days,full_term_edd",
                         [
                             pytest.param(date(2010, 12, 3), 27, 0, date(
                                 2011, 3, 4), id="edd of baby under 32 weeks")
                         ])
def test_edd_premature_baby_before_term(birth_date, gestation_weeks, gestation_days, full_term_edd):
    assert estimated_date_delivery(
        birth_date, gestation_weeks, gestation_days) == full_term_edd
