import unittest
from datetime import date
from ..date_calculations import chronological_decimal_age, corrected_decimal_age, estimated_date_delivery


# TODO: #92 TestDecimalAge needs to be converted to use PyTest

class TestDecimalAge(unittest.TestCase):

    # Tests for term children

    def test_chronological_decimal_age_under_one_child_term(self):
        """
        calculate the decimal age of a baby under a year born at term
        """
        birth_date = date(2009, 4, 1)
        observation_date = date(2010, 2, 19)
        decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.assertEqual(decimal_age, 0.8870636550308009)

    def test_chronological_decimal_age_over_two_child_term(self):
        """
        calculate the decimal age of a child over two born at term
        """
        birth_date = date(2009, 1, 3)
        observation_date = date(2011, 10, 3)
        decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.assertEqual(decimal_age, 2.746064339493498)

    def test_chronological_decimal_age_over_four_child_term(self):
        """
        calculate the decimal age of a child over four born at term
        """
        birth_date = date(2009, 1, 3)
        observation_date = date(2013, 11, 20)
        decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.assertEqual(decimal_age, 4.878850102669404)

    # tests from preterm children

    def test_chronological_decimal_age_premature_baby_before_term(self):
        """
        calculate the decimal age of a baby over 32 weeks not yet term
        """
        birth_date = date(2010, 12, 3)
        observation_date = date(2010, 12, 20)
        decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.assertEqual(decimal_age, 0.04654346338124572)

    def test_corrected_decimal_age_premature_baby_before_term(self):
        """
        calculate the decimal age of a baby under 32 weeks not yet term
        """
        birth_date = date(2010, 12, 3)
        observation_date = date(2010, 12, 20)
        decimal_age = corrected_decimal_age(
            birth_date, observation_date, 27, 0)
        self.assertEqual(decimal_age, -0.2026009582477755)

    def test_edd_premature_baby_before_term(self):
        """
        calculate the estimated date of delivery of an baby under 32 weeks
        """
        birth_date = date(2010, 12, 3)
        edd = estimated_date_delivery(birth_date, 27, 0)
        self.assertEqual(edd, date(2011, 3, 4))


if __name__ == '__main__':
    unittest.main()
