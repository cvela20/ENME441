
import RPi.GPIO as GPIO
import time


GPIO.setmode(GPIO.BCM)
dataPin, latchPin, clockPin = 23, 24, 25
GPIO.setup(dataPin, GPIO.OUT)
GPIO.setup(latchPin, GPIO.OUT, initial=0) # start latch & clock low
GPIO.setup(clockPin, GPIO.OUT, initial=0)

pattern = 0b01110111 # pattern to display

def ping(p):
	GPIO.output(p,1)
	time.sleep(0)
	GPIO.output(p,0)

def shiftByte(b):
	for i in range(8):
		GPIO.output(dataPin, b & (1<<i))
		ping(clockpin)
	ping(latchpin)


try:
	while 1:
		for i in range(2**8):
			shiftByte(i)
			time.sleep(0.5)

except:
	GPIO.cleanup()
