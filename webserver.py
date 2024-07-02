#!/usr/bin/env python3
import datetime
import time
from flask import Flask, jsonify, render_template
from flask_cors import CORS
import subprocess
import os

app = Flask(__name__)
CORS(app)

status_code_200: dict = {"status_code": 200}

# Get the base directory where the Flask app is located
base_dir = os.path.dirname(os.path.abspath(__file__))

@app.route("/")
def home():
    return render_template("index.html")


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-red.py")])
    return jsonify(status_code_200)


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-red.py"])
    return jsonify(status_code_200)


@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-green.py")])
    return jsonify(status_code_200)


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-green.py"])
    return jsonify(status_code_200)


@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/blink-rgb-blue.py")])
    return jsonify(status_code_200)


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led():
    subprocess.run(["pkill", "-f", "py-part/blink-rgb-blue.py"])
    return jsonify(status_code_200)


@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led():
    subprocess.Popen([os.path.join(base_dir, "py-part/rgb_led.py")])
    return jsonify(status_code_200)


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led():
    subprocess.run(["pkill", "-f", "py-part/rgb_led.py"])
    return jsonify(status_code_200)


@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor():
    # Run the script to get the temperature and humidity
    result = subprocess.run([os.path.join(base_dir, "py-part/temp_hum_sensor.py")], capture_output=True, text=True)
    
    if result.returncode != 0:
        return jsonify({"error": "Failed to read temperature and humidity", "details": result.stderr}), 500
    
    try:
        with open(os.path.join(base_dir, "temp_hum.txt"), 'r') as file:
            temp = file.readline().strip()
            hum = file.readline().strip()
            timestamp = file.readline().strip()
    except FileNotFoundError:
        return jsonify({"error": "temp_hum.txt file not found"}), 500

    return jsonify({"temp": temp, "hum": hum, "timestamp": timestamp})


@app.route("/shutdown", methods=['GET'])
def shutdown_raspberry_pi():
    os.system("sudo shutdown -h now")


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
