#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from deprecated import deprecated
from csibekelteto_utils import safe_exit

RELAY_PIN: int = 22

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)

@deprecated(reason="dont run this code bc it is not connected yet!")
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
