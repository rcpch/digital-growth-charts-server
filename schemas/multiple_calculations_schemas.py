from marshmallow import Schema, fields
from .measurement_schemas import MeasurementResponseSchema


class MultipleCalculationsRequestParameters(Schema):
    # Defines the schema that the API expects to receive. This is compiled into the openAPI spec, and used for data validation
    birth_date = fields.Date(
        required=True,
        description="Date of birth of the patient in YYYY-MM-DD ISO8601 format.")
    observation_date = fields.Date(
        required=True,
        description="The date that the measurement was taken, in YYYY-MM-DD ISO8601 format.")
    height = fields.Number(
        description="The height of the patient, which MUST be in centimetres to get correct results.")
    weight = fields.Number(
        description="The weight of the patient, which MUST be in kilograms to get correct results.")
    ofc = fields.Number(
        description="The head circumference (also described as occipito-frontal circumference, or 'OFC') of the patient, which **must** be in centimetres to get correct results.")
    sex = fields.String(
        required=True,
        enum=['male', 'female'],
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted")
    gestation_weeks = fields.Number(
        description="The number of completed weeks of gestation at which the patient was born. This enables Gestational Age correction if the child was not born at term. See also the other parameter `gestation_days` - both are usually required.")
    gestation_days = fields.Number(
        description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born. This enables Gestational Age correction if the child was not born at term. See also the other parameter `gestation_weeks` - both are usually required.")


class MultipleCalculationsResponseSchema(Schema):
    # Defines the schema of the API response. This is compiled into the openAPI spec.
    height = fields.Nested(MeasurementResponseSchema())
    weight = fields.Nested(MeasurementResponseSchema())
