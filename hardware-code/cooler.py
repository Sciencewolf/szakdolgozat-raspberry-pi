#!/usr/bin/env python3

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/relay-and-fan-wiring_image.png
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time
from csibekelteto_utils import RELAY_PINS

RELAY_GPIO_PIN: int = RELAY_PINS['cooler']

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_GPIO_PIN, gpio.OUT)

def main():
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        gpio.output(RELAY_GPIO_PIN, gpio.LOW)

        while True:
            time.sleep(1)
    except Exception as e:
        print(f"Error: {e}")
    finally:
        gpio.output(RELAY_GPIO_PIN, gpio.HIGH)
        gpio.cleanup()



def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()