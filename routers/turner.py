"""
Turner router
"""

# Standard imports
import json
from pathlib import Path
from typing import List

# Third party imports
from fastapi import APIRouter, Body, HTTPException, Depends
from schemas.response_schema_classes import Centile_Data, MeasurementObject, BulkMeasurementObject

# RCPCH imports
from rcpchgrowth import (
    Measurement,
    constants,
    generate_fictional_child_data,
    create_chart,
)
from rcpchgrowth.constants.reference_constants import TURNERS
from schemas import MeasurementRequest, BulkMeasurementRequest, ChartCoordinateRequest, FictionalChildRequest
from .validate_observation_value import validate_observation_value, MAX_BULK_OBSERVATIONS, validate_bulk_observations
from .utils import format_error

# set up the API router
turners = APIRouter(
    prefix="/turner",
)


@turners.post(
    "/calculation", tags=["turners-syndrome"], response_model=MeasurementObject
)
async def turner_calculation(
    measurementRequest: MeasurementRequest = Body(
        ...,
        examples=[
            {
                "birth_date": "2020-04-12",
                "observation_date": "2024-06-12",
                "observation_value": 78,
                "measurement_method": "height",
                "sex": "female",
                "gestation_weeks": 39,
                "gestation_days": 2,
            }
        ],
    ),
    
):
    """
    ## Turner's Syndrome Centile and SDS Calculations.

    * This endpoint MUST ONLY be used for **female** children with the chromosomal disorder Turner's Syndrome (45,XO karyotype).
    * Returns a single centile/SDS calculation for the selected `measurement_method`.
    * Gestational age correction will be applied automatically if appropriate, according to the gestational age at birth data supplied.
    * Available `measurement_method`s are: `height` **only** because this reference data is all that exists.
    * Dates will discard anything after first 'T' in YYYY-MM-DDTHH:MM:SS.milliseconds+TZ etc
    * Optional Bone age data associated with a height can be passed:
    *   - `bone_age` as a float in years
    *   - `bone_age_sds` and `bone_age_centile` as floats
    *   - `bone_age_type` as one of `greulich-pyle`, `tanner-whitehouse-ii`, `tanner-whitehouse-iiI`, `fels`, `bonexpert`
    * Optional events can be passed in as a list of strings - each list is associated with a measurement
    """

    # custom error handling for Turner's Syndrome
    
    if measurementRequest.sex != "female":
        formatted_error = format_error(loc=["body"], msg=str("Turner reference data only exists in girls."), error_type="value_error", input="sex")
        raise HTTPException(status_code=422, detail=[formatted_error])
    
    if measurementRequest.measurement_method != "height":
        formatted_error = format_error(loc=["body"], msg=str("Turner reference data only exists for height"), error_type="value_error", input="measurement_method")
        raise HTTPException(status_code=422, detail=[formatted_error])

    # Validate observation value
    try:
        validate_observation_value(TURNERS, measurementRequest)
    except ValueError as err:
         # Format the error to look like Pydantic validation errors
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="value_error", input="observation_value")
        raise HTTPException(status_code=422, detail=[formatted_error])
    except LookupError as err:
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="lookup_error", input="observation_value")
        raise HTTPException(status_code=422, detail=[formatted_error])

    try:
        calculation = Measurement(
            reference=constants.TURNERS,
            birth_date=measurementRequest.birth_date,
            gestation_days=measurementRequest.gestation_days,
            gestation_weeks=measurementRequest.gestation_weeks,
            measurement_method=measurementRequest.measurement_method,
            observation_date=measurementRequest.observation_date,
            observation_value=measurementRequest.observation_value,
            sex=measurementRequest.sex,
            bone_age=measurementRequest.bone_age,
            bone_age_centile=measurementRequest.bone_age_centile,
            bone_age_sds=measurementRequest.bone_age_sds,
            bone_age_text=measurementRequest.bone_age_text,
            bone_age_type=measurementRequest.bone_age_type,
            events_text=measurementRequest.events_text,
        ).measurement
    except ValueError as err:
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="value_error", input="calculation_error")
        raise HTTPException(status_code=422, detail=[formatted_error])


    return calculation


