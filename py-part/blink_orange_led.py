#!/usr/bin/env python

from gpiozero import LED
import time
from signal import signal, SIGHUP, SIGTERM

led = LED(5)

SLEEP: float = .4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        while True:
            led.on()
            time.sleep(SLEEP)
            led.off()
            time.sleep(SLEEP)
    except Exception as ex:
        print(ex.__str__())


def safe_exit(signum, frame) -> None:
    """ provides safe exit from a program """
    exit(1)


if __name__ == "__main__":
    main()
