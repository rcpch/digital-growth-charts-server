from .global_functions import sds_for_centile, rounded_sds_for_centile, generate_centile
from .uk_who import select_reference_data_for_uk_who_chart
from .trisomy_21 import select_reference_data_for_trisomy_21
from .turner import select_reference_data_for_turner
from .constants.reference_constants import UK_WHO, TURNERS, TRISOMY_21, COLE_TWO_THIRDS_SDS_NINE_CENTILES, COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION, THREE_PERCENT_CENTILE_COLLECTION, MEASUREMENT_METHODS, SEXES, UK_WHO_REFERENCES
import pprint


def create_chart(reference: str, centile_selection: str, measurement_method: str = "height", sex: str = "female",):
    """
    Global method - return chart for measurement_method, sex and reference
    """
    if reference == UK_WHO:
        return create_uk_who_chart(measurement_method=measurement_method, sex=sex, centile_selection=centile_selection)
    elif reference == TURNERS:
        return create_turner_chart(centile_selection=centile_selection)
    elif reference == TRISOMY_21:
        return create_trisomy_21_chart(measurement_method=measurement_method, sex=sex, centile_selection=centile_selection)
    else:
        print("No reference data returned. Is there a spelling mistake in your reference?")


def create_plottable_child_data(child_results_array):
    """
    Global method - receives a measurement object and returns the data in plottable format - the ages as x, the measurements
    as y and the centile values as l (label)
    """

    centile_data = []
    sds_data = []

    for count, child_result in enumerate(child_results_array):
        if(child_result):
            # create 4 plottable return objects for each measurement: one for each corrected and chronological age
            # per measurement and per SDS score
            # These measurement pairs and SDS pairs are stored in a 2 2-value arrays, so that each measurement/SDS
            # can be plotted as a series in the charts.
            # If there are multiple values to plot, the return array will be a string of arrays of paired values,
            # which allows them to be plotted as pairs: this is because corrected and chronological values should be
            # linked by a line, the chronological value denotes as a dot, the corrected value as a cross.

            chronological_data_point = {
                "measurement_method": child_result["child_observation_value"]["measurement_method"],
                "x": child_result["measurement_dates"]["chronological_decimal_age"],
                "y": child_result["child_observation_value"]["observation_value"],
                "observation_value_error": child_result["child_observation_value"]["observation_value_error"],
                "centile_band": child_result["measurement_calculated_values"]["chronological_centile_band"],
                "centile_value": child_result["measurement_calculated_values"]["chronological_centile"],
                "sds": child_result["measurement_calculated_values"]["chronological_sds"],
                "measurement_error": child_result["measurement_calculated_values"]["chronological_measurement_error"],
                "age_error": child_result["measurement_dates"]["chronological_decimal_age_error"],
                "age_type": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"],
                "lay_chronological_decimal_age_comment": child_result["measurement_dates"]["comments"]["lay_chronological_decimal_age_comment"],
                "clinician_chronological_decimal_age_comment": child_result["measurement_dates"]["comments"]["clinician_chronological_decimal_age_comment"]
            }
            corrected_data_point = {
                "measurement_method": child_result["child_observation_value"]["measurement_method"],
                "x": child_result["measurement_dates"]["corrected_decimal_age"],
                "y": child_result["child_observation_value"]["observation_value"],
                "observation_value_error": child_result["child_observation_value"]["observation_value_error"],
                "centile_band": child_result["measurement_calculated_values"]["corrected_centile_band"],
                "centile_value": child_result["measurement_calculated_values"]["corrected_centile"],
                "sds": child_result["measurement_calculated_values"]["corrected_sds"],
                "measurement_error": child_result["measurement_calculated_values"]["corrected_measurement_error"],
                "age_error": child_result["measurement_dates"]["corrected_decimal_age_error"],
                "age_type": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["corrected_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"],
                "lay_corrected_decimal_age_comment": child_result["measurement_dates"]["comments"]["lay_corrected_decimal_age_comment"],
                "clinician_corrected_decimal_age_comment": child_result["measurement_dates"]["comments"]["clinician_corrected_decimal_age_comment"],
            }
            chronological_sds_data_point = {
                "measurement_method": child_result["child_observation_value"]["measurement_method"],
                "x": child_result["measurement_dates"]["chronological_decimal_age"],
                "y": child_result["measurement_calculated_values"]["chronological_sds"],
                "observation_value_error": child_result["child_observation_value"]["observation_value_error"],
                "sds": child_result["measurement_calculated_values"]["chronological_sds"],
                "measurement_error": child_result["measurement_calculated_values"]["chronological_measurement_error"],
                "age_error": child_result["measurement_dates"]["chronological_decimal_age_error"],
                "age_type": "chronological_age",
                "calendar_age": child_result["measurement_dates"]["chronological_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"],
                "lay_chronological_decimal_age_comment": child_result["measurement_dates"]["comments"]["lay_chronological_decimal_age_comment"],
                "clinician_chronological_decimal_age_comment": child_result["measurement_dates"]["comments"]["clinician_chronological_decimal_age_comment"]
            }

            corrected_sds_data_point = {
                "measurement_method": child_result["child_observation_value"]["measurement_method"],
                "x": child_result["measurement_dates"]["corrected_decimal_age"],
                "y": child_result["measurement_calculated_values"]["corrected_sds"],
                "observation_value_error": child_result["child_observation_value"]["observation_value_error"],
                "sds": child_result["measurement_calculated_values"]["corrected_sds"],
                "measurement_error": child_result["measurement_calculated_values"]["corrected_measurement_error"],
                "age_error": child_result["measurement_dates"]["corrected_decimal_age_error"],
                "age_type": "corrected_age",
                "calendar_age": child_result["measurement_dates"]["corrected_calendar_age"],
                "corrected_gestation_weeks": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"],
                "corrected_gestation_days": child_result["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"],
                "lay_corrected_decimal_age_comment": child_result["measurement_dates"]["comments"]["lay_corrected_decimal_age_comment"],
                "clinician_corrected_decimal_age_comment": child_result["measurement_dates"]["comments"]["clinician_corrected_decimal_age_comment"],
            }

            measurement_data_points = [
                corrected_data_point, chronological_data_point]
            measurement_sds_data_points = [
                corrected_sds_data_point, chronological_sds_data_point]

            centile_data.append(measurement_data_points)
            sds_data.append(measurement_sds_data_points)

    result = {
        "measurement_method": child_result["child_observation_value"]["measurement_method"],
        "centile_data": centile_data,
        "sds_data": sds_data
    }

    return result

    """
    Return object structure

    [
        heights: [
            [{
                x: 9.415, `this is the corrected age of the child at date of measurement in decimal years
                y: 120 `this is the observation value - the units will be added in the client
                "centile_band": 'Your child's height is between the 75th and 91st centiles' `a text advice string for labelling - corrected,
                "centile_value": 86 `centile number value - reported but not used: the project board do not like exact centile numbers - corrected,
                "age_type": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
            }
            {
                x: 9.415, `this is the chronological age of the child at date of measurement in decimal years
                y: 120 `this is the observation value - the units will be added in the client
                "centile_band": 'Your child's height is between the 75th and 91st centiles' `a text advice string for labelling - based on chronological age,
                "centile_value": 86 `centile number value - reported but not used: the project board do not like exact centile numbers - based on chronological age, 
                "age_type": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
            }
            ]
        ],
        height_sds: [
                x: 9.415, `this is the age of the child at date of measurement in decimal years
                y: 1.3 `this is the SDS value for SDS charts
                "age_type": "corrected_age", `this is a flag to differentiate the two ages for the same observation_value
                "calendar_age": "9 years and 4 months" `this is the calendar age for labelling
                "corrected_gestational_weeks": 23 `the corrected gestational age if relevant for labelling
                "corrected_gestational_days": 1 `the corrected gestational age if relevant for labelling
        ],
        .... and so on for the other measurement_methods
        
    ]

    """


