# Cameron Vela Lab 4

import RPi.GPIO as GPIO
import math
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

p1 = 17
p2 = 27
f = 0.2
phi = math.pi/11

GPIO.setup(p1, GPIO.OUT, initial=0)
GPIO.setup(p2, GPIO.OUT, initial=0)

tstart = time.time()
pwm1 = GPIO.PWM(p1, 500)
pwm2 = GPIO.PWM(p2, 500)
pwm1.start(0)
pwm2.start(0)

try:
	while True:
		t = time.time() - tstart
		B1 = math.sin(2*(math.pi)*f*t)**2
		B2 = math.sin(2*(math.pi)*f*t-phi)**2
		pwm1.ChangeDutyCycle(B1*100)
		pwm2.ChangeDutyCycle(B2*100)

except KeyboardInterrupt:
	print('\nExiting')
except Exception as e:
	print('\ne')


GPIO.cleanup()