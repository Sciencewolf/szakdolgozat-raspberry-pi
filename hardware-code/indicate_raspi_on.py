#!/usr/bin/env python

from gpiozero import LED
import RPi.GPIO as gpio
import time
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import LED_PINS, LEDs


cold_white_led = LED_PINS.get(LEDs.cold_white)

gpio.setmode(gpio.BCM)
gpio.setup(cold_white_led, gpio.OUT)

pwm = gpio.PWM(cold_white_led, 1000)
pwm.start(0)

SLEEP: float = .01


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        for _ in range(4):
            for duty_cycle in range(0, 101, 1):  # Increase brightness
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(SLEEP)
            for duty_cycle in range(100, -1, -1):  # Decrease brightness
                pwm.ChangeDutyCycle(duty_cycle)
                time.sleep(SLEEP)

    except Exception as ex:
        print(ex.__str__())


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
