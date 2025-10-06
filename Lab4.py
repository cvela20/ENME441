# Cameron Vela Lab 4

import RPi.GPIO as GPIO
import math
import time
from time import sleep

GPIO.setmode(GPIO.BCM)

p = 17
f = 0.2
GPIO.setup(p, GPIO.OUT, initial=0)
tstart = time.time()
pwm = GPIO.PWM(p, 500)
pwm.start(0)

try:
	while True:
		t = time.time() - tstart
		B = math.sin(2*(math.pi)*f*t)**2
		pwm.ChangeDutyCycle(B*100)

except KeyboardInterrupt:
	print('\nExiting')
except Exception as e:
	print('\ne')


GPIO.cleanup()