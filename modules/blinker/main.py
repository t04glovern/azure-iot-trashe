import RPi.GPIO as GPIO
import time

# Configure the PIN # 18
GPIO.setmode(GPIO.BOARD)
GPIO.setup(18, GPIO.OUT)
GPIO.setwarnings(False)

# Blink Interval
blink_interval = .5 #Time interval in Seconds

# Blinker Loop
while True:
    GPIO.output(18, True)
    time.sleep(blink_interval)
    GPIO.output(18, False)
    time.sleep(blink_interval)

# Release Resources
GPIO.cleanup()
