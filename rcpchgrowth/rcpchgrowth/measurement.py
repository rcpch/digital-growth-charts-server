from datetime import date
from pprint import pprint

from marshmallow import ValidationError

from .centile_bands import centile_band_for_centile
from .date_calculations import chronological_decimal_age, corrected_decimal_age, chronological_calendar_age, estimated_date_delivery, corrected_gestational_age
from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height
from .growth_interpretations import comment_prematurity_correction
from .global_functions import sds_for_measurement, measurement_from_sds, centile
from .constants import *
from .schemas import *


class Measurement:

    def __init__(
        self,
        sex: str,
        birth_date: date,
        observation_date: date,
        measurement_method: str,
        observation_value: float,
        reference: str,
        gestation_weeks: int = 0,
        gestation_days: int = 0
    ):
        """
        The Measurement Class is the gatekeeper to all the functions in the RCPCHGrowth package, although the public
        functions can be accessed independently. The bulk of the error handling happens here so be aware that calling
        other functions independently may yield unexpected results.

        It is initialised with the following Required parameters:

        `birth_date`: (Python datetime object) The date of birth of the subject.
        `observation_date`: (Python datetime object) The date that the observation was made.
        `measurement_type`: (string) 'height', 'weight', 'bmi' or 'ofc' only are accepted.
        `observation_value`: (float) The value of the height, weight, BMI or ofc observation.

        Additionally there are the following optional parameters:

        `gestation_weeks`: (integer) gestation at birth in weeks.
        `gestation_days`: (integer) supplemental days in addition to gestation_weeks at birth.
        `reference`: ENUM refering to which reference dataset to use: ['uk-who', 'turners-syndrome', 'trisomy-21']
        """

        self.sex = sex
        self.birth_date = birth_date
        self.observation_date = observation_date
        self.measurement_method = measurement_method
        self.observation_value = observation_value
        self.gestation_weeks = gestation_weeks
        self.gestation_days = gestation_days
        self.reference = reference

        # Validate using the Marshmallow Schema
        try:
            MeasurementClassSchema().load({
                sex,
                birth_date,
                observation_date,
                measurement_method,
                observation_value,
                gestation_weeks,
                gestation_days,
                reference
            })
        except ValidationError as err:
            pass  # pprint(err.messages)

        valid = self.__validate_measurement_method(
            measurement_method=measurement_method, observation_value=observation_value)
        if valid == False:
            return

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
        self.calculate_measurements_object = self.sds_and_centile_for_measurement_method(
            sex=self.sex,
            corrected_age=self.ages_object['measurement_dates']['corrected_decimal_age'],
            chronological_age=self.ages_object['measurement_dates']['chronological_decimal_age'],
            measurement_method=self.measurement_method,
            observation_value=self.observation_value,
            born_preterm=self.born_preterm,
            reference=self.reference
        )

        self.measurement = {
            'birth_data': self.ages_object['birth_data'],
            'measurement_dates': self.ages_object['measurement_dates'],
            'child_observation_value': self.calculate_measurements_object['child_observation_value'],
            'measurement_calculated_values': self.calculate_measurements_object['measurement_calculated_values']
        }

    """
    These are 2 public class methods
    """

    def sds_and_centile_for_measurement_method(
        self,
        sex: str,
        corrected_age: float,
        chronological_age: float,
        measurement_method: str,
        observation_value: float,
        reference: str,
        born_preterm: bool = False,
    ):

        # returns sds for given measurement
        # bmi must be supplied precalculated

        # calculate sds based on reference, age, measurement, sex and prematurity
        corrected_measurement_sds = sds_for_measurement(reference=reference, age=corrected_age, measurement_method=measurement_method,
                                              observation_value=observation_value, sex=sex, born_preterm=born_preterm)
        chronological_measurement_sds = sds_for_measurement(reference=reference, age=chronological_age, measurement_method=measurement_method,
                                              observation_value=observation_value, sex=sex, born_preterm=born_preterm)

        corrected_measurement_centile = centile(z_score=corrected_measurement_sds)
        chronological_measurement_centile = centile(z_score=chronological_measurement_sds)

        corrected_centile_band = centile_band_for_centile(
            sds=corrected_measurement_sds, measurement_method=measurement_method)
        chronological_centile_band = centile_band_for_centile(
            sds=chronological_measurement_sds, measurement_method=measurement_method)

        self.return_measurement_object = self.__create_measurement_object(
            measurement_method=measurement_method,
            observation_value=observation_value,
            corrected_sds_value=corrected_measurement_sds,
            corrected_centile_value=corrected_measurement_centile,
            corrected_centile_band=corrected_centile_band,
            chronological_sds_value=chronological_measurement_sds,
            chronological_centile_value=chronological_measurement_centile,
            chronological_centile_band=chronological_centile_band
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
        self.corrected_decimal_age = corrected_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        self.chronological_decimal_age = chronological_decimal_age(
            birth_date=birth_date,
            observation_date=observation_date)
        self.chronological_calendar_age = chronological_calendar_age(
            birth_date=birth_date,
            observation_date=observation_date)
        self.age_comments = comment_prematurity_correction(
            chronological_decimal_age=self.chronological_decimal_age,
            corrected_decimal_age=self.corrected_decimal_age,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)
        self.lay_decimal_age_comment = self.age_comments['lay_comment']
        self.clinician_decimal_age_comment = self.age_comments['clinician_comment']
        self.corrected_gestational_age = corrected_gestational_age(
            birth_date=birth_date,
            observation_date=observation_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days)  # return None if no correction necessary

        if gestation_weeks < 37 and gestation_weeks >= 24:
            # born preterm - may need correction (not if >32 weeks and >1 y, or <32 weeks and >2 y)
            # decision to correct is made in the date_calculations module
            # if baby is <42 weeks currently, decimal age reflects the corrected gestational age
            self.estimated_date_delivery = estimated_date_delivery(
                birth_date, gestation_weeks, gestation_days)
            self.corrected_calendar_age = chronological_calendar_age(
                self.estimated_date_delivery, observation_date)
            self.estimated_date_delivery_string = self.estimated_date_delivery.strftime(
                '%a %d %B, %Y')
        else:
            # term baby
            self.estimated_date_delivery = None
            self.estimated_date_delivery_string = None
            self.corrected_calendar_age = self.chronological_calendar_age

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
            "clinician_decimal_age_comment": self.clinician_decimal_age_comment,
            "lay_decimal_age_comment": self.lay_decimal_age_comment
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
        corrected_sds_value: float,
        corrected_centile_value: float,
        corrected_centile_band: str,
        chronological_sds_value: float,
        chronological_centile_value: float,
        chronological_centile_band: str,
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
                chronological_centile_value = round(chronological_centile_value, 1)
            else:
                chronological_centile_value = int(chronological_centile_value)

        measurement_calculated_values = {
            "measurement_method": measurement_method,
            "corrected_sds": corrected_sds_value,
            "corrected_centile": corrected_centile_value,
            "corrected_centile_band": corrected_centile_band,
            "chronological_sds": chronological_sds_value,
            "chronological_centile": chronological_centile_value,
            "chronological_centile_band": chronological_centile_band
        }

        child_observation_value = {
            "measurement_method": measurement_method,
            "observation_value": observation_value
        }

        return {
            "child_observation_value": child_observation_value,
            "measurement_calculated_values": measurement_calculated_values
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
                    f'The height/length you have entered is very low and likely to be an error. Are you sure you meant a height of{observation_value} centimetres?')
            elif observation_value > MAXIMUM_HEIGHT_CM:
                raise ValueError(
                    f'The height/length you have entered is very high and likely to be an error. Are you sure you meant a height of{observation_value} centimetres?')
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
