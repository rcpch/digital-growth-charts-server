# third-party imports
from marshmallow import Schema, fields, validate

# rcpch imports
from .measurement_schemas import MeasurementResponseSchema
from rcpchgrowth import constants

class CalculationRequestParameters(Schema):
    """
    Defines the schema that the API expects to receive. This is compiled into the openAPI spec, and used for data validation
    """

    birth_date = fields.Date(
        required=True,
        description="Date of birth of the patient in `YYYY-MM-DD` format. Other formats such as the FHIR/ISO YYYY-MM-DDTHH:MM:SS and those that include milliseconds and timezones will be accepted but everything after the T will be discarded in processing. Time of day and time zone are not taken into account by the centile/SDS calculation")
    gestation_days = fields.Number(
        description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born. This enables Gestational Age correction if the child was not born at term. See also the other parameter `gestation_weeks` - both are usually required.")
    gestation_weeks = fields.Number(
        validate=validate.Range(
            min=constants.validation_constants.MINIMUM_GESTATION_WEEKS, max=constants.validation_constants.MAXIMUM_GESTATION_WEEKS),
        description="The number of completed weeks of gestation at which the patient was born. This enables Gestational Age Correction if the child was not born at term. See also the other parameter `gestation_days` - both are usually required. If the child is term then any value between 37 and 42 will be handled the same, and a value must be provided. Values outside the validation range will return errors.")
    measurement_method = fields.String(
        required=True,
        enum=["height", "weight", "bmi", "ofc"],
        validate=validate.OneOf(["height", "weight", "bmi", "ofc"]),
        description="The type of measurement performed on the infant or child (`height`, `weight`, `bmi` or `ofc`). The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.")
    observation_date = fields.Date(
        required=True,
        description="The date that the measurement was taken, in `YYYY-MM-DD` format.  Other formats such as the FHIR/ISO YYYY-MM-DDTHH:MM:SS and those that include milliseconds and timezones will be accepted but everything after the T will be discarded in processing. Time of day and time zone are not taken into account by the centile/SDS calculation")
    observation_value = fields.Float(
        required=True,
        description="The value of the measurement supplied. Used in conjunction with type of measurement performed(`height`, `weight`, `bmi` or `ofc`) on the infant or child.")
    sex = fields.String(
        required=True,
        enum=['male', 'female'],
        validate=validate.OneOf(['male', 'female']),
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted")


class CalculationResponseSchema(Schema):
    """
    Defines the schema of the API response. This is compiled into the openAPI spec.
    """

    calculation = fields.Nested(MeasurementResponseSchema())
