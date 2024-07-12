#!/usr/bin/env python3

import datetime
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import subprocess
import os
import sys

# the next 3 line for adding the parent directory into PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import logger

app = Flask(__name__)
CORS(app)

logger = logger.Logger("webserver-", remove_log=True)

status_code_200: dict = {"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()}
status_code_404: dict = {"status_code": 404, "content": "not found response", "timestamp": datetime.datetime.now()}

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def home():
    logger.info("accessing base url, homepage")
    return render_template("index.html")


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-red.py")])
    logger.info("turning on red led")
    return jsonify(status_code_200)


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-red.py"])
    logger.info("turning off red led")
    return jsonify(status_code_200)


@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-green.py")])
    logger.info("turning on green led")
    return jsonify(status_code_200)


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-green.py"])
    logger.info("turning off green led")
    return jsonify(status_code_200)


@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-blue.py")])
    logger.info("turning on blue led")
    return jsonify(status_code_200)


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-blue.py"])
    logger.info("turning off blue led")
    return jsonify(status_code_200)


@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/rgb-led.py")])
    logger.info("turning on all led")
    return jsonify(status_code_200)


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led():
    subprocess.run(["pkill", "-f", "py-part/rgb-led.py"])
    logger.info("turning off all led")
    return jsonify(status_code_200)


@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor():
    logger.info("accessing /get-temp-hum")
    result = subprocess.run([os.path.join(base_dir, "py-part/temp_hum_sensor.py")], capture_output=True, text=True)

    if result.returncode != 0:
        logger.error("failed to run temp_hum_sensor.py or some other error occurred")
        return jsonify(status_code_404)

    try:
        with open(os.path.join(base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip()
            hum = file.readline().strip()
            timestamp = file.readline().strip()
        logger.info("reading info from temp_hum.txt")
    except FileNotFoundError:
        logger.error("temp_hum.txt is not found")
        return jsonify(status_code_404)

    logger.info("return json with temp, hum, timestamp")
    return jsonify({"temp": temp, "hum": hum, "timestamp": timestamp})


if __name__ == "__main__":
    logger.info("webserver is on", os.path.abspath(__file__))
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt as ki:
        pass
    finally:
        logger.close()
