#!/usr/bin/env python

from gpiozero import LED
import time
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import LED_PINS, LEDs


led = LED(LED_PINS.get(LEDs.cold_white))

SLEEP: float = 8


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        led.on()
        time.sleep(SLEEP)
        led.off()

    except Exception as ex:
        print(ex.__str__())


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
