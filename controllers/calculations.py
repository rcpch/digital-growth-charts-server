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

    if chronological_decimal_age == corrected_decimal_age:
        corrected_decimal_age = 'None'
        age = chronological_decimal_age
    else:
        age = corrected_decimal_age
        edd = calculations.estimated_date_delivery(birth_date, gestation_weeks, gestation_days)
        corrected_calendar_age = calculations.chronological_calendar_age(edd, obs_date)
        edd_string = edd.strftime('%a %d %B, %Y')
        corrected_gestational_age = calculations.corrected_gestational_age(birth_date, obs_date, gestation_weeks, gestation_days)
    if height > 0.0:
        if age >= -0.287474333: # there is no length data below 25 weeks gestation
            height_sds = calculations.sds(age, 'height', height, sex)
            height_centile = calculations.centile(height_sds)
    if weight > 0.0:
        weight_sds = calculations.sds(age, 'weight', weight, sex)
        weight_centile = calculations.centile(weight_sds)
    if height > 0.0 and weight > 0.0:
        bmi = calculations.bmi_from_height_weight(height, weight)
        if age > 0.038329911: # BMI data not present < 42 weeks gestation
            bmi_sds = calculations.sds(age, 'bmi', bmi, sex)
            bmi_centile = calculations.centile(bmi_sds)
    if ofc > 0.0:
        if (age <= 17 and sex == 'female') or (age <= 18.0 and sex == 'male'): # OFC data not present >17y in girls or >18y in boys
            ofc_sds = calculations.sds(age, 'ofc', ofc, sex)
            ofc_centile = calculations.centile(ofc_sds)

    return {"dates": {"birth_date": birth_date, "obs_date": obs_date, "gestation_weeks": gestation_weeks, "gestation_days": gestation_days, "chronological_decimal_age": chronological_decimal_age, "corrected_decimal_age": corrected_decimal_age, "chronological_calendar_age": chronological_calendar_age, "corrected_calendar_age": corrected_calendar_age, "edd": edd, "edd_string": edd_string, "corrected_gestational_age": corrected_gestational_age}, "patient": {"sex": sex, "height": height, "weight": weight, "bmi": bmi, "ofc": ofc}, "calculations": {"height_sds": height_sds, "height_centile": height_centile, "weight_sds": weight_sds, "weight_centile":weight_centile, "bmi_sds": bmi_sds, "bmi_centile": bmi_centile, "ofc_sds": ofc_sds, "ofc_centile": ofc_centile} }