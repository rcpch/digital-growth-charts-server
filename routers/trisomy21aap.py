"""
trisomy-21-aap router
"""

# Standard imports
import json
from pathlib import Path
from typing import List
from pprint import pprint

# Third party imports
from schemas.response_schema_classes import Centile_Data, MeasurementObject, BulkMeasurementObject
from fastapi import APIRouter, Body, HTTPException, Depends

# RCPCH imports
from rcpchgrowth import (
    Measurement,
    constants,
    generate_fictional_child_data,
    create_chart,
)
from rcpchgrowth.constants.reference_constants import TRISOMY_21_AAP
from schemas import MeasurementRequest, BulkMeasurementRequest, ChartCoordinateRequest, FictionalChildRequest
from .validate_observation_value import validate_observation_value, MAX_BULK_OBSERVATIONS, validate_bulk_observations
from .utils import format_error

# set up the API router
trisomy_21_aap = APIRouter(
    prefix="/trisomy-21-aap",
)


@trisomy_21_aap.post("/calculation", tags=["trisomy-21-aap"], response_model=MeasurementObject)
def trisomy_21_aap_calculation(
    measurementRequest: MeasurementRequest = Body(
        ...,
        examples=[
            {
                "birth_date": "2020-04-12",
                "observation_date": "2028-06-12",
                "observation_value": 115,
                "sex": "female",
                "gestation_weeks": 40,
                "gestation_days": 0,
                "measurement_method": "height",
                "bone_age": 10,
                "bone_age_centile": 98,
                "bone_age_sds": 2.0,
                "bone_age_text": "This bone age is advanced",
                "bone_age_type": "greulich-pyle",
                "events_text": [
                    "Growth hormone start",
                    "Growth Hormone Deficiency diagnosis",
                ],
            }
        ],
    ),
):
    """
    ## Trisomy-21 AAP Centile and SDS Calculations

    * These are the 'standard' centiles for US children with trisomy-21. It uses the American Academy of Pediatrics dataset (American Academy of Pediatrics (AAP) Trisomy 21 reference. Zemel BS, Pipan M, Stallings VA, Hall W, Schgadt K, Freedman DS, Thorpe P. Growth Charts for Children with Down Syndrome in the U.S. Pediatrics, 2015).
    * UK users should use the UK Down Syndrome Growth Charts included in the RCPCHGrowth package and provide on a separate endpoint.
    * Returns a single centile/SDS calculation for the selected `measurement_method`.
    * Gestational age correction will be applied automatically if appropriate according to the gestational age at birth data supplied.
    * Available `measurement_method`s are: `height`, `weight`, `bmi`, or `ofc` (OFC = occipitofrontal circumference = 'head circumference').
    * Note that BMI must be precalculated for the `bmi` function.
    * Dates will discard anything after first 'T' in `YYYY-MM-DDTHH:MM:SS.milliseconds+TZ` etc
    * Bone ages are not supported for this reference.
    * Optional events can be passed in as a list of strings - each list is associated with a measurement
    """

    # Validate observation value
    try:
        validate_observation_value(TRISOMY_21_AAP, measurementRequest)
    except ValueError as err:
         # Format the error to look like Pydantic validation errors
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="value_error", input="observation_value")
        raise HTTPException(status_code=422, detail=[formatted_error])
    except LookupError as err:
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="lookup_error", input="observation_value")
        raise HTTPException(status_code=422, detail=[formatted_error])
    
    
    try:
        calculation = Measurement(
            reference=constants.TRISOMY_21_AAP,
            birth_date=measurementRequest.birth_date,
            gestation_days=measurementRequest.gestation_days,
            gestation_weeks=measurementRequest.gestation_weeks,
            measurement_method=measurementRequest.measurement_method,
            observation_date=measurementRequest.observation_date,
            observation_value=measurementRequest.observation_value,
            sex=measurementRequest.sex,
            bone_age=None,
            bone_age_centile=None,
            bone_age_sds=None,
            bone_age_text=None,
            bone_age_type=None,
            events_text=measurementRequest.events_text,
        ).measurement
    except ValueError as err:
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="value_error", input="calculation_error")
        raise HTTPException(status_code=422, detail=[formatted_error])
    except LookupError as err:
        formatted_error = format_error(loc=["body"], msg=str(err), error_type="lookup_error", input="observation_value")
        raise HTTPException(status_code=422, detail=[formatted_error])
    
    return calculation


