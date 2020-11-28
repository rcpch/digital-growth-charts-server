from datetime import date, datetime
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from rcpchgrowth.rcpchgrowth.date_calculations import chronological_decimal_age
from rcpchgrowth.rcpchgrowth.dynamic_growth import velocity, acceleration


def perform_calculation(*,
                        birth_date: date,
                        observation_date: date,
                        measurement_method: str,
                        observation_value: float,
                        sex: str,
                        gestation_weeks: int,
                        gestation_days: int):
    """
    * This function takes a measurement_method as a string ('height', 'weight', 'bmi' or 'ofc') and returns a Measurement object with the calculated values.
    
    * Note that BMI must be provided already calculated as a parameter to this function.
    
    * Note that measurement_method is a string passed by the form and is distinct from Measurement_Type which is a class relating to the same.
    
    * Dates supplied as valid JSON Date strings, passing Marshmallow validation in the Flask app will be converted to Python DateTime objects for passing to the Python RCPCHgrowth package
    """
    return Measurement(
        sex=str(sex),
        birth_date=datetime.strptime(birth_date, "%Y-%m-%d"),
        observation_date=datetime.strptime(observation_date,"%Y-%m-%d"),
        measurement_method=str(measurement_method),
        observation_value=float(observation_value),
        gestation_weeks=gestation_weeks,
        gestation_days=gestation_days,
        reference="uk-who"
    ).measurement


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
