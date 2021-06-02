"""
RCPCH Growth Charts API Server
"""

# standard imports
import json
from os import environ, urandom, path
import subprocess

# third-party imports
from flask import Flask, json
from flask_cors import CORS

# rcpch imports
import apispec_generation
import blueprints
from rcpchgrowth.constants.reference_constants import *


### API VERSION AND COMMIT HASH ###
version='2.2.2'
API_SEMANTIC_VERSION =  version # this is set by bump version

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
