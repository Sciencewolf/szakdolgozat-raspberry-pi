#!/usr/bin/env python

import RPi.GPIO as GPIO
from signal import signal, SIGTERM, SIGHUP
from datetime import datetime
import time
import os


GPIO.setmode(GPIO.BCM)

SWITCH_PIN: int = 23
GPIO_RED_PIN_NUM: int = 21 # led

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(GPIO_RED_PIN_NUM, GPIO.OUT, initial=GPIO.LOW)

# Get the home directory
home_dir = os.path.expanduser("~")

# Create the full path for the text file
lid_file_path = os.path.join(home_dir, "lid-status.txt")


def main() -> None:
    try:
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        pin_state: int = GPIO.input(SWITCH_PIN)

        with open(lid_file_path, 'w') as file:
            if pin_state == GPIO.LOW:
                print(f"Button pressed (GPIO LOW): {pin_state}")

                file.write("lid close @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Close")
            else:
                print(f"Button not pressed (GPIO HIGH): {pin_state}")

                file.write("lid open @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Open")

                for _ in range(5):
                    GPIO.output(GPIO_RED_PIN_NUM, GPIO.HIGH)
                    time.sleep(0.1)
                    GPIO.output(GPIO_RED_PIN_NUM, GPIO.LOW)
                    time.sleep(0.1)


    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


def safe_exit(signum, frame) -> None:
    """ Provides a safe shutdown of the program """
    exit(1)

if __name__ == "__main__":
    main()
