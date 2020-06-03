

def interpret(measurement: str, centile: float, age: float, sex: str):    
    """
    returns interpretations of centile values as string. Accepts age corrected if necessary
     - params: measurement (string, 'height', 'weight', 'ofc' 'bmi')
     - params: centile (float)
     - age: float (either a corrected or a chronological age)
    """
    
    lay_interpretation = ''
    clinician_interpretation = ''

    ## error handling
    if age < 0.038329911 and measurement == 'bmi': # below 42 weeks of age there is no BMI reference data
        lay_interpretation = "BMI centiles cannot be calculated below 2 weeks of age or before your baby has reached term."
        clinician_interpretation = "BMI SDS and Centiles cannot be calculated before 42 weeks as there is no reference data below this threshold."
    elif age < -0.287474333 and measurement == 'height': # below 25 weeks there is no height reference data
        lay_interpretation = "Height centiles cannot be calculate below 25 weeks gestation."
        clinician_interpretation = "Length SDS and Centiles cannot be calculated below 25 weeks as there is no reference data below this threshold."
    elif age > 17.0 and measurement == 'ofc' and sex == 'female':
        lay_interpretation = "Head circumference centiles cannot be calculated above 17 years in girls."
        clinician_interpretation = "Head circumference SDS and Centiles cannot be calculated above 17 y as there is no reference data beyond this threshold in girls."
    elif age > 18.0 and measurement == 'ofc' and sex == 'male':
        lay_interpretation = "Head circumference centiles cannot be calculated above 18 years in boys."
        clinician_interpretation = "Head circumference SDS and Centiles cannot be calculated above 18 y as there is no reference data below this threshold in boys."
    else: 
        ## return comments
        if measurement == 'height':
            if centile <= 0.4:
                if age < 2.0:
                    lay_interpretation = "Your child has a lower or the same length as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
                if age >= 2.0:
                    lay_interpretation = "Your child has a lower or the same height as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
                clinician_interpretation = "On or below the 0.4th centile for height. Medical review advised."
            elif centile <= 2.0:
                if age < 2.0:
                    lay_interpretation = "Your child is in the lowest 2 percent for length, sex and age. Consider seeing your doctor."
                if age >= 2.0:
                    lay_interpretation = "Your child is in the lowest 2 percent for height, sex and age. Consider seeing your doctor."
                clinician_interpretation = "On or below the 2nd centile. Consider reviewing trend."
            elif centile <= 9.0:
                if age < 2.0:
                    lay_interpretation = "Your child is in the lowest 9 percent of the population for length, sex and age."
                elif age >= 2.0:
                    lay_interpretation = "Your child is in the lowest 9 percent of the population for height, sex and age."
                clinician_interpretation = "On or below the 9th centile. Consider reviewing trend."
            elif centile <= 25.0:
                if age < 2.0:
                    lay_interpretation = "Your child is in the lowest 1/4 of the population for length, sex and age."
                if age >= 2.0:
                    lay_interpretation = "Your child is in the lowest 1/4 of the population for length, sex and age."
                clinician_interpretation = "On or below the 25th centile. Consider reviewing trend."
            elif centile <= 50.0:
                if age < 2.0:
                    lay_interpretation = "Your child is on or just below the average length of the population for sex and age."
                if age >= 2.0:
                    lay_interpretation = "Your child is on or just below the average height of the population for sex and age."
                clinician_interpretation = "On or below the 50th centile."
            elif centile <= 75.0:
                if age < 2.0:
                    lay_interpretation = "Your child has the same or a shorter length than 75 percent of children the same age and sex."
                if age >= 2.0:
                    lay_interpretation = "Your child has the same or a shorter height than 75 percent of children the same age and sex."
                clinician_interpretation = "On or below the 75th centile. Consider reviewing trend."
            elif centile <= 91.0:
                if age < 2.0:
                    lay_interpretation = "Your child is in the top 9 percent of children the same age and sex for their length."
                if age >= 2.0:
                    lay_interpretation = "Your child is in the top 9 percent of children the same age and sex for their height."
                clinician_interpretation = "On or below the 91st centile. Consider reviewing trend."
            elif centile <= 98.0:
                if age < 2.0:
                    lay_interpretation = "Your child is in the top 2 percent of children the same age and sex for their length."
                if age >= 2.0:
                    lay_interpretation = "Your child is in the top 2 percent of children the same age and sex for their length."
                clinician_interpretation = "On or below the 91st centile. Consider reviewing trend."
            elif centile <= 99.6:
                if age < 2.0:
                    lay_interpretation = "Your child is longer than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
                if age >= 2.0:
                    lay_interpretation = "Your child is taller than only 4 children in every 1000 the same age and sex. Consider seeking medical review."
                clinician_interpretation = "On or below the 99.6th centile. Consider medical review."
            elif centile > 99.6:
                if age < 2.0:
                    lay_interpretation = "Your child's length is outside the upper limit of the chart. Please discuss with your doctor."
                    clinician_interpretation = "Above 99.6th centile for length. Medical review is advised."
                if age >= 2.0:
                    lay_interpretation = "Your child's height is outside the upper limit of the chart. Please discuss with your doctor."
                    clinician_interpretation = "Above 99.6th centile for height. Medical review is advised."

        if measurement == 'weight':
            if centile <= 0.4:
                lay_interpretation = "Your child has a lower or the same weight as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
                clinician_interpretation = "On or below the 0.4th centile for weight. Medical review advised."
            elif centile <= 2.0:
                lay_interpretation = "Your child is in the lowest 2 percent for weight compared with other children the same age and sex. Consider seeing your doctor."
                clinician_interpretation = "On or below the 2nd centile. Consider reviewing trend."
            elif centile <= 9.0:
                lay_interpretation = "Your child is in the lowest 9 percent of the population for weight compared with other children the same age and sex."
                clinician_interpretation = "On or below the 9th centile. Consider reviewing trend."
            elif centile <= 25.0:
                lay_interpretation = "Your child is in the lowest 1/4 of the population for weight, compared with other children the same age and sex."
                clinician_interpretation = "On or below the 25th centile. Consider reviewing trend."
            elif centile <= 50.0:
                lay_interpretation = "Your child is on or just below the average weight of the population, compared with other children the same age and sex."
                clinician_interpretation = "On or below the 50th centile ."
            elif centile <= 75.0:
                lay_interpretation = "Your child is below or the same as 75 percent of children the same age and sex. This does not take account of their height."
                clinician_interpretation = "On or below the 75th centile. Consider reviewing trend."
            elif centile <= 91.0:
                lay_interpretation = "Your child is in the top 9 percent of children the same age and sex for their weight. This does not take account of their height."
                clinician_interpretation = "On or below the 91st centile. Consider reviewing trend."
            elif centile <= 98.0:
                lay_interpretation = "Your child is in the top 2 percent of children the same age and sex for their weight. This does not take account of their height. Consider seeking medical review ."
                clinician_interpretation = "On or below the 91st centile. Consider reviewing trend."
            elif centile <= 99.6:
                lay_interpretation = "Your child is taller than only 4 children in every 1000 the same age and sex. This does not take account of their height. Medical review is advised."
                clinician_interpretation = "On or below the 99.6th centile. Consider medical review."
            elif centile > 99.6:
                lay_interpretation = "Your child's weight is outside the upper limit of the chart. Please discuss with your doctor."
                clinician_interpretation = "Above 99.6th centile for weight. Medical review is advised."

        if measurement == 'bmi':
            if centile:
                if centile <= 0.4:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is below or the same weight as only 4 in every 1000 children. It is advisable to see your doctor."
                    clinician_interpretation = "On or below the 0.4th centile. Medical review advised."
                elif centile <= 2.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is is in the lowest 2 percent of the population for their weight. Consider seeing your doctor."
                    clinician_interpretation = "On or below the 2nd centile. Consider reviewing trend."            
                elif centile <= 9.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is in the lowest 9 percent of the population for weight."
                    clinician_interpretation = "On or below the 9th centile. Consider reviewing trend."
                elif centile <= 25.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is in the lowest 1/4 of the population for their weight."
                    clinician_interpretation = "On or below the 25th centile. Consider reviewing trend."
                elif centile <= 50.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is on or just below the average weight for the population ."
                    clinician_interpretation = "On or below the 50th centile ."
                elif centile <= 75.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is below or the same as 75 percent of children for their weight."
                    clinician_interpretation = "On or below the 75th centile. Consider reviewing trend."
                elif centile <= 91.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is in the top 9 percent of children for their weight."
                    clinician_interpretation = "On or below the 91st centile. Consider reviewing trend."
                elif centile <= 98.0:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child is in the top 2 percent of children for their weight. Consider seeing your doctor."
                    clinician_interpretation = "On or below the 98th centile. Meets definition for being overweight. Consider reviewing trend."
                elif centile <= 99.6:
                    lay_interpretation = "Compared with other children the same height, age and sex, your child's  weight is lower than only 4 children in every 1000 childre. Medical review is advised."
                    clinician_interpretation = "On or below the 99.6th centile. Above obesity threshold. Consider medical review."
                elif centile > 99.6:
                    lay_interpretation = "Your child's weight is outside the upper limit of the chart, compared with other children the same age, height and sex. Please discuss with your doctor."
                    clinician_interpretation = "Above 99.6th centile for BMI. Medical review is advised."
            else:
                lay_interpretation = "BMI is not interpretable below 2 weeks of age"
                clinician_interpretation = 'There is no reference data below 2 weeks of age'

        if measurement == 'ofc':
            if centile <= 0.4:
                lay_interpretation = "Your child's head size is larger than or the same as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
                clinician_interpretation = "On or below the 0.4th centile for head circumference. Medical review advised."
            elif centile <= 2.0:
                lay_interpretation = "Your child's head size is in the lowest 2 percent as other children the same sex and age. Consider seeing your doctor."
                clinician_interpretation = "On or below the 2nd centile for head circumference. Consider reviewing trend."
            elif centile <= 9.0:
                lay_interpretation = "Your child's head size is in the lowest 9 percent of the population for children the same sex and age."
                clinician_interpretation = "On or below the 9th centile for head circumference. Consider reviewing trend."
            elif centile <= 25.0:
                lay_interpretation = "Your child's head size is in the lowest 1/4 of the population compared with other children the same sex and age."
                clinician_interpretation = "On or below the 25th centile for head circumference. Consider reviewing trend."
            elif centile <= 50.0:
                lay_interpretation = "Your child is on or just below the average height of the population for sex and age."
                clinician_interpretation = "On or below the 50th centile for head circumference."
            elif centile <= 75.0:
                lay_interpretation = "Your child's head circumference is in the top 25 percent of children the same age and sex."
                clinician_interpretation = "On or below the 75th centile for head circumference. Consider reviewing trend."
            elif centile <= 91.0:
                lay_interpretation = "Your child's head circumference is in the top 9 percent of children the same age and sex."
                clinician_interpretation = "On or below the 91st centile for head circumference. Consider reviewing trend."
            elif centile <= 98.0:
                lay_interpretation = "Your child's head circumference is in the top 2 percent of children the same age and sex. Consider seeing your doctor."
                clinician_interpretation = "On or below the 91st centile for head circumference. Consider reviewing trend."
            elif centile <= 99.6:
                lay_interpretation = "Your child's head circumference is larger than only 4 children in every 1000 children the same age and sex. Medical review is advised."
                clinician_interpretation = "On or below the 99.6th centile for head circumference. Medical review is advised."
            elif centile > 99.6:
                lay_interpretation = "Your child's head circumference is outside the upper limit of the chart. Please discuss with your doctor."
                clinician_interpretation = "Above 99.6th centile for head circumference. Medical review is advised."

    return_comment =  {
        'clinician_comment': clinician_interpretation,
        'lay_comment': lay_interpretation
    }

    return return_comment

