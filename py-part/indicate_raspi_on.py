#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
import os
import sys


# define gpio pin's
GPIO_BLUE_PIN_NUM: int = 20

# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(GPIO_BLUE_PIN_NUM, gpio.OUT, initial=gpio.LOW)

# time
SLEEP: float = .4


def main() -> None:
    count: int = 0
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while count < 4:
            gpio.output(GPIO_BLUE_PIN_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_BLUE_PIN_NUM, gpio.LOW)
            time.sleep(SLEEP)
            count += 1
    except KeyboardInterrupt as ex:
        pass
    finally:
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
