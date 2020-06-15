from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, BooleanField, SubmitField, IntegerField, RadioField, SelectField
from wtforms.validators import DataRequired
from datetime import date

MEASUREMENT_TYPES = [('height', 'Height (cm)'), ('weight', 'Weight (kg)'), ('bmi', 'BMI (kg/m2)'), ('ofc', 'Head Circumference (cm)')]
INTERVAL_TYPES = [('days', 'Days'), ('weeks', 'Weeks'), ('months', 'Months'), ('years', 'Years')]

class MeasurementForm(FlaskForm):
    birth_date = DateField('Date of Birth', validators=[DataRequired()])
    obs_date = DateField('Observation Date', validators=[DataRequired()])
    height = DecimalField('Height (cm)', default=0.0)
    weight = DecimalField('Weight (kg)', default=0.0)
    ofc = DecimalField('Head Circumference (cm)', default=0.0)
    sex = RadioField('Sex', choices=[('male','Male'),('female','Female')], default='male')
    gestation_weeks = IntegerField('Gestation in Weeks', default=40)
    gestation_days = IntegerField('Gestation in Days', default=0)
    submit = SubmitField('Calculate')

class FictionalChildForm(FlaskForm):
    starting_age = DecimalField(label='Starting Decimal Age', validators=[DataRequired()])
    intervals = DecimalField(label='Units of Time', validators=[DataRequired()])
    interval_type = SelectField(label='Interval Type', choices=INTERVAL_TYPES, validators=[DataRequired()])
    starting_sds = DecimalField(label='Starting SDS', validators=[DataRequired()])
    measurement_requested = SelectField(label='Measurement Type', choices=MEASUREMENT_TYPES, validators=[DataRequired()])
    drift_amount = DecimalField(label='SDS Drift', validators=[DataRequired()])
    sex = RadioField('Sex', choices=[('male','Male'),('female','Female')], default='male')
    number_of_data_points = DecimalField('Number of Data Points', validators=[DataRequired()])
    submit = SubmitField('Generate Data Points')