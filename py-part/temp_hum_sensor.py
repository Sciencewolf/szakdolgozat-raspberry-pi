#!/usr/bin/env python

import sys
import datetime
import os
import board
import adafruit_ahtx0
sys.path.append("/home/aron/szakdolgozat-raspberry-pi/")

from logger import Logger


logger = Logger("hardware-t-h-sensor-")

try:
    logger.info("trying read the sensor")
    # Create sensor object, communicating over the board's default I2C
    i2c = board.I2C()  # uses board.SCL and board.SDA

    sensor = adafruit_ahtx0.AHTx0(i2c)

    temp = "%0.1f C" % sensor.temperature
    hum = "%0.1f %%" % sensor.relative_humidity
    logger.debug(temp, hum)

    # Get the directory where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct the path to the temp_hum.txt file
    temp_hum_file = os.path.join(script_dir, "../temp_hum.txt")

    with open(temp_hum_file, 'w') as file:
        file.write(temp + '\n')
        file.write(hum + '\n')
        file.write(datetime.datetime.now().__str__() + '\n')

    logger.info("looks good")
except Exception as ex:
    logger.error("error while reading the sensor", ex.__str__())
finally:
    logger.warn("exiting...")
    sys.exit(0)