"""
private functions
"""


def create_uk_who_chart(measurement_method: str, sex: str, centile_selection: str = COLE_TWO_THIRDS_SDS_NINE_CENTILES):

    # user selects which centile collection they want, for sex and measurement_method
    # If the Cole method is selected, conversion between centile and SDS
    # is different as SDS is rounded to the nearest 2/3
    # Cole method selection is stored in the cole_method flag.
    # If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False

    ##
    # iterate through the 4 references that make up UK-WHO
    # There will be a list for each one
    ##

    # all data for a given reference are stored here: this is returned to the user
    reference_data = []

    for reference_index, reference in enumerate(UK_WHO_REFERENCES):
        sex_list: dict = {}  # all the data for a given sex are stored here
        # For each reference we have 2 sexes
        # for sex_index, sex in enumerate(SEXES):
        # For each sex we have 4 measurement_methods

        measurements: dict = {}  # all the data for a given measurement_method are stored here

        # for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
        # for every measurement method we have as many centiles
        # as have been requested

        centiles = []  # all generated centiles for a selected centile collection are stored here

        for centile_index, centile in enumerate(centile_collection):
            # we must create a z for each requested centile
            # if the Cole 9 centiles were selected, these are rounded,
            # so conversion to SDS is different
            # Otherwise standard conversation of centile to z is used
            if cole_method:
                z = rounded_sds_for_centile(centile)
            else:
                z = sds_for_centile(centile)

            # Collect the LMS values from the correct reference
            lms_array_for_measurement = select_reference_data_for_uk_who_chart(
                uk_who_reference=reference, measurement_method=measurement_method, sex=sex)

            # Generate a centile. there will be nine of these if Cole method selected.
            # Some data does not exist at all ages, so any error reflects missing data.
            # If this happens, an empty list is returned.
            centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method,
                                            sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference="uk-who")

            # Store this centile for a given measurement
            centiles.append({"sds": round(z * 100) / 100,
                             "centile": centile, "data": centile_data})

        # this is the end of the centile_collection for loop
        # All the centiles for this measurement, sex and reference are added to the measurements list
        measurements.update({measurement_method: centiles})

        # this is the end of the measurement_methods loop
        # All data for all measurement_methods for this sex are added to the sex_list list

        sex_list.update({sex: measurements})

        # all data can now be tagged by reference_name and added to reference_data
        reference_data.append({reference: sex_list})

    # returns a list of 4 references, each containing 2 lists for each sex,
    # each sex in turn containing 4 datasets for each measurement_method
    return reference_data

    """
    structure:
    UK_WHO generates 4 json objects, each structure as below
    uk90_preterm: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }
    uk_who_infant: {...}
    uk_who_child:{...}
    uk90_child: {...}
    """


