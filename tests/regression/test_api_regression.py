"""Golden contract tests against the running HTTP API."""

import json

import httpx
import pytest

from tests.regression.cases import all_cases
from tests.regression.compare_snapshots import diff_value
from tests.regression.golden import (
    API_BASE_URL,
    FAILURE_DIR,
    GOLDEN_DIR,
    KNOWN_SERVER_ERROR_CASES,
    golden_path,
    normalize_result_for_golden,
    run_case,
    wait_for_api,
    write_result,
)


CASES = all_cases()


def test_snapshot_diff_ignores_expected_dynamic_values():
    assert list(diff_value(1.0, 1.0 + 1e-15)) == []
    assert list(diff_value(1.0, 1.0 + 1e-9)) == [("", 1.0, 1.0 + 1e-9)]
    path = "body.provenance.api_server.commit"
    assert list(diff_value("a" * 40, "b" * 40, path)) == []
    assert list(diff_value("a" * 40, "unknown", path)) == [
        (path, "a" * 40, "unknown")
    ]


def test_golden_normalization_replaces_only_volatile_provenance_values():
    result = {
        "status_code": 200,
        "body": {
            "results": [
                {
                    "provenance": {
                        "growth_reference": "uk-who",
                        "calculation_engine": {
                            "name": "rcpch/rcpchgrowth-python",
                            "version": "4.6.4",
                            "commit": "a" * 40,
                        },
                        "api_server": {
                            "name": "rcpch/digital-growth-charts-server",
                            "version": "5.1.0",
                            "commit": "b" * 40,
                        },
                    },
                    "value": 42,
                }
            ]
        },
    }

    normalized = normalize_result_for_golden(result)
    provenance = normalized["body"]["results"][0]["provenance"]

    assert provenance == {
        "growth_reference": "uk-who",
        "calculation_engine": {
            "name": "rcpch/rcpchgrowth-python",
            "version": "<calculation-engine-version>",
            "commit": "<calculation-engine-commit>",
        },
        "api_server": {
            "name": "rcpch/digital-growth-charts-server",
            "version": "<api-server-version>",
            "commit": "<api-server-commit>",
        },
    }
    assert normalized["body"]["results"][0]["value"] == 42
    assert result["body"]["results"][0]["provenance"]["api_server"]["version"] == "5.1.0"


@pytest.fixture(scope="module")
def running_api():
    with httpx.Client(base_url=API_BASE_URL, timeout=60) as client:
        wait_for_api(client)
        yield client


def test_regression_case_registry_matches_goldens():
    case_ids = [case["id"] for case in CASES]
    assert len(case_ids) == len(set(case_ids)), "Regression case IDs must be unique"
    assert KNOWN_SERVER_ERROR_CASES <= set(case_ids), (
        "Every known server-error exception must name a current regression case"
    )

    expected_paths = {golden_path(case_id) for case_id in case_ids}
    actual_paths = set(GOLDEN_DIR.rglob("*.json"))
    assert actual_paths == expected_paths, (
        "Golden files must exactly match the case registry. "
        "Run s/regression-accept after reviewing the running API."
    )


@pytest.mark.parametrize("case", CASES, ids=lambda case: case["id"])
def test_running_api_matches_golden(case, running_api):
    expected_file = golden_path(case["id"])
    assert expected_file.exists(), (
        f"Missing golden for {case['id']}. Run s/regression-accept after reviewing "
        "the running API."
    )

    actual = run_case(running_api, case)
    if actual["status_code"] >= 500:
        assert case["id"] in KNOWN_SERVER_ERROR_CASES, (
            f"Unexpected server error for {case['id']}; do not accept this into the "
            "goldens."
        )
    if "__non_json_response__" in actual["body"]:
        assert case["id"] in KNOWN_SERVER_ERROR_CASES, (
            f"Expected a JSON response for {case['id']}."
        )

    expected = json.loads(expected_file.read_text())
    differences = list(diff_value(expected, normalize_result_for_golden(actual)))
    if differences:
        actual_file = golden_path(case["id"], FAILURE_DIR)
        write_result(actual_file, actual)
        displayed = differences[:100]
        details = "\n".join(
            f"  {path}:\n    expected: {before!r}\n    actual:   {after!r}"
            for path, before, after in displayed
        )
        if len(differences) > len(displayed):
            details += f"\n  ... {len(differences) - len(displayed)} more differences"
        pytest.fail(
            f"API response changed for {case['id']}:\n{details}\n"
            f"Full actual response: {actual_file}"
        )
