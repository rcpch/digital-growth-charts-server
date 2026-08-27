"""
The case matrix for the API response regression sweep. See `README.md`.

A case is data, not code, so the matrix can grow without touching the
runner. `generate_snapshot.py` and `compare_snapshots.py` are the only
things that interpret this module.

Each generated calculation case is a dict:

    {
        "id": str,               # stable, human-readable, unique
        "endpoint": str,         # path relative to the reference prefix, e.g. "/calculation"
        "prefix": str,           # e.g. "/uk-who"
        "method": "POST",
        "body": dict,            # JSON request body
    }

Boundary ages are chosen to sit exactly on, or either side of, the
reference-selection and gestational-correction transitions identified as
highest-risk in the rcpchgrowth-rust specification: 42 weeks corrected,
2 years, 4 years, the WHO 1856-day (~5.081y) transition, and the upper
domain edges. A version bump that shifts behaviour at any of these
boundaries is exactly the kind of silent regression this sweep exists to
catch.
"""

from datetime import date, timedelta

REFERENCES = ["uk-who", "who", "cdc", "trisomy-21", "trisomy-21-aap"]
ALL_REFERENCES = REFERENCES + ["turner"]

SEXES = ["male", "female"]
METHODS = ["height", "weight", "ofc", "bmi"]

CHART_FORMATS = [
    "cole-nine-centiles",
    "three-percent-centiles",
    "five-percent-centiles",
    "eighty-five-percent-centiles",
    # "extended-who-centiles" deliberately excluded: known 500 (triage item 8).
    # Include it once that defect is resolved, so the sweep starts asserting
    # a 200 instead of silently continuing to skip it.
]

BASE_BIRTH_DATE = date(2015, 6, 15)

# (label, gestation_weeks, gestation_days, age_at_observation_years)
# age_at_observation_years is chronological age from birth, not corrected age.
BOUNDARY_CASES = [
    ("term_at_birth", 40, 0, 0.0),
    ("term_day_14", 40, 0, 14 / 365.25),
    ("very_preterm_25wk_at_birth", 25, 0, 0.0),
    ("preterm_32wk_at_birth", 32, 0, 0.0),
    ("preterm_36wk6d_at_birth", 36, 6, 0.0),
    ("preterm_37wk_at_birth", 37, 0, 0.0),
    ("postterm_42wk_at_birth", 42, 0, 0.0),
    # Chronological age at which a 32-weeker's *corrected* age crosses 42
    # weeks post-menstrual (i.e. corrected age = 0): 10 weeks chronological.
    ("preterm_32wk_at_corrected_term", 32, 0, (42 - 32) * 7 / 365.25),
    # Chronological age at which a 32-weeker's corrected age crosses 2 years.
    ("preterm_32wk_at_corrected_2y", 32, 0, 2 + (40 - 32) * 7 / 365.25),
    ("term_at_2y", 40, 0, 2.0),
    ("term_at_4y", 40, 0, 4.0),
    ("term_at_who_5081y_transition", 40, 0, 1856 / 365.25),
    ("term_at_10y", 40, 0, 10.0),
    ("term_at_17y", 40, 0, 17.0),
    ("term_at_18y", 40, 0, 18.0),
    ("term_at_20y", 40, 0, 20.0),
]

# Turner reference is female-height-only, and its data run 1-20y annually;
# gestation is not clinically applicable to it, so hold it at term.
TURNER_BOUNDARY_CASES = [
    ("just_above_1y", 40, 0, 1.001),
    ("term_at_2y", 40, 0, 2.0),
    ("term_at_10y", 40, 0, 10.0),
    ("term_at_17y", 40, 0, 17.0),
    ("term_at_20y", 40, 0, 20.0),
]

REFERENCE_PREFIX = {
    "uk-who": "/uk-who",
    "who": "/who",
    "cdc": "/cdc",
    "trisomy-21": "/trisomy-21",
    "trisomy-21-aap": "/trisomy-21-aap",
    "turner": "/turner",
}

# Plausible observation value per method, at the reference median, so most
# calculation cases hit the "ordinary" code path rather than a validation
# rejection. A few deliberately extreme cases are added separately.
OBSERVATION_VALUE = {
    "height": 100.0,
    "weight": 20.0,
    "ofc": 50.0,
    "bmi": 18.0,
}


