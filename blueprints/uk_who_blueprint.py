"""
This module contains the UK-WHO endpoints as Flask Blueprints
"""

from flask import Blueprint
import controllers
from flask import Flask, jsonify, request
import json
from datetime import datetime
from schemas import *
from rcpchgrowth.rcpchgrowth.constants.measurement_constants import *
from marshmallow import ValidationError
from pprint import pprint

uk_who = Blueprint("uk_who", __name__)


@uk_who.route("/calculation", methods=["POST"])
def uk_who_calculation():
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
            schema: SingleCalculationRequestParameters
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
              schema: SingleCalculationResponseSchema
    """
    if request.is_json:
        req = request.get_json()
        print(req)

        values = {
            'birth_date': req["birth_date"],
            'observation_date': req["observation_date"],
            'measurement_method': req["measurement_method"],
            'observation_value': req["observation_value"],
            'sex': req["sex"],
            'gestation_weeks': req["gestation_weeks"],
            'gestation_days': req["gestation_days"]
        }

        pprint(values)

        # Validate the request with Marshmallow
        try:
            SingleCalculationRequestParameters().load(values)
        except ValidationError as err:
            pprint(err.messages)
            return json.dumps(err.messages), 422

        calculation = controllers.perform_calculation(**values)

        return jsonify(calculation)
    else:
        return "Request body mimetype should be application/json", 400


@uk_who.route("/chart-coordinates", methods=["POST"])
def uk_who_chart_coordinates():
    """
    Chart data.
    ---
    post:
      summary: UK-WHO Chart coordinates in plottable format, including the plottable child measuremnt coordinates
      description: |
        * Requires calculated child measurement results from a preceding call to the `uk-who/calculation` endpoint.
        * Pass these results back in as the JSON body payload.
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
        results = request.get_json()["results"]

        # if the gestation is passed in as None this will be regarded as indicating Term
        if results[0]["birth_data"]["gestation_weeks"] is None and results[0]["birth_data"]["gestation_weeks"] > 0:
            results[0]["birth_data"]["gestation_weeks"] = 40

        # Born preterm flag to pass to charts
        if results[0]["birth_data"]["gestation_weeks"] < TERM_LOWER_THRESHOLD_LENGTH_DAYS:
            born_preterm = False
        else:
            born_preterm = True

        # Get the X and Y values for the results
        child_data = controllers.create_data_plots(results)

        # Create Centile Charts
        centiles = controllers.create_centile_values(
            sex=results[0]["birth_data"]["sex"], born_preterm=born_preterm)

        return jsonify({
            "sex": results[0]["birth_data"]["sex"],
            "child_data": child_data,
            "centile_data": centiles
        })
    else:
        return "Request body should be application/json", 400


@uk_who.route("/plottable-child-data", methods=["POST"])
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
        # born preterm flag to pass to charts
        # born_preterm = (results[0]["birth_data"]["gestation_weeks"]
        #                 != 0 and results[0]["birth_data"]["gestation_weeks"] < 37)

        # data are serial data points for a single child
        # Prepare data from plotting
        child_data = controllers.create_plottable_child_data(results)
        # Retrieve sex of child to select correct centile charts
        sex = results[0]["birth_data"]["sex"]
        return jsonify({
            "sex": sex,
            "child_data": child_data,
        })
    else:
        return "Request body mimetype should be application/json", 400
