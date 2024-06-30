#!/usr/bin/env python3
import time
from flask import Flask, jsonify, render_template
import os

app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/get/temp", methods=['GET'])
def get_temp():
    """ Get temperature from sensor """
    return jsonify({"temp": 30,
                    "status_code": 200,
                    "desc": "response from /get-temp"})


@app.route("/get/hum", methods=['GET'])
def get_hum():
    """ Get humidity from sensor """
    return jsonify({"hum": 60,
                    "status_code": 200,
                    "desc": "response from /get-hum"})


@app.route("/get/health", methods=['GET'])
def get_health():
    """ Get state of rpi """
    return jsonify({"health": "ok | average | bad",
                    "status_code": 200,
                    "desc": "response from /health"})


@app.route("/get/summary", methods=['GET'])
def get_summary():
    """ Get all info about rpi. Needed in home page android app """
    return jsonify({"temp": 30,
                    "hum": 60,
                    "health": "ok | average | bad",
                    "other": None,
                    "status_code": 200,
                    "desc": "response from /summary"})


@app.route("/set/temp", methods=['POST'])
def set_temp():
    """ Set temperature """
    return jsonify({"status_code": 200})


@app.route("/set/hum", methods=['POST'])
def set_hum():
    """ Set humidity """
    return jsonify({"status_code": 200})


@app.route("/on-red-led", methods=['GET'])
def turn_on_red_led():
    os.system("./py-part/blink-rgb-red.py &")
    return jsonify({"status_code": 200})


@app.route("/off-red-led", methods=['GET'])
def turn_off_red_led():
    os.system("pkill -f 'py-part/blink-rgb-red.py'")
    return jsonify({"status_code": 200})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
