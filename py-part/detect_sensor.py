#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP

# define gpio pin's


# setmode
gpio.setmode(gpio.BCM)

# setup
gpio.setup(, gpio.OUT)


def main() -> None:
	try:
		signal(SIGTERM, safe_exit)
		signal(SIGHUP, safe_exit)
		while True:
			# your code goes here
	except KeyboardInterrupt as ex:
		print(ex)
	finally:
		gpio.cleanup()


def safe_exit(signum, frame) -> None:
	""" Provides a safe shutdown of the program """
	exit(1)

if __name__ == "__main__":
	main()
