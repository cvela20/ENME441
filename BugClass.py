from shifter import Shifter
import time, random
import RPi.GPIO as GPIO

class Bug:
	def __init__(self, timestep = 0.1, x = 3, isWrapOn = False):
		self.timestep  = timestep
		self.x = x
		self.isWrapOn = isWrapOn
		self.__shifter = Shifter(serialPin=23, clockPin=25, latchPin=24)
		self.__running = False

	def start(self):
		self.__running = True
		self.__shifter.shiftByte(1 << self.x)
		time.sleep(self.timestep)
		self.x += random.choice([-1,1])

		if self.isWrapOn == True:
			self.x %= 8
		else:
			if self.x < 0:
				self.x = 1
			elif self.x > 7:
				self.x = 6
		

	def stop(self):
		self.running = False
		self.__shifter.shiftByte(0)

