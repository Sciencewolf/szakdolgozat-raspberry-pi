#!/usr/bin/env python3

import datetime
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import subprocess
import os
import sys

app = Flask(__name__)
CORS(app)

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

# Get the home directory
home_dir = os.path.expanduser("~")

# Create the full path for the text file
lid_file_path = os.path.join(home_dir, "lid-status.txt")


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_red.py")])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_red.py"])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_green.py")])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_green.py"])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink_rgb_blue.py")])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led():
    subprocess.run(["pkill", "-f", "py-part/blink_rgb_blue.py"])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/rgb_led.py")])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led():
    subprocess.run(["pkill", "-f", "py-part/rgb_led.py"])
    return jsonify({"status_code": 200, "content": "ok response", "timestamp": datetime.datetime.now()})


@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor():
    result = subprocess.run(
        [os.path.join(base_dir, "py-part/temp_hum_sensor.py")],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        return jsonify({"status_code": 404, "content": "not found response", "timestamp": datetime.datetime.now()})

    try:
        with open(os.path.join(base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip()
            hum = file.readline().strip()
            timestamp = file.readline().strip()
    except FileNotFoundError:
        return jsonify({"status_code": 404, "content": "not found response", "timestamp": datetime.datetime.now()})

    return jsonify({"temp": temp, "hum": hum, "timestamp": timestamp})


@app.route("/get-lid-status-test")
def get_lid_status():
    subprocess.Popen([os.path.join(base_dir, "py-part/switch.py")])

    if not os.path.exists(lid_file_path):
        return jsonify({"status_code": 404, "lid": "undefined", "timestamp": datetime.datetime.now()})

    with open(lid_file_path, 'r') as file:
        lines = file.readlines()
        for line in lines:
            if line.startswith("!"):
                return jsonify(
                    {"status_code": 200,
                     "lid": line.split(" ")[1],
                     "timestamp": datetime.datetime.now()}
                )


@app.route("/on-cooler")
def turn_on_cooler():
    subprocess.Popen([os.path.join(base_dir, "py-part/cooler.py")])

    return jsonify({"status_code": 200, "content": "cooler is on", "timestamp": datetime.datetime.now()})


@app.route("/off-cooler")
def turn_off_cooler():
    subprocess.run(["pkill", "-f", "py-part/cooler.py"])

    return jsonify({"status_code": 200, "content": "cooler is off", "timestamp": datetime.datetime.now()})


if __name__ == "__main__":
    try:
        app.run(host="0.0.0.0", port=8080)
    except KeyboardInterrupt as ki:
        pass
