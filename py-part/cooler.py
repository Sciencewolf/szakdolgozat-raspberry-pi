#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/relay-and-fan-wiring_image.png
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import safe_exit

RELAY_GPIO_PIN: int = 24

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_GPIO_PIN, gpio.OUT)


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        while True:
            gpio.output(RELAY_GPIO_PIN, gpio.LOW)
    except Exception as ex:
        print(ex.__str__())
    finally:
        gpio.output(RELAY_GPIO_PIN, gpio.HIGH)
        gpio.cleanup()


if __name__ == "__main__":
    main()
