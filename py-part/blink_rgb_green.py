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

# define gpio pin's
GPIO_GREEN_PIN_NUM: int = 16

# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(GPIO_GREEN_PIN_NUM, gpio.OUT, initial=gpio.LOW)

# time
SLEEP: float = .4

logger = logger.Logger("hardware-rgb-green-")


def main() -> None:
	logger.info("turning on/off green led")
	try:
		signal(SIGTERM, safe_exit)
		signal(SIGHUP, safe_exit)
		while True:
			gpio.output(GPIO_GREEN_PIN_NUM, gpio.HIGH)
			time.sleep(SLEEP)
			logger.debug("green led on")
			gpio.output(GPIO_GREEN_PIN_NUM, gpio.LOW)
			time.sleep(SLEEP)
			logger.debug("green led off")
	except KeyboardInterrupt as ex:
		logger.warn("keyboard interrupt", ex.__str__())
	finally:
		logger.info("gpio cleanup from green led")
		gpio.cleanup()


def safe_exit(signum, frame) -> None:
	""" Provides a safe shutdown of the program """
	logger.warn("safe exit method called by special signal")
	exit(1)


if __name__ == "__main__":
	logger.info(os.path.abspath(__file__))
	main()
