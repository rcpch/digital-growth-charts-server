from pydantic_core import ErrorDetails 

# Description: This file contains utility functions for the routers.
# It remaps the generic HTTP errors to match the FastAPI error format.
def format_error(loc, msg, error_type, input=None) -> ErrorDetails:
    return {
        "loc": loc,
        "msg": msg,
        "type": error_type,
        "input": input
    }