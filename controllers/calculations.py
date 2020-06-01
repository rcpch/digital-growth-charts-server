from datetime import date
from rcpchgrowth.rcpchgrowth.measurement import Measurement

def perform_calculations(form):
    birth_date = form.birth_date.data
    observation_date = form.obs_date.data
    height = float(form.height.data)
    weight = float(form.weight.data)
    ofc = float(form.ofc.data)
    sex = form.sex.data
    gestation_weeks = form.gestation_weeks.data
    gestation_days = form.gestation_days.data

    array_of_measurement_objects = []
    if height:
        height_measurement = Measurement(sex, birth_date, observation_date, gestation_weeks, gestation_days)
        array_of_measurement_objects.append(height_measurement.calculate_height_sds_centile(height))
    if weight:
        weight_measurement = Measurement(sex, birth_date, observation_date, gestation_weeks, gestation_days)
        array_of_measurement_objects.append(weight_measurement.calculate_weight_sds_centile(weight))
    if height and weight:
        bmi_measurement = Measurement(sex, birth_date, observation_date, gestation_weeks, gestation_days)
        array_of_measurement_objects.append(bmi_measurement.calculate_bmi_sds_centile(height, weight))
    if ofc:
        ofc_measurement = Measurement(sex, birth_date, observation_date, gestation_weeks, gestation_days)
        array_of_measurement_objects.append(ofc_measurement.calculate_ofc_sds_centile(ofc))
    
    # corrected_decimal_age = rcpchgrowth.corrected_decimal_age(birth_date, obs_date, gestation_weeks, gestation_days)
    # chronological_decimal_age = rcpchgrowth.chronological_decimal_age(birth_date, obs_date)
    # chronological_calendar_age = rcpchgrowth.chronological_calendar_age(birth_date, obs_date)
    # height_sds = 'None'
    # height_centile="None"
    # weight_sds = 'None'
    # weight_centile='None'
    # bmi_sds = 'None'
    # bmi_centile='None'
    # ofc_sds = 'None'
    # ofc_centile='None'
    # bmi = 'None'
    # edd = 'None'
    # edd_string = ""
    # corrected_calendar_age = ''
    # corrected_gestational_age = ''

    # clinician_height_comment = ''
    # clinician_weight_comment = ''
    # clinician_bmi_comment = ''
    # clinician_ofc_comment = ''
    # lay_height_comment = ''
    # lay_weight_comment = ''
    # lay_bmi_comment = ''
    # lay_ofc_comment = ''
    # clinician_decimal_age_comment = ''
    # lay_decimal_age_comment = ''

    # return_measurement_object = {}
    # array_of_measurement_objects = []

    # if chronological_decimal_age == corrected_decimal_age: ## assessment of need for correction made within the calculation functions
    #     corrected_decimal_age = 'None'
    #     age = chronological_decimal_age
    #     if gestation_weeks < 37 and gestation_weeks >= 32: ## was born premature but now >1y
    #         lay_decimal_age_comment =   "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth ."
    #         clinician_decimal_age_comment =  "Correction for gestational age is nolonger necessary after a year of age."
    #     if gestation_weeks < 33: ## was born extreme premature but now >2y
    #         lay_decimal_age_comment =   "Your child is now old enough nolonger to need to take their prematurity into account when considering their growth ."
    #         clinician_decimal_age_comment = "Correction for gestational age is nolonger necessary after two years of age."
    # else:
    #     age = corrected_decimal_age
    #     edd = rcpchgrowth.estimated_date_delivery(birth_date, gestation_weeks, gestation_days)
    #     corrected_calendar_age = rcpchgrowth.chronological_calendar_age(edd, obs_date)
    #     edd_string = edd.strftime('%a %d %B, %Y')
    #     corrected_gestational_age = rcpchgrowth.corrected_gestational_age(birth_date, obs_date, gestation_weeks, gestation_days)
    #     lay_decimal_age_comment =   "Your child's prematurity has been accounted for when considering their growth ."
    #     clinician_decimal_age_comment =  "Correction for gestational age has been made ."

    # if height > 0.0:
    #     if age >= -0.287474333: # there is no length data below 25 weeks gestation
    #         height_sds = rcpchgrowth.sds(age, 'height', height, sex)
    #         height_centile = rcpchgrowth.centile(height_sds)
    #         comment = rcpchgrowth.interpret('height', height_centile, age)
    #         clinician_height_comment = comment["clinician_comment"]
    #         lay_height_comment = comment["lay_comment"]
    #         ## create return object
    #         return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,height_sds,height_centile,clinician_height_comment,lay_height_comment,None,None,None,None,None,None,None,None,None,None,None,None, height, None, None, None)
    #         array_of_measurement_objects.append(return_measurement_object)
    # if weight > 0.0:
    #     weight_sds = rcpchgrowth.sds(age, 'weight', weight, sex)
    #     weight_centile = rcpchgrowth.centile(weight_sds)
    #     comment = rcpchgrowth.interpret('weight', weight_centile, age)
    #     clinician_weight_comment = comment['clinician_comment']
    #     lay_weight_comment = comment['lay_comment']
    #     ## create return object
    #     return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,weight_sds,weight_centile,clinician_weight_comment,lay_weight_comment,None,None,None,None,None,None,None,None, None, weight, None , None)
    #     array_of_measurement_objects.append(return_measurement_object)
    # if height > 0.0 and weight > 0.0:
    #     bmi = rcpchgrowth.bmi_from_height_weight(height, weight)
    #     if age > 0.038329911: # BMI data not present < 42 weeks gestation
    #         bmi_sds = rcpchgrowth.sds(age, 'bmi', bmi, sex)
    #         bmi_centile = rcpchgrowth.centile(bmi_sds)
    #         comment = rcpchgrowth.interpret('bmi', bmi_centile, age)
    #         clinician_bmi_comment = comment['clinician_comment']
    #         lay_bmi_comment = comment['lay_comment']
    #         ## create return object
    #         return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,None,None,None,None,bmi_sds,bmi_centile,clinician_bmi_comment,lay_bmi_comment,None,None,None,None, None, None, bmi, None)
    #         array_of_measurement_objects.append(return_measurement_object)
    # if ofc > 0.0:
    #     if (age <= 17 and sex == 'female') or (age <= 18.0 and sex == 'male'): # OFC data not present >17y in girls or >18y in boys
    #         ofc_sds = rcpchgrowth.sds(age, 'ofc', ofc, sex)
    #         ofc_centile = rcpchgrowth.centile(ofc_sds)
    #         comment = rcpchgrowth.interpret('ofc', ofc_centile, age)
    #         clinician_ofc_comment = comment['clinician_comment']
    #         lay_ofc_comment = comment['lay_comment']
    #         ## create return object
    #         return_measurement_object = create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,None,None,None,None,None,None,None,None,None,None,None,None, ofc_sds, ofc_centile, clinician_ofc_comment,lay_ofc_comment, None, None, None, ofc)
    #         array_of_measurement_objects.append(return_measurement_object)
    
    return array_of_measurement_objects
    

def create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age: str, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,height_sds,height_centile,clinician_height_comment,lay_height_comment,weight_sds,weight_centile,clinician_weight_comment,lay_weight_comment,bmi_sds,bmi_centile,clinician_bmi_comment,lay_bmi_comment, ofc_sds, ofc_centile, clinician_ofc_comment,lay_ofc_comment, height, weight, bmi, ofc):

    return {
                "birth_data": {
                    "birth_date": birth_date, 
                    "gestation_weeks": gestation_weeks, 
                    "gestation_days": gestation_days, 
                    "edd": edd, 
                    "edd_string": edd_string,
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