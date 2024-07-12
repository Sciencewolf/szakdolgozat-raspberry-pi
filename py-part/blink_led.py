#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
import sys
import os
current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.dirname(current_dir)

sys.path.append(parent_dir)


GPIO_PIN_NUM: int = # 21

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_PIN_NUM, gpio.OUT, initial=gpio.LOW)

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
