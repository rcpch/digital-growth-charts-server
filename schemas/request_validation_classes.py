# standard imports
from datetime import date, datetime
from typing import Optional, Literal, Union, List

# third party imports
from pydantic import BaseModel, Field, field_validator, model_validator, PrivateAttr
from pydantic_core.core_schema import FieldValidationInfo


# local / rcpch imports
from rcpchgrowth.constants.reference_constants import TRISOMY_21, TURNERS, UK_WHO
import rcpchgrowth.constants.validation_constants as limits
from rcpchgrowth.constants.reference_constants import (
    COLE_TWO_THIRDS_SDS_NINE_CENTILES,
    THREE_PERCENT_CENTILES,
)
from rcpchgrowth.constants.validation_constants import (
    MINIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS,
    MAXIMUM_HEIGHT_WEIGHT_OFC_ERROR_SDS,
    MINIMUM_BMI_ERROR_SDS,
    MAXIMUM_BMI_ERROR_SDS,
)
from rcpchgrowth.global_functions import sds_for_measurement
from rcpchgrowth.date_calculations import corrected_decimal_age


class BirthMeasurementsMixin:
    gestation_days: Optional[int] = Field(
        0,
        ge=0,
        le=6,
        description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_weeks` - both are usually required.",
    )
    gestation_weeks: Optional[int] = Field(
        40,
        ge=limits.MINIMUM_GESTATION_WEEKS,
        le=limits.MAXIMUM_GESTATION_WEEKS,
        description="The number of completed weeks of gestation at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then 40 weeks (term) is assumed. **IMPORTANT: See also the other parameter `gestation_days` - both are usually required.**",
    )
    measurement_method: Literal["height", "weight", "ofc", "bmi"] = Field(
        ...,
        description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.",
    )
    birth_date: date = Field(
        ..., description="Date of birth of the patient, in the format YYYY-MM-DD"
    )
    sex: Literal["male", "female"] = Field(
        ...,
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted.",
    )

    @field_validator("birth_date", mode="before")
    def parse_date(cls, value):
        return datetime.strptime(value, "%Y-%m-%d").date()
    
    @field_validator("birth_date", mode="after")
    def birth_date_not_after_clinic_date(cls, v, info: FieldValidationInfo):
        if 'observation_date' in info.data and v > info.data['observation_date']:
            raise ValueError("Birth date cannot be after observation date.")
        return v


class ObservationMeasurementsMixin:
    observation_date: date = Field(
        ..., description="Date of the observation, in the format YYYY-MM-DD."
    )
    observation_value: float = Field(
        ...,
        description="The value of the measurement supplied. This is supplied as a floating point number. All measurements should be supplied as **centimetres**, with the exception of Body Mass Index which is supplied as kilograms per metre squared (kg/m²).",
    )
    bone_age: Optional[float] = Field(
        None,
        description="Bone age in years. Age is paired with measurement taken at chronological age.",
    )
    bone_age_type: Optional[
        Literal[
            "greulich-pyle",
            "tanner-whitehouse-ii",
            "tanner-whitehouse-iii",
            "fels",
            "bonexpert",
        ]
    ] = Field(
        None,
        description="Method used to calculate bone age. Must be one of `'greulich-pyle`, `tanner-whitehouse-ii`, `tanner-whitehouse-iii`, `fels`,`bonexpert`",
    )
    bone_age_sds: Optional[float] = Field(
        None, description="The SDS of the bone age based on reference tables."
    )
    bone_age_centile: Optional[float] = Field(
        None, description="The centile for the bone age based on reference tables."
    )
    bone_age_text: Optional[str] = Field(
        None,
        description="Any report or contextual information relating to the bone age.",
    )
    events_text: Optional[list] = Field(
        None,
        description="A list of strings. Contextual text which are associated with each measurement.",
    )


class MeasurementRequest(BaseModel, BirthMeasurementsMixin, ObservationMeasurementsMixin):
    """
    This class definition creates a Python model which can be converted by FastAPI to openAPI3 schema.
    We aim to specify all textual information, constraints, and validation here.
    It all ends up in the openAPI documentation, automagically.
    """
    pass

class ObservationMeasurement(BaseModel, ObservationMeasurementsMixin):
    pass


class BulkMeasurementRequest(BaseModel, BirthMeasurementsMixin):
    observations: List[ObservationMeasurement] = Field(
        ...,
        description="A list of observation objects",
    )


cole_centiles = COLE_TWO_THIRDS_SDS_NINE_CENTILES
three_percent_centiles = THREE_PERCENT_CENTILES


