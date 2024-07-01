import RPi.GPIO as GPIO
import time

# Define GPIO pins
RED_PIN = 13
GREEN_PIN = 5
BLUE_PIN = 6

# Set GPIO numbering mode
GPIO.setmode(GPIO.BCM)

# Setup pins for PWM output
GPIO.setup(RED_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(GREEN_PIN, GPIO.OUT, initial=GPIO.LOW)
GPIO.setup(BLUE_PIN, GPIO.OUT, initial=GPIO.LOW)

# Initialize PWM objects
red_pwm = GPIO.PWM(RED_PIN, 100)    # 100 Hz frequency
green_pwm = GPIO.PWM(GREEN_PIN, 100)
blue_pwm = GPIO.PWM(BLUE_PIN, 100)

# Start PWM with 0% duty cycle (off)
red_pwm.start(0)
green_pwm.start(0)
blue_pwm.start(0)

def fade_color(pwm, target_dc):
    current_dc = pwm.start(0)
    if current_dc is None:
        current_dc = 0
        
    step = 1 if target_dc >= current_dc else -1

    for dc in range(current_dc, target_dc + step, step):
        pwm.ChangeDutyCycle(dc)
        time.sleep(0.01)  # Adjust the sleep time for smoother transitions

    pwm.ChangeDutyCycle(target_dc)

try:
    while True:
        # Fade through different colors
        fade_color(red_pwm, 100)   # Red
        fade_color(green_pwm, 100) # Yellow
        fade_color(blue_pwm, 100)  # White

        fade_color(red_pwm, 0)     # Cyan
        fade_color(green_pwm, 0)   # Green
        fade_color(blue_pwm, 0)    # Blue

except KeyboardInterrupt:
    pass
finally:
    # Cleanup GPIO
    red_pwm.stop()
    green_pwm.stop()
    blue_pwm.stop()
    GPIO.cleanup()
