"""
In this file we define or import the response schemas
"""
# standard imports

# third party imports

# local / rcpch imports
# from rcpchgrowth.schemas import MeasurementResponseSchema

from datetime import date

from typing import Optional, Literal

from fastapi import FastAPI
from pydantic import BaseModel

class CorrectedGestationalAge(BaseModel):
    corrected_gestation_weeks: int
    corrected_gestation_days: int
class Comments(BaseModel):
    clinician_corrected_decimal_age_comment: str
    lay_corrected_decimal_age_comment: str
    clinician_chronological_decimal_age_comment: str
    lay_chronological_decimal_age_comment: str

class ChronologicalDecimalAgeData(BaseModel):
    x: float
    y: float
    b: Optional[float]=None
    bone_age_label: Optional[str]=None
    events_label: Optional[list]=None
    bone_age_type: Optional[Literal['greulich-pyle', 'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels','bonexpert']]
    bone_age_sds: Optional[str]=None
    bone_age_centile: Optional[str]=None
    observation_error: Optional[str]
    age_type: Literal["chronological_age", "corrected_age"]
    calendar_age: str
    lay_comment: str
    clinician_comment: str
    age_error: Optional[str]
    centile_band: str
    observation_value_error: Optional[str]
class CorrectedDecimalAgeData(BaseModel):
    x: float
    y: float
    b: Optional[float]=None
    bone_age_label: Optional[str]=None
    events_label: Optional[list]=None
    bone_age_type: Optional[Literal['greulich-pyle', 'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels','bonexpert']]
    bone_age_sds: Optional[str]=None
    bone_age_centile: Optional[str]=None
    observation_error: Optional[str]
    age_type: Literal["chronological_age", "corrected_age"]
    calendar_age: str
    lay_comment: str
    clinician_comment: str
    age_error: Optional[str]
    centile_band: str
    observation_value_error: Optional[str]

class CentileData(BaseModel):
    chronological_decimal_age_data: ChronologicalDecimalAgeData
    corrected_decimal_age_data: CorrectedDecimalAgeData

class SDSData(BaseModel):
    chronological_decimal_age_data: ChronologicalDecimalAgeData
    corrected_decimal_age_data: CorrectedDecimalAgeData

class PlottableData(BaseModel):
    centile_data: CentileData
    sds_data: SDSData
class BirthData(BaseModel):
    birth_date: date
    gestation_weeks: int
    gestation_days: int
    estimated_date_delivery: str
    estimated_date_delivery_string: str
    sex: Literal['male', 'female']

class BoneAge(BaseModel):
    bone_age: Optional[float]=None
    bone_age_type: Optional[str]=None
    bone_age_sds: Optional[float]=None
    bone_age_centile: Optional[float]=None
    bone_age_text: Optional[str]=None

class EventsData(BaseModel):
    events_text: Optional[list]=None
class MeasurementDates(BaseModel):
    observation_date: date
    chronological_decimal_age: float
    corrected_decimal_age: float
    chronological_calendar_age: str
    corrected_calendar_age: str
    corrected_gestational_age: CorrectedGestationalAge
    comments: Comments
    corrected_decimal_age_error: Optional[str]
    chronological_decimal_age_error: Optional[str]

class ChildObservationValue(BaseModel):
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi']
    observation_value: float
    observation_value_error: Optional[str]

class MeasurementCalculatedValues(BaseModel):
    corrected_sds: float
    corrected_centile: float
    corrected_centile_band: str
    chronological_sds: float
    chronological_centile: float
    chronological_centile_band: str
    corrected_measurement_error: Optional[str]
    chronological_measurement_error: Optional[str]
    corrected_percentage_median_bmi: float
    chronological_percentage_median_bmi: float

class MeasurementObject(BaseModel):
    birth_data: BirthData
    measurement_dates: MeasurementDates
    child_observation_value: ChildObservationValue
    measurement_calculated_values: MeasurementCalculatedValues
    plottable_data: PlottableData
    bone_age: BoneAge
    events_data: EventsData
