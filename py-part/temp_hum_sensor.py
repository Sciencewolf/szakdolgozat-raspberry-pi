import board
import adafruit_ahtx0

# Create sensor object, communicating over the board's default I2C bus
i2c = board.I2C()  # uses board.SCL and board.SDA

sensor = adafruit_ahtx0.AHTx0(i2c)

temp = "%0.1f C" % sensor.temperature
hum = "%0.1f %%" % sensor.relative_humidity

with open('../temp_hum.txt', 'w') as file:
    file.write(temp + '\n')
    file.write(hum)
