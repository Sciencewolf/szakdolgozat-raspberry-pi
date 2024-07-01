#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP

GPIO_PIN_NUM: int = 21

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_PIN_NUM, gpio.OUT, initial=GPIO.LOW)

def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while True:
            gpio.output(GPIO_PIN_NUM, gpio.HIGH)
            time.sleep(0.2)
            gpio.output(GPIO_PIN_NUM, gpio.LOW)
            time.sleep(0.2)
    except KeyboardInterrupt as ex:
        print(ex)
    finally:
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
