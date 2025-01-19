#!/usr/bin/env python3

import datetime

from flask import Flask, jsonify, render_template, Response, make_response
from flask_cors import CORS
import os
from flask import request

# if error -> export PYTHONPATH=/home/aron/szakdolgozat-raspberry-pi:$PYTHONPATH
from csibekelteto_utils import Utils
from csibekelteto_utils import log


app = Flask(__name__)
CORS(app)

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

lid_file_path = os.path.join(base_dir, "lid-status.txt")

utils: Utils = Utils()


def api_200_ok_response(
        response: str,
        status_code: int=200,
        other: list | None=None
) -> Response:

    return make_response(
        jsonify({
            "status_code": status_code,
            "response": response,
            "timestamp": datetime.datetime.now(),
            "other": other
        }), 200
    )

def api_404_not_found_response(
        response: str,
        status_code: int=404,
        other: list | None=None
) -> Response:

    return make_response(
        jsonify({
            "status_code": status_code,
            "response": response,
            "timestamp": datetime.datetime.now(),
            "other": other
        }), 404
    )

def api_501_not_implemented_response(
        response: str,
        status_code: int=501,
        other: list | None=None
) -> Response:

    return make_response(
        jsonify({
            "status_code": status_code,
            "response": response,
            "timestamp": datetime.datetime.now(),
            "other": other
        }), 501
    )


""" Routes """


