from marshmallow import Schema, fields
from .measurement_schemas import MeasurementResponseSchema


class ChartDataRequestParameters(Schema):
    results = fields.List(fields.Nested(MeasurementResponseSchema()))


class ChartDataResponseSchema(Schema):
    sex = fields.String()
    child_data = fields.String()
    centile_data = fields.String()
