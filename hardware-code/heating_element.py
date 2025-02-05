#!/usr/bin/env python3

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/heating-element-and-relay-wiring_image.png
description:
"""


import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time
from csibekelteto_utils import RELAY_PINS

RELAY_PIN: int = RELAY_PINS.get("heating_element")

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        gpio.output(RELAY_PIN, gpio.LOW)

        while True:
            time.sleep(1)
    except Exception as ex:
        print(ex.__str__())
    finally:
        gpio.output(RELAY_PIN, gpio.HIGH)
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)
    

if __name__ == "__main__":
    main()
