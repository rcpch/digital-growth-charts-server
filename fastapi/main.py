# standard imports
import json

# third party imports
from fastapi import FastAPI
from fastapi.openapi.utils import get_openapi
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseSettings

# local / rcpch imports
from routers import uk_who, turners, trisomy_21

### API VERSION ###
version = '2.2.5'  # this is set by bump version
API_SEMANTIC_VERSION = version  


# change the route at which the openAPIspec is shown
class Settings(BaseSettings):
    openapi_url: str = "/openapi.json"

settings = Settings()

# declare the FastAPI app
app = FastAPI(
        openapi_url=settings.openapi_url
    )
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)



# include routers for each type of endpoint
app.include_router(uk_who)
app.include_router(turners)
app.include_router(trisomy_21)


@app.get("/")
def read_root():
    return {"200 OK"}


def custom_openapi():
    if app.openapi_schema:
        print(openapi_schema)
        return app.openapi_schema

    openapi_schema = get_openapi(
        title="RCPCH Growth API",
        version=API_SEMANTIC_VERSION,
        description="Returns SDS and centiles for child growth measurements using growth references.",
        routes=app.routes,
    )
    
    # openapi_schema["info"]["x-logo"] = {
    #     "url": "https://fastapi.tiangolo.com/img/logo-margin/logo-teal.png"
    # }
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi


def write_apispec_to_file():
    with open(r'openapi.yml', 'w') as file:
        file.write(spec.to_yaml())

    with open(r'openapi.json', 'w') as file:
        file.write(json.dumps(
            spec.to_dict(), sort_keys=True, indent=4))
