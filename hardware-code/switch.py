#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/limit-switch-wiring_image.png
description:
"""

import RPi.GPIO as gpio
from signal import signal, SIGTERM, SIGHUP
from datetime import datetime
import os
import time
from csibekelteto_utils import LED_PINS, LEDs


SWITCH_gpio_PIN: int = 4
red_led = LED_PINS.get(LEDs.red)

gpio.setmode(gpio.BCM)

gpio.setup(SWITCH_gpio_PIN, gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(red_led, gpio.OUT)

pwm = gpio.PWM(red_led, 1000)
pwm.start(0)

base_dir = os.path.dirname(os.path.abspath(__file__))

lid_file_path = os.path.join(base_dir, "../lid_status.txt")

SLEEP: float = .01


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        pin_state: int = gpio.input(SWITCH_gpio_PIN)

        with open(lid_file_path, 'w') as file:
            if pin_state == gpio.LOW:
                file.write("lid close @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Close")
            else:
                file.write("lid open @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Open")

                for duty_cycle in range(0, 101, 2):
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(SLEEP)
                for duty_cycle in range(100, -1, -2): 
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(SLEEP)

    except Exception as ex:
        print(ex.__str__())
    finally:
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)

if __name__ == "__main__":
    main()
