import rcpchgrowth.rcpchgrowth as rcpchgrowth

def generate_fictional_data(
        drift_amount,
        intervals,
        interval_type,
        measurement_requested,
        number_of_measurements,
        sex,
        starting_age,
        starting_sds,
    ):

    return rcpchgrowth.create_fictional_child(
        sex=sex,
        measurement_type=measurement_requested,
        requested_sds=starting_sds,
        number_of_measurements=number_of_measurements,
        starting_decimal_age=starting_age,
        measurement_interval_value=intervals,
        measurement_interval_type=interval_type,
        gestation_weeks=40,
        gestation_days=0,
        drift=True,
        drift_sds_range=drift_amount
    )