"""
Turner router
"""
# Standard imports
# from .measurement_class import MeasurementClass
from rcpchgrowth.constants.reference_constants import TRISOMY_21

# Third party imports
from fastapi import APIRouter
from rcpchgrowth import Measurement, constants, chart_functions, generate_fictional_child_data

# local imports
from .request_validation_classes import MeasurementRequest, ChartCoordinateRequest, FictionalChildRequest

# set up the API router
trisomy_21 = APIRouter(
    prefix="/trisomy-21",
)

@trisomy_21.post("/calculation")
def trisomy_21_calculation(measurementRequest: MeasurementRequest):
    """
    Centile calculation.
    ---
    post:
      summary: Trisomy 21 centile and SDS calculation.
      description: |
        * This endpoint MUST ONLY be used for children with Trisomy 21 (Down's Syndrome).
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

    try:
        calculation = Measurement(
            reference=constants.TRISOMY_21,
            **values
        ).measurement

        return calculation
    except Exception as err:
        return err, 400





@trisomy_21.post("/chart-coordinates")
def trisomy_21_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    Chart data.
    ---
    POST:
      summary: UK-WHO Chart coordinates in plottable format
        * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format
        * Requires a sex ('male' or 'female' lowercase) and a measurement_method ('height', 'weight' ,'bmi', 'ofc')

      requestBody:
        content:
          application/json:
            schema: ChartDataRequestParameters
            example:
                "sex": "female"
                "measurement_method":"height"

      responses:
        200:
          description: "Chart data for plotting a traditional growth chart was returned"
          content:
            application/json:
              schema: ChartDataResponseSchema
    """


    try:
        chart_data = chart_functions.create_chart(
            constants.TRISOMY_21, measurement_method=chartParams.measurement_method, sex=chartParams.sex, centile_selection=COLE_TWO_THIRDS_SDS_NINE_CENTILES)
    except Exception as err:
        print(err)

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

@trisomy_21.post('/fictional-child-data')
def fictional_child_data(fictional_child_request: FictionalChildRequest):
  try:
    life_course_fictional_child_data = generate_fictional_child_data(
      measurement_method=fictional_child_request.measurement_method,
      sex=fictional_child_request.sex,
      start_chronological_age=fictional_child_request.start_chronological_age,
      end_age=fictional_child_request.end_age,
      gestation_weeks=fictional_child_request.gestation_weeks,
      gestation_days=fictional_child_request.gestation_days,
      measurement_interval_type = fictional_child_request.measurement_interval_type,
      measurement_interval_number=fictional_child_request.measurement_interval_number,
      start_sds = fictional_child_request.start_sds,
      drift = fictional_child_request.drift,
      drift_range = fictional_child_request.drift_range,
      noise = fictional_child_request.noise,
      noise_range = fictional_child_request.noise_range,
      reference = TRISOMY_21
    )
    return life_course_fictional_child_data
  except ValueError:
    return 422