from .constants import DECIMAL_AGES
import random

def generate_fictional_children_data(
    measurement_method: str,
    sex: str
):
    # This function generates an array of decimal ages, sequential values alternating between an exact match 
    # of the decimal ages in the reference data with a randomly generated age between them.
    # These can be used to generate 
    new_age_array=[]
    for index, decimal_age in enumerate(DECIMAL_AGES):
      if index!=len(DECIMAL_AGES)-1:
        next_decimal_age = DECIMAL_AGES[index+1]
        random_age = decimal_age + ((next_decimal_age-decimal_age)/random.randint(1,10))
        new_age_array.append(decimal_age)
        new_age_array.append(random_age)
        