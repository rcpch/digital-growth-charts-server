"""
Turner router
"""
# Standard imports

# Third party imports
from fastapi import APIRouter, Body

# RCPCH imports
from rcpchgrowth import Measurement, constants, chart_functions, generate_fictional_child_data
from schemas import MeasurementRequest, ChartCoordinateRequest, FictionalChildRequest

# set up the API router
turners = APIRouter(
    prefix="/turner",
)


@turners.post("/calculation")
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
    ## Turner's Syndrome Calculations.
        
    Turner's Syndrome centile and SDS calculations.

    * This endpoint MUST ONLY be used for **female** children with the chromosomal disorder Turner's Syndrome (45,XO karyotype).  
    * Returns a single centile/SDS calculation for the selected `measurement_method`.  
    * Gestational age correction will be applied automatically if appropriate, according to the gestational age at birth data supplied.  
    * Available `measurement_method`s are: `height` **only** because this reference data is all that exists.  
    """

    # Dates will discard anything after first 'T' in YYYY-MM-DDTHH:MM:SS.milliseconds+TZ etc
    values = {
        'birth_date': measurementRequest.birth_date,
        'gestation_days': measurementRequest.gestation_days,
        'gestation_weeks': measurementRequest.gestation_weeks,
        'measurement_method': measurementRequest.measurement_method,
        'observation_date':
            measurementRequest.observation_date,
        'observation_value': measurementRequest.observation_value,
        'sex': measurementRequest.sex
    }

    # Send to calculation
    try:
        calculation = Measurement(
            reference=constants.TURNERS,
            **values
        ).measurement
    except ValueError as err:
        print(err.args)
        return err.args, 422

    return calculation


@turners.post("/chart-coordinates")
def turner_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    Chart data.
    ---
    POST:
      summary: UK-WHO Chart coordinates in plottable format
        * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format
        * Note height in girls conly be only returned. It is a post request to maintain consistency with other routes.

      requestBody:
        content:
          application/json:
            schema: ChartDataRequestParameters

      responses:
        200:
          description: "Chart data for plotting a traditional growth chart was returned"
          content:
            application/json:
              schema: ChartDataResponseSchema
    """

    if chartParams.sex == "male" or chartParams.measurement_method != "height":
        return "Turner data only exists for height in girls."

    try:
        chart_data = chart_functions.create_chart(
            constants.TURNERS, centile_selection=constants.COLE_TWO_THIRDS_SDS_NINE_CENTILES)
    except Exception as err:
        print(err)
        return "Server error fetching chart data.", 400
    return {
        "centile_data": chart_data
    }


"""
    Return object structure

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


@turners.post('/fictional-child-data')
def fictional_child_data(fictional_child_request: FictionalChildRequest):

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
            reference=TURNERS
        )

        return life_course_fictional_child_data
    except ValueError:
        return 422