@trisomy_21_aap.post("/bulk-calculation", tags=["trisomy-21-aap"], response_model=BulkMeasurementObject)
async def trisomy_21_aap_bulk_calculation(
    measurementRequest: BulkMeasurementRequest = Body(
        ...,
        examples=[
            {
                "measurement_method": "height",
                "birth_date": "2020-04-12",
                "sex": "female",
                "gestation_weeks": 40,
                "gestation_days": 0,
                "observations": [
                    {"observation_date": "2028-06-12", "observation_value": 115},
                    {"observation_date": "2028-12-12", "observation_value": 130},
                ],
            }
        ],
    ),
):
    results = []

    validate_bulk_observations(measurementRequest.observations)

    for observation in measurementRequest.observations:
        try:
            validate_observation_value(TRISOMY_21_AAP, measurementRequest, observation)
        except ValueError as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input="observation_value"))
            continue
        except LookupError as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="lookup_error", input="observation_value"))
            continue

        try:
            calculation = Measurement(
                reference=constants.TRISOMY_21_AAP,
                birth_date=measurementRequest.birth_date,
                gestation_days=measurementRequest.gestation_days,
                gestation_weeks=measurementRequest.gestation_weeks,
                measurement_method=measurementRequest.measurement_method,
                observation_date=observation.observation_date,
                observation_value=observation.observation_value,
                sex=measurementRequest.sex,
                bone_age=None,
                bone_age_centile=None,
                bone_age_sds=None,
                bone_age_text=None,
                bone_age_type=None,
                events_text=observation.events_text,
            ).measurement
        except Exception as err:
            results.append(format_error(loc=["body"], msg=str(err), error_type="value_error", input="calculation_error"))
            continue

        results.append(calculation)

    return {"results": results}


@trisomy_21_aap.post("/chart-coordinates", tags=["trisomy-21-aap"], response_model=Centile_Data)
def trisomy_21_aap_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    ## trisomy-21-aap Chart Coordinates data.

    * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format
    * Requires a sex ('male' or 'female' lowercase) and a measurement_method ('height', 'weight' ,'bmi', 'ofc')
    * If custom centiles/sds collections (individually or as a collection) are required, accepts a list of float values (up to 15) as centile_format parameter
    * The is_sds boolean flag (default false) specifies if the custom list is of SDS or centiles.
    * In addition to the custom list, "cole-nine-centiles" or "three-percent-centiles" can be specified which are standard collections.
    * If no centile_format is supplied, "cole-nine-centiles" are returned as a default.
    \f
    [
        "height": [
            {
                sds: -1.64,
                trisomy_21_aap_infants: [.....],
                trisomy_21_aap_children: [
                    {
                        label: 5, `this is the centile
                        x: 4, `this is the decimal age
                        y: 91.535  `this is the measurement
                    }
                    ....
                ]
            }
        ],
        ... repeat for weight, bmi, ofc, based on which measurements supplied. If only height data supplied, only height centile data returned
    ]
    """
    chart_data = None
    if type(chartParams.centile_format) is list:
        # custom centiles requested - calculate these and return. Do not persist.
        try:
            chart_data = create_chart(
                TRISOMY_21_AAP,
                chartParams.centile_format,
                measurement_method=chartParams.measurement_method,
                sex=chartParams.sex,
                is_sds=chartParams.is_sds,
            )
        except:
            return HTTPException(
                status_code=422,
                detail=f"Error creating {chartParams.sex} {chartParams.measurement_method} trisomy-21-aap chart on the server, using {chartParams.centile_format} centile format.",
            )
    else:
        chart_data_file = Path(
            f"chart-data/{chartParams.centile_format}-{constants.TRISOMY_21_AAP}-{chartParams.sex}-{chartParams.measurement_method}.json"
        )
        if chart_data_file.exists():
            print(
                f"Chart data file exists for {chartParams.centile_format}-{constants.TRISOMY_21_AAP}-{chartParams.sex}-{chartParams.measurement_method}."
            )
            with open(
                f"chart-data/{chartParams.centile_format}-{constants.TRISOMY_21_AAP}-{chartParams.sex}-{chartParams.measurement_method}.json",
                "r",
            ) as file:
                chart_data = json.load(file)
        else:
            return HTTPException(
                status_code=422,
                detail=f"Item not found: chart-data/{chartParams.centile_format}-{constants.TRISOMY_21_AAP}-{chartParams.sex}-{chartParams.measurement_method}.json",
            )
    return {"centile_data": chart_data}


@trisomy_21_aap.post(
    "/fictional-child-data", tags=["trisomy-21-aap"], response_model=List[MeasurementObject]
)
def fictional_child_data(fictional_child_request: FictionalChildRequest):
    """
    ## trisomy-21-aap Fictional Child Data Endpoint

    * Generates synthetic data for demonstration or testing purposes
    """
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
            reference=constants.TRISOMY_21_AAP,
        )
        return life_course_fictional_child_data
    except:
        return HTTPException(
            status_code=422,
            detail=f"Not possible to create trisomy-21-aap fictional child data.",
        )
