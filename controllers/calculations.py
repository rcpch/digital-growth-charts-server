from datetime import date
import rcpchgrowth.rcpchgrowth as calculations

def perform_calculations(form):
    birth_date = form.birth_date.data
    obs_date = form.obs_date.data
    height = float(form.height.data)
    weight = float(form.weight.data)
    ofc = float(form.ofc.data)
    sex = form.sex.data
    gestation_weeks = form.gestation_weeks.data
    gestation_days = form.gestation_days.data
    corrected_decimal_age = calculations.corrected_decimal_age(birth_date, obs_date, gestation_weeks, gestation_days)
    chronological_decimal_age = calculations.chronological_decimal_age(birth_date, obs_date)
    chronological_calendar_age = calculations.chronological_calendar_age(birth_date, obs_date)

    height_sds = 'None'
    height_centile="None"
    weight_sds = 'None'
    weight_centile='None'
    bmi_sds = 'None'
    bmi_centile='None'
    ofc_sds = 'None'
    ofc_centile='None'
    bmi = 'None'
    edd = 'None'
    edd_string = ""
    corrected_calendar_age = ''
    corrected_gestational_age = ''

    clinician_height_comment = ''
    clinician_weight_comment = ''
    clinician_bmi_comment = ''
    clinician_ofc_comment = ''
    lay_height_comment = ''
    lay_weight_comment = ''
    lay_bmi_comment = ''
    lay_ofc_comment = ''
    clinician_decimal_age_comment = ''
    lay_decimal_age_comment = ''

    array_of_measurement_objects = [];
    return_measurement_object = {}

    if chronological_decimal_age == corrected_decimal_age:
        corrected_decimal_age = 'None'
        age = chronological_decimal_age
        if gestation_weeks < 37 and gestation_weeks >= 32:
            lay_decimal_age_comment =   "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth ."
            clinician_decimal_age_comment =  "Correction for gestational age is nolonger necessary after a year of age."
        if gestation_weeks < 33:
            lay_decimal_age_comment =   "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth ."
            clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after two years of age."
    else:
        age = corrected_decimal_age
        edd = calculations.estimated_date_delivery(birth_date, gestation_weeks, gestation_days)
        corrected_calendar_age = calculations.chronological_calendar_age(edd, obs_date)
        edd_string = edd.strftime('%a %d %B, %Y')
        corrected_gestational_age = calculations.corrected_gestational_age(birth_date, obs_date, gestation_weeks, gestation_days)
        lay_decimal_age_comment =   "Your child's prematurity has been accounted for when considering their growth ."
        clinician_decimal_age_comment =  "Correction for gestational age has been made ."

    if height > 0.0:
        if age >= -0.287474333: # there is no length data below 25 weeks gestation
            height_sds = calculations.sds(age, 'height', height, sex)
            height_centile = calculations.centile(height_sds)
            comment = interpret('height', height_centile, age)
            clinician_height_comment = comment["clinician_comment"]
            lay_height_comment = comment["lay_comment"]
            ## create return object
            return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,height_sds,height_centile,clinician_height_comment,lay_height_comment,None,None,None,None,None,None,None,None,None,None,None,None, height, None, None, None)
            array_of_measurement_objects.append(return_measurement_object)
    if weight > 0.0:
        weight_sds = calculations.sds(age, 'weight', weight, sex)
        weight_centile = calculations.centile(weight_sds)
        comment = interpret('weight', weight_centile, age)
        clinician_weight_comment = comment['clinician_comment']
        lay_weight_comment = comment['lay_comment']
        ## create return object
        return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,weight_sds,weight_centile,clinician_weight_comment,lay_weight_comment,None,None,None,None,None,None,None,None, None, weight, None , None)
        array_of_measurement_objects.append(return_measurement_object)
    if height > 0.0 and weight > 0.0:
        bmi = calculations.bmi_from_height_weight(height, weight)
        if age > 0.038329911: # BMI data not present < 42 weeks gestation
            bmi_sds = calculations.sds(age, 'bmi', bmi, sex)
            bmi_centile = calculations.centile(bmi_sds)
            comment = interpret('bmi', bmi_centile, age)
            clinician_bmi_comment = comment['clinician_comment']
            lay_bmi_comment = comment['lay_comment']
            ## create return object
            return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,None,None,None,None,bmi_sds,bmi_centile,clinician_bmi_comment,lay_bmi_comment,None,None,None,None, None, None, bmi, None)
            array_of_measurement_objects.append(return_measurement_object)
    if ofc > 0.0:
        if (age <= 17 and sex == 'female') or (age <= 18.0 and sex == 'male'): # OFC data not present >17y in girls or >18y in boys
            ofc_sds = calculations.sds(age, 'ofc', ofc, sex)
            ofc_centile = calculations.centile(ofc_sds)
            comment = interpret('ofc', ofc_centile, age)
            clinician_ofc_comment = comment['clinician_comment']
            lay_ofc_comment = comment['lay_comment']
            ## create return object
            return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,None,None,None,None,None,None,None,None, ofc_sds, ofc_centile, clinician_ofc_comment,lay_ofc_comment, None, None, None, ofc)
            array_of_measurement_objects.append(return_measurement_object)
    
    return array_of_measurement_objects
    

