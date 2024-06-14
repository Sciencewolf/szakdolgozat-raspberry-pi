#!/usr/bin/env python3

from flask import Flask, jsonify

app = Flask(__name__)


@app.route("/")
def home():
    return jsonify({"status_code": 200,
                    "desc": "default response",
                    "routes": ["/get/temp", "/get/hum", "/get/health", "/get/summary"]})


@app.route("/get/temp")
def get_temp():
    """ Get temperature from sensor """
    return jsonify({"temp": 30,
                    "status_code": 200,
                    "desc": "response from /get-temp"})


@app.route("/get/hum")
def get_hum():
    """ Get humidity from sensor """
    return jsonify({"hum": 60,
                    "status_code": 200,
                    "desc": "response from /get-hum"})


@app.route("/get/health")
def get_health():
    """ Get state of rpi """
    return jsonify({"health": "ok | average | bad",
                    "status_code": 200,
                    "desc": "response from /health"})


@app.route("/get/summary")
def get_summary():
    """ Get all info about rpi. Needed in home page android app """
    return jsonify({"temp": 30, 
                    "hum": 60,
                    "health": "ok | average | bad",
                    "other": None,
                    "status_code": 200,
                    "desc": "response from /summary"})


@app.route("/set/temp")
def set_temp():
    """ Set temperature """
    return jsonify({"status_code": 200})


@app.route("/set/hum")
def set_hum():
    """ Set humidity """
    return jsonify({"status_code": 200})


app.run(host="0.0.0.0", port=8080)
