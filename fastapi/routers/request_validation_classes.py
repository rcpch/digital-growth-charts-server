from pydantic import BaseModel, validator
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