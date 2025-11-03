from dataclasses import dataclass

from schemas.response_schema_classes import ExampleFictionalChild

EXAMPLES: dict[str, dict[ExampleFictionalChild, str]] = {
    "cdc": {
        ExampleFictionalChild(
            measurement_method="bmi",
            sex="female",
            id="obesity"
        ): "Example 1"
    }
}

def get_examples_for_reference(reference: str) -> list[ExampleFictionalChild]:
    if reference in EXAMPLES:
        return list(EXAMPLES[reference].keys())

    return []

def get_example(reference: str, measurement_method: str, sex: str, id: str) -> str | None:
    pass