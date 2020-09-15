# imports for API only
from flask import Flask, render_template, request, flash, redirect, url_for, send_from_directory, make_response, jsonify, session
from flask_cors import CORS
from werkzeug.utils import secure_filename
from os import path, listdir, remove
from datetime import datetime
from pathlib import Path
from controllers import import_csv_file

# imports for client only
import markdown
import requests

# imports for both
import json
import controllers as controllers


app = Flask(__name__, static_folder="static")
app.config["SECRET_KEY"] = "UK_WHO" #not very secret - this will need complicating and adding to config
CORS(app) # TODO #75

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
* Although the API is stateless
* Each API endpoint has a distinct Controller
"""


"""
Centile Calculations API route. Expects parameters in the body as below:
    birth_date            STRING          date of birth of the patient in YYYY-MM-DD ISO8601 format (will be converted to Date)
    observation_date      STRING          date of the measurement in YYYY-MM-DD ISO8601 format (will be converted to Date)
    height_in_cm          FLOAT           the height in CENTIMETRES
    weight_in_kg          FLOAT           the weight in kilograms
    head_circ_in_cm       FLOAT           head circumference in CENTIMETRES
    sex                   STRING          either "male or "female"
    gestation_weeks       INTEGER         gestational age in completed weeks
    gestation_days        INTEGER         gestational age in completed days
"""
# JSON CALCULATION
@app.route("/api/v1/json/calculations", methods=["POST"])
def api_json_calculations():
    
    # check here for all the right query params, if not present raise error
    response = controllers.perform_calculations(
        birth_date=datetime.strptime(request.form["birth_date"], "%Y-%m-%d"),
        observation_date=datetime.strptime(request.form["observation_date"], "%Y-%m-%d"),
        height=float(request.form["height_in_cm"]),
        weight=float(request.form["weight_in_kg"]),
        ofc=float(request.form["head_circ_in_cm"]),
        sex=str(request.form["sex"]),
        gestation_weeks=int(request.form["gestation_weeks"]),
        gestation_days=int(request.form["gestation_days"])
    )
    return jsonify(response)

# JSON CALCULATION OF SINGLE MEASUREMENT_METHOD ('height', 'weight', 'bmi', 'ofc'): Note that BMI must be precalculated for this function
@app.route("/api/v1/json/calculation", methods=["POST"])
def api_json_calculation():
    # check here for all the right query params, if not present raise error
    final_calculations = controllers.perform_calculation(
        birth_date=datetime.strptime(request.form["birth_date"], "%Y-%m-%d"),
        observation_date=datetime.strptime(request.form["observation_date"], "%Y-%m-%d"),
        measurement_method=str(request.form["measurement_method"]),
        observation_value =float(request.form["observation_value"]),
        sex=str(request.form["sex"]),
        gestation_weeks=int(request.form["gestation_weeks"]),
        gestation_days=int(request.form["gestation_days"])
    )

    response = jsonify(final_calculations)

    return response

# JSON Calculation of serial data
@app.route("/api/v1/json/serial_data_calculations", methods=["POST"])
def api_json_serial_data_calculations():

    # check here for all the right query params, if not present raise error

    serial_data = json.loads(request.form["uploaded_data"])

    response = controllers.prepare_data_as_array_of_measurement_objects(
        uploaded_data=serial_data
    )

    return jsonify(response)


# FHIR CALCULATION
@app.route("/api/v1/fhir", methods=["POST"])
def api_fhir():
    return jsonify({"path": "/api/v1/fhir"})


"""
Centile References Library API route
Does not expect any parameters
Returns data on the growth references that we are aware of
To add a new reference please submit a pull request
"""
@app.route("/api/v1/json/references", methods=["GET"])
def references():
    references_data = controllers.references()
    return jsonify(references_data)


"""
Chart data API route
requires results data params
Returns HTML content derived from the README.md of the API repository
To amend the instructions please submit a pull request
"""
@app.route("/api/v1/json/chart_data", methods=["POST"])
def chart_data():

    results=json.loads(request.form["results"])
    unique_child = request.form["unique_child"]
    # unique_child = request.args["unique_child"]
    
    # born preterm flag to pass to charts
    born_preterm = (results[0]["birth_data"]["gestation_weeks"]!= 0 and results[0]["birth_data"]["gestation_weeks"] < 37)
    
    if unique_child == "true":
        #data are serial data points for a single child
        
        # Prepare data from plotting
        child_data = controllers.create_data_plots(results)

        # Retrieve sex of child to select correct centile charts
        sex = results[0]["birth_data"]["sex"]
        
    else:
        
        # Prepare data from plotting
        child_data = controllers.create_data_plots(results)
        # Retrieve sex of child to select correct centile charts
        sex = results[0]["birth_data"]["sex"]
        
    # Create Centile Charts
    centiles = controllers.create_centile_values(sex, born_preterm=born_preterm)
    
    return jsonify({
        "sex": sex,
        "child_data": child_data,
        "centile_data": centiles
    })


"""
Instructions API route
Does not expect any parameters
Returns HTML content derived from the README.md of the API repository
To amend the instructions please submit a pull request
"""
@app.route("/api/v1/json/instructions", methods=["GET"])
def instructions():
    #open README.md file
    file = path.join(path.abspath(path.dirname(__file__)), "README.md")
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
@app.route("/api/v1/json/fictionalchild", methods=["POST"])
def fictionalchild():
    fictional_child_data = controllers.generate_fictional_data(
        drift_amount = float(request.form["drift_amount"]),
        intervals = int(request.form["intervals"]),
        interval_type = request.form["interval_type"],
        measurement_requested = request.form["measurement_requested"],
        number_of_measurements = int(request.form["number_of_measurements"]),
        sex = request.form["sex"],
        starting_age = float(request.form["starting_age"]),
        starting_sds = float(request.form["starting_sds"])
    )
    return jsonify(fictional_child_data)


@app.route("/api/v1/json/spreadsheet", methods=["POST"])
def spreadsheet():
    csv_file = request.files["csv_file"]
    calculated_results = import_csv_file(csv_file)
    return calculated_results
   
# return value from upload.py
# {
#         data: [an array of Measurement class objects]
#         unique_child: boolean - refers to whether data is from one child or many children
#         valid: boolean - refers to whether imported data was valid for calculation
#         error: string  - error message if invalid file
# }

if __name__ == "__main__":
    app.run()
