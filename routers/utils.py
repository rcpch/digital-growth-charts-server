from typing import Any


# Description: This file contains utility functions for the routers.
# It remaps the generic HTTP errors to match the FastAPI error format.
def format_error(
    loc: list[str | int], msg: str, error_type: str, input: Any = None
) -> dict[str, Any]:
    return {
        "loc": loc,
        "msg": msg,
        "type": error_type,
        "input": input
    }
