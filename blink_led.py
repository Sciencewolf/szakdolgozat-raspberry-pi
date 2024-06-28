import RPi.GPIO as gpio
import time

gpio.setmode(gpio.BCM)

gpio.setup(21, gpio.OUT)

try:
    while True:
        gpio.output(21, gpio.HIGH)
        time.sleep(0.5)
        gpio.output(21, gpio.LOW)
        time.sleep(0.5)
except KeyboardInterrupt as ex:
    print(ex)
finally:
    gpio.cleanup()