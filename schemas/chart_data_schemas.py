from marshmallow import Schema, fields


class ChartDataRequestParameters(Schema):
    sex = fields.String(
        required= True,
        description="Accepts male or female as sex of chart required."
    )
    measurement_method=fields.String(
        required=True,
        descriptions="Must be one of height, weight, ofc (head circumference) or bmi (body mass index). Parameter to return correct chart."
    )


class ChartDataResponseSchema(Schema):
    sex = fields.String()
    centile_data = fields.String()
