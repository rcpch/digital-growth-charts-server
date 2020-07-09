from datetime import date, datetime
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from rcpchgrowth.rcpchgrowth.measurement_type import Measurement_Type
from rcpchgrowth.rcpchgrowth.date_calculations import chronological_decimal_age
from rcpchgrowth.rcpchgrowth.dynamic_growth import velocity, acceleration

# this wrapper changes form data to the right kwargs for the calculation function
def form_wrapper(form):
    return perform_calculations(
        birth_date=form.birth_date.data,
        observation_date=form.obs_date.data,
        height=float(form.height.data),
        weight=float(form.weight.data),
        ofc=float(form.ofc.data),
        sex=form.sex.data,
        gestation_weeks=form.gestation_weeks.data,
        gestation_days=form.gestation_days.data)


# for clarity and safety, accepts only named (keyword) arguments, not positional arguments
# I've used this style of indentation for clarity:
# https://github.com/python/typing/issues/433#issuecomment-302491149
# This function takes up to 3 measurements performed on the same day and returns SDS and centiles on 4 (BMI is itself a calculated value)
def perform_calculations(*, 
        birth_date: date,
        observation_date: date,
        height: float,
        weight: float,
        ofc: float,
        sex: str,
        gestation_weeks: int,
        gestation_days:int):

    array_of_measurement_objects = []
    if height:
        measurement_type = Measurement_Type("height", height=height)
        measurement_object = Measurement(sex=sex, birth_date=birth_date, observation_date=observation_date, measurement_type=measurement_type, gestation_weeks=gestation_weeks, gestation_days=gestation_days, default_to_youngest_reference=False)
        array_of_measurement_objects.append(measurement_object.measurement)
    if weight:
        measurement_type = Measurement_Type("weight", weight=weight)
        measurement_object = Measurement(sex=sex, birth_date=birth_date, observation_date=observation_date, measurement_type=measurement_type, gestation_weeks=gestation_weeks, gestation_days=gestation_days, default_to_youngest_reference=False)
        array_of_measurement_objects.append(measurement_object.measurement)
    if height and weight: 
        measurement_type = Measurement_Type("bmi", height=height, weight=weight)
        measurement_object = Measurement(sex=sex, birth_date=birth_date, observation_date=observation_date, measurement_type=measurement_type, gestation_weeks=gestation_weeks, gestation_days=gestation_days, default_to_youngest_reference=False)
        array_of_measurement_objects.append(measurement_object.measurement)
    if ofc:
        measurement_type = Measurement_Type("ofc", ofc=ofc)
        measurement_object = Measurement(sex=sex, birth_date=birth_date, observation_date=observation_date, measurement_type=measurement_type, gestation_weeks=gestation_weeks, gestation_days=gestation_days, default_to_youngest_reference=False)
        array_of_measurement_objects.append(measurement_object.measurement)
    return array_of_measurement_objects

# This function takes a measurement_method as a string ('height', 'weight', 'bmi' or 'ofc') and returns a Measurement object with the calculated values.
# Note that BMI must be provided already calculated as a parameter to this function.
# Note that measurement_method is a string passed by the form and is distinct from Measurement_Type which is a class relating to the same
def perform_calculation(*,
    birth_date: date,
    observation_date: date,
    measurement_method: str,
    observation_value: float,
    sex: str,
    gestation_weeks: int,
    gestation_days: int):

    array_of_measurement_objects = []

    if measurement_method == "height":
        measurement_type = Measurement_Type("height", measurement_value=float(observation_value))
    if measurement_method == "weight":
        measurement_type = Measurement_Type("weight", measurement_value=float(observation_value))
    if measurement_method == "bmi": 
        measurement_type = Measurement_Type("bmi", measurement_value=float(observation_value))
    if measurement_method == "ofc":
        measurement_type = Measurement_Type("ofc", measurement_value=float(observation_value))
    measurement_object = Measurement(sex=sex, birth_date=birth_date, observation_date=observation_date, measurement_type=measurement_type, gestation_weeks=gestation_weeks, gestation_days=gestation_days, default_to_youngest_reference=False)
    
    ## return measurement object as an array
    array_of_measurement_objects.append(measurement_object.measurement)
    return array_of_measurement_objects

def calculate_velocity_acceleration(data):
    height_velocity = velocity("height", data)
    weight_velocity = velocity("weight", data)
    bmi_velocity = velocity("bmi", data)
    ofc_velocity = velocity("ofc", data)
    height_acceleration = acceleration("height", data)
    weight_acceleration = acceleration("weight", data)
    bmi_acceleration = acceleration("bmi", data)
    ofc_acceleration = acceleration("ofc", data)
    return {
        "height_velocity": height_velocity,
        "weight_velocity": weight_velocity,
        "bmi_velocity": bmi_velocity,
        "ofc_velocity": ofc_velocity,
        "height_acceleration": height_acceleration,
        "weight_acceleration": weight_acceleration,
        "bmi_acceleration": bmi_acceleration,
        "ofc_acceleration": ofc_acceleration
    }