def create_turner_chart(centile_selection: str):
   # user selects which centile collection they want
    # If the Cole method is selected, conversion between centile and SDS
    # is different as SDS is rounded to the nearest 2/3
    # Cole method selection is stored in the cole_method flag.
    # If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False

    # all data for a the reference are stored here: this is returned to the user
    reference_data = {}

    # for sex_index, sex in enumerate(SEXES):
    # For each sex we have 4 measurement_methods
    # Turner is female only, but we will generate empty arrays for male
    # data to keep all objects the same

    sex_list: dict = {}
    sex = "female"

    measurements: dict = {}  # all the data for a given measurement_method are stored here

    # for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
    # for every measurement method we have as many centiles
    # as have been requested

    centiles = []  # all generated centiles for a selected centile collection are stored here

    for centile_index, centile in enumerate(centile_collection):
        # we must create a z for each requested centile
        # if the Cole 9 centiles were selected, these are rounded,
        # so conversion to SDS is different
        # Otherwise standard conversation of centile to z is used
        if cole_method:
            z = rounded_sds_for_centile(centile)
        else:
            z = sds_for_centile(centile)

        # Collect the LMS values from the correct reference
        lms_array_for_measurement = select_reference_data_for_trisomy_21(
            measurement_method="height", sex=sex)
        # Generate a centile. there will be nine of these if Cole method selected.
        # Some data does not exist at all ages, so any error reflects missing data.
        # If this happens, an empty list is returned.

        centile_data = generate_centile(z=z, centile=centile, measurement_method="height",
                                        sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference=TURNERS)

        # Store this centile for a given measurement
        centiles.append({"sds": round(z * 100) / 100,
                         "centile": centile, "data": centile_data})

    # this is the end of the centile_collection for loop
    # All the centiles for this measurement, sex and reference are added to the measurements list
    measurements.update({"height": centiles})

    # this is the end of the measurement_methods loop
    # All data for all measurement_methods for this sex are added to the sex_list list

    sex_list.update({sex: measurements})

    # all data can now be tagged by reference_name and added to reference_data
    reference_data = {TURNERS: sex_list}
    return reference_data

    """
    Return object structure
    trisomy_21: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }
    """


