from marshmallow import Schema, fields


class FictionalChildRequestParameters(Schema):
    drift_amount = fields.String(
        description="The SDS range over which you want serial generated values to drift, simulating growth or pathological state")
    intervals = fields.Integer(
        description="The value of the time intervals between generated measurements. Set the time intervals using the `interval_type` parameter.")
    interval_type = fields.String(
        enum=['d', 'day', 'days', 'weeks', 'm',
              'month', 'months', 'y', 'year', 'years'],
        description="The length of the time intervals used. Can be `d`, `day`, `days`, `weeks`, `m`, `month`, `months`, `y`, `year`, `years`. For example, setting the time interval to `months` and the intervals to `3` would generate fictional child growth data at 3-monthly intervals")
    measurement_method = fields.String(
        enum=['height', 'weight', 'ofc', 'bmi'],
        description="The type of measurement requested: can be `height`, `weight`, `ofc` or `bmi`")
    number_of_measurements = fields.Integer(
        description="The number of sequential measurements you would like the API to generate, at intervals specified by the `intervals` and `interval_type` parameters.")
    sex = fields.String(
        enum=["male", "female"],
        description="The sex of the child")
    starting_age = fields.Float(
        description="The **decimal** age at which the fictional child data series should start. Decimal ages are the child's age in years as a floating point number")
    starting_sds = fields.Float(
        description="The starting SDS at which you want the API to generate fictional measurements. This SDS values will drift upwards or downwards over the time series, according to the `drift_amount` parameter.")


class FictionalChildResponseSchema(Schema):
    response = fields.String()
