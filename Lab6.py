from shifter import shifter
import RPi.GPIO as GPIO
import time

try:
    sr = Shifter(serialPin=23, clockPin=25, latchPin=24)
    sr.shiftByte(0b01100110)  # light your pattern
    while True:
        time.sleep(1)          # keep outputs on
except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