def create_trisomy_21_chart(measurement_method: str, sex: str, centile_selection: str):
   # user selects which centile collection they want
    # If the Cole method is selected, conversion between centile and SDS
    # is different as SDS is rounded to the nearest 2/3
    # Cole method selection is stored in the cole_method flag.
    # If no parameter is passed, default is the Cole method

    centile_collection = []

    if centile_selection == COLE_TWO_THIRDS_SDS_NINE_CENTILES:
        centile_collection = COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION
        cole_method = True
    else:
        centile_collection = THREE_PERCENT_CENTILE_COLLECTION
        cole_method = False

    # all data for a the reference are stored here: this is returned to the user
    reference_data = {}
    sex_list: dict = {}

    # for sex_index, sex in enumerate(SEXES):
    # For each sex we have 4 measurement_methods

    measurements: dict = {}  # all the data for a given measurement_method are stored here

    # for measurement_index, measurement_method in enumerate(MEASUREMENT_METHODS):
    # for every measurement method we have as many centiles
    # as have been requested

    centiles = []  # all generated centiles for a selected centile collection are stored here

    for centile_index, centile in enumerate(centile_collection):
        # we must create a z for each requested centile
        # if the Cole 9 centiles were selected, these are rounded,
        # so conversion to SDS is different
        # Otherwise standard conversation of centile to z is used
        if cole_method:
            z = rounded_sds_for_centile(centile)
        else:
            z = sds_for_centile(centile)

        # Collect the LMS values from the correct reference
        lms_array_for_measurement = select_reference_data_for_trisomy_21(
            measurement_method=measurement_method, sex=sex)
        # Generate a centile. there will be nine of these if Cole method selected.
        # Some data does not exist at all ages, so any error reflects missing data.
        # If this happens, an empty list is returned.

        centile_data = generate_centile(z=z, centile=centile, measurement_method=measurement_method,
                                        sex=sex, lms_array_for_measurement=lms_array_for_measurement, reference=TRISOMY_21)

        # Store this centile for a given measurement
        centiles.append({"sds": round(z * 100) / 100,
                         "centile": centile, "data": centile_data})

    # this is the end of the centile_collection for loop
    # All the centiles for this measurement, sex and reference are added to the measurements list
    measurements.update({measurement_method: centiles})

    # this is the end of the measurement_methods loop
    # All data for all measurement_methods for this sex are added to the sex_list list

    sex_list.update({sex: measurements})

    # all data can now be tagged by reference_name and added to reference_data
    reference_data = {TRISOMY_21: sex_list}
    return reference_data

    """
    # return object structure
    trisomy_21: {
        male: {
            height: [
                {
                    sds: -2.667,
                    centile: 0.4
                    data: [{l: , x: , y: }, ....]
                }
            ],
            weight: [...]
        },
        female {...}
    }
    """
