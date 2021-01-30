"""
This module contains the Turner endpoints as Flask Blueprints
"""

import json
from pprint import pprint
from flask import Blueprint
from flask import jsonify, request
from marshmallow import ValidationError
from rcpchgrowth.rcpchgrowth.constants.parameter_constants import COLE_TWO_THIRDS_SDS_NINE_CENTILES, TRISOMY_21
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from rcpchgrowth.rcpchgrowth.chart_functions import create_plottable_child_data
from rcpchgrowth.rcpchgrowth.constants.parameter_constants import TRISOMY_21
from datetime import date, datetime
from schemas import *


trisomy_21 = Blueprint(TRISOMY_21, __name__)


@trisomy_21.route("/calculation", methods=["POST"])
def trisomy_21_calculation():
    """
    Centile calculation.
    ---
    post:
      summary: Centile and SDS Calculation route.
      description: |
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
            birth_date=datetime.strptime(req["birth_date"], "%Y-%m-%d"),
            observation_date=datetime.strptime(req["observation_date"],"%Y-%m-%d"),
            measurement_method=str(req["measurement_method"]),
            observation_value=float(req["observation_value"]),
            gestation_weeks=req["gestation_weeks"],
            gestation_days=req["gestation_days"],
            reference=TRISOMY_21
        ).measurement

        return jsonify(calculation)
    else:
        return "Request body mimetype should be application/json", 400


@trisomy_21.route("/plottable-child-data", methods=["POST"])
def trisomy_21_plottable_child_data():
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