def _dates(gestation_weeks, gestation_days, age_years):
    birth_date = BASE_BIRTH_DATE
    observation_date = birth_date + timedelta(days=age_years * 365.25)
    return birth_date, observation_date


def calculation_cases():
    cases = []
    for reference in REFERENCES:
        prefix = REFERENCE_PREFIX[reference]
        for sex in SEXES:
            for method in METHODS:
                for label, gw, gd, age in BOUNDARY_CASES:
                    birth_date, observation_date = _dates(gw, gd, age)
                    cases.append(
                        {
                            "id": f"calc/{reference}/{sex}/{method}/{label}",
                            "prefix": prefix,
                            "endpoint": "/calculation",
                            "method": "POST",
                            "body": {
                                "birth_date": birth_date.isoformat(),
                                "observation_date": observation_date.isoformat(),
                                "observation_value": OBSERVATION_VALUE[method],
                                "sex": sex,
                                "measurement_method": method,
                                "gestation_weeks": gw,
                                "gestation_days": gd,
                            },
                        }
                    )
    # Turner: female height only.
    for label, gw, gd, age in TURNER_BOUNDARY_CASES:
        birth_date, observation_date = _dates(gw, gd, age)
        cases.append(
            {
                "id": f"calc/turner/female/height/{label}",
                "prefix": "/turner",
                "endpoint": "/calculation",
                "method": "POST",
                "body": {
                    "birth_date": birth_date.isoformat(),
                    "observation_date": observation_date.isoformat(),
                    "observation_value": OBSERVATION_VALUE["height"],
                    "sex": "female",
                    "measurement_method": "height",
                    "gestation_weeks": gw,
                    "gestation_days": gd,
                },
            }
        )
    # Deliberate extreme values, one per method, against uk-who: exercises
    # the validation-rejection error strings at the documented ±8/±15 SD
    # boundary, which are exactly the kind of hand-authored text a
    # refactor can silently reword.
    extreme_birth, extreme_obs = _dates(40, 0, 5.0)
    for method, extreme_value in [
        ("height", 300.0),
        ("weight", 200.0),
        ("ofc", 5.0),
        ("bmi", 100.0),
    ]:
        cases.append(
            {
                "id": f"calc/uk-who/female/{method}/extreme_value",
                "prefix": "/uk-who",
                "endpoint": "/calculation",
                "method": "POST",
                "body": {
                    "birth_date": extreme_birth.isoformat(),
                    "observation_date": extreme_obs.isoformat(),
                    "observation_value": extreme_value,
                    "sex": "female",
                    "measurement_method": method,
                    "gestation_weeks": 40,
                    "gestation_days": 0,
                },
            }
        )
    return cases


def chart_coordinate_cases():
    cases = []
    for reference in REFERENCES:
        prefix = REFERENCE_PREFIX[reference]
        for sex in SEXES:
            for method in METHODS:
                for centile_format in CHART_FORMATS:
                    cases.append(
                        {
                            "id": f"chart/{reference}/{sex}/{method}/{centile_format}",
                            "prefix": prefix,
                            "endpoint": "/chart-coordinates",
                            "method": "POST",
                            "body": {
                                "sex": sex,
                                "measurement_method": method,
                                "is_sds": False,
                                "centile_format": centile_format,
                            },
                        }
                    )
    for centile_format in CHART_FORMATS:
        cases.append(
            {
                "id": f"chart/turner/female/height/{centile_format}",
                "prefix": "/turner",
                "endpoint": "/chart-coordinates",
                "method": "POST",
                "body": {
                    "sex": "female",
                    "measurement_method": "height",
                    "is_sds": False,
                    "centile_format": centile_format,
                },
            }
        )
    return cases


