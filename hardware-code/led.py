#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/led-panel-wiring_image.png
"""

import sys
import RPi.GPIO as gpio
import time
import os
from signal import signal, SIGHUP, SIGTERM

# if error -> export PYTHONPATH=/home/aron/szakdolgozat-raspberry-pi:$PYTHONPATH
from csibekelteto_utils import LED_PINS

if len(sys.argv) == 1:
    print(f"Usage: \nled.py {list(LED_PINS.keys())} 'blink/hold' ")
    print("Example: led.py 'yellow' 'hold' ")
    sys.exit(1)

if sys.argv[1] not in LED_PINS:
    print(f"{sys.argv[1]} led not found")
    print(f"\n\tTry:  {list(LED_PINS.keys())}")
    sys.exit(1)

led_num: int = LED_PINS.get(sys.argv[1])

gpio.setmode(gpio.BCM)
gpio.setup(led_num, gpio.OUT)

pwm = gpio.PWM(led_num, 100)  # Set PWM frequency to 100 Hz
pwm.start(0)

SLEEP: float = 0.02


def safe_exit(signum, frame) -> None:
    """ Safe exit by stopping PWM and cleaning up GPIO """
    pwm.stop()
    gpio.cleanup()
    sys.exit(1)


def main() -> None:
    try:
        mode = sys.argv[2] if len(sys.argv) > 2 else None

        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        if mode == "hold":
            for i in range(0, 101, 2):
                pwm.ChangeDutyCycle(i)
                time.sleep(0.01)
            while True:
                time.sleep(1)

        elif mode == "blink":
            while True:
                for duty_cycle in range(0, 101, 2):
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(SLEEP)
                for duty_cycle in range(100, -1, -2): 
                    pwm.ChangeDutyCycle(duty_cycle)
                    time.sleep(SLEEP)
                time.sleep(0.5)
    except Exception as ex:
        print(ex)
    finally:
        safe_exit(0, 0)


if __name__ == "__main__":
    main()
