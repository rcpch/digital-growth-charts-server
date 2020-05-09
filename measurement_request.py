from flask_wtf import FlaskForm
from wtforms import DateField, DecimalField, BooleanField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from datetime import date

class MeasurementForm(FlaskForm):
    birth_date = DateField('Date of Birth', validators=[DataRequired()])
    obs_date = DateField('Observation Date', validators=[DataRequired()])
    height = DecimalField('Height (cm)', default=0.0)
    weight = DecimalField('Weight (kg)', default=0.0)
    ofc = DecimalField('Head Circumference (cm)', default=0.0)
    sex = BooleanField('Male', default=False)
    gestation_weeks = IntegerField('Gestation in Weeks', default=40)
    gestation_days = IntegerField('Gestation in Days', default=0)
    submit = SubmitField('Calculate')