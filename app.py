"""
RCPCH Growth Charts API Server
"""

from os import environ, urandom

from flask import Flask, request
from flask_cors import CORS

import controllers
import blueprints
import schemas


#######################
##### FLASK SETUP #####
app = Flask(__name__, static_folder="static")
CORS(app)

# Mount all Utilities endpoints from the blueprint
app.register_blueprint(
    blueprints.utilities_blueprint.utilities, url_prefix='/utilities')

# Mount all UK-WHO endpoints from the blueprint
app.register_blueprint(
    blueprints.uk_who_blueprint.uk_who, url_prefix='/uk-who')

# Mount openAPI3 spec endpoint from the blueprint
app.register_blueprint(
    blueprints.openapi_blueprint.openapi)

# ENVIRONMENT
# Load the secret key from the ENV if it has been set
if "FLASK_SECRET_KEY" in environ:
    app.secret_key = environ["FLASK_SECRET_KEY"]
    print(f"{blueprints.OKGREEN} * FLASK_SECRET_KEY was loaded from the environment{blueprints.ENDC}")
# Otherwise create a new one. (NB: We don't need session persistence between reboots of the app)
else:
    app.secret_key = urandom(16)
    print(f"{blueprints.OKGREEN} * A new SECRET_KEY for Flask was automatically generated{blueprints.ENDC}")

from app import app     # position of this import is important. Don't allow it to be autoformatted alphabetically to the top of the imports!

##### END FLASK SETUP #####
###########################


######################
##### BLUEPRINTS #####

# UK-WHO calculation endpoint as blueprint
blueprints.spec.components.schema(
    "calculation", schema=schemas.CalculationResponseSchema)
with app.test_request_context():
    blueprints.spec.path(view=blueprints.uk_who_blueprint.uk_who_calculation)

# UK-WHO chart data endpoint as blueprint
blueprints.spec.components.schema(
    "chartData", schema=schemas.ChartDataResponseSchema)
with app.test_request_context():
    blueprints.spec.path(
        view=blueprints.uk_who_blueprint.uk_who_chart_coordinates)

blueprints.spec.components.schema(
    "plottableChildData",
    schema=schemas.PlottableChildDataResponseSchema)
with app.test_request_context():
    blueprints.spec.path(
        view=blueprints.uk_who_blueprint.uk_who_plottable_child_data)

# Utilities endpoints as blueprints
blueprints.spec.components.schema(
    "references", schema=schemas.ReferencesResponseSchema)
with app.test_request_context():
    blueprints.spec.path(view=blueprints.utilities_blueprint.references)

# TODO #122 Fictional child endpoint may be better renamed as a researcher tool?
blueprints.spec.components.schema(
    "fictionalChild", schema=schemas.FictionalChildResponseSchema)
with app.test_request_context():
    blueprints.spec.path(
        view=blueprints.utilities_blueprint.create_fictional_child_measurements)

# Instructions endpoint (TODO: #121 #120 candidate for deprecation)
with app.test_request_context():
    blueprints.spec.path(view=blueprints.utilities_blueprint.instructions)

# OpenAPI3 specification endpoint
with app.test_request_context():
    blueprints.spec.path(view=blueprints.openapi_blueprint.openapi_endpoint)

# TODO Trisomy 21 endpoint

# TODO Turner's syndrome endpoint

##### END API SPEC ########
###########################


# TODO #123 the spreadsheet endpoint probably needs to be deprecated
@app.route("/uk-who/spreadsheet", methods=["POST"])
def ukwho_spreadsheet():
    """
    ***INCOMPLETE***
    Spreadsheet file uploadte.
    ---
    post:
      summary: Spreadsheet file upload API route.
      description: |
        * This endpoint is used for development and testing only and it is not envisaged that it will be in the live API.

      requestBody:
        content:
          text/csv:
            schema: ChartDataRequestParameters

      responses:
        200:
          description: |
            * Chart data for plotting a traditional growth chart was returned.
          content:
            application/json:
              schema: ChartDataResponseSchema
    """
    csv_file = request.files["csv_file"]
    calculated_results = controllers.import_csv_file(csv_file)
    return calculated_results


if __name__ == "__main__":
    app.run()