@turners.post("/bulk-calculation", tags=["turners-syndrome"], response_model=BulkMeasurementObject)
async def turner_bulk_calculation(
    measurementRequest: BulkMeasurementRequest = Body(
        ...,
        examples=[
            {
                "measurement_method": "height",
                "birth_date": "2020-04-12",
                "sex": "female",
                "gestation_weeks": 39,
                "gestation_days": 2,
                "observations": [
                    {"observation_date": "2024-06-12", "observation_value": 78},
                    {"observation_date": "2024-08-12", "observation_value": 80},
                ],
            }
        ],
    ),
):
    results = []

    validate_bulk_observations(measurementRequest.observations)

    for observation in measurementRequest.observations:
        # custom reference constraints
        if measurementRequest.sex != "female":
            results.append(format_error(loc=["body"], msg="Turner reference data only exists in girls.", error_type="value_error", input="sex"))
            continue
        if measurementRequest.measurement_method != "height":
            results.append(format_error(loc=["body"], msg="Turner reference data only exists for height", error_type="value_error", input="measurement_method"))
            continue

        try:
            validate_observation_value(TURNERS, measurementRequest, observation)
        except ValueError as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input="observation_value"))
            continue
        except LookupError as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="lookup_error", input="observation_value"))
            continue

        try:
            calculation = Measurement(
                reference=constants.TURNERS,
                birth_date=measurementRequest.birth_date,
                gestation_days=measurementRequest.gestation_days,
                gestation_weeks=measurementRequest.gestation_weeks,
                measurement_method=measurementRequest.measurement_method,
                observation_date=observation.observation_date,
                observation_value=observation.observation_value,
                sex=measurementRequest.sex,
                bone_age=observation.bone_age,
                bone_age_centile=observation.bone_age_centile,
                bone_age_sds=observation.bone_age_sds,
                bone_age_text=observation.bone_age_text,
                bone_age_type=observation.bone_age_type,
                events_text=observation.events_text,
            ).measurement
        except Exception as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input="calculation_error"))
            continue

        results.append(calculation)

    return {"results": results}

@turners.post(
    "/chart-coordinates", tags=["turners-syndrome"], response_model=Centile_Data
)
def turner_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    ## Turner's Syndrome Chart Coordinates data.

    * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format
    * Note height in girls conly be only returned. It is a post request to maintain consistency with other routes.
    * If custom centiles/sds collections (individually or as a collection) are required, accepts a list of float values (up to 15) as centile_format parameter
    * The is_sds boolean flag (default false) specifies if the custom list is of SDS or centiles.
    * In addition to the custom list, "cole-nine-centiles" or "three-percent-centiles" can be specified which are standard collections.
    * If no centile_format is supplied, "cole-nine-centiles" are returned as a default.
    \f
    [
        "height": [
            {
                sds: -2.666666,
                uk90_child_data:[.....],
                uk90_preterm_data: [...],
                who_child_data: [...],
                who_infant_data: [
                    {
                        label: 0.4, `this is the centile
                        x: 4, `this is the decimal age
                        y: 91.535  `this is the measurement
                    }
                ]
            }
        ],
    ... repeat for weight, bmi, ofc, based on which measurements supplied. If only height data supplied, only height centile data returned
    ]
    """
    if chartParams.sex == "male" or chartParams.measurement_method != "height":
        raise HTTPException(status_code=422, detail="Turner data only exists for height in girls.")

    chart_data = None
    if type(chartParams.centile_format) is list:
        # custom centiles requested - calculate these and return. Do not persist
        try:
            chart_data = create_chart(
                constants.TURNERS,
                chartParams.centile_format,
                measurement_method=chartParams.measurement_method,
                sex=chartParams.sex,
                is_sds=chartParams.is_sds,
            )
        except:
            raise HTTPException(
                status_code=422,
                detail=f"Error creating {chartParams.sex} {chartParams.measurement_method} Turner's syndrome chart on the server, using {chartParams.centile_format} centile format.",
            )
    else:
        chart_data_file = Path(
            f"chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json"
        )
        if chart_data_file.exists():
            print(
                f"Chart data file exists for {chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}."
            )
            with open(
                f"chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json",
                "r",
            ) as file:
                chart_data = json.load(file)
        else:
            raise HTTPException(
                status_code=422,
                detail=f"Item not found: chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json",
            )

    return {"centile_data": chart_data}


@turners.post(
    "/fictional-child-data",
    tags=["turners-syndrome"],
    response_model=List[MeasurementObject],
)
def fictional_child_data(fictional_child_request: FictionalChildRequest):
    """
    ## Turner's Fictional Child Data Endpoint

    * Generates synthetic data for demonstration or testing purposes
    """
    if fictional_child_request.sex != "female":
        raise HTTPException(
            status_code=422,
            detail="Turner's Syndrome data only exists for girls.",
        )
    
    if fictional_child_request.measurement_method != "height":
        raise HTTPException(
            status_code=422,
            detail="Turner's Syndrome data only exists for height.",
        )

    try:
        life_course_fictional_child_data = generate_fictional_child_data(
            measurement_method=fictional_child_request.measurement_method,
            sex=fictional_child_request.sex,
            start_chronological_age=fictional_child_request.start_chronological_age,
            end_age=fictional_child_request.end_age,
            gestation_weeks=fictional_child_request.gestation_weeks,
            gestation_days=fictional_child_request.gestation_days,
            measurement_interval_type=fictional_child_request.measurement_interval_type,
            measurement_interval_number=fictional_child_request.measurement_interval_number,
            start_sds=fictional_child_request.start_sds,
            drift=fictional_child_request.drift,
            drift_range=fictional_child_request.drift_range,
            noise=fictional_child_request.noise,
            noise_range=fictional_child_request.noise_range,
            reference=constants.TURNERS,
        )
        return life_course_fictional_child_data
    except:
        raise HTTPException(
            status_code=422,
            detail=f"Not possible to create Turner fictional child data.",
        )
