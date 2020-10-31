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
    Centile References Library API route.
    ---
    get:
      summary: Centile References Library API route.
      description: |
        * Does not expect any parameters.
        * Returns data on the growth reference data sources that this project is aware of.
        * To add a new reference please submit a pull request, create a GitHub Issue, or otherwise contact the Growth Charts team.

      responses:
        200:
          description: "Reference data was returned"
          content:
            application/json:
              schema: ReferencesResponseSchema
    """
    references_data = controllers.references()
    return jsonify(references_data)


@utilities.route("/create_fictional_child_measurements", methods=["POST"])
def create_fictional_child_measurements():
    """
    Fictional Child Data Generator API route.
    ---
    post:
      summary: Fictional Child Data Generator API route.
      description: |
        * Returns a series of generated fictional measurement data for a child.
        * Used for testing, demonstration and research purposes.

      requestBody:
        content:
          application/json:
            schema: FictionalChildRequestParameters

      responses:
        200:
          description: "Fictional child test data was returned"
          content:
            application/json:
              schema: FictionalChildResponseSchema
    """
    if request.is_json:
        req = request.get_json()
        fictional_child_data = controllers.generate_fictional_data(
            drift_amount=float(req["drift_amount"]),
            intervals=int(req["intervals"]),
            interval_type=req["interval_type"],
            measurement_method=req["measurement_method"],
            number_of_measurements=int(req["number_of_measurements"]),
            sex=req["sex"],
            starting_age=float(req["starting_age"]),
            starting_sds=float(req["starting_sds"])
        )
        return jsonify(fictional_child_data)
    else:
        return "Request body should be application/json", 400


@utilities.route("/instructions", methods=["GET"])
def instructions():
    """
    Instructions API route.
    ---
    get:
      summary: Instructions API route.
      description: |
        * Does not expect any parameters.
        * Returns HTML content derived from the README.md of the API repository
        * To amend the instructions please submit a pull request to https://github.com/rcpch/digital-growth-charts-server

      responses:
        200:
          description: "API Instructions and information was returned"
          content:
            application/json:
              schema:
                type: string
    """
    file = path.join(path.abspath(path.dirname(
        path.dirname(__file__))), "README.md")
    with open(file) as markdown_file:
        html = markdown.markdown(markdown_file.read())
    return jsonify(html)
