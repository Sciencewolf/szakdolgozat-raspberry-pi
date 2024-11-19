#!/usr/bin/env python

"""
wiring: https://github.com/Sciencewolf/szakdolgozat-raspberry-pi/blob/main/sketches/images/rgb-led-aht20-temp-hum-sensor-wiring_image.png
description:
"""

import sys
import datetime
import os
import board
import adafruit_ahtx0

try:
    # Create sensor object, communicating over the board's default I2C
    i2c = board.I2C()  # uses board.SCL and board.SDA

    sensor = adafruit_ahtx0.AHTx0(i2c)

    temp = "%0.1f C" % sensor.temperature
    hum = "%0.1f %%" % sensor.relative_humidity

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the temp_hum.txt file
    temp_hum_file = os.path.join(script_dir, "../temp_hum.txt")

    with open('temp_hum.txt', 'w') as file:
        file.write(temp + '\n')
        file.write(hum + '\n')
        file.write(datetime.datetime.now().__str__() + '\n')

except Exception as ex:
    print(ex.__str__())
finally:
    print("finally block")
    sys.exit(0)
