import unittest
from datetime import date
from ..date_calculations import chronological_decimal_age

class TestDecimalAge(unittest.TestCase):
    def test_chronological_decimal_age_term_male(self):
        """
        Test that it can sum a list of integers
        """
        birth_date = date('1/4/2009')
        observation_date = ('19/02/2010')
        decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.assertEqual(decimal_age, 0.887063655030801)

if __name__ == '__main__':
    unittest.main()