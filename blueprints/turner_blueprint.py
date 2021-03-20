"""
This module contains the Turner endpoints as Flask Blueprints
"""

import json
from pprint import pprint
from flask import Blueprint
from flask import jsonify, request
from marshmallow import ValidationError
from rcpchgrowth.rcpchgrowth.constants.parameter_constants import COLE_TWO_THIRDS_SDS_NINE_CENTILES, TURNERS
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from rcpchgrowth.rcpchgrowth.chart_functions import create_plottable_child_data, create_chart
from datetime import date, datetime
from schemas import *


turners = Blueprint("turners", __name__)


@turners.route("/calculation", methods=["POST"])
def turner_calculation():
    """
    Centile calculation.
    ---
    post:
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
                birth_date: "2020-04-12T12:00:00Z"
                observation_date: "2020-06-12T12:00:00Z"
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
    if request.is_json:
        req = request.get_json()

        values = {
            'birth_date': req["birth_date"],
            'observation_date': req["observation_date"],
            'measurement_method': req["measurement_method"],
            'observation_value': req["observation_value"],
            'sex': req["sex"],
            'gestation_weeks': req["gestation_weeks"],
            'gestation_days': req["gestation_days"]
        }

        # Validate the request with Marshmallow
        try:
            CalculationRequestParameters().load(values)
        except ValidationError as err:
            pprint(err.messages)
            return json.dumps(err.messages), 422

        calculation = Measurement(
            sex=req["sex"],
            birth_date=datetime.strptime(
                req["birth_date"], "%Y-%m-%dT%H:%M:%S"),
            observation_date=datetime.strptime(
                req["observation_date"], "%Y-%m-%dT%H:%M:%S"),
            measurement_method=str(req["measurement_method"]),
            observation_value=float(req["observation_value"]),
            gestation_weeks=req["gestation_weeks"],
            gestation_days=req["gestation_days"],
            reference=TURNERS
        ).measurement

        return jsonify(calculation)
    else:
        return "Request body mimetype should be application/json", 400


@turners.route("/plottable-child-data", methods=["POST"])
def turner_plottable_child_data():
    """
    Child growth data in plottable format.
    ---
    post:
      summary: Child growth data in plottable format.
      description: |
        * Requires results data parameters from a call to the calculation endpoint.
        * Returns child measurement data in a plottable format (x and y parameters), with centiles and ages for labels.

      requestBody:
        content:
          application/json:
            schema: ChartDataRequestParameters

      responses:
        200:
          description: |
            * Child growth data in plottable format (x and y parameters, centile and age labels) was returned.
          content:
            application/json:
              schema: ChartDataResponseSchema
    """
    if request.is_json:
        req = request.get_json()
        results = req["results"]

        # data are serial data points for a single child
        # Prepare data from plotting
        child_data = create_plottable_child_data(results)
        # Retrieve sex of child to select correct centile charts
        sex = results[0]["birth_data"]["sex"]
        return jsonify({
            "sex": sex,
            "child_data": child_data,
        })
    else:
        return "Request body mimetype should be application/json", 400


@turners.route("/chart-coordinates", methods=["GET"])
def turner_chart_coordinates():
    """
    Chart data.
    ---
    get:
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
        chart_data = create_chart(
            TURNERS, centile_selection=COLE_TWO_THIRDS_SDS_NINE_CENTILES)
    except Exception as err:
        print(err)
        return "Server error fetching chart data.", 400
    return jsonify({
        "centile_data": chart_data
    })


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
