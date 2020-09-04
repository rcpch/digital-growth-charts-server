from datetime import date
from .sds_calculations import sds, centile, percentage_median_bmi, measurement_from_sds
from .date_calculations import chronological_decimal_age, corrected_decimal_age, chronological_calendar_age, estimated_date_delivery, corrected_gestational_age
from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height
from .growth_interpretations import comment_prematurity_correction
from .constants import TWENTY_FIVE_WEEKS_GESTATION, FORTY_TWO_WEEKS_GESTATION, THIRTY_SEVEN_WEEKS_GESTATION
from .measurement_type import Measurement_Type


class Measurement:

    def __init__(
            self,
            sex: str,
            birth_date: date,
            observation_date,
            measurement_type: Measurement_Type,
            gestation_weeks: int = 0,
            gestation_days: int = 0,
            default_to_youngest_reference: bool = False):

        """
        The Measurement Class is the gatekeeper to all the functions in the RCPCHGrowth package, although the public
        functions can be accessed independently. The bulk of the error handling happens here so be aware that calling 
        other functions independently may yield unexpected results.
        It is initialised with this parameters:
        birth_date (Python datetime object)
        observation_date (Python object)
        measurement_type: Custom class Measurement_Type (see documentation separately): attributes include a string
            'height', 'weight', 'bmi' or 'ofc', and an observation_value (float)
        Optional parameters:
        gestation_weeks: gestation at birth in weeks (integer)
        gestation_days: supplemental days in addition to gestation_weeks at birth (integer)
        default_to_youngest_reference: boolean. If the request is for an age where 2 references overlap, the user 
            can override the default to use the 'oldest' one

        # Measurement object is made up of 4 JSON elements: "birth_data", "measurement_dates",
        #  "child_observation_value" and "measurement_calculated_values"
        # All Measurement objects return the "birth_data" and "measurement_dates" elements
        # Only those calculations relevant to the measurement_type requested populate the final JSON 
        # object.

        NOTE - THE ADVICE STRINGS HAVE BEEN DEPRECATED AS OF JULY 2020 - THE CALLS AND FUNCTION REMAIN IN PLACE,
        BUT THE STRINGS BEEN COMMENTED OUT IN THE FINAL JSON
        """

        self.measurement_method = measurement_type.measurement_method
        self.observation_value = measurement_type.observation_value

        if gestation_weeks < 37 and gestation_weeks >= 23:
            born_preterm = True
        else:
            born_preterm = False

        # the age_object receives birth_data and measurement_dates objects
        ages_object = self.__calculate_ages(
            sex=sex,
            birth_date=birth_date,
            observation_date=observation_date,
            gestation_weeks=gestation_weeks,
            gestation_days=gestation_days
        )

        # the calculate_measurements_object receives the child_observation_value and measurement_calculated_values objects
        calculate_measurements_object = self.sds_and_centile_for_measurement_method(
            sex=sex,
            age=ages_object['measurement_dates']['corrected_decimal_age'],
            measurement_method=self.measurement_method,
            observation_value=self.observation_value,
            born_preterm=born_preterm,
            default_to_youngest_reference=default_to_youngest_reference
        )

        self.measurement = {
            'birth_data': ages_object['birth_data'],
            'measurement_dates': ages_object['measurement_dates'],
            'child_observation_value': calculate_measurements_object['child_observation_value'],
            'measurement_calculated_values': calculate_measurements_object['measurement_calculated_values']
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

        if height and height > 0.0:
            if age >= TWENTY_FIVE_WEEKS_GESTATION:  # there is no length data below 25 weeks gestation
                height_sds = sds(
                    age=age,
                    measurement='height',
                    measurement_value=height,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)
                height_centile = centile(height_sds)
            else:
                height_sds = None
                height_centile = None
            return self.__create_measurement_object(
                measurement_method='height',
                observation_value=height,
                sds_value=height_sds,
                centile_value=height_centile)
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

        if weight and weight > 0.0:
            weight_sds = sds(
                age=age,
                measurement='weight',
                measurement_value=weight,
                sex=sex,
                default_to_youngest_reference=False,
                born_preterm=born_preterm)           
            weight_centile = centile(weight_sds)
            return self.__create_measurement_object(
                measurement_method='weight',
                observation_value=weight,
                sds_value=weight_sds,
                centile_value=weight_centile)
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
        height: float = 0.0,
        weight: float = 0.0,
        bmi: float = 0.0):

        """
        This method calculates bmi SDS and centiles. It has been refactored and originally it took a
        height and weight in cm before calculating a bmi which then was used to generate SDS and centile.
        The Measurement_Type class now calculates BMI from height and weight and passes this to this method.
        The original ability to pass a height and weight is retained, but has essentially been deprecated 
        and in future iterations is likely to be removed.
        """
        if (height and height > 0.0) and (weight and weight > 0.0):
            bmi = bmi_from_height_weight(height, weight)
            if age > FORTY_TWO_WEEKS_GESTATION:  # BMI data not present < 42 weeks gestation
                bmi_sds = sds(age=age,
                    measurement='bmi',
                    measurement_value=bmi,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)  # does not default to youngest reference
                bmi_centile = centile(z_score=bmi_sds)
                return self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile)
            else:
                bmi_sds = None
                bmi_centile = None
                return self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile)
        elif bmi and bmi > 0.0:
            if age >= FORTY_TWO_WEEKS_GESTATION:  # BMI data not present < 42 weeks gestation
                bmi_sds = sds(
                    age=age,
                    measurement='bmi',
                    measurement_value=bmi,
                    sex=sex,
                    default_to_youngest_reference=default_to_youngest_reference,
                    born_preterm=born_preterm)  # does not default to youngest reference
                bmi_centile = centile(z_score=bmi_sds)
                return self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile)
            else:
                bmi_centile = None
                bmi_sds = None
                return self.__create_measurement_object(
                    measurement_method='bmi',
                    observation_value=bmi,
                    sds_value=bmi_sds,
                    centile_value=bmi_centile)
        else:
            raise LookupError('Unable to return SDS or centile values for BMI')

    def __calculate_ofc_sds_centile(
        self,
        sex: str,
        age: float,
        ofc: float,
        default_to_youngest_reference: bool = False,
        born_preterm: bool = False):

        if ofc and ofc > 0.0:
            # OFC data not present >17y in girls or >18y in boys
            if (age <= 17 and sex == 'female') or (age <= 18.0 and sex == 'male'):
                ofc_sds = sds(age=age, measurement='ofc', measurement_value=ofc, sex=sex,
                              default_to_youngest_reference=default_to_youngest_reference, born_preterm=born_preterm)
                ofc_centile = centile(z_score=ofc_sds)
                return self.__create_measurement_object(
                    measurement_method='ofc',
                    observation_value=ofc,
                    sds_value=ofc_sds,
                    centile_value=ofc_centile)
            else:
                ofc_sds = None
                ofc_centile = None
                return self.__create_measurement_object(
                    measurement_method='ofc',
                    observation_value=ofc,
                    sds_value=ofc_sds,
                    centile_value=ofc_centile)
        else:
            raise LookupError(
                'Unable to return SDS or centile values for head circumference')

    def __create_measurement_object(
        self,
        measurement_method: str,
        observation_value: float,
        sds_value: float,
        centile_value: float):

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

        measurement_calculated_values = {
            "measurement_method": measurement_method,
            "sds": sds_value,
            "centile": centile_value,
        }

        child_observation_value = {
            "measurement_method": measurement_method,
            "measurement_value": observation_value
        }

        return {
            "child_observation_value": child_observation_value,
            "measurement_calculated_values": measurement_calculated_values
        }
