#!/usr/bin/env python

import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP
import time


GPIO.setmode(GPIO.BCM)

TRIG_PIN: int = 24
ECHO_PIN: int = 25

GPIO.setup(TRIG_PIN, GPIO.OUT)
GPIO.setup(ECHO_PIN, GPIO.IN)

GPIO.output(TRIG_PIN, False)

# waiting for sensor
time.sleep(2)

def main() -> None:
    pulse_end: float = 0.0
    pulse_start: float = 0.0

    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        GPIO.output(TRIG_PIN, True)
        time.sleep(0.00001)
        GPIO.output(TRIG_PIN, False)

        while GPIO.input(ECHO_PIN) == 0:
            pulse_start = time.time()

        while GPIO.input(ECHO_PIN) == 1:
            pulse_end = time.time()

        pulse_duration = pulse_end - pulse_start

        distance: float = pulse_duration * 17_150 # half cm/s speed of sound from object to sensor
        distance_rounded: float = round(distance, 2)
        print(f"{distance_rounded} cm")

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)

if __name__ == "__main__":
    main()
