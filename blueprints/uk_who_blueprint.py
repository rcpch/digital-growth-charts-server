"""
This module contains the UK-WHO endpoints as Flask Blueprints
"""

# standard imports
from datetime import datetime
import json
from pprint import pprint

# third-party imports
from flask import Blueprint, jsonify, request
from marshmallow import ValidationError

# rcpch imports
from rcpchgrowth.rcpchgrowth.constants.measurement_constants import *
from rcpchgrowth.rcpchgrowth.constants.parameter_constants import COLE_TWO_THIRDS_SDS_NINE_CENTILES, UK_WHO
from rcpchgrowth.rcpchgrowth.chart_functions import create_plottable_child_data, create_chart
from rcpchgrowth.rcpchgrowth.measurement import Measurement
from schemas import *

uk_who = Blueprint("uk_who", __name__)


@uk_who.route("/calculation", methods=["POST"])
def uk_who_calculation():
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
    if request.is_json:
        req = request.get_json()
        print(req)

        # Dates will discard anything after first 'T' in YYYY-MM-DDTHH:MM:SS.milliseconds+TZ etc
        values = {
            'birth_date': req["birth_date"].split('T', 1)[0],
            'gestation_days': req["gestation_days"],
            'gestation_weeks': req["gestation_weeks"],
            'measurement_method': req["measurement_method"],
            'observation_date':
                req["observation_date"].split('T', 1)[0],
            'observation_value': float(req["observation_value"]),
            'sex': req["sex"]
        }

        # Validate the request with Marshmallow
        try:
            CalculationRequestParameters().load(values)
        except ValidationError as err:
            pprint(err.messages)
            return json.dumps(err.messages), 422

        # convert string dates to Python dates for the Measurement class
        values['birth_date'] = datetime.strptime(
            values['birth_date'], "%Y-%m-%d")
        values['observation_date'] = datetime.strptime(
            values['observation_date'], "%Y-%m-%d")

        # Send to calculation
        try:
            calculation = Measurement(
                reference=UK_WHO,
                **values
            ).measurement
        except ValueError as err:
            pprint(err.args)
            return json.dumps(err.args), 422

        return jsonify(calculation)
    else:
        return "Request body mimetype should be application/json", 400


@ uk_who.route("/chart-coordinates", methods=["POST"])
def uk_who_chart_coordinates():
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
    if request.is_json:
        req = request.get_json()
        print(req)
        values = {
            "sex": req["sex"],
            'measurement_method': req["measurement_method"]
        }

        try:
            ChartDataRequestParameters().load(values)
        except ValidationError as err:
            pprint(err.messages)
            return json.dumps(err.messages), 422

        try:
            chart_data = create_chart(
                UK_WHO, measurement_method=req["measurement_method"], sex=req["sex"], centile_selection=COLE_TWO_THIRDS_SDS_NINE_CENTILES)
        except Exception as err:
            print(err)

        return jsonify({
            "centile_data": chart_data
        })
    else:
        return "Request body mimetype should be application/json", 400


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


@ uk_who.route("/plottable-child-data", methods=["POST"])
def uk_who_plottable_child_data():
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


"""
There has been debate about this endpoint - ultimately it will become necessary when we start implementing multiple measurements
and analysing trends.
"""
# @uk_who.route("/calculations", methods=["POST"])
# def uk_who_calculations():
#     """
#     Centile calculations.
#     ---
#     post:
#       summary: Centile and SDS Calculation route.
#       description: |
#         * Returns multiple centile/SDS calculations for an array of measurements of the same 'measurement_method'.
#         * Gestational age correction will be applied automatically according to the gestational age at birth data supplied.
#         * Available `measurement_method`s are: `height`, `weight`, `bmi`, or `ofc` (OFC = occipitofrontal circumference = 'head circumference').
#         * Note that BMI must be precalculated for the `bmi` function.

#       requestBody:
#         content:
#           application/json:
#             schema: CalculationRequestParameters
#             example:
#                 birth_date: "2020-04-12"
#                 observation_date: "2020-06-12"
#                 observation_value: 60
#                 measurement_method: "height"
#                 sex: male
#                 gestation_weeks: 40
#                 gestation_days: 4

#       responses:
#         200:
#           description: "Centile calculation (single) according to the supplied data was returned"
#           content:
#             application/json:
#               schema: CalculationResponseSchema
#     """
#     if request.is_json:
#       req = request.get_json()
#       print(req)

#       results = []

#       for count,  measurement in enumerate(req):
#         value = {
#             'birth_date': measurement["birth_date"],
#             'observation_date': measurement["observation_date"],
#             'measurement_method': measurement["measurement_method"],
#             'observation_value': measurement["observation_value"],
#             'sex': measurement["sex"],
#             'gestation_weeks': measurement["gestation_weeks"],
#             'gestation_days': measurement["gestation_days"]
#         }

#         # Validate the request with Marshmallow
#         try:
#             CalculationRequestParameters().load(value)
#         except ValidationError as err:
#             pprint(err.messages)
#             return json.dumps(err.messages), 422

#         calculation = Measurement(
#             sex=measurement["sex"],
#             birth_date=datetime.strptime(measurement["birth_date"], "%Y-%m-%d"),
#             observation_date=datetime.strptime(measurement["observation_date"],"%Y-%m-%d"),
#             measurement_method=str(measurement["measurement_method"]),
#             observation_value=float(measurement["observation_value"]),
#             gestation_weeks=measurement["gestation_weeks"],
#             gestation_days=measurement["gestation_days"],
#             reference=UK_WHO
#         ).measurement

#         results.append(calculation)
#       return jsonify(results)
#     else:
#         return "Request body mimetype should be application/json", 400
