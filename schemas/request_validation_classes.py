# standard imports
from datetime import date, datetime
from typing import Optional, Literal

# third party imports
from pydantic import BaseModel, Field, validator
from rcpchgrowth import constants

# local / rcpch imports
from rcpchgrowth.constants.reference_constants import TRISOMY_21, TURNERS, UK_WHO
import rcpchgrowth.constants.validation_constants as limits
from rcpchgrowth.constants.reference_constants import COLE_TWO_THIRDS_SDS_NINE_CENTILES, THREE_PERCENT_CENTILES, CENTILE_FORMATS



class MeasurementRequest(BaseModel):
    """
    This class definition creates a Python model which can be converted by FastAPI to openAPI3 schema.
    We aim to specify all textual information, constraints, and validation here.
    It all ends up in the openAPI documentation, automagically.
    """
    birth_date: date = Field(
        ..., description="Date of birth of the patient, in the format YYYY-MM-DD")
    gestation_days: Optional[int] = Field(
        0, ge=0, le=6, description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_weeks` - both are usually required.")
    gestation_weeks: Optional[int] = Field(
        40, ge=limits.MINIMUM_GESTATION_WEEKS, le=limits.MAXIMUM_GESTATION_WEEKS, description="The number of completed weeks of gestation at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then 40 weeks (term) is assumed. **IMPORTANT: See also the other parameter `gestation_days` - both are usually required.**")
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi'] = Field(
        ..., description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.")
    observation_date: date = Field(
        ..., description="Date of the observation, in the format YYYY-MM-DD.")
    observation_value: float = Field(
        ..., description="The value of the measurement supplied. This is supplied as a floating point number. All measurements should be supplied as **centimetres**, with the exception of Body Mass Index which is supplied as kilograms per metre squared (kg/m²).")
    sex: Literal['male', 'female'] = Field(
        ..., description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted.")
    bone_age: Optional[float] = Field(None, description="Bone age in years. Age is paired with measurement taken at chronological age.")
    bone_age_type: Optional[Literal['greulich-pyle', 'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels','bonexpert']] = Field(None, description="Method used to calculate bone age. Must be one of `'greulich-pyle`, `tanner-whitehouse-ii`, `tanner-whitehouse-iii`, `fels`,`bonexpert`")
    bone_age_sds: Optional[float] = Field(None, description="The SDS of the bone age based on reference tables.")
    bone_age_centile: Optional[float] = Field(None, description="The centile for the bone age based on reference tables.")
    bone_age_text: Optional[str] = Field(None, description="Any report or contextual information relating to the bone age.")
    events_text: Optional[list] = Field(None, description="A list of strings. Contextual text which are associated with each measurement.")

    @validator("birth_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()


cole_centiles = COLE_TWO_THIRDS_SDS_NINE_CENTILES
three_percent_centiles = THREE_PERCENT_CENTILES
class ChartCoordinateRequest(BaseModel):
    sex: Literal['male', 'female'] = Field(
        ..., description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted.")
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi'] = Field(
        ..., description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.")
    centile_format: Optional[Literal["cole-nine-centiles", "three-percent-centiles"]]=Field('cole-nine-centiles', description="Optional selection of centile format using 9 centile standard ['nine-centiles'], or older three-percent centile format ['three-percent-centiles']. Defaults to cole-nine-centiles")

class FictionalChildRequest(BaseModel):
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi'] = Field(
        ..., description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.")
    sex: Literal['male', 'female'] = Field(
        ..., description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted.")
    start_chronological_age: Optional[float] = Field(0.0, description="Decimal age as a float. The age from which fictional data is to be generated.")
    end_age: Optional[float] = Field(20.0, description="Decimal age as float. Age until which fictional data is returned.")
    gestation_weeks: Optional[int] = Field(
        40, ge=limits.MINIMUM_GESTATION_WEEKS, le=limits.MAXIMUM_GESTATION_WEEKS, description="The number of completed weeks of gestation at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then 40 weeks (term) is assumed. **IMPORTANT: See also the other parameter `gestation_days` - both are usually required.**")
    gestation_days: Optional[int] = Field(
        0, ge=0, le=6, description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_weeks` - both are usually required.")
    measurement_interval_type: Optional[Literal['d', 'day', 'days', 'w', 'week', 'weeks', 'm', 'month', 'months', 'y', 'year', 'years']] = Field("months", description="Interval type between fictional measurements as integer. Accepts days as ['d', 'day', 'days'], weeks as ['w', 'weeks', 'weeks'], months as ['m', 'month', 'months'] or years as ['y', 'year', 'years']")
    measurement_interval_number: Optional[int] = Field(20, description="Interval length as integer between fictional measurements returned.")
    start_sds: Optional[float] = Field(0, description="Starting SDS as float. SDS value at which fictional data starts.")
    drift: bool = Field(False, description="Drift as boolean value. Default true. Selected if fictional measurements are intended to drift from starting SDS.")
    drift_range: Optional[float] = Field(-0.05, description="Drift range as float. Default is -0.05. The SDS drift expected over the requested age period.")
    noise: bool = Field(False, description="Noise as boolean. Default is false. Simulates measurement error.")
    noise_range: Optional[float] = Field(0.005, description="Noise range as float. Prescribes the amount of measurement error generated randomly. Default is 0.5%")
    reference: Optional[Literal["uk-who", "trisomy-21", "turners-syndrome"]] = Field('uk-who', description="Selected reference as string. Case sensitive and accepts only once of ['uk-who', 'trisomy-21', 'turners-syndrome']")

class MidParentalHeightRequest(BaseModel):
    height_paternal: float = Field(
        gt=0, description="The height of the child's biological father, passed as float, measured in centimeters")
    height_maternal: float = Field(
        gt=0, description="The height of the child's biological mother, passed as float, measured in centimeters")
    sex: Literal['male', 'female'] = Field(
        ..., description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted.")
    