"""
Turner router
"""
# Standard imports
import json
from pathlib import Path

# Third party imports
from fastapi import APIRouter, Body, HTTPException

# RCPCH imports
from rcpchgrowth import Measurement, constants, chart_functions, generate_fictional_child_data
from schemas import MeasurementRequest, ChartCoordinateRequest, FictionalChildRequest

# set up the API router
turners = APIRouter(
    prefix="/turner",
)

@turners.post("/calculation", tags=["turners-syndrome"])
def turner_calculation(measurementRequest: MeasurementRequest = Body(
        ...,
        example={
            "birth_date": "2020-04-12",
            "observation_date": "2024-06-12",
            "observation_value": 78,
            "measurement_method": "height",
            "sex": "female",
            "gestation_weeks": 39,
            "gestation_days": 2,
        }
)):
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
            events_text=measurementRequest.events_text
        ).measurement
    except ValueError as err:
        print(err.args)
        return err.args, 422
    return calculation
    

@turners.post("/chart-coordinates", tags=["turners-syndrome"])
def turner_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    ## Turner's Syndrome Chart Coordinates data.
    
    * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format
    * Note height in girls conly be only returned. It is a post request to maintain consistency with other routes.
    \f
    Return object structure (this needs to be moved into the schema)
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
        return "Turner data only exists for height in girls."

    chart_data=None
    chart_data_file = Path(
                f'chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json')
    if chart_data_file.exists():
        print(f'Chart data file exists for {chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.')
        with open(f'chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json', 'r') as file:
            chart_data = json.load(file)
    else:
        return HTTPException(status_code=422, detail=f"Item not found: chart-data/{chartParams.centile_format}-{constants.TURNERS}-{chartParams.sex}-{chartParams.measurement_method}.json")
        
    return {
        "centile_data": chart_data
    }


@turners.post('/fictional-child-data', tags=["turners-syndrome"])
def fictional_child_data(fictional_child_request: FictionalChildRequest):
    """
    ## Turner's Fictional Child Data Endpoint
    
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
            reference=constants.TURNERS
        )
        return life_course_fictional_child_data
    except ValueError:
        return 422
