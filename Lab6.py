from shifter import Shifter
import RPi.GPIO as GPIO
import time, random

sr = Shifter(serialPin=23, clockPin=25, latchPin=24)
position = 0

try:
    while True: 
        sr.shiftByte(1 << position)
        time.sleep(0.05)

        step = random.choice([-1,1])
        position += step
        if position < 0:
        	position = 1
        elif position > 7:
        	position = 6

except KeyboardInterrupt:
    pass
finally:
    GPIO.cleanup()
