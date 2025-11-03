from rcpchgrowth import corrected_decimal_age, MINIMUM_BMI_ERROR_SDS, MAXIMUM_BMI_ERROR_SDS, MINIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS, MAXIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS, sds_for_measurement, chronological_calendar_age

MAX_BULK_OBSERVATIONS = 200

def validate_observation_value(reference, values, observation_values=None):
    """
    Validate the observation value for the given reference
    """
   
    measurement_method = values.measurement_method
    observation_value = (observation_values or values).observation_value
    sex = values.sex
    gestation_weeks = values.gestation_weeks
    gestation_days = values.gestation_days
    observation_date = (observation_values or values).observation_date
    birth_date = values.birth_date
    decimal_age  = corrected_decimal_age(birth_date=birth_date, observation_date=observation_date, gestation_weeks=gestation_weeks, gestation_days=gestation_days)

    try:
        calculated_sds = sds_for_measurement(
                observation_value=observation_value,
                measurement_method=measurement_method,
                sex=sex,
                reference=reference,
                age=decimal_age
            )
    except LookupError as e:
        print(e)
        raise ValueError(e)
    
    try:
        calendar_age = chronological_calendar_age(
            birth_date=birth_date,
            observation_date=observation_date,
        )
    except ValueError as e:
        print(e)
        raise ValueError(e)

    units = "cm" if measurement_method in ["height", "ofc"] else "kg"
    boy_girl = "boy" if sex == "male" else "girl"
    if measurement_method == "bmi":
        units = "kg/m²"
        if calculated_sds < MINIMUM_BMI_ERROR_SDS:
            raise ValueError("Body mass index cannot be less than -15 SD.")
        if calculated_sds > MAXIMUM_BMI_ERROR_SDS:
            raise ValueError("Body mass index cannot be more than +15 SD.")
    else:
        if measurement_method == "ofc":
            measurement_method = "Head circumference"
        if calculated_sds < MINIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS:
            raise ValueError(f"A {measurement_method} of {observation_value} {units} in a {boy_girl} of {calendar_age} is less than -8 SD. Please recheck the measurement and date of birth.")
        if calculated_sds > MAXIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS:
            raise ValueError(f"A {measurement_method} of {observation_value} {units} in a {boy_girl} of {calendar_age} is more than +8 SD. Please recheck the measurement and date of birth.")

    return values