class ChartCoordinateRequest(BaseModel):
    sex: Literal["male", "female"] = Field(
        ...,
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted."
    )
    measurement_method: Literal["height", "weight", "ofc", "bmi"] = Field(
        ...,
        description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**."
    )
    is_sds: bool = Field(
        False,
        description="Boolean flag (default False) referring to centile_format. If custom lines requested as SDS, rather than as centiles, set this to True."
    )
    centile_format: Optional[
        Union[Literal["cole-nine-centiles", "extended-who-centiles", "three-percent-centiles", "five-percent-centiles", "eighty-five-percent-centiles"], List[float]]
    ] = Field(
        "cole-nine-centiles",
        description="Optional selection of centile format using 9 centile standard ['cole-nine-centiles'], or 'extended-who-centiles' [1, 3, 5, 10, 15, 50, 85, 90, 95, 97, 99], 'three-percent-centiles' [3.0, 10.0, 25.0, 50.0, 75.0, 90.0, 97.0], five-percent-centiles [5.0, 10.0, 25.0, 50.0, 75.0, 90.0, 95.0] or eight-five-percent-centiles as used in CDC BMI [3.0, 5.0, 10.0, 25.0, 50.0, 75.0, 85, 90.0, 95, 98.0, 99.0, 99.9, 99.99] or accepts a list of floats as a custom centile format e.g. [7/10/20/30/40/50/60/70/80/90/93]. Defaults to cole-nine-centiles"
    )

    @model_validator(mode='after')
    def custom_centiles_must_not_exceed_fifteen(cls, values):
        centile_format = values.centile_format
        is_sds = values.is_sds

        if isinstance(centile_format, list):
            if len(centile_format) > 15:
                raise ValueError("Centile/SDS formats cannot exceed 15 items.")
            if len(centile_format) < 1:
                raise ValueError(
                    "Empty list. Please provide at least one value or one of the standard collection flags."
                )
            if not is_sds:
                for cent in centile_format:
                    if cent < 0:
                        raise ValueError("Centile values cannot be negative.")
        return values


class FictionalChildRequest(BaseModel):
    measurement_method: Literal["height", "weight", "ofc", "bmi"] = Field(
        ...,
        description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**."
    )
    sex: Literal["male", "female"] = Field(
        ...,
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted."
    )
    start_chronological_age: Optional[float] = Field(
        0.0,
        description="Decimal age as a float. The age from which fictional data is to be generated."
    )
    end_age: Optional[float] = Field(
        20.0,
        description="Decimal age as float. Age until which fictional data is returned."
    )
    gestation_weeks: Optional[int] = Field(
        40,
        ge=limits.MINIMUM_GESTATION_WEEKS,
        le=limits.MAXIMUM_GESTATION_WEEKS,
        description="The number of completed weeks of gestation at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then 40 weeks (term) is assumed. **IMPORTANT: See also the other parameter `gestation_days` - both are usually required.**"
    )
    gestation_days: Optional[int] = Field(
        0,
        ge=0,
        le=6,
        description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_weeks` - both are usually required."
    )
    measurement_interval_type: Optional[
        Literal[
            "d",
            "day",
            "days",
            "w",
            "week",
            "weeks",
            "m",
            "month",
            "months",
            "y",
            "year",
            "years",
        ]
    ] = Field(
        "months",
        description="Interval type between fictional measurements as integer. Accepts days as ['d', 'day', 'days'], weeks as ['w', 'weeks', 'weeks'], months as ['m', 'month', 'months'] or years as ['y', 'year', 'years']"
    )
    measurement_interval_number: Optional[int] = Field(
        20,
        description="Interval length as integer between fictional measurements returned."
    )
    start_sds: Optional[float] = Field(
        0,
        description="Starting SDS as float. SDS value at which fictional data starts."
    )
    drift: bool = Field(
        False,
        description="Drift as boolean value. Default true. Selected if fictional measurements are intended to drift from starting SDS."
    )
    drift_range: Optional[float] = Field(
        -0.05,
        description="Drift range as float. Default is -0.05. The SDS drift expected over the requested age period."
    )
    noise: bool = Field(
        False,
        description="Noise as boolean. Default is false. Simulates measurement error.",
    )
    noise_range: Optional[float] = Field(
        0.005,
        description="Noise range as float. Prescribes the amount of measurement error generated randomly. Default is 0.5%"
    )


class MidParentalHeightRequest(BaseModel):
    height_paternal: float = Field(
        description="The height of the child's biological father, passed as float, measured in centimeters",
    )
    height_maternal: float = Field(
        description="The height of the child's biological mother, passed as float, measured in centimeters",
    )
    sex: Literal["male", "female"] = Field(
        ...,
        description="The sex of the patient, as a string value which can either be 'male' or 'female'. Abbreviations or alternatives are not accepted."
    )
    reference: Literal["uk-who", "cdc", "who"] = Field(
        default="uk-who",
        description="Selected reference as string. Case sensitive and accepts only one of ['uk-who', 'cdc']"
    )


"""
Validation has changed. Thes are values from the Guinness Book of Records and left here for interest.
They nolonger form part of the validation process.

the shortest man in the world was 54.6 cm Chandra Bahadur Dangi
the shortest woman in the world is Jyoti Kishanji Amge at 62.8 cm
the tallest woman ever to live is Rumeysa Gelgi (born 1979) is 215.16 cm
the tallest man at  272 cm was Robert Wadlow (1918-1940)

Validation now rejects heights < or > 8 SD
This calculation is made in the Utilities route and includes a check for heights < or > 8 SD against the reference supplied.
"""
