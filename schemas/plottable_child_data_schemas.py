from marshmallow import Schema, fields


class PlottableChildDataRequestParameters(Schema):
    results = fields.String()


class PlottableChildDataResponseSchema(Schema):
    sex = fields.String()
    child_data = fields.String()