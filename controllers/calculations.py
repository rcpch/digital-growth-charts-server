from datetime import date
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from rcpchgrowth.rcpchgrowth.dynamic_growth import velocity

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

def calculate_velocity(data):
    height_velocity = velocity('height', data)
    weight_velocity = velocity('weight', data)
    bmi_velocity = velocity('bmi', data)
    ofc_velocity = velocity('ofc', data)
    return {
        'height_velocity': height_velocity,
        'weight_velocity': weight_velocity,
        'bmi_velocity': bmi_velocity,
        'ofc_velocity': ofc_velocity
    }
    