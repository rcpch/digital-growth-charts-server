from datetime import date
from .sds_calculations import sds, centile, percentage_median_bmi, measurement_from_sds
from .centile_bands import centile_band_for_centile
from .date_calculations import chronological_decimal_age, corrected_decimal_age, chronological_calendar_age, estimated_date_delivery, corrected_gestational_age
from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height
from .growth_interpretations import comment_prematurity_correction
from .constants import *


class Measurement:

    def __init__(
            self,
            sex: str,
            birth_date: date,
            observation_date,
            measurement_method: str,
            observation_value: float,
            gestation_weeks: int = 0,
            gestation_days: int = 0,
            default_to_youngest_reference: bool = False):
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
        `default_to_youngest_reference`: (boolean) If the request is for an age where 2 references overlap, the user
            can override the default to use the 'oldest' reference.
        """

        # self.measurement_method = measurement_type.measurement_method
        # self.observation_value = measurement_type.observation_value
        self.sex = sex
        self.birth_date = birth_date
        self.observation_date = observation_date
        self.measurement_method = measurement_method
        self.observation_value = observation_value
        self.gestation_weeks = gestation_weeks
        self.gestation_days = gestation_days
        self.default_to_youngest_reference = default_to_youngest_reference

        valid = self.__validate_measurement_method(
            measurement_method=measurement_method, observation_value=observation_value)
        if valid == False:
            return

        if gestation_weeks < 37 and gestation_weeks >= 23:
            self.born_preterm = True
        else:
            self.born_preterm = False

        # the age_object receives birth_data and measurement_dates objects
        self.ages_object = self.__calculate_ages(
            sex=self.sex,
            birth_date=self.birth_date,
            observation_date=self.observation_date,
            gestation_weeks=self.gestation_weeks,
            gestation_days=self.gestation_days)
        # the calculate_measurements_object receives the child_observation_value and measurement_calculated_values objects
        self.calculate_measurements_object = self.sds_and_centile_for_measurement_method(
            sex=self.sex,
            age=self.ages_object['measurement_dates']['corrected_decimal_age'],
            measurement_method=self.measurement_method,
            observation_value=self.observation_value,
            born_preterm=self.born_preterm,
            default_to_youngest_reference=self.default_to_youngest_reference)

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
            age: float,
            measurement_method: str,
            observation_value: float,
            born_preterm: bool = False,
            default_to_youngest_reference: bool = False):

        # returns sds for given measurement
        # bmi must be supplied precalculated

        if measurement_method == 'height':
            self.return_measurement_object = self.__calculate_height_sds_centile(
                sex=sex,
                age=age,
                height=observation_value,
                born_preterm=born_preterm,
                default_to_youngest_reference=default_to_youngest_reference)
        elif measurement_method == 'weight':
            self.return_measurement_object = self.__calculate_weight_sds_centile(
                sex=sex,
                age=age,
                weight=observation_value,
                born_preterm=born_preterm,
                default_to_youngest_reference=default_to_youngest_reference)
        elif measurement_method == 'bmi':
            self.return_measurement_object = self.__calculate_bmi_sds_centile(
                sex=sex,
                age=age,
                bmi=observation_value,
                born_preterm=born_preterm,
                default_to_youngest_reference=default_to_youngest_reference)
        elif measurement_method == 'ofc':
            self.return_measurement_object = self.__calculate_ofc_sds_centile(
                sex=sex,
                age=age,
                ofc=observation_value,
                born_preterm=born_preterm,
                default_to_youngest_reference=default_to_youngest_reference)
        else:
            raise ValueError(
                'Only the following measurement methods are accepted: height, weight, bmi or ofc')
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
            self.corrected_calendar_age = None

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

    def __calculate_height_sds_centile(
            self,
            sex: str,
            age: float,
            height: float,
            born_preterm: bool = False,
            default_to_youngest_reference: bool = False):
        """
        Private class method to return SDS and centile for height measurement
        """

        if height and height > 0.0:
            # there is no length data below 25 weeks gestation
            if age >= DECIMAL_AGES[TWENTY_FIVE_WEEKS_GESTATION_INDEX]:
                height_sds = sds(
                    age=age,
                    measurement_method='height',
                    measurement_value=height,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)
                height_centile = centile(height_sds)
                height_centile_band = centile_band_for_centile(
                    sds=height_sds, measurement_method="height")

            else:
                height_sds = None
                height_centile = None
                height_centile_band = ""

            return_measurement_object = self.__create_measurement_object(
                measurement_method='height',
                observation_value=height,
                sds_value=height_sds,
                centile_value=height_centile,
                centile_band=height_centile_band
            )
            return return_measurement_object
        else:
            raise LookupError(
                "Unable to return SDS or centile values for height")

    def __calculate_weight_sds_centile(
            self,
            sex: str,
            age: float,
            weight: float,
            default_to_youngest_reference: bool = False,
            born_preterm: bool = False):
        """
        private class method to return sds and centile for weight meaasurement
        """

        if weight and weight > 0.0:
            weight_sds = sds(
                age=age,
                measurement_method='weight',
                measurement_value=weight,
                sex=sex,
                default_to_youngest_reference=False,
                born_preterm=born_preterm)
            weight_centile = centile(weight_sds)
            weight_centile_band = centile_band_for_centile(
                sds=weight_sds, measurement_method="weight")

            # create return object
            return_measurement_object = self.__create_measurement_object(
                measurement_method='weight',
                observation_value=weight,
                sds_value=weight_sds,
                centile_value=weight_centile,
                centile_band=weight_centile_band
            )
            return return_measurement_object
        else:
            raise LookupError(
                "Unable to return SDS or centile values for weight.")

    def __calculate_bmi_sds_centile(
            self,
            sex: str,
            age: float,
            born_preterm: bool = False,
            default_to_youngest_reference: bool = False,
            bmi: float = 0.0):
        """
        This method calculates bmi SDS and centiles. It has been refactored and originally it took a
        height and weight in cm before calculating a bmi which then was used to generate SDS and centile.
        The Measurement_Type class now calculates BMI from height and weight and passes this to this method.
        The original ability to pass a height and weight is retained, but has essentially been deprecated
        and in future iterations is likely to be removed.
        """
        if bmi and bmi > 0.0:
            # BMI data not present < 42 weeks gestation
            if age >= DECIMAL_AGES[FORTY_TWO_WEEKS_GESTATION_INDEX]:
                bmi_sds = sds(
                    age=age,
                    measurement_method='bmi',
                    measurement_value=bmi,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)  # does not default to youngest reference
                bmi_centile = centile(z_score=bmi_sds)
                bmi_centile_band = centile_band_for_centile(
                    sds=bmi_sds,
                    measurement_method="bmi")
                # create return object
                return_measurement_object = self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile,
                    centile_band=bmi_centile_band
                )
            else:
                bmi_centile = None
                bmi_sds = None
                bmi_centile_band = ""

                # create return object
                return_measurement_object = self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile,
                    centile_band=bmi_centile_band

                )
            return return_measurement_object
        else:
            raise LookupError('Unable to return SDS or centile values for BMI')

    def __calculate_ofc_sds_centile(
            self,
            sex: str,
            age: float,
            ofc: float,
            default_to_youngest_reference: bool = False,
            born_preterm: bool = False):
        """
        private class method to calculate sds and centile for ofc
        """

        if ofc and ofc > 0.0:
            # OFC data not present >17y in girls or >18y in boys
            if (age <= 17 and sex == 'female') or (age <= 18.0 and sex == 'male'):
                ofc_sds = sds(
                    age=age,
                    measurement_method='ofc',
                    measurement_value=ofc,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)
                ofc_centile = centile(z_score=ofc_sds)
                ofc_centile_band = centile_band_for_centile(
                    sds=ofc_sds,
                    measurement_method="ofc")

                return_measurement_object = self.__create_measurement_object(
                    measurement_method='ofc',
                    observation_value=ofc,
                    sds_value=ofc_sds,
                    centile_value=ofc_centile,
                    centile_band=ofc_centile_band
                )
            else:
                ofc_sds = None
                ofc_centile = None
                ofc_centile_band = ""

                # create return object
                return_measurement_object = self.__create_measurement_object(
                    measurement_method='ofc',
                    observation_value=ofc,
                    sds_value=ofc_sds,
                    centile_value=ofc_centile,
                    centile_band=ofc_centile_band
                )
            return return_measurement_object
        else:
            raise LookupError(
                'Unable to return SDS or centile values for head circumference')

    def __create_measurement_object(
        self,
        measurement_method: str,
        observation_value: float,
        sds_value: float,
        centile_value: float,
        centile_band: str,
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

        if centile_value:
            if centile_value > 99 or centile_value < 1:
                centile_value = round(centile_value, 1)
            else:
                centile_value = int(centile_value)

        measurement_calculated_values = {
            "measurement_method": measurement_method,
            "sds": sds_value,
            "centile": centile_value,
            "centile_band": centile_band
        }

        child_observation_value = {
            "measurement_method": measurement_method,
            "measurement_value": observation_value
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
                raise ValueError('Missing value for BMI.')
            else:
                is_valid = True

        elif measurement_method == 'height':
            if observation_value is None:
                raise ValueError(
                    'Missing value for height. Please pass a height in cm.')
            elif observation_value < 2:
                # most likely metres passed instead of cm.
                raise AssertionError(
                    'Height must be passed in cm, not metres')
            elif observation_value < 30.0:
                # a baby is unlikely to be < 30 cm long - probably a data entry error
                raise AssertionError(
                    f'The height you have entered is very short. Are you sure you meant {observation_value} cm?')
            else:
                is_valid = True

        elif measurement_method == 'weight':
            if observation_value is None:
                raise ValueError(
                    'Missing value for weight. Please pass a weight in kilograms.')
            elif observation_value < 0.20:
                # 200g is very small. Like this is an error
                raise AssertionError(
                    f'Error. {observation_value} kg is very low. Please pass an accurate weight in kilograms')
            elif observation_value > 500.0:
                # it is likely the weight is passed in grams, not kg. The heaviest man according to google is
                # Jon Brower Minnoch (US), who had suffered from obesity since childhood. In September 1976,
                # he measured 185 cm (6 ft 1 in) tall and weighed 442 kg (974 lb; 69 st 9 lb)
                raise AssertionError(
                    f"{observation_value} kg is very high. Weight must be passed in kg.")
            else:
                is_valid = True

        elif measurement_method == 'ofc':
            if observation_value is None:
                raise ValueError(
                    'No value for head circumference. Please pass a head circumference in cm.')
            elif observation_value < 5.0:
                # A head circumference less than 5 cm is likely to be an error
                raise AssertionError(
                    f'{observation_value} cm is likely an error. Please pass an accurate head circumference in cm.')
            elif observation_value > 150.0:
                # A head circumference > 150 cm is likely to be an error
                raise AssertionError(
                    f'{observation_value} is likely an error. Please pass an accurate head circumference in cm.')
            else:
                is_valid = True

        return is_valid
