# standard imports
import json
from pathlib import Path
import os

# third party imports
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.openapi.utils import get_openapi
from pydantic import BaseSettings

# local / rcpch imports
from rcpchgrowth import chart_functions, constants
from routers import trisomy_21, turners, uk_who


version='3.1.0'  # this is set by bump version

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


# Include routers for each type of endpoint.
app.include_router(uk_who)
app.include_router(turners)
app.include_router(trisomy_21)


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
def generate_and_store_chart_data():
    for centile_format in [constants.COLE_TWO_THIRDS_SDS_NINE_CENTILES, constants.THREE_PERCENT_CENTILES]:
        for reference in constants.REFERENCES:
            for sex in constants.SEXES:
                for measurement_method in constants.MEASUREMENT_METHODS:
                    # Don't generate files for Turner's for references we don't have (males or non-height measurements)
                    if reference == "turners-syndrome" and (sex != "female" or measurement_method != "height"):
                        continue
                    chart_data_file = Path(
                        f'chart-data/{centile_format}-{reference}-{sex}-{measurement_method}.json')
                    if chart_data_file.exists():
                        print(f'Chart data file exists for {centile_format}-{reference}-{sex}-{measurement_method}.')
                    else:
                        print(f'Chart data file does not exist for {centile_format}-{reference}-{sex}-{measurement_method}')
                        try:
                            chart_data = chart_functions.create_chart(
                                reference,
                                measurement_method=measurement_method,
                                sex=sex,
                                centile_selection=centile_format
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
