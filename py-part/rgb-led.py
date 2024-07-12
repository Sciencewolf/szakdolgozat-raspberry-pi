#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
import os
import sys

# the next 3 line for adding the parent directory into PATH
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)
sys.path.append(parent_dir)

import logger


GPIO_PIN_R_NUM: int = 21 # red led
GPIO_PIN_G_NUM: int = 16 # green led 
GPIO_PIN_B_NUM: int = 20 # blue leb

SLEEP: float = 0.4

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_PIN_G_NUM, gpio.OUT, initial=gpio.LOW)
gpio.setup(GPIO_PIN_R_NUM, gpio.OUT, initial=gpio.LOW)
gpio.setup(GPIO_PIN_B_NUM, gpio.OUT, initial=gpio.LOW)

logger = logger.Logger("hardware-rgb-all-")


def main() -> None:
    logger.info("turning on/off all led")
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while True:
            # blink red
            gpio.output(GPIO_PIN_R_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            logger.debug("red led on")
            gpio.output(GPIO_PIN_R_NUM, gpio.LOW)
            time.sleep(SLEEP)
            logger.debug("red led off")
            # blink green
            gpio.output(GPIO_PIN_G_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            logger.debug("green led on")
            gpio.output(GPIO_PIN_G_NUM, gpio.LOW)
            time.sleep(SLEEP)
            logger.debug("green led off")
            # blink blue
            gpio.output(GPIO_PIN_B_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            logger.debug("blue led on")
            gpio.output(GPIO_PIN_B_NUM, gpio.LOW)
            time.sleep(SLEEP)
            logger.debug("blue led off")
    except KeyboardInterrupt as ex:
        logger.warn("keyboard interrupt", ex.__str__())
    finally:
        logger.info("gpio cleanup from all led")
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    logger.warn("safe exit method called by special signal")
    exit(1)


if __name__ == "__main__":
    logger.info(os.path.abspath(__file__))
    main()
