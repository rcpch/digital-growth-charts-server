"""
This file defines the schema for a Measurement object, enabling validation
"""

from marshmallow import Schema, fields, validate


class MeasurementClassSchema(Schema):
    """
    Marshmallow schema for Measurement class
    """
    sex = fields.String(
        required=True,
        validate=validate.OneOf(['male', 'female']),
        description="The sex of the patient, as a string value which can either be `male` or `female`. Abbreviations or alternatives are not accepted")

    birth_date = fields.Date(
        required=True,
        description="Date of birth of the patient, as a Python Date object.")

    observation_date = fields.Date(
        required=True,
        description="The date that the measurement was taken, as a Python Date object.")

    measurement_method = fields.String(
        required=True,
        validate=validate.OneOf(["height", "weight", "bmi", "ofc"]),
        description="The type of measurement performed on the infant or child as a string which can be `height`, `weight`, `bmi` or `ofc`. The value of this measurement is supplied as the `observation_value` parameter. The measurements represent height **in centimetres**, weight *in kilograms**, body mass index **in kilograms/metre²** and occipitofrontal circumference (head circumference, OFC) **in centimetres**.")

    observation_value = fields.Float(
        required=True,
        description="The value of the measurement supplied. This is supplied as a floating point Python number")

    reference = fields.String(
        required=True,
        validate=validate.OneOf(["uk-who", "turners-syndrome", "trisomy-21"]),
        description="The set of references to use for calculation of all the parameters. This can is selected by passing a string which can be 'uk-who', 'turners-syndrome', or 'trisomy-21'. For most UK applications, 'uk-who' is the correct reference. 'turners-syndrome' and 'trisomy-21' are specialist references for use in patients with specific medical conditions, and are more likely to be used only in a specialist context. Use of the incorrect reference will result in totally incorrect data, please ensure you know which data set you wish to use. Contact the RCPCH Growth Charts team if you need help or want to add a new reference")

    gestation_weeks = fields.Number(
        description="The number of completed weeks of gestation at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_days` - both are usually required.")

    gestation_days = fields.Number(
        description="The number of additional days _beyond the completed weeks of gestation_ at which the patient was born, passed as an integer. Supplying this data enables Gestational Age correction if the child was not born at term. If no gestational age is passed then term is assumed. IMPORTANT: See also the other parameter `gestation_weeks` - both are usually required.")
