"""
UK-WHO router
"""
# Standard imports
from rcpchgrowth.constants.reference_constants import UK_WHO

# Third party imports
from fastapi import APIRouter, HTTPException
from rcpchgrowth import Measurement, constants, chart_functions, generate_fictional_child_data

# local imports
from .request_validation_classes import FictionalChildRequest, MeasurementRequest, ChartCoordinateRequest

# set up the API router
uk_who = APIRouter(
    prefix="/uk-who",
)


@uk_who.post("/calculation/")
def uk_who_calculation(measurementRequest: MeasurementRequest):
    """
    Centile calculation.
    ---
    POST:
      summary: UK-WHO centile and SDS calculation.
      description: |
        * These are the 'standard' centiles for children in the UK. It uses a hybrid of the WHO and UK90 datasets.
        * For non-UK use you may need the WHO-only or CDC charts which we do not yet support, but we may add if demand is there.
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
        # 'birth_date': req["birth_date"].split('T', 1)[0],
        'birth_date': measurementRequest.birth_date,
        'gestation_days': measurementRequest.gestation_weeks,
        'gestation_weeks': measurementRequest.gestation_days,
        'measurement_method': measurementRequest.measurement_method,
        'observation_date': measurementRequest.observation_date,
        'observation_value': measurementRequest.observation_value,
        'sex': measurementRequest.sex
    }

    # Send to calculation
    try:
        calculation = Measurement(
            reference=constants.UK_WHO,
            **values
        ).measurement
    except ValueError as err:
        print(err.args)
        return err.args, 422

    return calculation

@uk_who.post("/chart-coordinates")
def uk_who_chart_coordinates(chartParams: ChartCoordinateRequest):
    """
    Chart data.
    ---
    POST:
      summary: UK-WHO Chart coordinates in plottable format
        * Returns coordinates for constructing the lines of a traditional growth chart, in JSON format

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

    try:
        chart_data = chart_functions.create_chart(
            constants.UK_WHO, measurement_method=chartParams.measurement_method, sex=chartParams.sex, centile_selection=constants.COLE_TWO_THIRDS_SDS_NINE_CENTILES)
    except HTTPException(status_code=404, detail="Item not found") as err:
        print(err)
        return err, 422

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

@uk_who.post('/fictional-child-data')
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
      reference = UK_WHO
    )
    return life_course_fictional_child_data
  except ValueError:
    return 422