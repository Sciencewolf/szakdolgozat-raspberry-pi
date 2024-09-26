#!/usr/bin/env python

import RPi.GPIO as GPIO
import time

# Set the GPIO mode to BCM
GPIO.setmode(GPIO.BCM)

# Define the GPIO pin for your button
SWITCH_PIN = 23  # GPIO 23, or whichever you're using

# Set the pull-up resistor for the button
GPIO.setup(SWITCH_PIN, GPIO.IN, pull_up_down=GPIO.PUD_UP)

try:
    # Main loop to monitor button state
    print("Monitoring button state...")
    while True:
        pin_state = GPIO.input(SWITCH_PIN)
        if pin_state == GPIO.LOW:
            print("Button pressed (GPIO LOW)")
        else:
            print(f"Button not pressed (GPIO HIGH): {pin_state}")  # Add more details
        time.sleep(0.5)

except KeyboardInterrupt:
    # Clean up GPIO on exit
    print("Cleaning up GPIO...")
    GPIO.cleanup()
