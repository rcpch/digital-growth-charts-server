# imports for API only
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from os import path, listdir, remove
from datetime import datetime
from pathlib import Path

# imports for client only
import markdown
import requests

# imports for both
import json
import controllers as controllers


app = Flask(__name__, static_folder='static')
app.config['SECRET_KEY'] = 'UK_WHO' #not very secret - this will need complicating and adding to config
CORS(app)

from app import app

"""
TODO: TO BE DEPRECATED
Uses session variables to store form or uploaded unique child data
These session variables are accessed when user wants to download the calculated data,
or chart them.
    session["results"] are the form data entered by the user or uploaded from excel
    session["serial_data"] is a boolean value flagging if data are single measurements 
    or serial unique patient data
"""  

"""
API DEFINITIONS SECTION
* The API is versioned in a hard-coded fashion for now, however in time the versioning
  will happen at the level of the API management layer, which will direct requests to the
  correct versioned server accordingly
* There are different endpoints for a simple JSON response and a more complex FHIR response
* Each API endpoint has a distinct Controller
"""


"""
Centile Calculations API route. Expects query params as below:
    birth_date            STRING          date of birth of the patient in YYYY-MM-DD ISO8601 format (will be converted to Date)
    observation_date      STRING          date of the measurement in YYYY-MM-DD ISO8601 format (will be converted to Date)
    height_in_metres      FLOAT           the height in METRES NOT CENTIMETRES
    weight_in_kg          FLOAT           the weight in kilograms
    occipitofrontal_circ_in_cm  FLOAT     head circumference in CENTIMETRES
    sex                   STRING          either 'male or 'female'
    gestation_weeks       INTEGER         gestational age in completed weeks
    gestation_days        INTEGER         gestational age in completed days
"""
# JSON CALCULATION
@app.route("/api/v1/json/calculations", methods=['GET'])
def api_json_calculations():
    # check here for all the right query params, if not present raise error
    response = controllers.perform_calculations(
        birth_date=datetime.strptime(request.args['birth_date'], '%Y-%m-%d'),
        observation_date=datetime.strptime(request.args['observation_date'], '%Y-%m-%d'),
        height=float(request.args['height_in_metres']),
        weight=float(request.args['weight_in_kg']),
        ofc=float(request.args['occipitofrontal_circ_in_cm']),
        sex=str(request.args['sex']),
        gestation_weeks=int(request.args['gestation_weeks']),
        gestation_days=int(request.args['gestation_days'])
    )
    return jsonify(response)

# JSON Calculation of serial data
@app.route("/api/v1/json/serial_data_calculations", methods=['GET'])
def api_json_serial_data_calculations():

    # check here for all the right query params, if not present raise error

    serial_data = json.loads(request.args['uploaded_data']) #deserialised json

    response = controllers.prepare_data_as_array_of_measurement_objects(
        uploaded_data=serial_data
    )

    return jsonify(response)


# FHIR CALCULATION
@app.route("/api/v1/fhir", methods=['GET'])
def api_fhir():
    return jsonify({'path': '/api/v1/fhir'})


"""
Centile References Library API route
Does not expect any parameters
Returns data on the growth references that we are aware of
To add a new reference please submit a pull request
"""
@app.route("/api/v1/json/references", methods=['GET'])
def references():
    references_data = controllers.references()
    return jsonify(references_data)


"""
Chart data API route
requires results data params
Returns HTML content derived from the README.md of the API repository
To amend the instructions please submit a pull request
"""
@app.route("/api/v1/json/chart_data", methods=['GET'])
def chart_data():
    results = json.loads(request.args['results'])
    unique_child = request.args['unique_child']
    
    if unique_child == "true":
        #data come from a table and are not formatted for the charts
        formatted_child_data = controllers.prepare_data_as_array_of_measurement_objects(json.loads(results))
        
        # Prepare data from plotting
        child_data = controllers.create_data_plots(formatted_child_data)
        # Retrieve sex of child to select correct centile charts
        sex = formatted_child_data[0]['birth_data']['sex']
        
    else:
        # Prepare data from plotting
        child_data = controllers.create_data_plots(results)
        # Retrieve sex of child to select correct centile charts
        sex = results[0]['birth_data']['sex']
        
    # Create Centile Charts
    centiles = controllers.create_centile_values(sex)
    
    return jsonify({
        'sex': sex,
        'child_data': child_data,
        'centile_data': centiles
    })


"""
Instructions API route
Does not expect any parameters
Returns HTML content derived from the README.md of the API repository
To amend the instructions please submit a pull request
"""
@app.route("/api/v1/json/instructions", methods=['GET'])
def instructions():
    #open README.md file
    file = path.join(path.abspath(path.dirname(__file__)), 'README.md')
    with open(file) as markdown_file:
        html = markdown.markdown(markdown_file.read())
    return jsonify(html)

"""
Fictional Child Data Generator API route. Expects query params as below:
    drift_amount
    intervals
    interval_type
    measurement_requested
    number_of_measurements
    sex
    starting_age
    starting_sds
Returns a series of fictional data for a child
"""
@app.route("/api/v1/json/fictionalchild", methods=["GET"])
def fictionalchild():
    fictional_child_data = controllers.generate_fictional_data(
        drift_amount = float(request.args['drift_amount']),
        intervals = int(request.args['intervals']),
        interval_type = request.args['interval_type'],
        measurement_requested = request.args['measurement_requested'],
        number_of_measurements = int(request.args['number_of_measurements']),
        sex = request.args['sex'],
        starting_age = float(request.args['starting_age']),
        starting_sds = float(request.args['starting_sds'])
    )
    return jsonify(fictional_child_data)


if __name__ == '__main__':
    app.run()
