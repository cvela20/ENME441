# LED bar wave with phase offsets (12 LEDs)
import RPi.GPIO as GPIO
import math, time

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

# === adjust to match your wiring: 12 BCM pins ===
pins = list(range(2, 14))          # 2..13 gives 12 LEDs; change if needed

PWM_FREQ = 500                      # Hz (carrier)
f = 0.2                             # Hz (brightness envelope)

GPIO.setup(pins, GPIO.OUT, initial=GPIO.LOW)

# Create and start PWM objects
pwms = [GPIO.PWM(p, PWM_FREQ) for p in pins]
for pwm in pwms:
    pwm.start(0)

# Phase step: π/11 so LED i has φ = i * (π/11)
phase_step = math.pi / 11.0

t0 = time.time()
try:
    while True:
        t = time.time() - t0
        for i, pwm in enumerate(pwms):
            B = math.sin(2 * math.pi * f * t - i * phase_step) ** 2  # 0..1
            pwm.ChangeDutyCycle(B * 100.0)                           # 0..100
except KeyboardInterrupt:
    pass
finally:
    for pwm in pwms:
        pwm.stop()
    GPIO.cleanup()
