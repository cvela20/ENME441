from BugClass import Bug
import RPi.GPIO as GPIO
import time, random

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(27, GPIO.IN, pull_up_down = GPIO.PUD_UP)
GPIO.setup(22, GPIO.IN, pull_up_down = GPIO.PUD_UP)

dt = 0.1
bug = Bug(timestep=dt, x=3, isWrapOn=False)
s2 = 0

try:
	while True:
		previous_s2 = s2
		s1 = GPIO.input(17)
		s2 = GPIO.input(27)
		s3 = GPIO.input(22)

	if s1 == True:
		bug.start()
	elif s1 == False:
		bug.stop()

	if s2 != previous_s2:
		bug.isWrapOn = not bug.isWrapOn
		previous_s2 = s2 


	if s3 == True:
		bug.timestep = dt/3.0
		dt /= 3.0

except KeyboardInterrupt:
	pass
finally:
	GPIO.cleanup()