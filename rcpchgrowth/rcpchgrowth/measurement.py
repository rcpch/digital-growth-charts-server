# standard imports
from datetime import date
from pprint import pprint

# third-party imports
from marshmallow import ValidationError

# rcpch imports
from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height
from .centile_bands import centile_band_for_centile
from .constants import *
from .date_calculations import (chronological_decimal_age, corrected_decimal_age,
                                chronological_calendar_age, estimated_date_delivery, corrected_gestational_age)
from .global_functions import sds_for_measurement, measurement_from_sds, centile
from .growth_interpretations import comment_prematurity_correction
from .schemas import *


class Measurement:

    def __init__(
        self,
        birth_date: date,
        measurement_method: str,
        observation_date: date,
        observation_value: float,
        reference: str,
        sex: str,
        gestation_days: int = 0,
        gestation_weeks: int = 0,
    ):
        """
        The Measurement Class is the gatekeeper to all the functions in the RCPCHGrowth package, although the public
        functions can be accessed independently. The bulk of the error handling happens here so be aware that calling
        other functions independently may yield unexpected results.

        It is initialised with the following Required parameters:

        `birth_date`: (Python datetime object) The date of birth of the subject.
        `measurement_type`: (string) 'height', 'weight', 'bmi' or 'ofc' only are accepted.
        `observation_date`: (Python datetime object) The date that the observation was made.
        `observation_value`: (float) The value of the height, weight, BMI or ofc observation.
        `sex`: (string) The sex of the child, which can either be 'male' or 'female'.

        Additionally there are the following optional parameters:

        `gestation_weeks`: (integer) gestation at birth in weeks.
        `gestation_days`: (integer) supplemental days in addition to gestation_weeks at birth.
        `reference`: ENUM refering to which reference dataset to use: ['uk-who', 'turners-syndrome', 'trisomy-21'].
        """

        self.birth_date = birth_date
        self.gestation_days = gestation_days
        self.gestation_weeks = gestation_weeks
        self.measurement_method = measurement_method
        self.observation_date = observation_date
        self.observation_value = observation_value
        self.reference = reference
        self.sex = sex

        # Validate using the Marshmallow Schema
        # Note that Marshmallow validates only STRING dates, not Python Dates, hence the conversion here

        MeasurementClassSchema().load({
            'birth_date': birth_date.strftime('%Y-%m-%d'),
            'gestation_days': gestation_days,
            'gestation_weeks': gestation_weeks,
            'measurement_method': measurement_method,
            'observation_date': observation_date.strftime('%Y-%m-%d'),
            'observation_value': observation_value,
            'reference': reference,
            'sex': sex
        })

        try:
            self.__validate_measurement_method(
                measurement_method=measurement_method, observation_value=observation_value)
            observation_value_error = None
        except Exception as err:
            observation_value_error = f"{err}"

        if gestation_weeks < 37 and gestation_weeks >= 23:
            self.born_preterm = True
        else:
            self.born_preterm = False

        # the ages_object receives birth_data and measurement_dates objects
        self.ages_object = self.__calculate_ages(
            sex=self.sex,
            birth_date=self.birth_date,
            observation_date=self.observation_date,
            gestation_weeks=self.gestation_weeks,
            gestation_days=self.gestation_days)

        # the calculate_measurements_object receives the child_observation_value and measurement_calculated_values objects
        self.calculated_measurements_object = self.sds_and_centile_for_measurement_method(
            sex=self.sex,
            corrected_age=self.ages_object['measurement_dates']['corrected_decimal_age'],
            chronological_age=self.ages_object['measurement_dates']['chronological_decimal_age'],
            measurement_method=self.measurement_method,
            observation_value=self.observation_value,
            observation_value_error=observation_value_error,
            born_preterm=self.born_preterm,
            reference=self.reference
        )

        corrected_gestational_age = ""
        if (self.ages_object["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"] is not None):
            corrected_gestational_age = f'{ self.ages_object["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_weeks"] } + { self.ages_object["measurement_dates"]["corrected_gestational_age"]["corrected_gestation_days"]} weeks'

        self.plottable_centile_data = {
            "chronological_decimal_age_data": {
                "x": self.ages_object['measurement_dates']['chronological_decimal_age'],
                "y": self.observation_value,
                "observation_error": self.calculated_measurements_object['child_observation_value']["observation_value_error"],
                "age_type": "chronological_age",
                "calendar_age": self.ages_object["measurement_dates"]["chronological_calendar_age"],
                "lay_comment": self.ages_object["measurement_dates"]["comments"]["lay_chronological_decimal_age_comment"],
                "clinician_comment": self.ages_object["measurement_dates"]["comments"]["clinician_chronological_decimal_age_comment"],
                "age_error": self.ages_object["measurement_dates"]["corrected_decimal_age_error"],
                "centile_band": self.calculated_measurements_object['measurement_calculated_values']["chronological_centile_band"],
                "observation_value_error": self.calculated_measurements_object["measurement_calculated_values"]["chronological_measurement_error"]

            },
            "corrected_decimal_age_data": {
                "x": self.ages_object['measurement_dates']['corrected_decimal_age'],
                "y": self.observation_value,
                "observation_error": self.calculated_measurements_object['child_observation_value']["observation_value_error"],
                "age_type": "corrected_age",
                "corrected_gestational_age": corrected_gestational_age,
                "calendar_age": self.ages_object["measurement_dates"]["corrected_calendar_age"],
                "lay_comment": self.ages_object["measurement_dates"]["comments"]["lay_corrected_decimal_age_comment"],
                "clinician_comment": self.ages_object["measurement_dates"]["comments"]["clinician_corrected_decimal_age_comment"],
                "age_error": self.ages_object["measurement_dates"]["corrected_decimal_age_error"],
                "centile_band": self.calculated_measurements_object['measurement_calculated_values']["corrected_centile_band"],
                "observation_value_error": self.calculated_measurements_object["measurement_calculated_values"]["corrected_measurement_error"]
            }
        }

        self.plottable_sds_data = {
            "chronological_decimal_age_data": {
                "x": self.ages_object['measurement_dates']['chronological_decimal_age'],
                "y": self.calculated_measurements_object['measurement_calculated_values']["chronological_sds"],
                "age_type": "chronological_age",
                "calendar_age": self.ages_object["measurement_dates"]["chronological_calendar_age"],
                "lay_comment": self.ages_object["measurement_dates"]["comments"]["lay_chronological_decimal_age_comment"],
                "clinician_comment": self.ages_object["measurement_dates"]["comments"]["clinician_chronological_decimal_age_comment"],
                "age_error": self.ages_object["measurement_dates"]["corrected_decimal_age_error"],
                "centile_band": self.calculated_measurements_object['measurement_calculated_values']["chronological_centile_band"],
                "observation_value_error": self.calculated_measurements_object["measurement_calculated_values"]["chronological_measurement_error"]
            },
            "corrected_decimal_age_data": {
                "x": self.ages_object['measurement_dates']['corrected_decimal_age'],
                "y": self.calculated_measurements_object['measurement_calculated_values']["corrected_sds"],
                "age_type": "corrected_age",
                "corrected_gestational_age": corrected_gestational_age,
                "calendar_age": self.ages_object["measurement_dates"]["corrected_calendar_age"],
                "lay_comment": self.ages_object["measurement_dates"]["comments"]["lay_corrected_decimal_age_comment"],
                "clinician_comment": self.ages_object["measurement_dates"]["comments"]["clinician_corrected_decimal_age_comment"],
                "age_error": self.ages_object["measurement_dates"]["corrected_decimal_age_error"],
                "centile_band": self.calculated_measurements_object['measurement_calculated_values']["corrected_centile_band"],
                "observation_value_error": self.calculated_measurements_object["measurement_calculated_values"]["corrected_measurement_error"]
            },
        }

        # the final object is made up of these five components
        self.measurement = {
            'birth_data': self.ages_object['birth_data'],
            'measurement_dates': self.ages_object['measurement_dates'],
            'child_observation_value': self.calculated_measurements_object['child_observation_value'],
            'measurement_calculated_values': self.calculated_measurements_object['measurement_calculated_values'],
            'plottable_data': {
                "centile_data": self.plottable_centile_data,
                "sds_data": self.plottable_sds_data
            }
        }

    """
    These are 2 public class methods
    """

    def sds_and_centile_for_measurement_method(
        self,
        sex: str,
        corrected_age: float,
        chronological_age: float,
        observation_value_error: str,
        measurement_method: str,
        observation_value: float,
        reference: str,
        born_preterm: bool = False,
    ):

        # returns sds for given measurement
        # bmi must be supplied precalculated

        # calculate sds based on reference, age, measurement, sex and prematurity

        if corrected_age is None or chronological_age is None:
            # there has been an age calculation error. Further calculation impossible
            self.return_measurement_object = self.__create_measurement_object(
                measurement_method=measurement_method,
                observation_value=observation_value,
                observation_value_error=observation_value_error,
                corrected_sds_value=None,
                corrected_centile_value=None,
                corrected_centile_band=None,
                chronological_sds_value=None,
                chronological_centile_value=None,
                chronological_centile_band=None,
                chronological_measurement_error="Dates error. Calculations impossible.",
                corrected_measurement_error="Dates error. Calculations impossible."
            )
            return self.return_measurement_object

        try:
            corrected_measurement_sds = sds_for_measurement(reference=reference, age=corrected_age, measurement_method=measurement_method,
                                                            observation_value=observation_value, sex=sex, born_preterm=born_preterm)
        except Exception as err:
            corrected_measurement_error = f"{err}"
            corrected_measurement_sds = None

        try:
            chronological_measurement_sds = sds_for_measurement(reference=reference, age=chronological_age, measurement_method=measurement_method,
                                                                observation_value=observation_value, sex=sex, born_preterm=born_preterm)
        except LookupError as err:
            chronological_measurement_error = f"{err}"
            chronological_measurement_sds = None

        if chronological_measurement_sds is None:
            chronological_measurement_centile = None
            chronological_centile_band = None
        else:
            chronological_measurement_error = None
            try:
                chronological_measurement_centile = centile(
                    z_score=chronological_measurement_sds)
            except TypeError as err:
                chronological_measurement_error = "Not possible to calculate centile"
                chronological_measurement_centile = None
            try:
                chronological_centile_band = centile_band_for_centile(
                    sds=chronological_measurement_sds, measurement_method=measurement_method)
            except TypeError as err:
                chronological_measurement_error = "Not possible to calculate centile"
                chronological_centile_band = None

        if corrected_measurement_sds is None:
            corrected_measurement_centile = None
            corrected_centile_band = None
        else:
            corrected_measurement_error = None
            try:
                corrected_measurement_centile = centile(
                    z_score=corrected_measurement_sds)
            except TypeError as err:
                corrected_measurement_error = "Not possible to calculate centile"
                corrected_measurement_centile = None

            try:
                corrected_centile_band = centile_band_for_centile(
                    sds=corrected_measurement_sds, measurement_method=measurement_method)
            except TypeError as err:
                corrected_measurement_error = "Not possible to calculate centile"
                corrected_centile_band = None

        self.return_measurement_object = self.__create_measurement_object(
            measurement_method=measurement_method,
            observation_value=observation_value,
            observation_value_error=observation_value_error,
            corrected_sds_value=corrected_measurement_sds,
            corrected_centile_value=corrected_measurement_centile,
            corrected_centile_band=corrected_centile_band,
            chronological_sds_value=chronological_measurement_sds,
            chronological_centile_value=chronological_measurement_centile,
            chronological_centile_band=chronological_centile_band,
            chronological_measurement_error=chronological_measurement_error,
            corrected_measurement_error=corrected_measurement_error
        )

        return self.return_measurement_object

    """
    These are all private class methods and are only accessed by this class on initialisation
    """

    def __calculate_ages(
            self,
            sex: str,
            birth_date: date,
            observation_date: date,
            gestation_weeks: int = 0,
            gestation_days=0):

        if gestation_weeks == 0:
            # if gestation not specified, set to 40 weeks
            gestation_weeks = 40
        # calculate ages from dates and gestational ages at birth

        try:
            self.corrected_decimal_age = corrected_decimal_age(
                birth_date=birth_date,
                observation_date=observation_date,
                gestation_weeks=gestation_weeks,
                gestation_days=gestation_days)
        except Exception as err:
            self.corrected_decimal_age = None
            corrected_decimal_age_error = f"{err}"

        try:
            self.chronological_decimal_age = chronological_decimal_age(
                birth_date=birth_date,
                observation_date=observation_date)
        except Exception as err:
            self.chronological_decimal_age = None
            chronological_decimal_age_error = f"{err}"

        if self.corrected_decimal_age is None:
            self._age_comments = None
            self.lay_corrected_decimal_age_comment = None
            self.clinician_corrected_decimal_age_comment = None
        else:
            corrected_decimal_age_error = None
            try:
                self.age_comments = comment_prematurity_correction(
                    chronological_decimal_age=self.chronological_decimal_age,
                    corrected_decimal_age=self.corrected_decimal_age,
                    gestation_weeks=gestation_weeks,
                    gestation_days=gestation_days)
            except:
                self.age_comments = None
                corrected_decimal_age_error = "Error in comment on prematurity."

            try:
                self.lay_corrected_decimal_age_comment = self.age_comments['lay_corrected_comment']
            except:
                self.lay_corrected_decimal_age_comment = None
                corrected_decimal_age_error = "Error in comment on corrected decimal age."

            try:
                self.clinician_corrected_decimal_age_comment = self.age_comments[
                    'clinician_corrected_comment']
            except:
                self.clinician_corrected_decimal_age_comment = None
                corrected_decimal_age_error = "Error in comment on corrected decimal age."

        if chronological_decimal_age is None:
            self.chronological_calendar_age = None
            self.lay_chronological_decimal_age_comment = None
            self.clinician_chronological_decimal_age_comment = None
            self.corrected_gestational_age = None
            self.estimated_date_delivery = None
            self.estimated_date_delivery_string = None
        else:
            chronological_decimal_age_error = None
            try:
                self.chronological_calendar_age = chronological_calendar_age(
                    birth_date=birth_date,
                    observation_date=observation_date)
            except:
                self.chronological_calendar_age = None
                chronological_decimal_age_error = "Chronological age calculation error."

            try:
                self.lay_chronological_decimal_age_comment = self.age_comments[
                    'lay_chronological_comment']
            except:
                self.lay_chronological_decimal_age_comment = None
                chronological_decimal_age_error = "Chronological age calculation error."

            try:
                self.clinician_chronological_decimal_age_comment = self.age_comments[
                    'clinician_chronological_comment']
            except:
                self.clinician_chronological_decimal_age_comment = None
                chronological_decimal_age_error = "Chronological age calculation error."

            try:
                self.corrected_gestational_age = corrected_gestational_age(
                    birth_date=birth_date,
                    observation_date=observation_date,
                    gestation_weeks=gestation_weeks,
                    gestation_days=gestation_days)
            except:
                self.corrected_gestational_age = None
                chronological_decimal_age_error = "Corrected gestational age calculation error."

            try:
                self.estimated_date_delivery = estimated_date_delivery(
                    birth_date, gestation_weeks, gestation_days)
            except:
                self.estimated_date_delivery = None
                self.estimated_date_delivery_string = None
                chronological_decimal_age_error = "Estimated date of delivery calculation error."

            # ISSUE: #155 observation date COULD be before estimated date delivery in a preterm
            try:
                self.corrected_calendar_age = chronological_calendar_age(
                    self.estimated_date_delivery, observation_date)
            except:
                self.corrected_calendar_age = None
                if self.estimated_date_delivery > observation_date:
                    # ISSUE: #157 if observation date is BEFORE birth date then an error should be raised
                    chronological_decimal_age_error = "The due date is after the observation date - a calendar age cannot be calculated."
                else:
                    chronological_decimal_age_error = "A calendar age cannot be calculated."

            try:
                self.estimated_date_delivery_string = self.estimated_date_delivery.strftime(
                    '%a %d %B, %Y')
            except:
                self.estimated_date_delivery_string = None
                chronological_decimal_age_error = "Estimated date of delivery calculation error."

        birth_data = {
            "birth_date": birth_date,
            "gestation_weeks": gestation_weeks,
            "gestation_days": gestation_days,
            "estimated_date_delivery": self.estimated_date_delivery,
            "estimated_date_delivery_string": self.estimated_date_delivery_string,
            "sex": sex
        }

        measurement_dates = {
            "observation_date": observation_date,
            "chronological_decimal_age": self.chronological_decimal_age,
            "corrected_decimal_age": self.corrected_decimal_age,
            "chronological_calendar_age": self.chronological_calendar_age,
            "corrected_calendar_age": self.corrected_calendar_age,
            "corrected_gestational_age": {
                "corrected_gestation_weeks": self.corrected_gestational_age["corrected_gestation_weeks"],
                "corrected_gestation_days": self.corrected_gestational_age["corrected_gestation_days"],
            },
            "comments": {
                "clinician_corrected_decimal_age_comment": self.clinician_corrected_decimal_age_comment,
                "lay_corrected_decimal_age_comment": self.lay_corrected_decimal_age_comment,
                "clinician_chronological_decimal_age_comment": self.clinician_chronological_decimal_age_comment,
                "lay_chronological_decimal_age_comment": self.lay_chronological_decimal_age_comment
            },
            "corrected_decimal_age_error": corrected_decimal_age_error,
            "chronological_decimal_age_error": chronological_decimal_age_error
        }

        child_age_calculations = {
            "birth_data": birth_data,
            "measurement_dates": measurement_dates
        }
        return child_age_calculations

    def __create_measurement_object(
        self,
        measurement_method: str,
        observation_value: float,
        observation_value_error: str,
        corrected_sds_value: float,
        corrected_centile_value: float,
        corrected_centile_band: str,
        chronological_sds_value: float,
        chronological_centile_value: float,
        chronological_centile_band: str,
        chronological_measurement_error: str,
        corrected_measurement_error: str
    ):
        """
        private class method
        This is the end step, having calculated dates, SDS/Centiles and selected appropriate clinical advice,
        to then create a bespoke json Measurement object with values relevant only to the measurement_method requested
        @params: measurement_method: string accepting only 'height', 'weight', 'bmi', 'ofc' lowercase only
        """

        # Measurement object is made up of 4 JSON elements: "birth_data", "measurement_dates",
        #  "child_observation_value" and "measurement_calculated_values"
        # All Measurement objects return the "birth_data" and "measurement_dates" elements
        # Only those calculations relevant to the measurement_method requested populate the final JSON
        # object.

        if corrected_centile_value:
            if corrected_centile_value > 99 or corrected_centile_value < 1:
                corrected_centile_value = round(corrected_centile_value, 1)
            else:
                corrected_centile_value = int(corrected_centile_value)

        if chronological_centile_value:
            if chronological_centile_value > 99 or chronological_centile_value < 1:
                chronological_centile_value = round(
                    chronological_centile_value, 1)
            else:
                chronological_centile_value = int(chronological_centile_value)

        measurement_calculated_values = {
            "corrected_sds": corrected_sds_value,
            "corrected_centile": corrected_centile_value,
            "corrected_centile_band": corrected_centile_band,
            "chronological_sds": chronological_sds_value,
            "chronological_centile": chronological_centile_value,
            "chronological_centile_band": chronological_centile_band,
            "corrected_measurement_error": corrected_measurement_error,
            "chronological_measurement_error": chronological_measurement_error
        }

        child_observation_value = {
            "measurement_method": measurement_method,
            "observation_value": observation_value,
            "observation_value_error": observation_value_error
        }

        return {
            "child_observation_value": child_observation_value,
            "measurement_calculated_values": measurement_calculated_values,
        }

    def __validate_measurement_method(
            self,
            measurement_method: str,
            observation_value: float):

        # Private method which accepts a measurement_method (height, weight, bmi or ofc) and
        # and returns True if valid

        is_valid = False

        if measurement_method == 'bmi':
            if observation_value is None:
                raise ValueError(
                    'Missing observation_value for Body Mass Index. Please pass a Body Mass Index in kilograms per metre squared (kg/m2)')
            else:
                is_valid = True

        elif measurement_method == 'height':
            if observation_value is None:
                raise ValueError(
                    'Missing observation_value for height/length. Please pass a height/length in cm.')
            elif observation_value < 2:
                # most likely metres passed instead of cm.
                raise ValueError(
                    'Height/length must be passed in cm, not metres')
            elif observation_value < MINIMUM_LENGTH_CM:
                # a baby is unlikely to be < 30 cm long - probably a data entry error
                raise ValueError(
                    f'The height/length you have entered is very low and likely to be an error. Are you sure you meant a height of {observation_value} centimetres?')
            elif observation_value > MAXIMUM_HEIGHT_CM:
                raise ValueError(
                    f'The height/length you have entered is very high and likely to be an error. Are you sure you meant a height of {observation_value} centimetres?')
            else:
                is_valid = True

        elif measurement_method == 'weight':
            if observation_value is None:
                raise ValueError(
                    'Missing observation_value for weight. Please pass a weight in kilograms.')
            elif observation_value < MINIMUM_WEIGHT_KG:
                raise ValueError(
                    f'Error. {observation_value} kilograms is very low. Please pass an accurate weight in kilograms')
            elif observation_value > MAXIMUM_WEIGHT_KG:
                # it is likely the weight is passed in grams, not kg.
                raise ValueError(
                    f'{observation_value} kilograms is very high. Weight must be passed in kilograms.')
            else:
                is_valid = True

        elif measurement_method == 'ofc':
            if observation_value is None:
                raise ValueError(
                    'Missing observation_value for head circumference. Please pass a head circumference in centimetres.')
            elif observation_value < MINIMUM_OFC_CM:
                raise ValueError(
                    f'Please check this value: {observation_value}. A head circumference less than 5 centimetres is likely an error. Please pass an accurate head circumference in centimetres.')
            elif observation_value > MAXIMUM_OFC_CM:
                raise ValueError(
                    f'Please check this value: {observation_value}. A head circumference > 150 centimetres is likely an error. Please pass an accurate head circumference in cm.')
            else:
                is_valid = True

        return is_valid
