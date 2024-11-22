#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time

ENA: int = 5
IN1: int = 6
IN2: int = 13

gpio.setmode(gpio.BCM)

gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(ENA, gpio.OUT)

pwm = gpio.PWM(ENA, 100)  # 100Hz PWM
pwm.start(0)  # speed 0%

def main():
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        # motor forward
        gpio.output(IN1, gpio.HIGH)
        gpio.output(IN2, gpio.LOW)
        pwm.ChangeDutyCycle(100)  # 100% speed
        time.sleep(5)

        # Motor stop
        gpio.output(IN1, gpio.LOW)
        gpio.output(IN2, gpio.LOW)
        pwm.ChangeDutyCycle(0)
        time.sleep(2)

        # Motor backward
        gpio.output(IN1, gpio.LOW)
        gpio.output(IN2, gpio.HIGH)
        pwm.ChangeDutyCycle(10)
        time.sleep(5)

    except Exception as ex:
        print("exiting...", ex.__str__())
    finally:
        pwm.stop()
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
