#!/usr/bin/env python

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from datetime import datetime
import time
import os

RELAY_PIN: int = 18

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)

gpio.output(RELAY_PIN, gpio.HIGH)
time.sleep(10)
gpio.output(RELAY_PIN, gpio.LOW)

gpio.cleanup()
