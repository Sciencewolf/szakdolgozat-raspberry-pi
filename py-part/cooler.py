#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/relay-and-fan-wiring_image.png
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP

RELAY_PIN: int = 18

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        while True:
<<<<<<< HEAD
            gpio.output(RELAY_PIN, gpio.HIGH)
    except Exception as ex:
        print(ex.__str__())
=======
            gpio.output(RELAY_PIN, gpio.LOW)
    except KeyboardInterrupt:
        pass
>>>>>>> 9af76ca3adf9d54d8056bbfe77de3926deadfb6c
    finally:
        gpio.output(RELAY_PIN, gpio.HIGH)
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
