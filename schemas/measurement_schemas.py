from marshmallow import Schema, fields


class BirthDataSchema(Schema):
    birth_date = fields.Date()
    estimated_date_delivery = fields.Date()
    estimated_date_delivery_string = fields.String()
    gestation_days = fields.Number()
    gestation_weeks = fields.Number()
    sex = fields.String()


class ChildObservationValueSchema(Schema):
    measurement_method = fields.String()
    observation_value = fields.Number()


class MeasurementCalculatedValues(Schema):
    centile = fields.Float()
    centile_band = fields.String()
    measurement_method = fields.String()
    sds = fields.Float()


class MeasurementDatesSchema(Schema):
    chronological_calendar_age = fields.String()
    chronological_decimal_age = fields.Float()
    clinician_decimal_age_comment = fields.String()
    corrected_calendar_age = fields.String()
    corrected_decimal_age = fields.Float()
    #  corrected_gestational_age = fields.{
    #      corrected_gestation_days: null,
    #      corrected_gestation_weeks: null
    #  },
    lay_decimal_age_comment = fields.String()
    observation_date = fields.DateTime()


# This is a composite of the preceding nested data types
class MeasurementResponseSchema(Schema):
    birth_data = fields.Nested(BirthDataSchema())
    child_observation_value = fields.Nested(ChildObservationValueSchema())
    measurement_calculated_values = fields.Nested(
        MeasurementCalculatedValues())
    measurement_dates = fields.Nested(MeasurementDatesSchema())
