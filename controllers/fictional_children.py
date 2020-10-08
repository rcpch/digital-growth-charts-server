import rcpchgrowth.rcpchgrowth as rcpchgrowth

def generate_fictional_children_data(
        measurement_method,
        sex,
        default_to_youngest_reference
    ):

    return rcpchgrowth.generate_fictional_children_data(
        measurement_method=measurement_method,
        sex=sex,
        default_to_youngest_reference=default_to_youngest_reference
    )