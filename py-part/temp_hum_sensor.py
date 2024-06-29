#!/usr/bin/env python3

import time
import board
import adafruit_sht4x

# Create the I2C bus interface
i2c = board.I2C()

# Create the sensor object using I2C
try:
    sensor = adafruit_sht4x.SHT4x(i2c, address=0x38)
    sensor.mode = adafruit_sht4x.Mode.NOHEAT_HIGHPRECISION
    print("Found SHT4x sensor")
    print("Current mode is: ", adafruit_sht4x.Mode.string[sensor.mode])
except Exception as e:
    print("Failed to initialize sensor: ", e)
    exit(1)

time.sleep(1)
while True:
    try:
        time.sleep(1)
        temp, hum = sensor.measurements
        print(temp, hum)
    except RuntimeError as error:
        # Errors happen fairly often, DHT's are hard to read, just keep going
        print("Error: ", error)
    except Exception as error:
        print("An error occurred: ", error)
    time.sleep(2.0)
