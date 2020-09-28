"""
This module contains the Utilities endpoints as Flask Blueprints
"""
from os import path
from flask import Blueprint
from flask import jsonify, request
import markdown
import controllers


utilities = Blueprint("utilities", __name__)


@utilities.route("/references", methods=["GET"])
def references():
    """
    Centile References Library API route. Does not expect any parameters. Returns data on the growth reference data sources that this project is aware of. To add a new reference please submit a pull request, create a GitHub Issue, or otherwise contact the Growth Charts team.
    ---
    get:
      responses:
        200:
          description: "Reference data"
          content:
            application/json:
              schema: ReferencesResponseSchema
    """
    references_data = controllers.references()
    return jsonify(references_data)


@utilities.route("/create_fictional_child_measurements", methods=["POST"])
def create_fictional_child_measurements():
    """
    Fictional Child Data Generator API route. Returns a series of fictional measurement data for a child.
    Used for testing, demonstration and research purposes.
    ---
    post:
      parameters:
      - in: header
        schema: FictionalChildRequestParameters
      responses:
        200:
          description: "Fictional child test data generation endpoint"
          content:
            application/json:
              schema: FictionalChildResponseSchema
    """
    fictional_child_data = controllers.generate_fictional_data(
        drift_amount=float(request.form["drift_amount"]),
        intervals=int(request.form["intervals"]),
        interval_type=request.form["interval_type"],
        measurement_method=request.form["measurement_method"],
        number_of_measurements=int(request.form["number_of_measurements"]),
        sex=request.form["sex"],
        starting_age=float(request.form["starting_age"]),
        starting_sds=float(request.form["starting_sds"])
    )
    return jsonify(fictional_child_data)


@utilities.route("/instructions", methods=["GET"])
def instructions():
    """
    Instructions API route. Does not expect any parameters.
    Returns HTML content derived from the README.md of the API repository
    To amend the instructions please submit a pull request to https://github.com/rcpch/digital-growth-charts-server
    ---
    get:
      responses:
        200:
          description: "API Instructions and information endpoint"
          content:
            application/json:
              schema:
                type: string
    """
    # open README.md file
    file = path.join(path.abspath(path.dirname(
        path.dirname(__file__))), "README.md")
    with open(file) as markdown_file:
        html = markdown.markdown(markdown_file.read())
    return jsonify(html)
