#!/usr/bin/env python

import RPi.GPIO as GPIO
import time
from signal import signal, SIGTERM, SIGHUP
from datetime import datetime
import subprocess


GPIO.setmode(GPIO.BCM)

SWITCH_PIN: int = 23

GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

def main() -> None:
    try:
        print("Monitoring button state...")
        signal(SIGTERM, safe_exit)
        signal(SIGHUP, safe_exit)

        pin_state: int = GPIO.input(SWITCH_PIN)
        
        with open("lid-status.txt", 'w') as file:
            if pin_state == GPIO.LOW:
                print(f"Button pressed (GPIO LOW): {pin_state}")
                file.write("lid close @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Close")

                subprocess.run(["pkill", "-f", "blink_rgb_red.py"])
            else:
                print(f"Button not pressed (GPIO HIGH): {pin_state}")
                file.write("lid open @ ")
                file.write(f"{datetime.now()} \n")
                file.write("! Open")

                subprocess.Popen(["blink_rgb_red.py"])

    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


def safe_exit(signum, frame) -> None:
    exit(1)

if __name__ == "__main__":
    main()
