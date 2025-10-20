from bug import Bug
import RPi.GPIO as GPIO
import time

# --- Test 1: Bounce mode (no wrapping) ---
print("Running Test 1: Bounce Mode (Ctrl+C to stop)")
bug = Bug(timestep=0.1, x=0, isWrapOn=False)
try:
    bug.start()   # LED should move left and right, bouncing at ends
except KeyboardInterrupt:
    print("\nStopping bounce mode test...")
    bug.stop()
    time.sleep(1)

# --- Test 2: Wrap-around mode ---
print("\nRunning Test 2: Wrap Mode (Ctrl+C to stop)")
bug = Bug(timestep=0.1, x=0, isWrapOn=True)
try:
    bug.start()   # LED should move continuously in a loop (wrap 7→0)
except KeyboardInterrupt:
    print("\nStopping wrap mode test...")
    bug.stop()
    time.sleep(1)

# --- Cleanup all pins before exiting ---
GPIO.cleanup()
print("✅ GPIO cleaned up. Test complete.")
