"""
In this file we define or import the response schemas
"""
# standard imports
from typing import Dict, List, Optional, Literal
from datetime import date

# third party imports
from pydantic import BaseModel


class CorrectedGestationalAge(BaseModel):
    corrected_gestation_weeks: Optional[int] = 40
    corrected_gestation_days: Optional[int] = 0


class Comments(BaseModel):
    clinician_corrected_decimal_age_comment: str
    lay_corrected_decimal_age_comment: str
    clinician_chronological_decimal_age_comment: str
    lay_chronological_decimal_age_comment: str


class ChronologicalDecimalAgeData(BaseModel):
    x: Optional[float]
    y: Optional[float]
    b: Optional[float] = None
    centile: Optional[float]
    sds: Optional[float]
    bone_age_label: Optional[str] = None
    events_text: Optional[list] = None
    bone_age_type: Optional[Literal['greulich-pyle',
                                    'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels', 'bonexpert']]
    bone_age_sds: Optional[str] = None
    bone_age_centile: Optional[str] = None
    observation_error: Optional[str]
    age_type: Literal["chronological_age", "corrected_age"]
    calendar_age: Optional[str]
    lay_comment: str
    clinician_comment: str
    age_error: Optional[str]
    centile_band: Optional[str]
    observation_value_error: Optional[str]


class CorrectedDecimalAgeData(BaseModel):
    x: Optional[float]
    y: Optional[float]
    b: Optional[float] = None
    centile: Optional[float]
    sds: Optional[float]
    bone_age_label: Optional[str] = None
    events_text: Optional[list] = None
    bone_age_type: Optional[Literal['greulich-pyle',
                                    'tanner-whitehouse-ii', 'tanner-whitehouse-iii', 'fels', 'bonexpert']]
    bone_age_sds: Optional[str] = None
    bone_age_centile: Optional[str] = None
    observation_error: Optional[str]
    age_type: Literal["chronological_age", "corrected_age"]
    calendar_age: Optional[str]
    corrected_gestational_age: Optional[str] = None
    lay_comment: str
    clinician_comment: str
    age_error: Optional[str]
    centile_band: Optional[str]
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
    gestation_weeks: Optional[int]
    gestation_days: Optional[int]
    estimated_date_delivery: Optional[date]
    estimated_date_delivery_string: Optional[str]
    sex: Literal['male', 'female']


class BoneAge(BaseModel):
    bone_age: Optional[float] = None
    bone_age_type: Optional[str] = None
    bone_age_sds: Optional[float] = None
    bone_age_centile: Optional[float] = None
    bone_age_text: Optional[str] = None


class EventsData(BaseModel):
    events_text: Optional[list] = None


class MeasurementDates(BaseModel):
    observation_date: date
    chronological_decimal_age: float
    corrected_decimal_age: float
    chronological_calendar_age: Optional[str]
    corrected_calendar_age: Optional[str]
    corrected_gestational_age: CorrectedGestationalAge
    comments: Comments
    corrected_decimal_age_error: Optional[str]
    chronological_decimal_age_error: Optional[str]


class ChildObservationValue(BaseModel):
    measurement_method: Literal['height', 'weight', 'ofc', 'bmi']
    observation_value: float
    observation_value_error: Optional[str]


class MeasurementCalculatedValues(BaseModel):
    corrected_sds: Optional[float]
    corrected_centile: Optional[float]
    corrected_centile_band: Optional[str]
    chronological_sds: Optional[float]
    chronological_centile: Optional[float]
    chronological_centile_band: Optional[str]
    corrected_measurement_error: Optional[str]
    chronological_measurement_error: Optional[str]
    corrected_percentage_median_bmi: Optional[float]
    chronological_percentage_median_bmi: Optional[float]


class MeasurementObject(BaseModel):
    birth_data: BirthData
    measurement_dates: MeasurementDates
    child_observation_value: ChildObservationValue
    measurement_calculated_values: MeasurementCalculatedValues
    plottable_data: PlottableData
    bone_age: BoneAge
    events_data: EventsData


class Data(BaseModel):
    l: str
    x: float
    y: Optional[float]


class Centile(BaseModel):
    sds: float
    centile: float
    data: Optional[List[Data]]


class MeasurementMethod(BaseModel):
    height: Optional[List[Centile]]
    weight: Optional[List[Centile]]
    ofc: Optional[List[Centile]]
    bmi: Optional[List[Centile]]


class Sex(BaseModel):
    male: Optional[MeasurementMethod]
    female: Optional[MeasurementMethod]


class ReferenceCreate(BaseModel):
    #__root__: Dict[str, Sex]
    root: Dict[str, Sex]
    # class Config:
    #     schema_extra = {
    #         "uk90_preterm": {
    #             "male": {
    #                 "height": [
    #                     {
    #                         "sds": -2.67,
    #                         "centile": 0.4,
    #                         "data": [
    #                             {
    #                                 "l": "0.4",
    #                                 "x": -0.2875,
    #                                 "y": 27.7419
    #                             },
    #                             {
    #                                 "l": "0.4",
    #                                 "x": -0.2683,
    #                                 "y": 28.7883
    #                             }
    #                         ]
    #                     }
    #                 ]
    #             }
    #         }
    #     }


class Centile_Data(BaseModel):
    centile_data: List[ReferenceCreate]


class MidParentalHeightResponse(BaseModel):
    mid_parental_height: float
    mid_parental_height_sds: float
    mid_parental_height_centile: float
    mid_parental_height_centile_data: List[ReferenceCreate]
    mid_parental_height_lower_centile_data: List[ReferenceCreate]
    mid_parental_height_upper_centile_data: List[ReferenceCreate]
    mid_parental_height_upper_value: Optional[float]
    mid_parental_height_lower_value: Optional[float]
