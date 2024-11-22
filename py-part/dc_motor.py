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

# GPIO mód kiválasztása
gpio.setmode(gpio.BCM)

# GPIO lábak beállítása kimenetként
gpio.setup(IN1, gpio.OUT)
gpio.setup(IN2, gpio.OUT)
gpio.setup(ENA, gpio.OUT)

# PWM inicializálása (sebességvezérléshez)
pwm = gpio.PWM(ENA, 100)  # 100Hz PWM
pwm.start(0)  # Sebesség 0%

def main():
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)
        
        # Motor előre
        gpio.output(IN1, gpio.HIGH)
        gpio.output(IN2, gpio.LOW)
        pwm.ChangeDutyCycle(100)  # 100% sebesség
        time.sleep(5)

        # Motor megállítása
        gpio.output(IN1, gpio.LOW)
        gpio.output(IN2, gpio.LOW)
        pwm.ChangeDutyCycle(0)
        time.sleep(2)

        # Motor hátra
        gpio.output(IN1, gpio.LOW)
        gpio.output(IN2, gpio.HIGH)
        pwm.ChangeDutyCycle(10)  # 10% sebesség
        time.sleep(5)

    except KeyboardInterrupt:
        print("exiting...")
    finally:
        pwm.stop()
        gpio.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
