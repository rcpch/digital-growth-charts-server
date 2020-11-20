from marshmallow import Schema, fields


class OpenApiSchema(Schema):
    results = fields.String()
