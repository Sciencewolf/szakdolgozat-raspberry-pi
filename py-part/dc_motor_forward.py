#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP

ENA_GPIO_PIN: int = 16
IN1_GPIO_PIN: int = 20
IN2_GPIO_PIN: int = 21

gpio.setmode(gpio.BCM)

gpio.setup(IN1_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(IN2_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(ENA_GPIO_PIN, gpio.OUT, initial=gpio.LOW)

pwm = gpio.PWM(ENA_GPIO_PIN, 100)  # 100Hz PWM
pwm.start(0)  # speed 0%


def main(*args, **kwargs):
    """ TODO: add args to set speed """
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        while True:
            gpio.output(IN1_GPIO_PIN, gpio.LOW)
            gpio.output(IN2_GPIO_PIN, gpio.HIGH)
            pwm.ChangeDutyCycle(100)  # 100% speed
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
