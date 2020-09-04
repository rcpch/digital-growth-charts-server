from .constants import FORTY_TWO_WEEKS_GESTATION, TWENTY_FIVE_WEEKS_GESTATION

## THIS HANDLER FOR LIMITS OF REFERENCE DATA MAY NEED TO BE RE-ENABLED - MB 4.9.20

# if age < FORTY_TWO_WEEKS_GESTATION and measurement == 'bmi': # below 42 weeks of age there is no BMI reference data
#     lay_interpretation = "BMI centiles cannot be calculated below 2 weeks of age or before your baby has reached term."
#     clinician_interpretation = "BMI SDS and Centiles cannot be calculated before 42 weeks as there is no reference data below this threshold."
# elif age < TWENTY_FIVE_WEEKS_GESTATION and measurement == 'height': # below 25 weeks there is no height reference data
#     lay_interpretation = "Height centiles cannot be calculate below 25 weeks gestation."
#     clinician_interpretation = "Length SDS and Centiles cannot be calculated below 25 weeks as there is no reference data below this threshold."
# elif age > 17.0 and measurement == 'ofc' and sex == 'female':
#     lay_interpretation = "Head circumference centiles cannot be calculated above 17 years in girls."
#     clinician_interpretation = "Head circumference SDS and Centiles cannot be calculated above 17 y as there is no reference data beyond this threshold in girls."
# elif age > 18.0 and measurement == 'ofc' and sex == 'male':
#     lay_interpretation = "Head circumference centiles cannot be calculated above 18 years in boys."
#     clinician_interpretation = "Head circumference SDS and Centiles cannot be calculated above 18 y as there is no reference data below this threshold in boys."
# else: 
 

def comment_prematurity_correction(
    chronological_decimal_age: float,
    corrected_decimal_age: float,
    gestation_weeks: int,
    gestation_days: int):
    """
    Returns interpretations on age correction as a string
    """
    if chronological_decimal_age == corrected_decimal_age:
        if gestation_weeks >= 37:
            lay_decimal_age_comment = f"At {gestation_weeks}+{gestation_days}, your child is considered to have been born at term. No age adjustment is necessary."
            clinician_decimal_age_comment = "Born Term. No correction necessary."
        elif gestation_weeks >= 32:
            lay_decimal_age_comment = "Your child is now old enough no longer to need to take their prematurity into account when considering their growth."
            clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after a year of age."
        else:
            lay_decimal_age_comment = "Your child is now old enough no longer to need to take their prematurity into account when considering their growth."
            clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after two years of age."
    elif chronological_decimal_age > corrected_decimal_age:
        if gestation_weeks >= 32 and corrected_decimal_age < 1.0:
            lay_decimal_age_comment = f"Because your child was born at {gestation_weeks}+{gestation_days}, an adjustment has been made to take into account their prematurity. This will be made up to a year of age."
            clinician_decimal_age_comment = "Correction for gestational age has been made. This occurs until a year of age."
        elif gestation_weeks < 23:
            lay_decimal_age_comment = "Your child has been born below the threshold of the charts."
            clinician_decimal_age_comment = "Reference data does not exist below the age of 23 weeks gestation."
        else:
            lay_decimal_age_comment = f"Because your child was born at {gestation_weeks}+{gestation_days}, an adjustment had been made to take into account their prematurity. This occurs up to two years of age."
            clinician_decimal_age_comment = "Correction for gestational age has been made. This occurs until two years of age."
    else:
        #some error
        lay_decimal_age_comment = "It has not been possible to calculate age this time."
        clinician_decimal_age_comment = "It has not been possible to calculate age this time."
    
    comment = {
        'lay_comment': lay_decimal_age_comment,
        'clinician_comment': clinician_decimal_age_comment
    }
    return comment