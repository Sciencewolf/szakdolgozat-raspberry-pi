#!/usr/bin/env python3

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/heating-element-and-relay-wiring_image.png
description:
"""


import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import safe_exit

RELAY_PIN: int = 23

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        while True:
            gpio.output(RELAY_PIN, gpio.LOW)
    except Exception as ex:
        print(ex.__str__())
    finally:
        gpio.output(RELAY_PIN, gpio.HIGH)
        gpio.cleanup()
    

if __name__ == "__main__":
    main()
