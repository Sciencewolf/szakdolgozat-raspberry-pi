#!/usr/bin/env python
import os.path

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
import logger

# define gpio pin's
GPIO_BLUE_PIN_NUM: int = 6

# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(GPIO_BLUE_PIN_NUM, gpio.OUT, initial=gpio.LOW)

# time
SLEEP: float = .4

logger = logger.Logger("hardware-rgb-blue-")


def main() -> None:
    logger.info("turning on/off blue led")
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while True:
            gpio.output(GPIO_BLUE_PIN_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_BLUE_PIN_NUM, gpio.LOW)
            time.sleep(SLEEP)
    except KeyboardInterrupt as ex:
        logger.warn("keyboard interrupt", ex.__str__())
    finally:
        logger.info("gpio cleanup from blue led")
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    logger.warn("safe exit method called by special signal")
    exit(1)


if __name__ == "__main__":
    logger.info(os.path.abspath(__file__))
    main()
