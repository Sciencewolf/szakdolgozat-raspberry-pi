#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/dc-engine-wiring_image.png
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
import time

ENA_GPIO_PIN: int = 16
IN1_GPIO_PIN: int = 20
IN2_GPIO_PIN: int = 21

gpio.setmode(gpio.BCM)

gpio.setup(IN1_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(IN2_GPIO_PIN, gpio.OUT, initial=gpio.LOW)
gpio.setup(ENA_GPIO_PIN, gpio.OUT, initial=gpio.LOW)

pwm = gpio.PWM(ENA_GPIO_PIN, 100)  # 100Hz PWM
pwm.start(0)


def main():
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        pwm.ChangeDutyCycle(0)
        time.sleep(0.5)

        gpio.output(IN1_GPIO_PIN, gpio.HIGH)
        gpio.output(IN2_GPIO_PIN, gpio.LOW)
        pwm.ChangeDutyCycle(20)  # 20% speed

        while True:
            time.sleep(1)
    except Exception as ex:
        print("Exiting...", ex.__str__())
    finally:
        pwm.stop()
        gpio.cleanup()



def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