def fictional_child_cases():
    cases = []
    for reference in REFERENCES:
        prefix = REFERENCE_PREFIX[reference]
        for sex in SEXES:
            for method in METHODS:
                cases.append(
                    {
                        "id": f"fictional/{reference}/{sex}/{method}",
                        "prefix": prefix,
                        "endpoint": "/fictional-child-data",
                        "method": "POST",
                        "body": {
                            "measurement_method": method,
                            "sex": sex,
                            "noise": False,
                            "drift": False,
                        },
                    }
                )
    cases.append(
        {
            "id": "fictional/turner/female/height",
            "prefix": "/turner",
            "endpoint": "/fictional-child-data",
            "method": "POST",
            "body": {
                "measurement_method": "height",
                "sex": "female",
                "noise": False,
                "drift": False,
            },
        }
    )
    for label, request_overrides in [
        (
            "end_age_equals_start_age",
            {"start_chronological_age": 2.0, "end_age": 2.0},
        ),
        ("zero_interval", {"measurement_interval_number": 0}),
        (
            "range_shorter_than_interval",
            {
                "start_chronological_age": 0.0,
                "end_age": 0.01,
                "measurement_interval_type": "years",
                "measurement_interval_number": 1,
            },
        ),
    ]:
        cases.append(
            {
                "id": f"fictional/uk-who/female/height/{label}",
                "prefix": "/uk-who",
                "endpoint": "/fictional-child-data",
                "method": "POST",
                "body": {
                    "measurement_method": "height",
                    "sex": "female",
                    "noise": False,
                    "drift": False,
                    **request_overrides,
                },
            }
        )
    return cases


def bulk_calculation_cases():
    cases = []
    for reference in REFERENCES:
        prefix = REFERENCE_PREFIX[reference]
        birth_date, _ = _dates(40, 0, 0.0)
        all_valid_observations = [
            {
                "observation_date": (birth_date + timedelta(days=age_years * 365.25)).isoformat(),
                "observation_value": OBSERVATION_VALUE["height"],
            }
            for age_years in (0.05, 1.0, 5.0)
        ]
        mixed_observations = all_valid_observations + [
            {
                "observation_date": (birth_date + timedelta(days=5 * 365.25)).isoformat(),
                "observation_value": 300.0,  # deliberately out of range
            }
        ]
        cases.append(
            {
                "id": f"bulk/{reference}/all_valid",
                "prefix": prefix,
                "endpoint": "/bulk-calculation",
                "method": "POST",
                "body": {
                    "birth_date": birth_date.isoformat(),
                    "sex": "female",
                    "measurement_method": "height",
                    "gestation_weeks": 40,
                    "gestation_days": 0,
                    "observations": all_valid_observations,
                },
            }
        )
        cases.append(
            {
                "id": f"bulk/{reference}/mixed_valid_and_invalid",
                "prefix": prefix,
                "endpoint": "/bulk-calculation",
                "method": "POST",
                "body": {
                    "birth_date": birth_date.isoformat(),
                    "sex": "female",
                    "measurement_method": "height",
                    "gestation_weeks": 40,
                    "gestation_days": 0,
                    "observations": mixed_observations,
                },
            }
        )
    # Cardinality edges, checked once (not reference-specific behaviour).
    cases.append(
        {
            "id": "bulk/uk-who/empty_observations",
            "prefix": "/uk-who",
            "endpoint": "/bulk-calculation",
            "method": "POST",
            "body": {
                "birth_date": "2015-06-15",
                "sex": "female",
                "measurement_method": "height",
                "observations": [],
            },
        }
    )
    cases.append(
        {
            "id": "bulk/uk-who/exceeds_max_201",
            "prefix": "/uk-who",
            "endpoint": "/bulk-calculation",
            "method": "POST",
            "body": {
                "birth_date": "2015-06-15",
                "sex": "female",
                "measurement_method": "height",
                "observations": [
                    {"observation_date": "2020-06-15", "observation_value": 100.0}
                ]
                * 201,
            },
        }
    )
    return cases


def utility_cases():
    cases = []
    for reference in ["uk-who", "cdc", "who"]:
        for sex in SEXES:
            cases.append(
                {
                    "id": f"utility/mid_parental_height/{reference}/{sex}/typical",
                    "prefix": "/utilities",
                    "endpoint": "/mid-parental-height",
                    "method": "POST",
                    "body": {
                        "height_paternal": 178.0,
                        "height_maternal": 165.0,
                        "sex": sex,
                        "reference": reference,
                    },
                }
            )
            cases.append(
                {
                    "id": f"utility/mid_parental_height/{reference}/{sex}/extreme",
                    "prefix": "/utilities",
                    "endpoint": "/mid-parental-height",
                    "method": "POST",
                    "body": {
                        "height_paternal": 250.0,
                        "height_maternal": 60.0,
                        "sex": sex,
                        "reference": reference,
                    },
                }
            )
    return cases


def all_cases():
    return (
        calculation_cases()
        + chart_coordinate_cases()
        + fictional_child_cases()
        + bulk_calculation_cases()
        + utility_cases()
    )
