#!/usr/bin/env python3
# Drive a single 28BYJ-48 stepper via a 74HC595 shift register on a Raspberry Pi Zero
# Uses half-step sequence for smooth motion

import time
import RPi.GPIO as GPIO

# ----------------------
# USER CONFIG
# ----------------------
DATA_PIN  = 16  # Pi BCM pin → 74HC595 SER
LATCH_PIN = 20  # Pi BCM pin → 74HC595 RCLK (latch)
CLOCK_PIN = 21  # Pi BCM pin → 74HC595 SRCLK (shift clock)

STEP_DELAY_S = 0.12  # 1.2 ms between half-steps (tune for your setup)
STEPS_PER_REV = 4096   # Typical for 28BYJ-48 in half-step mode

# Coil order expected (A,B,C,D) must match wiring to driver channels
# Half-step sequence (8 states) for 28BYJ-48:
SEQ = [
    0b0001,  # A
    0b0011,  # A+B
    0b0010,  # B
    0b0110,  # B+C
    0b0100,  # C
    0b1100,  # C+D
    0b1000,  # D
    0b1001   # D+A
]

# ----------------------
# Shift register helper
# ----------------------
class Shifter:
    def __init__(self, data, clock, latch):
        self.data = data
        self.clock = clock
        self.latch = latch
        GPIO.setup(self.data,  GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.clock, GPIO.OUT, initial=GPIO.LOW)
        GPIO.setup(self.latch, GPIO.OUT, initial=GPIO.LOW)

    def _pulse(self, pin):
        GPIO.output(pin, GPIO.HIGH)
        # very short pulse is fine; hardware is fast
        GPIO.output(pin, GPIO.LOW)

    def write_byte(self, value):
        """Shift out 8 bits (LSB first) then latch to outputs."""
        for i in range(8):
            bit = (value >> i) & 1
            GPIO.output(self.data, GPIO.HIGH if bit else GPIO.LOW)
            self._pulse(self.clock)
        self._pulse(self.latch)

# ----------------------
# Simple stepper driver
# ----------------------
class Stepper:
    def __init__(self, shifter, bit_offset=0):
        """
        bit_offset: where this motor's 4 control bits live (0..4..8..)
        We use Q0..Q3 (offset 0) for a single motor.
        """
        self.s = shifter
        self.offset = bit_offset
        self.state = 0          # index into SEQ
        self.outputs = 0        # current 8-bit register image

    def _apply_coils(self, nibble):
        """
        Update only this motor's 4-bit slice (offset..offset+3) inside self.outputs
        and write the full byte to the shift register.
        """
        mask = 0b1111 << self.offset
        self.outputs &= ~mask
        self.outputs |= (nibble << self.offset)
        self.s.write_byte(self.outputs)

    def step(self, direction=1):
        """direction = +1 (CW or CCW depending on wiring) or -1"""
        self.state = (self.state + direction) % len(SEQ)
        self._apply_coils(SEQ[self.state])
        time.sleep(STEP_DELAY_S)

    def rotate_degrees(self, degrees, direction=1):
        """
        Rotate approximately 'degrees' in the given direction.
        direction: +1 or -1 (choose what gives you the desired sense).
        """
        steps = int(abs(degrees) * STEPS_PER_REV / 360.0)
        if degrees < 0:
            direction = -direction
        for _ in range(steps):
            self.step(direction)

    def release(self):
        """De-energize coils (optional)."""
        self._apply_coils(0b0000)

# ----------------------
# Demo
# ----------------------
def main():
    GPIO.setmode(GPIO.BCM)
    try:
        sh = Shifter(DATA_PIN, CLOCK_PIN, LATCH_PIN)
        m = Stepper(shifter=sh, bit_offset=0)  # use Q0..Q3

        print("Rotate +90°")
        m.rotate_degrees(90, direction=1)

        print("Rotate -90°")
        m.rotate_degrees(90, direction=-1)

        print("Full revolution +360°")
        m.rotate_degrees(360, direction=1)

        print("Done. Releasing coils.")
        m.release()

    finally:
        GPIO.cleanup()

if __name__ == "__main__":
    main()

