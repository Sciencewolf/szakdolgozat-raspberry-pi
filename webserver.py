#!/usr/bin/env python3

import datetime

from flask import Flask, jsonify, render_template, Response
from flask_cors import CORS
import os
from flask import request
from csibekelteto_utils import Utils
from csibekelteto_utils import log

app = Flask(__name__)
CORS(app)

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Create the full path for the text file
lid_file_path = os.path.join(base_dir, "lid-status.txt")

# Csibekelteto utils
utils: Utils = Utils()


@app.route("/")
def home():
    log(
        description="Home page loaded",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    return render_template(
        template_name_or_list="index.html",
        version="v2024.11.23",
        title="Csibekeltető",
        header="Csibekeltető"
    )

""" hatching """

@app.route("/prepare-hatching")
def prepare_hatching() -> Response:
    log(
        description="preparing hatching",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.prepare_hatching()

    return jsonify({
        "status_code": 200,
        "response": "ok",
        "timestamp": datetime.datetime.now()
    })

@app.route("/start-hatching", methods=['GET'])
def start_hatching() -> Response:
    log(
        description="starting hatching",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.start_hatching()

    return jsonify({
        "status_code": 200,
        "response": "hatching is started",
        "timestamp": datetime.datetime.now()
    })


@app.route("/is-start-hatching", methods=['GET'])
def is_start_hatching() -> Response:
    """ TODO: check if hatching is started """
    return jsonify({})

""" red led """

@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led() -> Response:
    log(
        description="red led is on",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_red_led()

    return jsonify({
        "status_code": 200,
        "content": "red led is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led() -> Response:
    log(
        description="red led is off",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_red_led()

    return jsonify({
        "status_code": 200,
        "content": "red led is off",
        "timestamp": datetime.datetime.now()
    })

""" green led """

@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led() -> Response:
    log(
        description="green led is on",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_green_led()

    return jsonify({
        "status_code": 200,
        "content": "green led is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led() -> Response:
    log(
        description="green led is off",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_green_led()

    return jsonify({
        "status_code": 200,
        "content": "green led is off",
        "timestamp": datetime.datetime.now()
    })

""" blue led """

@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led() -> Response:
    log(
        description="blue led is on",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_blue_led()

    return jsonify({
        "status_code": 200,
        "content": "blue led is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led() -> Response:
    log(
        description="blue led is off",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_blue_led()

    return jsonify({
        "status_code": 200,
        "content": "blue led is off",
        "timestamp": datetime.datetime.now()
    })

""" yellow led """

@app.route("/on-yellow-led", methods=['GET'])
def turn_on_yellow_led() -> Response:
    log(
        description="yellow led is on",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_yellow_led()

    return jsonify({
        "status_code": 200,
        "content": "yellow led is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-yellow-led", methods=['GET'])
def turn_off_yellow_led() -> Response:
    log(
        description="yellow led is off",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_yellow_led()

    return jsonify({
        "status_code": 200,
        "content": "yellow led is off",
        "timestamp": datetime.datetime.now()
    })

""" all led """

@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led() -> Response:
    log(
        description="all led is on",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_all_led()

    return jsonify({
        "status_code": 200,
        "content": "all led is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led() -> Response:
    log(
        description="all led is off",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_all_led()

    return jsonify({
        "status_code": 200,
        "content": "all led is off",
        "timestamp": datetime.datetime.now()
    })

""" get temp and hum """

@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor() -> Response:
    log(
        description="get temperature and humidity",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    return utils.get_temp_and_hum(
        api_base_url=request.base_url,
        timestamp=datetime.datetime.now(),
        headers=request.headers.__str__()
    )

""" set temp and hum """

@app.route("/set-temp", methods=['GET', 'PUT'])
def set_temperature() -> Response:
    log(
        description="set temperature",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    temp: str = request.args.get("t")  # url/set-temp?t=40.1 | type: float
    return jsonify({
        "status_code": 501,
        "content": "Not Implemented"
    })


@app.route("/set-hum", methods=['GET', 'PUT'])
def set_humidity() -> Response:
    log(
        description="set humidity",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    hum: str = request.args.get("h")  # url/set-hum?h=62.5 | type: float
    return jsonify({
        "status_code": 501,
        "content": "Not Implemented"
    })

""" lid/limit switch"""

@app.route("/get-lid-status", methods=['GET'])
def get_lid_status() -> Response:
    log(
        description="get lid status [on/off]",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    return utils.lid_status(
        api_base_url=request.base_url,
        timestamp=datetime.datetime.now(),
        headers=request.headers.__str__()
    )


""" cooler """

@app.route("/on-cooler", methods=['GET', 'PUT'])
def turn_on_cooler() -> Response:
    log(
        description="turn on cooler",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_cooler()

    return jsonify({
        "status_code": 200,
        "content": "cooler is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-cooler", methods=['GET', 'PUT'])
def turn_off_cooler() -> Response:
    log(
        description="turn off cooler",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_cooler()

    return jsonify({
        "status_code": 200,
        "content": "cooler is off",
        "timestamp": datetime.datetime.now()
    })

""" heating element """

@app.route("/on-heating-element", methods=['GET'])
def turn_on_heating_element() -> Response:
    log(
        description="turn on heating element",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_heating_element()

    return jsonify({
        "status_code": 200,
        "content": "heating element is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-heating-element", methods=['GET'])
def turn_off_heating_element() -> Response:
    log(
        description="turn off heating element",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_heating_element()

    return jsonify({
        "status_code": 200,
        "content": "heating element is off",
        "timestamp": datetime.datetime.now()
    })

""" dc motor """

@app.route("/on-dc-motor-forward", methods=['GET'])
def turn_on_dc_motor_forward() -> Response:
    log(
        description="turn on dc motor forward",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_dc_motor_forward()

    return jsonify({
        "status_code": 200,
        "content": "dc motor forward is on",
        "timestamp": datetime.datetime.now()
    })

@app.route("/off-dc-motor-forward", methods=['GET'])
def turn_off_dc_motor_forward() -> Response:
    log(
        description="turn off dc motor forward",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_dc_motor_forward()

    return jsonify({
        "status_code": 200,
        "content": "dc motor forward is off",
        "timestamp": datetime.datetime.now()
    })

@app.route("/on-dc-motor-backward", methods=['GET'])
def turn_on_dc_motor_backward() -> Response:
    log(
        description="turn on dc motor backward",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.on_dc_motor_backward()

    return jsonify({
        "status_code": 200,
        "content": "dc motor backward is on",
        "timestamp": datetime.datetime.now()
    })


@app.route("/off-dc-motor-backward", methods=['GET'])
def turn_off_dc_motor_backward() -> Response:
    log(
        description="turn off dc motor backward",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    utils.off_dc_motor_backward()

    return jsonify({
        "status_code": 200,
        "content": "dc motor backward is off",
        "timestamp": datetime.datetime.now()
    })

""" other """

@app.route("/endpoints", methods=['GET'])
def endpoints() -> Response:
    log(
        description="get api endpoints",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    lst: list = ["%s" % rule for rule in app.url_map.iter_rules()][1:]

    return jsonify({
        "status_code": 200,
        "content": "Ok",
        "routes": lst
    })


@app.route("/overall", methods=['GET'])
def overall() -> Response:
    log(
        description="overall",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    return jsonify({
        "day": 0,
        "updated": datetime.datetime.now().__str__(),
        "temp": 0.0,
        "hum": 0.0
    })


@app.route("/alive", methods=['GET'])
def alive() -> Response:
    """ TODO: the webserver will check if maintenance or not """
    log(
        description="checking if csibekelteto is alive",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    return jsonify({"response": "csibekelteto is alive"})


@app.route("/shutdown")
def shutdown() -> Response:
    """ Make some safety check??? """
    log(
        description="turn off raspi/csibekelteto",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )

    # Respond to the client before shutting down
    response = jsonify({
        "status_code": 200,
        "content": "RasPi is shutting down...",
        "timestamp": datetime.datetime.now()
    })
    utils.shutdown()

    return response


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt as ki:
        pass
