import unittest
from datetime import date
from ..sds_calculations import sds

class TestSDS(unittest.TestCase):

    ## Tests for term children

    def test_sds_term_boy_at_birth_length(self):
        """
        calculate the length sds of a boy born at term
        """
        z = sds(0, 'height', 60.0, 'male')
        self.assertEqual(z, 0.8870636550308009)
    
    def test_sds_term_girl_at_birth_length(self):
        """
        calculate the length sds of a girl born at term
        """
        z = sds(0, 'height', 60, 'female')
        self.assertEqual(z, 0.8870636550308009)
    
    def test_sds_term_boy_at_birth_weight(self):
        """
        calculate the weight sds of a boy born at term
        """
        z = sds(0, 'weight', 3.5, 'male')
        self.assertEqual(z, 0.8870636550308009)
    
    def test_sds_term_girl_at_birth_weight(self):
        """
        calculate the weight sds of a girl born at term
        """
        z = sds(0.0, 'weight', 2.7, 'female')
        self.assertEqual(z, -1.39508903)
    
    def test_sds_term_boy_at_birth_ofc(self):
        """
        calculate the ofc sds of a boy born at term
        """
        z = sds(0, 'ofc', 45.0, 'male')
        self.assertEqual(z, 0.8870636550308009)
    
    def test_sds_term_girl_at_birth_ofc(self):
        """
        calculate the ofc sds of a girl born at term
        """
        z = sds(0, 'ofc', 45, 'female')
        self.assertEqual(z, 0.8870636550308009)
    
    
    
if __name__ == '__main__':
    unittest.main()