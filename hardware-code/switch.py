#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/limit-switch-wiring_image.png
description:
"""

import RPi.GPIO as GPIO
from gpiozero import LED
from signal import signal, SIGTERM, SIGHUP
from datetime import datetime
import os
import time
from csibekelteto_utils import LED_PINS, LEDs


SWITCH_GPIO_PIN: int = 4
red_led = LED(LED_PINS.get(LEDs.red))

GPIO.setmode(GPIO.BCM)

GPIO.setup(SWITCH_GPIO_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

base_dir = os.path.dirname(os.path.abspath(__file__))

lid_file_path = os.path.join(base_dir, "../lid-status.txt")


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        pin_state: int = GPIO.input(SWITCH_GPIO_PIN)

        with open(lid_file_path, 'w') as file:
            if pin_state == GPIO.LOW:
                file.write("lid close @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Close")
            else:
                file.write("lid open @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Open")

                red_led.on()
                time.sleep(1)
                red_led.off()
    except Exception as ex:
        print(ex.__str__())
    finally:
        GPIO.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)

if __name__ == "__main__":
    main()
