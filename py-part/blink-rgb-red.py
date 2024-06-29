#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP

# define gpio pin's
GPIO_RED_PIN_NUM: int = 13


# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(GPIO_RED_PIN_NUM, gpio.OUT)

#time
SLEEP: float = .4


def main() -> None:
	try:
		signal(SIGTERM, safe_exit)
		signal(SIGHUP, safe_exit)
		while True:
			gpio.output(GPIO_RED_PIN_NUM, gpio.HIGH)
			time.sleep(SLEEP)
			gpio.output(GPIO_RED_PIN_NUM, gpio.LOW)
			time.sleep(SLEEP)
	except KeyboardInterrupt as ex:
		print(ex)
	finally:
		gpio.cleanup()


def safe_exit(signum, frame) -> None:
	""" Provides a safe shutdown of the program """
	exit(1)

if __name__ == "__main__":
	main()
