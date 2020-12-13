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
from rcpchgrowth.rcpchgrowth import create_all_charts


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

try:
  # create all the charts and store in chart_data
  references = ["trisomy-21", "turners-syndrome", 'uk-who']
  for references in enumerate(references):
    for index, sex in enumerate(sexes):
            for place, measurement_method in enumerate(measurement_methods):
                born_preterm = False
                if reference=="uk-who":
                    born_preterm = True
                try:
                    data = create_chart(reference=reference, measurement_method=measurement_method, sex=sex, born_preterm=born_preterm)
                except:
                    data = []
                return_object = { f"{reference}-{measurement_method}-{sex}": }
                all_charts.append(data)
   # This stores the data to file if the raw data is needed: too big to dump to console
  with open(filename, 'w') as file:
      file.write(json.dumps(return_object, separators=(',', ':')))
      file.close()
except:
  raise ValueError("Unable to create charts")

if __name__ == "__main__":
    app.run(host='0.0.0.0')
