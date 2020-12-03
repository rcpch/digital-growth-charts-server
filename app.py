"""
RCPCH Growth Charts API Server
"""

from os import environ, urandom

from flask import Flask, request
from flask_cors import CORS

import controllers
import blueprints
import schemas
import apispec_generation


# Declare shell colour variables for pretty logging output
OKBLUE = "\033[94m"
OKGREEN = "\033[92m"
WARNING = "\033[93m"
FAIL = "\033[91m"
ENDC = "\033[0m"


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
    print(f"{OKGREEN} * FLASK_SECRET_KEY was loaded from the environment{ENDC}")
# Otherwise create a new one. (NB: We don't need session persistence between reboots of the app)
else:
    app.secret_key = urandom(16)
    print(f"{OKGREEN} * A new SECRET_KEY for Flask was automatically generated{ENDC}")

from app import app     # position of this import is important. Don't allow it to be autoformatted alphabetically to the top of the imports!

##### END FLASK SETUP #####
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


# generate the API spec
try:
    spec = apispec_generation.generate(app)
    print(f"{OKGREEN} * openAPI3.0 spec was generated and saved to the repo{ENDC}")

except Exception as error:
    print(f"{FAIL} * An error occurred while processing the openAPI3.0 spec{ENDC}")
    print(f"{FAIL} *  > {error} {ENDC}")


if __name__ == "__main__":
    app.run(host='0.0.0.0')
