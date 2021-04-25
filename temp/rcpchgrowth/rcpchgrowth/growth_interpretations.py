def comment_prematurity_correction(
    chronological_decimal_age: float,
    corrected_decimal_age: float,
    gestation_weeks: int,
    gestation_days: int):
    """
    Returns interpretations on age correction as a string
    """

    if chronological_decimal_age == corrected_decimal_age:
        # no adjustment has been made so the baby was born at 40 weeks
            lay_corrected_decimal_age_comment = "Your baby was born on their due date."
            clinician_corrected_decimal_age_comment = "Born at term. No correction has been made for gestation."
            lay_chronological_decimal_age_comment = "Your baby was born on their due date."
            clinician_chronological_decimal_age_comment = "Born Term. No correction has been made for gestation."
    elif chronological_decimal_age > corrected_decimal_age:
        ## adjustment for gestational age has been made - even if >=37 weeks
        lay_corrected_decimal_age_comment = f"Because your child was born at {gestation_weeks}+{gestation_days} weeks gestation, an adjustment has been made to take this into account."
        clinician_corrected_decimal_age_comment = "Correction for gestational age has been made."
        lay_chronological_decimal_age_comment = "This is your child's age without taking into account their gestation at birth."
        clinician_chronological_decimal_age_comment = "No correction has been made for gestational age."
        if gestation_weeks < 23:
            lay_corrected_decimal_age_comment = "Your child has been born below the threshold of the charts."
            clinician_corrected_decimal_age_comment = "Your child has been born below the threshold of the charts."
            lay_chronological_decimal_age_comment = "Your child has been born below the threshold of the charts."
            clinician_chronological_decimal_age_comment = "Your child has been born below the threshold of the charts."
    else:
        #some error
        lay_corrected_decimal_age_comment = "It has not been possible to calculate age this time."
        clinician_corrected_decimal_age_comment = "It has not been possible to calculate age this time."
        lay_chronological_decimal_age_comment = "It has not been possible to calculate age this time."
        clinician_chronological_decimal_age_comment = "It has not been possible to calculate age this time."

    comment = {
        'lay_corrected_comment': lay_corrected_decimal_age_comment,
        'lay_chronological_comment': lay_chronological_decimal_age_comment,
        'clinician_corrected_comment': clinician_corrected_decimal_age_comment,
        'clinician_chronological_comment': clinician_chronological_decimal_age_comment
    }
    return comment