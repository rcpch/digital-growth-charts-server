from rcpchgrowth.constants.reference_constants import TRISOMY_21, TURNERS, UK_WHO
from pydantic import BaseModel, validator, StrictBool
from typing import Optional, Literal
from datetime import date, datetime

class MeasurementRequest(BaseModel):
    birth_date: date
    observation_date: date
    observation_value: float
    sex: Literal['male', 'female']
    gestation_weeks: Optional[int]=40
    gestation_days: Optional[int]=0
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi']
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