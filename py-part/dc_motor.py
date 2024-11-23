#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time

ENA_GPIO_PIN: int = 5
IN1_GPIO_PIN: int = 6
IN2_GPIO_PIN: int = 13

gpio.setmode(gpio.BCM)

gpio.setup(IN1_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(IN2_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(ENA_GPIO_PIN, gpio.OUT, initial=gpio.LOW)

pwm = gpio.PWM(ENA_GPIO_PIN, 100)  # 100Hz PWM
pwm.start(0)  # speed 0%

def main(*args, **kwargs):
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        # motor forward
        gpio.output(IN1_GPIO_PIN, gpio.HIGH)
        gpio.output(IN2_GPIO_PIN, gpio.LOW)
        pwm.ChangeDutyCycle(100)  # 100% speed
        time.sleep(5)

        # Motor stop
        gpio.output(IN1_GPIO_PIN, gpio.LOW)
        gpio.output(IN2_GPIO_PIN, gpio.LOW)
        pwm.ChangeDutyCycle(0)
        time.sleep(2)

        # Motor backward
        gpio.output(IN1_GPIO_PIN, gpio.LOW)
        gpio.output(IN2_GPIO_PIN, gpio.HIGH)
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
