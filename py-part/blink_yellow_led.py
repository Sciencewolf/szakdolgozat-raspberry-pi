#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP

# define gpio pin's
GPIO_YELLOW_PIN_NUM: int = 18

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_YELLOW_PIN_NUM, gpio.OUT, initial=gpio.LOW)

SLEEP: float = .4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        while True:
            gpio.output(GPIO_YELLOW_PIN_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_YELLOW_PIN_NUM, gpio.LOW)
            time.sleep(SLEEP)
    except KeyboardInterrupt as ex:
        print(ex.__str__())
    finally:
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
