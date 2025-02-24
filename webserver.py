#!/usr/bin/env python3

import datetime

from flask import Flask, jsonify, render_template, Response, make_response
from flask_cors import CORS
import os
from flask import request
import threading

from csibekelteto_utils import Utils
from csibekelteto_utils import log


app = Flask(__name__)
CORS(app)

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

utils: Utils = Utils()


def api_200_ok_response(
        response: str | list | dict | None,
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
        version="v2025.02.10",
        text="Csibekeltető",
    )

""" hatching """

@app.route("/start-hatching", methods=['GET'])
def start_hatching() -> Response:
    log(
        description="starting hatching",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    threading.Thread(target=utils.start_hatching, daemon=True).start()

    return api_200_ok_response(response="hatching started")

@app.route("/stop-hatching")
def stop_hatching() -> Response:
    log(
        description="stop hatching",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.stop_hatching()

    return api_200_ok_response(response="hatching stopped")

@app.route("/resume-hatching", methods=["GET"])
def resume_hatching():
    log(
        reason="resume hatching",
        description="hatching is resumed after if manually stopped",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    response = utils.resume_hatching()

    if not response:
        return api_200_ok_response(response="hatching already running")
    
    return api_200_ok_response(response="hatching resumed")

@app.route("/is-hatching", methods=['GET'])
def is_hatching() -> Response:
    return api_200_ok_response(response=utils.is_hatching())


""" led config """

@app.route('/led-indication', methods=['GET'])
def led_indication() -> Response:
    val: str = request.args.get('val')

    with open('/home/aron/szakdolgozat-raspberry-pi/led_indication.txt', 'w') as file:
        file.write(f'led: {val}')

    return api_200_ok_response(response=f"led is {val}")

""" get day"""

@app.route("/get-day")
def get_day() -> Response:
    log(
        description="get day",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return api_200_ok_response(response=utils.get_day())

""" get stats """
@app.route("/get-stats")
def get_stats() -> Response:
    day = request.args.get("day")

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

    return utils.get_temp_and_hum()

""" set temp """

@app.route("/set-temp", methods=['GET', 'PUT'])
def set_temperature() -> Response:
    temp: str = request.args.get("t")  # url/set-temp?t=40.1 | type: float

    log(
        description=f"set temperature to {temp}",
        api_url=request.base_url,
        headers=request.user_agent.string
    )


    utils.set_temp(temp=temp)

    return api_200_ok_response(response=f"temperature set to {temp}")


""" lid/limit switch"""

@app.route("/get-lid-status", methods=['GET'])
def get_lid_status() -> Response:
    log(
        description="get lid status [Open/Close]",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return utils.lid_status()


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

@app.route("/on-engine-forward", methods=['GET'])
def turn_on_engine_forward() -> Response:
    log(
        description="turn on engine forward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_engine_forward()

    return api_200_ok_response("dc motor forward is on")

@app.route("/off-engine-forward", methods=['GET'])
def turn_off_engine_forward() -> Response:
    log(
        description="turn off engine forward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.off_engine_forward()

    return api_200_ok_response("dc motor forward is off")

@app.route("/on-engine-backward", methods=['GET'])
def turn_on_engine_backward() -> Response:
    log(
        description="turn on engine backward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.on_engine_backward()

    return api_200_ok_response("dc motor backward is on")


@app.route("/off-engine-backward", methods=['GET'])
def turn_off_engine_backward() -> Response:
    log(
        description="turn off engine backward",
        api_url=request.base_url,
        headers=request.user_agent.string
    )
    
    utils.off_engine_backward()

    return api_200_ok_response("dc motor backward is off")

@app.route("/rotate-eggs", methods=['GET'])
def rotate_eggs() -> Response:
    log(
        description="rotating eggs",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    utils.rotate_eggs()

    return api_200_ok_response(response="rotating eggs")


@app.route("/get-last-eggs-rotation", methods=['GET'])
def get_last_eggs_rotation(self) -> Response:
    log(
        description="get last eggs rotation",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return api_200_ok_response(response=utils.get_last_eggs_rotation())

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
        "response": utils.processes
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
    log(
        description="checking if csibekelteto is alive",
        api_url=request.base_url,
        headers=request.user_agent.string
    )

    return api_200_ok_response("csibekelteto is alive")


@app.route("/shutdown")
def shutdown() -> Response:
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
