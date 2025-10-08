# Cameron Vela Lab 4

import RPi.GPIO as GPIO
import math
import time

GPIO.setmode(GPIO.BCM)


def calcB(x, t, f, phase, direction):
	B = math.sin((2*(math.pi)*f*t)-(direction*x*phase))**2
	return B

def changeDirection(pin):
	direction[0] *= -1

pins = list(range(2,12))
f = 0.2
phase = math.pi/11
GPIO.setup(pins, GPIO.OUT, initial = 0)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
direction = [1]

pwms = [GPIO.PWM(p, 500) for p in pins]
tstart = time.time()

for pwm in pwms:
	pwm.start(0)

try:
	GPIO.add_event_detect(21, GPIO.RISING, callback=changeDirection, bouncetime=200)
	while True:
		t = time.time() - tstart
		for x, pwm in enumerate(pwms):
		    B = calcB(x, t, f, phase, direction[0])
		    pwm.ChangeDutyCycle(B*100)
		

except KeyboardInterrupt:
	print('\nExiting')
except Exception as e:
	print('\ne')
finally:
	GPIO.cleanup()