#!/usr/bin/env python

from gpiozero import LED
import time
from signal import signal, SIGTERM, SIGHUP


red_led = LED(21)
green_led = LED(16)
blue_led = LED(20)

SLEEP: float = 0.4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        while True:
            # blink red
            red_led.on()
            time.sleep(SLEEP)
            red_led.off()
            time.sleep(SLEEP)

            # blink green
            green_led.on()
            time.sleep(SLEEP)
            green_led.off()
            time.sleep(SLEEP)

            # blink blue
            blue_led.on()
            time.sleep(SLEEP)
            blue_led.off()
            time.sleep(SLEEP)
    except Exception as ex:
        print(ex.__str__())


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
