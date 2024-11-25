#!/usr/bin/env python

"""
wiring:
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import safe_exit

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


if __name__ == "__main__":
    main()
