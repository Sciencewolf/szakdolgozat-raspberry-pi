#!/usr/bin/env python3
import time
from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)

status_code_200: dict = {"status_code": 200}


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    os.system("./py-part/blink-rgb-red.py &")
    return jsonify(status_code_200)


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    os.system("pkill -f 'py-part/blink-rgb-red.py'")
    return jsonify(status_code_200)


@app.route("/on-green-led", methods=['GET'])
def turn_on_green_led():
    os.system("./py-part/blink-rgb-green.py &")
    return jsonify(status_code_200)


@app.route("/off-green-led", methods=['GET'])
def turn_off_green_led():
    os.system("pkill -f 'py-part/blink-rgb-green.py'")
    return jsonify(status_code_200)


@app.route("/on-blue-led", methods=['GET'])
def turn_on_blue_led():
    os.system("./py-part/blink-rgb-blue.py &")
    return jsonify(status_code_200)


@app.route("/off-blue-led", methods=['GET'])
def turn_off_blue_led():
    os.system("pkill -f 'py-part/blink-rgb-blue.py'")
    return jsonify(status_code_200)


@app.route("/on-all-led", methods=['GET'])
def turn_on_all_led():
    os.system("./py-part/rgb_led.py &")
    return jsonify(status_code_200)


@app.route("/off-all-led", methods=['GET'])
def turn_off_all_led():
    os.system("pkill -f 'py-part/rgb_led.py'")
    return jsonify(status_code_200)


@app.route("/get-temp-hum", methods=['GET'])
def get_temperature_and_humidity_from_sensor():
    os.system("./py-part/temp_hum_sensor.py &")
    with open("temp_hum.txt", 'r') as file:
        temp = file.readline()
        hum = file.readline()
        
    return jsonify({"temp": temp, "hum": hum})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
