#!/usr/bin/env python

import sys

from gpiozero import LED
import time
from signal import signal, SIGHUP, SIGTERM
# if error -> export PYTHONPATH=/home/aron/szakdolgozat-raspberry-pi:$PYTHONPATH
from csibekelteto_utils import LED_PINS

if sys.argv[1] not in list(LED_PINS.keys()):
    print(f"{sys.argv[1]} led not found")
    print(f"\n\tTry:  {list(LED_PINS.keys())}")
    sys.exit(1)
    
led = LED(LED_PINS.get(sys.argv[1]))

SLEEP: float = .4


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        if sys.argv[2] == "blink" and len(sys.argv) == 3:
            while True:
                led.on()
                time.sleep(SLEEP)
                led.off()
                time.sleep(SLEEP)
        elif sys.argv[2] == 'hold' and len(sys.argv) == 3 :
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