def comment_prematurity_correction(chronological_decimal_age, corrected_decimal_age, gestation_weeks, gestation_days):
    """
    Return interpretations on age correction as a string
    :Params - chronological_decimal_age : float
    :Params - corrected_decimal_age : float
    :Params - gestation_weeks : int
    :Params - gestation_days : int
    """
    if chronological_decimal_age == corrected_decimal_age:
        if gestation_weeks >= 37:
            lay_decimal_age_comment = f"At {gestation_weeks}+{gestation_days}, your child is considered to have been born at term. No age adjustment is necessary."
            clinician_decimal_age_comment = "Born Term. No correction necessary."
        elif gestation_weeks < 37 and gestation_weeks >= 32:
            lay_decimal_age_comment = "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth."
            clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after a year of age."
        elif gestation_weeks < 33:
            lay_decimal_age_comment = "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth."
            clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after two years of age."
    elif chronological_decimal_age > corrected_decimal_age:
        if gestation_weeks < 37 and gestation_weeks >= 32 and corrected_decimal_age < 1.0:
            lay_decimal_age_comment = f"Because your child was born at {gestation_weeks}+{gestation_days}, an adjustment has been made to take into account their prematurity. This will be made up to a year of age."
            clinician_decimal_age_comment = "Correction for gestational age has been made. This occurs until a year of age."
        elif gestation_weeks < 33:
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