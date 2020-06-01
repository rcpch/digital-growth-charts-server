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
    
    return array_of_measurement_objects
    

# def create_measurement_object(birth_date, edd, obs_date, edd_string, sex, chronological_decimal_age, chronological_calendar_age: str, gestation_weeks, gestation_days, corrected_decimal_age, corrected_calendar_age, corrected_gestational_age, clinician_decimal_age_comment, lay_decimal_age_comment,height_sds,height_centile,clinician_height_comment,lay_height_comment,weight_sds,weight_centile,clinician_weight_comment,lay_weight_comment,bmi_sds,bmi_centile,clinician_bmi_comment,lay_bmi_comment, ofc_sds, ofc_centile, clinician_ofc_comment,lay_ofc_comment, height, weight, bmi, ofc):

#     return {
#                 "birth_data": {
#                     "birth_date": birth_date, 
#                     "gestation_weeks": gestation_weeks, 
#                     "gestation_days": gestation_days, 
#                     "edd": edd, 
#                     "edd_string": edd_string,
#                     "sex": sex, 
#                 },

#                 "measurement_dates": {
#                     "obs_date": obs_date, 
#                     "chronological_decimal_age": chronological_decimal_age, 
#                     "corrected_decimal_age": corrected_decimal_age, 
#                     "chronological_calendar_age": chronological_calendar_age, 
#                     "corrected_calendar_age": corrected_calendar_age, 
#                     "corrected_gestational_age": corrected_gestational_age, 
#                     'clinician_decimal_age_comment': clinician_decimal_age_comment, 
#                     'lay_decimal_age_comment': lay_decimal_age_comment
#                 }, 
#                 "child_measurement_value": {
#                     "height": height, 
#                     "weight": weight, 
#                     "bmi": bmi, 
#                     "ofc": ofc
#                     }, 
#                 "measurement_calculated_values": {
#                     "height_sds": height_sds, 
#                     "height_centile": height_centile, 
#                     'clinician_height_comment': clinician_height_comment, 
#                     'lay_height_comment': lay_height_comment, 
#                     "weight_sds": weight_sds, 
#                     "weight_centile":weight_centile, 
#                     'clinician_weight_comment': clinician_weight_comment, 
#                     'lay_weight_comment': lay_weight_comment, 
#                     "bmi_sds": bmi_sds,
#                     "bmi_centile": bmi_centile,
#                     'clinician_bmi_comment': clinician_bmi_comment, 
#                     'lay_bmi_comment': lay_bmi_comment, 
#                     "ofc_sds": ofc_sds, 
#                     "ofc_centile": ofc_centile, 
#                     'clinician_ofc_comment': clinician_ofc_comment, 
#                     'lay_ofc_comment': lay_ofc_comment
#                 } 
#         }