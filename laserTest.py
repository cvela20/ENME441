import RPi.GPIO as GPIO
import time

PIN = 15

GPIO.setmode(GPIO.BCM)
GPIO.setup(PIN, GPIO.OUT)

GPIO.output(PIN, GPIO.HIGH)  # LED ON
time.sleep(1)
GPIO.output(PIN, GPIO.LOW)   # LED OFF

GPIO.cleanup()
