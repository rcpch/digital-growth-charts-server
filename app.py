"""
RCPCH Growth Charts API Server
"""

import json
from os import environ, urandom, path
import subprocess

from flask import Flask, request, json
from flask_cors import CORS

import controllers
import blueprints
import schemas
import apispec_generation
from rcpchgrowth.rcpchgrowth.constants.parameter_constants import *
from rcpchgrowth.rcpchgrowth.chart_functions import create_chart


### API VERSION AND COMMIT HASH ###
API_SEMANTIC_VERSION = "1.0.12"  # this is manually set

# Read saved version info from **saved** JSON APIspec
# (Because Git may not exist in Live and may not be able to get current commit hash)
with open('openapi.json') as json_file:
    api = json.load(json_file)
    SAVED_API_VERSION = api['info']['version']

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

# Declare growth chart folder for growth chart data
chart_data_folder = path.join(app.root_path, 'chart_data')

# Mount all Utilities endpoints from the blueprint
app.register_blueprint(
    blueprints.utilities_blueprint.utilities, url_prefix='/utilities')

# Mount all UK-WHO endpoints from the blueprint
app.register_blueprint(
    blueprints.uk_who_blueprint.uk_who, url_prefix='/uk-who')

# Mount all Trisomy 21 endpoints from the blueprint
app.register_blueprint(
    blueprints.trisomy_21_blueprint.trisomy_21, url_prefix='/trisomy-21')

# Mount all Turner's endpoints from the blueprint
app.register_blueprint(
    blueprints.turner_blueprint.turners, url_prefix='/turner')


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

# create all the charts and store in chart_data: commenting out as builds locally but causes failure to deploy to azure.
# try:
#   result = create_chart(reference="uk-who", measurement_method="height", sex="female", centile_selection=COLE_TWO_THIRDS_SDS_NINE_CENTILE_COLLECTION)
#   filename = "uk_who_girls.json"
#   file_path = path.join(chart_data_folder, filename)
#   with open(file_path, 'w') as file:
#       print("now writing to file...")
#       file.write(json.dumps(result, separators=(',', ':')))
#       file.close()
#       print(f" * {OKGREEN}New UK-WHO Chart Data has been generated.")
# except:
#   raise ValueError("Unable to create UK-WHO charts")

# # Trisomy 21
# try:
#   result = create_chart(TRISOMY_21, COLE_TWO_THIRDS_SDS_NINE_CENTILES)
#   filename = "trisomy_21_chart_data.json"
#   file_path = path.join(chart_data_folder, filename)
#   with open(file_path, 'w') as file:
#       print("now writing to file...")
#       file.write(json.dumps(result, separators=(',', ':')))
#       file.close()
#       print(f" * {OKGREEN}New Trisomy 21 Chart Data has been generated.")
# except:
#   raise Exception("Unable to create Trisomy 21 charts")

# # Turner's Syndrome
# try:
#   result = create_turner_chart(COLE_TWO_THIRDS_SDS_NINE_CENTILES)
#   filename = "turners_chart_data.json"
#   file_path = path.join(chart_data_folder, filename)
#   with open(file_path, 'w') as file:
#       print("now writing to file...")
#       file.write(json.dumps(result, separators=(',', ':')))
#       file.close()
#       print(f" * {OKGREEN}New Turner's Syndrome Chart Data has been generated.")
# except:
#   raise ValueError("Unable to create Turner's Syndrome charts")

# generate the API spec
try:
    try:
        # if Git is available when the server is running (ie in dev) then update the server version from the Git commit hash
        # This means we can 'bake' the commit into the openAPI spec
        api_commit_hash = subprocess.check_output(
            ["git", "rev-parse", "HEAD"]).strip().decode('utf-8')
        spec = apispec_generation.generate(
            app, api_commit_hash, API_SEMANTIC_VERSION)
        print(f"{OKGREEN} * openAPI3.0 spec was generated and saved to the repo{ENDC}")
        print(f"{OKGREEN} * API semantic version is {API_SEMANTIC_VERSION}, commit hash is {api_commit_hash} {ENDC}")
    except:
        api_commit_hash = "Git not available"

except Exception as error:
    print(f"{FAIL} * An error occurred while processing the openAPI3.0 spec{ENDC}")
    print(f"{FAIL} *  > {error} {ENDC}")


# adds API version details to all requests
@app.after_request
def add_api_version(response):
    response.headers.add('Growth-Api-Version', SAVED_API_VERSION)
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0')