def create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age: str, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,height_sds,height_centile,clinician_height_comment,lay_height_comment,weight_sds,weight_centile,clinician_weight_comment,lay_weight_comment,bmi_sds,bmi_centile,clinician_bmi_comment,lay_bmi_comment, ofc_sds, ofc_centile, clinician_ofc_comment,lay_ofc_comment, height, weight, bmi, ofc):

    return {
                "birth_data": {
                    "birth_date": birth_date, 
                    "gestation_weeks": gestation_weeks, 
                    "gestation_days": gestation_days, 
                    "edd": edd, 
                    "edd_string": edd_string, #redundant? need to check
                    "sex": sex, 
                },

                "measurement_dates": {
                    "obs_date": obs_date, 
                    "chronological_decimal_age": chronological_decimal_age, 
                    "corrected_decimal_age": corrected_decimal_age, 
                    "chronological_calendar_age": chronological_calendar_age, 
                    "corrected_calendar_age": corrected_calendar_age, 
                    "corrected_gestational_age": corrected_gestational_age, 
                    'clinician_decimal_age_comment': clinician_decimal_age_comment, 
                    'lay_decimal_age_comment': lay_decimal_age_comment
                }, 
                "child_measurement_value": {
                    "height": height, 
                    "weight": weight, 
                    "bmi": bmi, 
                    "ofc": ofc
                    }, 
                "measurement_calculated_values": {
                    "height_sds": height_sds, 
                    "height_centile": height_centile, 
                    'clinician_height_comment': clinician_height_comment, 
                    'lay_height_comment': lay_height_comment, 
                    "weight_sds": weight_sds, 
                    "weight_centile":weight_centile, 
                    'clinician_weight_comment': clinician_weight_comment, 
                    'lay_weight_comment': lay_weight_comment, 
                    "bmi_sds": bmi_sds,
                    "bmi_centile": bmi_centile,
                    'clinician_bmi_comment': clinician_bmi_comment, 
                    'lay_bmi_comment': lay_bmi_comment, 
                    "ofc_sds": ofc_sds, 
                    "ofc_centile": ofc_centile, 
                    'clinician_ofc_comment': clinician_ofc_comment, 
                    'lay_ofc_comment': lay_ofc_comment
                } 
        }


def interpret(measurement: str, centile: float, age: float):    
    """
    returns interpretations of measurement and centile as string. Accepts age corrected if necessary
    """
    
    lay_interpretation = ''
    clinician_interpretation = ''

    if measurement == 'height':
        if centile <= 0.04:
            if age < 2.0:
                lay_interpretation = "Your child has a lower or the same length as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
            if age >= 2.0:
                lay_interpretation = "Your child has a lower or the same height as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
            clinician_interpretation = "On or below the 0.04th centile for height. Medical review advised."
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

    if measurement == 'weight':
        if centile <= 0.04:
            lay_interpretation = "Your child has a lower or the same weight as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
            clinician_interpretation = "On or below the 0.04th centile for weight. Medical review advised."
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

    if measurement == 'bmi':
        if centile <= 0.04:
            lay_interpretation = "Compared with other children the same height, age and sex, your child is below or the same weight as only 4 in every 1000 children. It is advisable to see your doctor."
            clinician_interpretation = "On or below the 0.04th centile. Medical review advised."
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

    if measurement == 'ofc':
        if centile <= 0.04:
            lay_interpretation = "Your child's head size is larger than or the same as only 4 in every 1000 children the same age and sex. It is advisable to see your doctor."
            clinician_interpretation = "On or below the 0.04th centile for head circumference. Medical review advised."
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

    return_comment =  {
        'clinician_comment': clinician_interpretation,
        'lay_comment': lay_interpretation
    }

    return return_comment
        
        
