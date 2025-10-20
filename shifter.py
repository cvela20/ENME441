import RPi.GPIO as GPIO
import time

class Shifter:

	def __init__(self, serialPin, clockPin, latchPin):
		self.serialPin = serialPin
		self.clockPin = clockPin
		self.latchPin = latchPin

		GPIO.setmode(GPIO.BCM)
		dataPin, latchPin, clockPin = 23, 24, 25
		GPIO.setup(self.dataPin, GPIO.OUT)
		GPIO.setup(self.latchPin, GPIO.OUT, initial=0) # start latch & clock low
		GPIO.setup(self.clockPin, GPIO.OUT, initial=0)

	def _ping(self, pin):
		GPIO.output(pin,1)
		time.sleep(0)
		GPIO.output(pin,0)

	def shiftByte(b):
		for i in range(8):
			GPIO.output(self.dataPin, b & (1<<i))
			ping(self.clockpin)
		ping(self.latchpin)

