#!/usr/bin/env python

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP

RELAY_PIN: int = 18

gpio.setmode(gpio.BCM)
gpio.setup(RELAY_PIN, gpio.OUT)


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        while True:
            gpio.output(RELAY_PIN, gpio.HIGH)
    except KeyboardInterrupt:
        pass
    finally:
        gpio.output(RELAY_PIN, gpio.LOW)
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
