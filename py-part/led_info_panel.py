#!/usr/bin/env python3

"""
wiring:
description:
"""
import os.path

from gpiozero import LED
import time
from signal import signal, SIGTERM, SIGHUP
from csibekelteto_utils import safe_exit
from webserver import utils

red_led = LED()
green_led = LED()
blue_led = LED()
yellow_led = LED()
pink_led = LED()
purple_led = LED()
white_led = LED()

path: str = os.path.join(utils.base_dir, 'led_panel.txt')


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        # open file to get which led is necessary to turn on
        with open(path, 'r') as file:
            # TODO
            print(file.readline())

    except Exception as ex:
        print(ex.__str__())


if __name__ == "__main__":
    main()


