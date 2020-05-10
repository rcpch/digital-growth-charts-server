from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory
import os
import markdown
from datetime import date
from measurement_request import MeasurementForm
import json
import rcpchgrowth.rcpchgrowth as calculations

app = Flask(__name__)
app.config['SECRET_KEY'] = 'UK_WHO' #not very secret - this will need complicating and adding to config

from app import app

@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static'),
                               'favicon.ico', mimetype='image/vnd.microsoft.icon')

@app.route("/", methods=['GET', 'POST'])
def home():
    form = MeasurementForm(request.form)
    if request.method == 'POST':
        if form.validate_on_submit():
            results = perform_calculations(form)
            return render_template('test_results.html', result=results)
        
        # form not validated. Need flash warning here
        return render_template('measurement_form.html', form = form)
    else:
        return render_template('measurement_form.html', form = form)

def perform_calculations(form):
    birth_date = form.birth_date.data
    obs_date = form.obs_date.data
    height = float(form.height.data)
    weight = float(form.weight.data)
    ofc = float(form.ofc.data)
    isMale = form.sex.data
    if isMale:
        sex = 'male'
    else:
        sex = 'female'
    gestation_weeks = form.gestation_weeks.data
    gestation_days = form.gestation_days.data
    corrected_decimal_age = calculations.corrected_decimal_age(birth_date, obs_date, gestation_weeks, gestation_days)
    chronological_decimal_age = calculations.chronological_decimal_age(birth_date, obs_date)
    chronological_calendar_age = calculations.chronological_calendar_age(birth_date, obs_date)

    height_sds = 'None'
    height_centile="None"
    weight_sds = 'None'
    weight_centile='None'
    bmi_sds = 'None'
    bmi_centile='None'
    ofc_sds = 'None'
    ofc_centile='None'
    bmi = 'None'
    edd = 'None'
    edd_string = ""
    corrected_calendar_age = ''
    corrected_gestational_age = ''

    if chronological_decimal_age == corrected_decimal_age:
        corrected_decimal_age = 'None'
        age = chronological_decimal_age
    else:
        age = corrected_decimal_age
        edd = calculations.estimated_date_delivery(birth_date, gestation_weeks, gestation_days)
        corrected_calendar_age = calculations.chronological_calendar_age(edd, obs_date)
        edd_string = edd.strftime('%a %d %B, %Y')
        corrected_gestational_age = calculations.corrected_gestational_age(birth_date, obs_date, gestation_weeks, gestation_days)
    if height > 1:
        if age >= -0.287474333: # there is no length data below 25 weeks gestation
            height_sds = calculations.sds(age, 'height', height, sex)
            height_centile = calculations.centile(height_sds)
    if weight > 1:
        weight_sds = calculations.sds(age, 'weight', weight, sex)
        weight_centile = calculations.centile(weight_sds)
    if height > 1 and weight> 1:
        bmi = calculations.bmi_from_height_weight(height, weight)
        if age > 0.038329911: # BMI data not present < 42 weeks gestation
            bmi_sds = calculations.sds(age, 'bmi', bmi, sex)
            bmi_centile = calculations.centile(bmi_sds)
    if ofc > 1:
        if (age <= 17 and not isMale) or (age <= 18 and isMale): # OFC data not present >17y in girls or >18y in boys
            ofc_sds = calculations.sds(age, 'ofc', ofc, sex)
            ofc_centile = calculations.centile(ofc_sds)

    return {"dates": {"birth_date": birth_date, "obs_date": obs_date, "gestation_weeks": gestation_weeks, "gestation_days": gestation_days, "chronological_decimal_age": chronological_decimal_age, "corrected_decimal_age": corrected_decimal_age, "chronological_calendar_age": chronological_calendar_age, "corrected_calendar_age": corrected_calendar_age, "edd": edd, "edd_string": edd_string, "corrected_gestational_age": corrected_gestational_age}, "patient": {"sex": sex, "height": height, "weight": weight, "bmi": bmi, "ofc": ofc}, "calculations": {"height_sds": height_sds, "height_centile": height_centile, "weight_sds": weight_sds, "weight_centile":weight_centile, "bmi_sds": bmi_sds, "bmi_centile": bmi_centile, "ofc_sds": ofc_sds, "ofc_centile": ofc_centile} }

@app.route("/instructions", methods=['GET'])
def instructions():
    #open README.md file
    this_directory = os.path.abspath(os.path.dirname(__file__))
    file = os.path.join(this_directory, 'README.md')
    with open(file) as markdown_file:

        #read contents of file
        content = markdown_file.read()

        #convert to HTML
        html = markdown.markdown(content)
    return render_template('instructions.html', fill=html)

@app.route("/references", methods=['GET'])
def references():

    # starting with a hard-coded list, but as it grows probably belongs in database
    with open('./resource_data/growth_reference_repository.json') as json_file:
            data = json.load(json_file)
            json_file.close()
    return render_template('references.html', data=data)

if __name__ == '__main__':
    app.run()