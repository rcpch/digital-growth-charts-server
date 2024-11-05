from rcpchgrowth import corrected_decimal_age, MINIMUM_BMI_ERROR_SDS, MAXIMUM_BMI_ERROR_SDS, MINIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS, MAXIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS, sds_for_measurement

def validate_observation_value(reference, values):
    """
    Validate the observation value for the given reference
    """
   
    measurement_method = values.measurement_method
    observation_value = values.observation_value
    sex = values.sex
    gestation_weeks = values.gestation_weeks if "gestation_weeks" in values else 40
    gestation_days = values.gestation_days if "gestation_days" in values else 0
    observation_date = values.observation_date
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
        raise ValueError(e)

    if measurement_method == "bmi":
        if calculated_sds < MINIMUM_BMI_ERROR_SDS:
            raise ValueError("Body mass index cannot be less than -15 SD.")
        if calculated_sds > MAXIMUM_BMI_ERROR_SDS:
            raise ValueError("Body mass index cannot be more than +15 SD.")
    else:
        if measurement_method == "ofc":
            measurement_method = "Head circumference"
        if calculated_sds < MINIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS:
            raise ValueError(f"{measurement_method} cannot be less than -8 SD.")
        if calculated_sds > MAXIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS:
            raise ValueError(f"{measurement_method} cannot be more than +8 SD.")

    return values