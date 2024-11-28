#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time

RELAY_PIN: int = 25

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)


def main() -> None:
    for i in range(1, 5, -1):
        print(i)
        time.sleep(1)

    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        gpio.output(RELAY_PIN, gpio.LOW)
        time.sleep(0.5)
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
