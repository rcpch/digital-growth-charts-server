"""
This module contains the opeanAPI3 spec root endpoint as a Flask Blueprints
"""
import json
from flask import Blueprint


openapi = Blueprint("openapi", __name__)

# Create JSON OpenAPI Spec and serve it at /


@openapi.route("/", methods=["GET"])
def openapi_endpoint():
    """
    openAPI3.0 Specification.
    ---
    get:
      summary: openAPI3.0 Specification.
      description: |
        * The root endpoint of the Digital Growth Charts API returns the openAPI3.0 specification in JSON format.
        * This can be used to autogenerate client scaffolding and tests.
        * We use it internally to generate all documentation, Postman collections and tests.
        * The openAPI specification is also available in YAML form, in the root of the Server codebase at https://github.com/rcpch/digital-growth-charts-server

      responses:
        200:
          description: |
            * openAPI3.0 Specification in JSON format, conforming to https://swagger.io/specification/, is returned.
          content:
            application/json:
              schema: OpenApiSchema
    """
    # read the spec from file and serve it
    with open('openapi.json') as json_file:
        openapi_json = json.load(json_file)

    return openapi_json, 200
