# standard imports
import json
from pathlib import Path
import os

# third party imports
from fastapi import FastAPI, Request
from fastapi.exception_handlers import http_exception_handler
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from fastapi.responses import JSONResponse
from starlette.exceptions import HTTPException as StarletteHTTPException

# local / rcpch imports
from rcpchgrowth import chart_functions, constants
from routers import (
    cdc,
    format_error,
    trisomy_21,
    trisomy_21_aap,
    turners,
    uk_who,
    utilities,
    who,
)
from schemas import UnprocessableEntityResponse


version='5.0.0'  # this is set by bump version

# To ensure the API can only be accessed in production via our API gateway
authorization_key = os.getenv('AUTHORIZATION_KEY')

# Declare the FastAPI app
app = FastAPI(
        openapi_url="/",
        redoc_url=None,
        license_info={
            "name": "GNU Affero General Public License",
            "url": "https://www.gnu.org/licenses/agpl-3.0.en.html"
            },
    )

# Set up CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*', 'http://localhost:8000'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def authorization_key_middleware(request, call_next):
    # Homepage always open to act as the healthcheck
    if not authorization_key or request.url.path == '/':
        return await call_next(request)

    if request.headers.get("Authorization") == f"Bearer {authorization_key}":
        return await call_next(request)
    
    return JSONResponse(status_code=403, content={"detail": "Forbidden"})

github_sha = os.getenv('GITHUB_SHA')

@app.middleware("http")
async def include_github_sha_for_prout(request, call_next):
    response = await call_next(request)
    
    if request.url.path == '/' and github_sha:
        response.headers["X-Git-Revision"] = github_sha

    return response


@app.exception_handler(StarletteHTTPException)
async def consistent_http_exception_handler(
    request: Request, exception: StarletteHTTPException
):
    if exception.status_code == 422 and isinstance(exception.detail, str):
        exception = StarletteHTTPException(
            status_code=exception.status_code,
            detail=[
                format_error(
                    loc=["request"],
                    msg=exception.detail,
                    error_type="value_error",
                    input=None,
                )
            ],
            headers=exception.headers,
        )
    return await http_exception_handler(request, exception)


# Include routers for each type of endpoint.
unprocessable_entity_response = {
    422: {
        "model": UnprocessableEntityResponse,
        "description": "Request validation or application-generated error",
    }
}

app.include_router(uk_who, responses=unprocessable_entity_response)
app.include_router(turners, responses=unprocessable_entity_response)
app.include_router(trisomy_21, responses=unprocessable_entity_response)
app.include_router(trisomy_21_aap, responses=unprocessable_entity_response)
app.include_router(cdc, responses=unprocessable_entity_response)
app.include_router(who, responses=unprocessable_entity_response)
app.include_router(utilities, responses=unprocessable_entity_response)


# Customise API metadata
def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="RCPCH Digital Growth API",
        version=version,
        description="Returns SDS and centiles for child growth measurements using growth references. Currently provides calculations based on the UK-WHO, Turner's Syndrome and Trisomy-21 references.",
        routes=app.routes,
    )
    app.openapi_schema = openapi_schema
    return app.openapi_schema


app.openapi = custom_openapi


# Include the root endpoint (so it is _described_ in the APIspec).
@app.get("/", tags=["openapi3"])
def root():
    """
    # API spec endpoint
    * The root `/` API endpoint returns the openAPI3 specification in JSON format
    * This spec is also available in the root of the server code repository
    """
    return


# Generate and store the chart plotting data for the centile background curves.
# This data is only generated once and then is stored and served from file.
def generate_and_store_chart_data(overwrite=False):
    for centile_format in [constants.COLE_TWO_THIRDS_SDS_NINE_CENTILES, constants.THREE_PERCENT_CENTILES, constants.FIVE_PERCENT_CENTILES, constants.EIGHTY_FIVE_PERCENT_CENTILES]:
        for reference in constants.REFERENCES:
            for sex in constants.SEXES:
                for measurement_method in constants.MEASUREMENT_METHODS:
                    # Don't generate files for Turner's for references we don't have (males or non-height measurements)
                    if reference == "turners-syndrome" and (sex != "female" or measurement_method != "height"):
                        continue
                    chart_data_file = Path(
                        f'chart-data/{centile_format}-{reference}-{sex}-{measurement_method}.json')
                    if chart_data_file.exists() and not overwrite:
                        print(f'Chart data file exists for {centile_format}-{reference}-{sex}-{measurement_method}.')
                    else:
                        print(f'Chart data file does not exist for {centile_format}-{reference}-{sex}-{measurement_method}')
                        try:
                            chart_data = chart_functions.create_chart(
                                reference,
                                measurement_method=measurement_method,
                                sex=sex,
                                centile_format=centile_format
                            )
                            script_dir = os.path.dirname(__file__)
                            path = os.path.join(script_dir, f'chart-data/{centile_format}-{reference}-{sex}-{measurement_method}.json')
                            with open(path, 'w') as file:
                                file.write(json.dumps(chart_data, indent=4))
                            print(f'chart data file created for {centile_format}-{reference}-{sex}-{measurement_method}')
                        except Exception as error:
                            print(f'Chart data not created due to: {error}')

generate_and_store_chart_data()


# Saves openAPI3 spec to file in the project root.
def write_apispec_to_file():
    # check if openapi.json is already the same as the autogenerated
    file = open(r'openapi.json', 'r')
    if file.read() == json.dumps(app.openapi(), indent=4):
        print("Generated internal openAPI3 spec and openapi.json have equal file content")
    else:
        file = open(r'openapi.json', 'w')
        file.write(json.dumps(app.openapi(), indent=4))
    file.close()
        
write_apispec_to_file()
