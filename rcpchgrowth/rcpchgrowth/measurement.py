from datetime import date
from .sds_calculations import sds, centile, percentage_median_bmi, measurement_from_sds
from .date_calculations import chronological_decimal_age, corrected_decimal_age, chronological_calendar_age, estimated_date_delivery, corrected_gestational_age
from .bmi_functions import bmi_from_height_weight, weight_for_bmi_height
from .growth_interpretations import interpret, comment_prematurity_correction
from .constants import TWENTY_FIVE_WEEKS_GESTATION, FORTY_TWO_WEEKS_GESTATION


class Measurement:

    def __init__(self, sex: str, birth_date: date, observation_date, gestation_weeks: int = 0, gestation_days: int = 0,):

        self.sex = sex
        self.birth_date = birth_date
        self.gestation_weeks = gestation_weeks
        self.gestation_days = gestation_days
        self.observation_date = observation_date
        
        self.height = None
        self.weight = None
        self.bmi = None
        self.ofc = None
        
        self.calculated_corrected_decimal_age = corrected_decimal_age(birth_date, observation_date, gestation_weeks, gestation_days)
        self.chronological_decimal_age = chronological_decimal_age(birth_date, observation_date)
        self.chronological_calendar_age = chronological_calendar_age(birth_date, observation_date)

        self.height_sds = 'None'
        self.height_centile="None"
        self.weight_sds = 'None'
        self.weight_centile='None'
        self.bmi_sds = 'None'
        self.bmi_centile='None'
        self.ofc_sds = 'None'
        self.ofc_centile='None'
        self.bmi = 'None'
        self.estimated_date_delivery = 'None'
        self.estimated_date_delivery_string = ""
        self.corrected_calendar_age = ''
        self.corrected_gestational_age = {}

        self.clinician_height_comment = ''
        self.clinician_weight_comment = ''
        self.clinician_bmi_comment = ''
        self.clinician_ofc_comment = ''
        self.lay_height_comment = ''
        self.lay_weight_comment = ''
        self.lay_bmi_comment = ''
        self.lay_ofc_comment = ''
        self.clinician_decimal_age_comment = ''
        self.lay_decimal_age_comment = ''

        self.return_measurement_object = {}

        age_comments = comment_prematurity_correction(self.chronological_decimal_age, self.calculated_corrected_decimal_age, self.gestation_weeks, self.gestation_days)
        self.lay_decimal_age_comment =  age_comments['lay_comment']
        self.clinician_decimal_age_comment = age_comments['clinician_comment']

        if self.chronological_decimal_age == self.calculated_corrected_decimal_age: ## assessment of need for correction made within the calculation functions
            self.calculated_corrected_decimal_age = 'None'
            self.age = self.chronological_decimal_age
            self.corrected_gestational_age = corrected_gestational_age(self.birth_date, self.observation_date, self.gestation_weeks, self.gestation_days) #return None as no correction necessary
        else:
            self.age = self.calculated_corrected_decimal_age
            self.estimated_date_delivery = estimated_date_delivery(self.birth_date, self.gestation_weeks, self.gestation_days)
            self.corrected_calendar_age = chronological_calendar_age(self.estimated_date_delivery, self.observation_date)
            self.estimated_date_delivery_string = self.estimated_date_delivery.strftime('%a %d %B, %Y')
            self.corrected_gestational_age = corrected_gestational_age(self.birth_date, self.observation_date, self.gestation_weeks, self.gestation_days)

    def calculate_height_sds_centile(self, height: float):
        if height and height > 0.0:
            self.height = height
            if self.age >= TWENTY_FIVE_WEEKS_GESTATION: # there is no length data below 25 weeks gestation
                self.height_sds = sds(self.age, 'height', self.height, self.sex)
                self.height_centile = centile(self.height_sds)
                comment = interpret('height', self.height_centile, self.age, self.sex)
                self.clinician_height_comment = comment["clinician_comment"]
                self.lay_height_comment = comment["lay_comment"]
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
                return self.return_measurement_object
            else:
                self.height_sds = None
                self.height_centile = None
                comment = interpret('height', self.height_centile, self.age, self.sex) # returns ref data error to user
                self.clinician_height_comment = comment["clinician_comment"]
                self.lay_height_comment = comment["lay_comment"]
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
                return self.return_measurement_object
        else:
            raise LookupError("Unable to return SDS or centile values for height")

    def calculate_weight_sds_centile(self, weight: float):
        if weight and weight > 0.0:
            self.weight = weight
            self.weight_sds = sds(self.age, 'weight', self.weight, self.sex)
            self.weight_centile = centile(self.weight_sds)
            comment = interpret('weight', self.weight_centile, self.age, self.sex)
            self.clinician_weight_comment = comment['clinician_comment']
            self.lay_weight_comment = comment['lay_comment']
            ## create return object
            self.return_measurement_object = self.__create_measurement_object()
            return self.return_measurement_object
        else:
            raise LookupError("Unable to return SDS or centile values for weight.")

    def calculate_ofc_sds_centile(self, ofc: float):
        if ofc and ofc > 0.0:
            self.ofc = ofc
            if (self.age <= 17 and self.sex == 'female') or (self.age <= 18.0 and self.sex == 'male'): # OFC data not present >17y in girls or >18y in boys
                self.ofc_sds = sds(self.age, 'ofc', self.ofc, self.sex)
                self.ofc_centile = centile(self.ofc_sds)
                comment = interpret('ofc', self.ofc_centile, self.age, self.sex)
                self.clinician_ofc_comment = comment['clinician_comment']
                self.lay_ofc_comment = comment['lay_comment']
                self.return_measurement_object = self.__create_measurement_object()
            else:
                self.ofc_sds = None
                self.ofc_centile = None
                comment = interpret('ofc', self.ofc_centile, self.age, self.sex)
                self.clinician_ofc_comment = comment['clinician_comment']
                self.lay_ofc_comment = comment['lay_comment']
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
            return self.return_measurement_object
        else:
            raise LookupError('Unable to return SDS or centile values for head circumference')

    def calculate_bmi_sds_centile(self, height: float = 0.0, weight: float = 0.0, bmi: float = 0.0):
        if (height and height > 0.0) and (weight and weight > 0.0):
            self.bmi = bmi_from_height_weight(height, weight)
            if self.age > FORTY_TWO_WEEKS_GESTATION: # BMI data not present < 42 weeks gestation
                self.bmi_sds = sds(self.age, 'bmi', self.bmi, self.sex)
                self.bmi_centile = centile(self.bmi_sds)
                comment = interpret('bmi', self.bmi_centile, self.age, self.sex)
                self.clinician_bmi_comment = comment['clinician_comment']
                self.lay_bmi_comment = comment['lay_comment']
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
            else:
                self.bmi_sds = None
                self.bmi_centile = None
                comment = interpret('bmi', self.bmi_centile, self.age, self.sex)
                self.clinician_bmi_comment = comment['clinician_comment']
                self.lay_bmi_comment = comment['lay_comment']
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
            return self.return_measurement_object
        elif bmi and bmi > 0.0:
            self.bmi = bmi
            comment = interpret('bmi', self.bmi_centile, self.age, self.sex)
            if self.age >= FORTY_TWO_WEEKS_GESTATION: # BMI data not present < 42 weeks gestation
                self.bmi_sds = sds(self.age, 'bmi', self.bmi, self.sex)
                self.bmi_centile = centile(self.bmi_sds)
                self.clinician_bmi_comment = comment['clinician_comment']
                self.lay_bmi_comment = comment['lay_comment']
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
            else:
                self.clinician_bmi_comment = comment['clinician_comment']
                self.lay_bmi_comment = comment['lay_comment']
                self.bmi_centile = None
                self.bmi_sds = None
                ## create return object
                self.return_measurement_object = self.__create_measurement_object()
            return self.return_measurement_object
        else:
            raise LookupError('Unable to return SDS or centile values for BMI')

    def __create_measurement_object(self):

        return {
                    "birth_data": {
                        "birth_date": self.birth_date, 
                        "gestation_weeks": self.gestation_weeks, 
                        "gestation_days": self.gestation_days, 
                        "edd": self.estimated_date_delivery, 
                        "edd_string": self.estimated_date_delivery_string,
                        "sex": self.sex
                    },

                    "measurement_dates": {
                        "obs_date": self.observation_date, 
                        "chronological_decimal_age": self.chronological_decimal_age, 
                        "corrected_decimal_age": self.calculated_corrected_decimal_age,
                        "chronological_calendar_age": self.chronological_calendar_age, 
                        "corrected_calendar_age": self.corrected_calendar_age, 
                        "corrected_gestational_age": {
                            "corrected_gestation_weeks": self.corrected_gestational_age["corrected_gestation_weeks"],
                            "corrected_gestation_days": self.corrected_gestational_age["corrected_gestation_days"],
                        }, 
                        "clinician_decimal_age_comment": self.clinician_decimal_age_comment, 
                        "lay_decimal_age_comment": self.lay_decimal_age_comment
                    }, 

                    "child_measurement_value": {
                        "height": self.height, 
                        "weight": self.weight, 
                        "bmi": self.bmi, 
                        "ofc": self.ofc
                    },

                    "measurement_calculated_values": {
                        "height_sds": self.height_sds, 
                        "height_centile": self.height_centile, 
                        "clinician_height_comment": self.clinician_height_comment, 
                        "lay_height_comment": self.lay_height_comment, 
                        "weight_sds": self.weight_sds, 
                        "weight_centile":self.weight_centile, 
                        "clinician_weight_comment": self.clinician_weight_comment, 
                        "lay_weight_comment": self.lay_weight_comment, 
                        "bmi_sds": self.bmi_sds,
                        "bmi_centile": self.bmi_centile,
                        "clinician_bmi_comment": self.clinician_bmi_comment, 
                        "lay_bmi_comment": self.lay_bmi_comment, 
                        "ofc_sds": self.ofc_sds, 
                        "ofc_centile": self.ofc_centile, 
                        "clinician_ofc_comment": self.clinician_ofc_comment, 
                        "lay_ofc_comment": self.lay_ofc_comment
                    } 
            }