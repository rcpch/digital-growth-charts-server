"""
UK-WHO router
"""
# Standard imports
import json
from pathlib import Path
from typing import List

# Third party imports
from schemas.response_schema_classes import Centile_Data, MeasurementObject
from fastapi import APIRouter, Body, HTTPException

# RCPCH imports
from rcpchgrowth import Measurement, constants, generate_fictional_child_data, create_chart
from rcpchgrowth.constants.reference_constants import UK_WHO
from schemas import MeasurementRequest, ChartCoordinateRequest, FictionalChildRequest

# set up the API router
uk_who = APIRouter(
    prefix="/uk-who",
)


@uk_who.post("/calculation", tags=["uk-who"], response_model=MeasurementObject)
def uk_who_calculation(
    measurementRequest: MeasurementRequest = Body(
        ...,
            example={
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
                "events_text": ["Growth hormone start", "Growth Hormone Deficiency diagnosis"]
            }
        )
    ):
    """
    ## UK-WHO Centile and SDS Calculations
        
    * These are the 'standard' centiles for children in the UK. It uses a hybrid of the WHO and UK90 datasets.  
    * For non-UK use you may need the WHO-only or CDC charts which we do not yet support, but we may add if demand is there.  Please contact us.
    * Returns a single centile/SDS calculation for the selected `measurement_method`.  
    * Gestational age correction will be applied automatically if appropriate according to the gestational age at birth data supplied.  
    * Available `measurement_method`s are: `height`, `weight`, `bmi`, or `ofc` (OFC = occipitofrontal circumference = 'head circumference').  
    * Note that BMI must be precalculated for the `bmi` function.  
    * Dates will discard anything after first 'T' in `YYYY-MM-DDTHH:MM:SS.milliseconds+TZ` etc
    * Optional Bone age data associated with a height can be passed:
    *   - `bone_age` as a float in years
    *   - `bone_age_sds` and `bone_age_centile` as floats
    *   - `bone_age_type` as one of `greulich-pyle`, `tanner-whitehouse-ii`, `tanner-whitehouse-iiI`, `fels`, `bonexpert`
    * Optional events can be passed in as a list of strings - each list is associated with a measurement
    """
    try:
        calculation = Measurement(
            reference=constants.UK_WHO,
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
            events_text=measurementRequest.events_text
        ).measurement
    except ValueError as err:
        print(err.args)
        return err.args, 422
    return calculation


@uk_who.post("/chart-coordinates", tags=["uk-who"], response_model=Centile_Data)
def uk_who_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    ## UK-WHO Chart Coordinates data.
        
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
                sds: -2.666666,
                uk90_child_data: [.....],
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
    chart_data=None
    if (type(chartParams.centile_format) is list):
        # custom centiles requested - calculate these and return. Do not persist.
        try:
            chart_data = create_chart(
                UK_WHO, 
                chartParams.centile_format, 
                measurement_method=chartParams.measurement_method, 
                sex=chartParams.sex,
                is_sds=chartParams.is_sds)
        except:
            return HTTPException(status_code=422, detail=f"Error creating {chartParams.sex} {chartParams.measurement_method} UK-WHO chart on the server, using {chartParams.centile_format} centile format.")
    else:
        chart_data_file = Path(
                    f'chart-data/{chartParams.centile_format}-{constants.UK_WHO}-{chartParams.sex}-{chartParams.measurement_method}.json')
        if chart_data_file.exists():
            print(f'Chart data file exists for {chartParams.centile_format}-{constants.UK_WHO}-{chartParams.sex}-{chartParams.measurement_method}.')
            with open(f'chart-data/{chartParams.centile_format}-{constants.UK_WHO}-{chartParams.sex}-{chartParams.measurement_method}.json', 'r') as file:
                chart_data = json.load(file)
        else:
            return HTTPException(status_code=422, detail=f"Item not found: chart-data/{chartParams.centile_format}-{constants.UK_WHO}-{chartParams.sex}-{chartParams.measurement_method}.json")
        
    return {
        "centile_data": chart_data
    }

@uk_who.post('/fictional-child-data', tags=["uk-who"], response_model=List[MeasurementObject])
def fictional_child_data(fictional_child_request: FictionalChildRequest):
    """
    ## UK-WHO Fictional Child Data Endpoint

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
            reference=constants.UK_WHO
        )
        return life_course_fictional_child_data
    except:
        return HTTPException(status_code=422, detail=f"Not possible to create UK-WHO fictional child data.")


