#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
import os
import sys


# define gpio pin's
GPIO_RED_PIN_NUM: int = 21

# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(GPIO_RED_PIN_NUM, gpio.OUT, initial=gpio.LOW)

# time
SLEEP: float = .4

logger = logger.Logger("hardware-rgb-red-")


def main() -> None:
	logger.info("turning on/off red led")
	try:
		signal(SIGTERM, safe_exit)
		signal(SIGHUP, safe_exit)
		while True:
			gpio.output(GPIO_RED_PIN_NUM, gpio.HIGH)
			time.sleep(SLEEP)
			gpio.output(GPIO_RED_PIN_NUM, gpio.LOW)
			time.sleep(SLEEP)
	except KeyboardInterrupt as ex:
		pass
	finally:
		gpio.cleanup()


def safe_exit(signum, frame) -> None:
	""" Provides a safe shutdown of the program """
	exit(1)


if __name__ == "__main__":
	main()
