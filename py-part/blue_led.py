#!/usr/bin/env python
import sys

from gpiozero import LED
import time
from signal import signal, SIGHUP, SIGTERM

led = LED(19)

SLEEP: float = .4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        if sys.argv[1] == "blink" and len(sys.argv) == 2:
            while True:
                led.on()
                time.sleep(SLEEP)
                led.off()
                time.sleep(SLEEP)
        elif sys.argv[1] == 'hold' and len(sys.argv) == 2 :
            while True:
                led.on()
    except Exception as ex:
        print(ex.__str__())
    finally:
        led.off()


def safe_exit(signum, frame) -> None:
    """ provides safe exit from a program """
    exit(1)


if __name__ == "__main__":
    main()
