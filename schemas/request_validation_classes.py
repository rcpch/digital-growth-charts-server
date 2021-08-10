# standard imports
from datetime import date, datetime
from typing import Optional, Literal

# third party imports
from pydantic import BaseModel, Field, validator

# local / rcpch imports
from rcpchgrowth.constants.reference_constants import TRISOMY_21, TURNERS, UK_WHO
import rcpchgrowth.constants.validation_constants as limits



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
                                
    @validator("birth_date", pre=True)
    def parse_date(cls, value):
        return datetime.strptime(
            value,
            "%Y-%m-%d"
        ).date()

class ChartCoordinateRequest(BaseModel):
    sex: Literal['male', 'female']
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi']

class FictionalChildRequest(BaseModel):
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi']
    sex: Literal['male', 'female']
    start_chronological_age: Optional[float] = 0.0
    end_age: Optional[float] = 20.0
    gestation_weeks: Optional[int] = 40
    gestation_days: Optional[int] = 0
    measurement_interval_type: Literal['d', 'day', 'days', 'w', 'week', 'weeks', 'm', 'month', 'months', 'y', 'year', 'years'] = "days"
    measurement_interval_number: Optional[int] = 20
    start_sds: Optional[float] = 0
    drift: bool = False
    drift_range: Optional[float] = -0.05
    noise: bool = False
    noise_range: Optional[float] = 0.005
    reference: Literal["uk-who", "trisomy-21", "turners-syndrome"]
