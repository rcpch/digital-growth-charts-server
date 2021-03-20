"""
This module contains the Utilities endpoints as Flask Blueprints
"""

# python imports
from os import path

# third party imports
from flask import Blueprint
from flask import jsonify, request
import markdown

# internal imports
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
