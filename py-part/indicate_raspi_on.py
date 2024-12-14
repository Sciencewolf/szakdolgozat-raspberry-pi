#!/usr/bin/env python

from gpiozero import LED
import time
from signal import signal, SIGTERM, SIGHUP


led = LED(19)

SLEEP: float = .4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        led.on()
        time.sleep(SLEEP*10)
    except Exception as ex:
        print(ex.__str__())


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)


if __name__ == "__main__":
    main()
