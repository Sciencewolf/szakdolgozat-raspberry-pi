#!/usr/bin/env python

from gpiozero import LED
import time
from signal import signal, SIGHUP, SIGTERM
from csibekelteto_utils import safe_exit

led = LED(21)

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


if __name__ == "__main__":
    main()