@app.route("/")
def index():
    log(
        description="Home page loaded",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return render_template(
        template_name_or_list="index.html",
        version="v2025.01.09",
        text="Csibekeltető",
    )

""" hatching """

@app.route("/prepare-hatching")
def prepare_hatching() -> Response:
    log(
        description="preparing hatching",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.prepare_hatching()

    return api_501_not_implemented_response("/prepare-hatching not implemented yet")

@app.route("/start-hatching", methods=['GET'])
def start_hatching() -> Response:
    log(
        description="starting hatching",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.start_hatching()

    return api_501_not_implemented_response("/start-hatching not implemented yet")


@app.route("/is-start-hatching", methods=['GET'])
def is_start_hatching() -> Response:
    """ TODO: check if hatching is started """
    return api_501_not_implemented_response("/is-start-hatching not implemented yet")

""" red led """

@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led() -> Response:
    log(
        description="red led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_red_led()

    return api_200_ok_response("red led is on")


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led() -> Response:
    log(
        description="red led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_red_led()

    return api_200_ok_response("red led is off")

""" green led """

@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led() -> Response:
    log(
        description="green led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_green_led()

    return api_200_ok_response("green led is on")


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led() -> Response:
    log(
        description="green led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_green_led()

    return api_200_ok_response("green led is off")

""" white led"""

@app.route("/on-white-led", methods=['GET'])
def turn_on_white_led() -> Response:
    log(
        description="white led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_white_led()

    return api_200_ok_response("white led is on")


@app.route("/off-white-led", methods=['GET'])
def turn_off_white_led() -> Response:
    log(
        description="white led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_white_led()

    return api_200_ok_response("white led is off")

""" orange led """

@app.route("/on-orange-led")
def turn_on_orange_led() -> Response:
    log(
        description="orange led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_orange_led()

    return api_200_ok_response("orange led is on")

@app.route("/off-orange-led")
def turn_off_orange_led() -> Response:
    log(
        description="orange led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_orange_led()

    return api_200_ok_response("orange led is off")

""" yellow led """

@app.route("/on-yellow-led", methods=['GET'])
def turn_on_yellow_led() -> Response:
    log(
        description="yellow led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_yellow_led()

    return api_200_ok_response("yellow led is on")


@app.route("/off-yellow-led", methods=['GET'])
def turn_off_yellow_led() -> Response:
    log(
        description="yellow led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_yellow_led()

    return api_200_ok_response("yellow led is off")

""" cold white led """

@app.route("/on-cold-white-led", methods=['GET'])
def turn_on_cold_white_led() -> Response:
    log(
        description="cold white led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_cold_white_led()

    return api_200_ok_response("cold white led is on")


@app.route("/off-cold-white-led", methods=['GET'])
def turn_off_cold_white_led() -> Response:
    log(
        description="cold_white led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_cold_white_led()

    return api_200_ok_response("cold_white led is off")


""" blue led """

@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led() -> Response:
    log(
        description="blue led is on",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.on_blue_led()

    return api_200_ok_response("blue led is on")


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led() -> Response:
    log(
        description="blue led is off",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    utils.off_blue_led()

    return api_200_ok_response("blue led is off")



""" get temp and hum """

@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor() -> Response:
    log(
        description="get temperature and humidity",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return utils.get_temp_and_hum(
        api_base_url=request.base_url,
        timestamp=datetime.datetime.now(),
        headers=request.user_agent.string
    )

""" set temp and hum """
""" TODO: if file has t and h and another api call enters, override value  """

@app.route("/set-temp", methods=['GET', 'PUT'])
def set_temperature() -> Response:
    log(
        description="set temperature",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    temp: str = request.args.get("t")  # url/set-temp?t=40.1 | type: float

    with open('set_temp_hum.txt', 'a+') as file:
        file.write(f"t: {temp}\n")

    return api_501_not_implemented_response("/set-temp not implemented yet")


@app.route("/set-hum", methods=['GET', 'PUT'])
def set_humidity() -> Response:
    log(
        description="set humidity",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    hum: str = request.args.get("h")  # url/set-hum?h=62.5 | type: float

    with open("set_temp)hum.txt", 'a+') as file:
        file.write(f"h: {hum}\n")

    return api_501_not_implemented_response("/set-hum not implemented yet")

""" lid/limit switch"""

@app.route("/get-lid-status", methods=['GET'])
def get_lid_status() -> Response:
    log(
        description="get lid status [on/off]",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return utils.lid_status(
        api_base_url=request.base_url,
        timestamp=datetime.datetime.now(),
        headers=request.user_agent.string
    )


""" cooler """

@app.route("/on-cooler", methods=['GET', 'PUT'])
def turn_on_cooler() -> Response:
    log(
        description="turn on cooler",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_cooler()

    return api_200_ok_response("cooler is on")


@app.route("/off-cooler", methods=['GET', 'PUT'])
def turn_off_cooler() -> Response:
    log(
        description="turn off cooler",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.off_cooler()

    return api_200_ok_response("cooler is off")

""" heating element """

@app.route("/on-heating-element", methods=['GET'])
def turn_on_heating_element() -> Response:
    log(
        description="turn on heating element",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_heating_element()

    return api_200_ok_response("heating element is on")


@app.route("/off-heating-element", methods=['GET'])
def turn_off_heating_element() -> Response:
    log(
        description="turn off heating element",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.off_heating_element()

    return api_200_ok_response("heating element is off")

""" dc motor """

@app.route("/on-dc-motor-forward", methods=['GET'])
def turn_on_dc_motor_forward() -> Response:
    log(
        description="turn on dc motor forward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_dc_motor_forward()

    return api_200_ok_response("dc motor forward is on")

@app.route("/off-dc-motor-forward", methods=['GET'])
def turn_off_dc_motor_forward() -> Response:
    log(
        description="turn off dc motor forward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.off_dc_motor_forward()

    return api_200_ok_response("dc motor forward is off")

@app.route("/on-dc-motor-backward", methods=['GET'])
def turn_on_dc_motor_backward() -> Response:
    log(
        description="turn on dc motor backward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_dc_motor_backward()

    return api_200_ok_response("dc motor backward is on")


@app.route("/off-dc-motor-backward", methods=['GET'])
def turn_off_dc_motor_backward() -> Response:
    log(
        description="turn off dc motor backward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    
    utils.off_dc_motor_backward()

    return api_200_ok_response("dc motor backward is off")


""" humidifier """

@app.route("/on-humidifier")
def turn_on_humidifier():
    log(
        description="turn on humidifier",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    # utils.on_humidifier()

    return api_501_not_implemented_response("/on-humidifier not implemented yet")


@app.route("/off-humidifier")
def turn_off_humidifier() -> Response:
    log(
        description="turn off humidifier",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    # utils.off_humidifier()

    return api_501_not_implemented_response("/off-humidifier not implemented yet")

""" other """

@app.route("/endpoints", methods=['GET'])
def endpoints() -> Response:
    log(
        description="get api endpoints",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    lst: list = ["%s" % rule for rule in app.url_map.iter_rules()][1:]

    return api_200_ok_response("ok", other=lst)


@app.route("/overall", methods=['GET'])
def overall() -> Response:
    log(
        description="overall",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return jsonify({
        "day": 0,
        "updated": datetime.datetime.now().__str__(),
        "temp": 0.0,
        "hum": 0.0
    })


@app.route('/health', methods=['GET'])
def health() -> Response:
    log(
        description="health",
        api_url=request.base_url,
    )

    return jsonify({
        "cpu": utils.health()[0][1],
        "total_ram": utils.health()[1][1],
        "ram": utils.health()[2][1],
        "vram": utils.health()[3][1]
    })


@app.route("/alive", methods=['GET'])
def alive() -> Response:
    """ TODO: the webserver will check if maintenance or not """
    log(
        description="checking if csibekelteto is alive",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return api_200_ok_response("csibekelteto is alive")


@app.route("/shutdown")
def shutdown() -> Response:
    """ Make some safety check??? """
    log(
        description="turn off raspi/csibekelteto",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    response = api_200_ok_response("RasPi is shutting down...")
    utils.shutdown()

    return response


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt as ki:
        pass
