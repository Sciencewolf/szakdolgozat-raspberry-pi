#!/usr/bin/env python3

import datetime
from deprecated import deprecated

from flask import Flask, jsonify, render_template, make_response, Response
from flask_cors import CORS
import subprocess
import os
from flask import request
import requests as re
from csibekelteto_system import Utils
from csibekelteto_system import log

app = Flask(__name__)
CORS(app)

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Get the home directory
home_dir = os.path.expanduser("~")

# Create the full path for the text file
lid_file_path = os.path.join(home_dir, "lid-status.txt")

# Csibekelteto system
utils: Utils = Utils()

@deprecated(reason="no reason to use this method")
def is_csibekelteto_online() -> bool:
    r = re.get(os.getenv("API_URL_ALIVE"))
    response_code = r.status_code
    print(response_code)
    return response_code == re.codes.ok


def csibekelteto_error(reason: str, description: str="") -> Response:
    log(
        reason=reason,
        description=description
    )
    return make_response({"content": "offline"}, 500)


@app.route("/")
def home():
    log(
        description="Home page loaded",
        api_url=request.base_url,
        headers=request.headers.__str__()
    )
    return render_template("index.html", version="v2024.11.17", title="Csibekeltető", header="Csibekeltető")


@app.route("/alive")
def alive():
    """ TODO: the webserver will check if maintenance or not """
    log(
        description="checking if csibekelteto is alive",
        api_url=request.base_url
    )
    return make_response({"response": "csibekelteto is alive"}, 200)


@app.route("/prepare-hatching")
def prepare_hatching():
    log(description="preparing hatching")
    utils.prepare_hatching()
    return make_response({"response": "ok", "timestamp": datetime.datetime.now()}, 200)

@app.route("/start-hatching", methods=['GET'])
def start_hatching():
    log(description="starting hatching")
    utils.start_hatching()
    return make_response({"response": "ok", "timestamp": datetime.datetime.now()}, 200)


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_red.py")])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_red.py"])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_green.py")])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_green.py"])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_blue.py")])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_blue.py"])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/rgb_led.py")])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led():
    subprocess.run(["pkill", "-f", "py-part/rgb_led.py"])

    return jsonify(
        {"status_code": 200,
         "content": "ok response",
         "timestamp": datetime.datetime.now()}
    )


@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor():
    result = subprocess.run(
        [os.path.join(base_dir, "py-part/temp_hum_sensor.py")],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify(
            {"status_code": 404,
             "content": "not found response",
             "timestamp": datetime.datetime.now()}
        )

    try:
        with open(os.path.join(base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip()
            hum = file.readline().strip()
            timestamp = file.readline().strip()
    except FileNotFoundError:
        return jsonify(
            {"status_code": 404,
             "content": "not found response",
             "timestamp": datetime.datetime.now()}
        )

    return jsonify(
        {"temp": temp,
         "hum": hum,
         "timestamp": timestamp}
    )


@app.route("/set-temp", methods=['GET'])
def set_temperature():
    temp: str = request.args.get("t")  # url/set-temp?t=40.1 | type: float
    return jsonify(
        {"status_code": 501,
         "content": "Not Implemented"}
    )


@app.route("/set-hum", methods=['GET'])
def set_humidity():
    hum: str = request.args.get("h")  # url/set-hum?h=62.5 | type: float
    return jsonify(
        {"status_code": 501,
         "content": "Not Implemented"}
    )


@app.route("/get-lid-status", methods=['GET'])
def get_lid_status():
    subprocess.Popen([os.path.join(base_dir, "py-part/switch.py")])

    if not os.path.exists(lid_file_path):
        return jsonify(
            {"status_code": 404,
             "lid": "undefined",
             "timestamp": datetime.datetime.now()}
        )

    with open(lid_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("!"):
                return jsonify(
                    {"status_code": 200,
                     "lid": line.split(" ")[1],
                     "timestamp": datetime.datetime.now()}
                )


@app.route("/on-cooler", methods=['GET', 'PUT'])
def turn_on_cooler():
    subprocess.Popen([os.path.join(base_dir, "py-part/cooler.py")])

    return make_response(
        jsonify(
            {"status_code": 200,
             "content": "cooler is on",
             "timestamp": datetime.datetime.now()}
        ),
        200
    )


@app.route("/off-cooler", methods=['GET', 'PUT'])
def turn_off_cooler():
    subprocess.run(["pkill", "-f", "py-part/cooler.py"])

    return make_response(
        jsonify(
            {"status_code": 200,
             "content": "cooler is off",
             "timestamp": datetime.datetime.now()}
        ),
        200
    )


@app.route("/on-heating-element")
def turn_on_heating_element():
    subprocess.Popen([os.path.join(base_dir, "py-part/heating_element.py")])

    return make_response(
        jsonify(
            {"status_code": 200,
             "content": "heating element is on",
             "timestamp": datetime.datetime.now()}
        ),
        200
    )


@app.route("/off-heating-element")
def turn_off_heating_element():
    subprocess.run(["pkill", "-f", "py-part/heating_element.py"])

    return make_response(
        jsonify(
            {"status_code": 200,
             "content": "heating element is off",
             "timestamp": datetime.datetime.now()}
        ),
        200
    )


@app.route("/endpoints", methods=['GET'])
def endpoints():
    lst: list = ["%s" % rule for rule in app.url_map.iter_rules()][1:]

    return make_response(
        jsonify(
            {"status_code": 200,
             "content": "Ok",
             "routes": lst}
        ),
        200)


@app.route("/overall", methods=['GET'])
def overall():
    return make_response({"day": 0,
                          "updated": datetime.datetime.now().__str__(),
                          "temp": 0.0,
                          "hum": 0.0}, 200)


@app.route("/shutdown")
def shutdown():
    """ Make some safety check??? """
    os.system("sudo shutdown -h now")


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt as ki:
        pass
