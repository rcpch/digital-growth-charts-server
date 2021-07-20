"""
Turner router
"""
# Standard imports
# from .measurement_class import MeasurementClass
import json
from datetime import datetime

# Third party imports
from fastapi import APIRouter
from rcpchgrowth import Measurement, constants, chart_functions

# local imports
from .request_validation_classes import MeasurementRequest, ChartCoordinateRequest

# set up the API router
turners = APIRouter(
    prefix="/turners",
    # tags=["uk90", "uk-who", "WHO", "England"]
)


@turners.post("/calculation")
def turner_calculation(measurementRequest: MeasurementRequest):
    """
    Centile calculation.
    ---
    POST:
      summary: Turner's Syndrome centile and SDS calculation.
      description: |
        * This endpoint MUST ONLY be used for children with the chromosomal disorder Turner's Syndrome (45,XO karyotype).
        * Returns a single centile/SDS calculation for the selected `measurement_method`.
        * Gestational age correction will be applied automatically if appropriate according to the gestational age at birth data supplied.
        * Available `measurement_method`s are: `height`, `weight`, `bmi`, or `ofc` (OFC = occipitofrontal circumference = 'head circumference').
        * Note that BMI must be precalculated for the `bmi` function.

      requestBody:
        content:
          application/json:
            schema: CalculationRequestParameters
            example:
                birth_date: "2020-04-12"
                observation_date: "2020-06-12"
                observation_value: 60
                measurement_method: "height"
                sex: male
                gestation_weeks: 40
                gestation_days: 4

      responses:
        200:
          description: "Centile calculation (single) according to the supplied data was returned"
          content:
            application/json:
              schema: CalculationResponseSchema
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