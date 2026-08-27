"""
Registry test: every `return HTTPException(...)` in the six reference
routers must be a `raise HTTPException(...)` instead.

Bug found by inspection, confirmed interactively: `HTTPException` objects
were being *returned* from three call sites per router (18 occurrences
across cdc.py, trisomy21.py, trisomy21aap.py, turner.py, ukwho.py, who.py):

  1. chart-coordinates, custom centile/SDS list -> create_chart() raises
  2. chart-coordinates, standard centile format -> chart asset file missing
  3. fictional-child-data -> generate_fictional_child_data() raises

Each of these endpoints declares a `response_model` (`Centile_Data` or
`List[MeasurementObject]`). Returning an `HTTPException` instance means
FastAPI tries to *serialise it as the declared response*, which fails
`response_model` validation and raises `fastapi.exceptions.ResponseValidationError`,
turning the intended 422 into an unhandled 500. Confirmed live:

    POST /uk-who/chart-coordinates {"centile_format": "extended-who-centiles", ...}
    -> fastapi.exceptions.ResponseValidationError:
       {'input': HTTPException(status_code=422, detail='Item not found: ...')}
    -> TestClient(raise_server_exceptions=False) reports status 500

Path 1 (missing chart asset) is exercised with a real request, using
`extended-who-centiles`, which is schema-valid but has no generated asset
file for any reference - a reliable, natural trigger.

Paths 1 (custom-centile error) and 3 (fictional-child error) are exercised
by monkeypatching `create_chart` / `generate_fictional_child_data` in the
router module under test to raise, because finding an input that reliably
makes the underlying `rcpchgrowth` functions themselves raise is fragile
and version-dependent, whereas the router's *own* handling of "the engine
raised" is exactly the contract this test needs to prove, independent of
what natural input would trigger it in practice.
"""

import pytest
from fastapi.testclient import TestClient

from main import app

client = TestClient(app, raise_server_exceptions=False)

# (route prefix, module import path, valid sex, valid measurement_method)
# Turner is female-height only; an upfront guard in the router returns a
# plain string for any other combination, which is a separate defect
# (triage item #12) and out of scope here.
ROUTERS = [
    ("/uk-who", "routers.ukwho", "male", "height"),
    ("/who", "routers.who", "male", "height"),
    ("/cdc", "routers.cdc", "male", "height"),
    ("/trisomy-21", "routers.trisomy21", "male", "height"),
    ("/trisomy-21-aap", "routers.trisomy21aap", "male", "height"),
    ("/turner", "routers.turner", "female", "height"),
]


@pytest.mark.parametrize("prefix,module_path,sex,method", ROUTERS)
def test_chart_coordinates_returns_422_for_a_missing_asset_file(prefix, module_path, sex, method):
    response = client.post(
        f"{prefix}/chart-coordinates",
        json={
            "sex": sex,
            "measurement_method": method,
            "is_sds": False,
            "centile_format": "extended-who-centiles",  # schema-valid, no asset generated for it
        },
    )
    assert response.status_code == 422, (
        f"{prefix}/chart-coordinates returned {response.status_code} for a missing "
        f"chart asset file; expected 422. A 500 here means an HTTPException object "
        f"was returned instead of raised."
    )
    assert "Item not found" in response.json()["detail"][0]["msg"]


@pytest.mark.parametrize("prefix,module_path,sex,method", ROUTERS)
def test_chart_coordinates_returns_422_when_create_chart_raises(
    prefix, module_path, sex, method, monkeypatch
):
    import importlib

    module = importlib.import_module(module_path)

    def raise_error(*args, **kwargs):
        raise RuntimeError("simulated create_chart failure")

    monkeypatch.setattr(module, "create_chart", raise_error)

    response = client.post(
        f"{prefix}/chart-coordinates",
        json={
            "sex": sex,
            "measurement_method": method,
            "is_sds": False,
            "centile_format": [10, 50, 90],  # a list selects the custom-centile branch
        },
    )
    assert response.status_code == 422, (
        f"{prefix}/chart-coordinates returned {response.status_code} when create_chart() "
        f"raised; expected 422. A 500 here means an HTTPException object was returned "
        f"instead of raised."
    )
    assert "Error creating" in response.json()["detail"][0]["msg"]


@pytest.mark.parametrize("prefix,module_path,sex,method", ROUTERS)
def test_fictional_child_data_returns_422_when_generator_raises(
    prefix, module_path, sex, method, monkeypatch
):
    import importlib

    module = importlib.import_module(module_path)

    def raise_error(*args, **kwargs):
        raise RuntimeError("simulated generate_fictional_child_data failure")

    monkeypatch.setattr(module, "generate_fictional_child_data", raise_error)

    response = client.post(
        f"{prefix}/fictional-child-data",
        json={"measurement_method": method, "sex": sex},
    )
    assert response.status_code == 422, (
        f"{prefix}/fictional-child-data returned {response.status_code} when "
        f"generate_fictional_child_data() raised; expected 422. A 500 here means "
        f"an HTTPException object was returned instead of raised."
    )
