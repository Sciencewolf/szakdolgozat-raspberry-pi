#!/usr/bin/env python

import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP

GPIO_PIN_R_NUM: int = 13 # red led
GPIO_PIN_G_NUM: int = 5 # green led 
GPIO_PIN_B_NUM: int = 6 # blue leb

SLEEP: float = 0.4

gpio.setmode(gpio.BCM)

gpio.setup(GPIO_PIN_G_NUM, gpio.OUT, initial=gpio.LOW)
gpio.setup(GPIO_PIN_R_NUM, gpio.OUT, initial=gpio.LOW)
gpio.setup(GPIO_PIN_B_NUM, gpio.OUT, initial=gpio.LOW)

def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        while True:
            # blink red
            gpio.output(GPIO_PIN_R_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_PIN_R_NUM, gpio.LOW)
            time.sleep(SLEEP)
            # blink green
            gpio.output(GPIO_PIN_G_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_PIN_G_NUM, gpio.LOW)
            time.sleep(SLEEP)
            #blink blue
            gpio.output(GPIO_PIN_B_NUM, gpio.HIGH)
            time.sleep(SLEEP)
            gpio.output(GPIO_PIN_B_NUM, gpio.LOW)
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
