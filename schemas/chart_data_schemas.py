from marshmallow import Schema, fields


class ChartDataRequestParameters(Schema):
    results = fields.String()


class ChartDataResponseSchema(Schema):
    sex = fields.String()
    centile_data = fields.String()
