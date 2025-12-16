import math
import time
from aim import Aim

# -------------------------
# Mock motors (prints only)
# -------------------------
class MockStepper:
    def __init__(self, name="motor"):
        self.name = name
        self.last_angle = 0.0

    def zero(self):
        self.last_angle = 0.0
        print(f"[{self.name}] zero() -> angle = 0")

    def goAngle(self, angle_deg):
        print(f"[{self.name}] goAngle({angle_deg:.2f} deg)")
        self.last_angle = angle_deg


def run_test(use_real_motors=False):
    # -------------------------
    # Choose motors
    # -------------------------
    if use_real_motors:
        # ONLY enable this on the Pi with your real Stepper + Shifter setup
        import multiprocessing
        from shifter import Shifter
        from Stepper_Lab8_3 import Stepper

        Stepper.shifter_outputs = multiprocessing.Value('i')
        s = Shifter(data=17, latch=27, clock=22)

        lock1 = multiprocessing.Lock()
        lock2 = multiprocessing.Lock()

        m1 = Stepper(s, lock1)  # theta motor
        m2 = Stepper(s, lock2)  # phi motor
    else:
        m1 = MockStepper("theta_motor")
        m2 = MockStepper("phi_motor")

    m1.zero()
    m2.zero()

    # -------------------------
    # Aim object settings
    # IMPORTANT: keep r and z in SAME UNITS (cm or m)
    # theta inputs must be RADIANS
    # -------------------------
    aim = Aim(
        calib_theta_deg=0.0,
        calib_phi_deg=0.0,
        laser_height=7.62  # if you're using cm everywhere, keep this in cm
    )

    # -------------------------
    # Fake "parsed JSON" data (matches your Webpage_connection structure)
    # -------------------------
    fake_data = {
        "turrets": {
            "1": {"r": 100.0, "theta": math.radians(0)},     # r in cm
            "2": {"r": 100.0, "theta": math.radians(90)},
            "3": {"r": 100.0, "theta": math.radians(180)},
        },
        "globes": [
            {"r": 100.0, "theta": math.radians(45),  "z": 30.0},   # z in cm
            {"r": 100.0, "theta": math.radians(135), "z": 10.0},
            {"r": 100.0, "theta": math.radians(225), "z": 0.0},
        ]
    }

    # -------------------------
    # Build the same lists/dicts your code builds
    # -------------------------
    turret_dict = {int(k): v for k, v in fake_data["turrets"].items()}
    turret_ids = sorted(turret_dict.keys())

    globes = fake_data["globes"]

    # -------------------------
    # Choose which turret is "you"
    # -------------------------
    Turret_ID = 1
    r0 = turret_dict[Turret_ID]["r"]
    theta0_rad = turret_dict[Turret_ID]["theta"]

    print("\n=== TEST: AIM at other turrets ===")
    for tid in turret_ids:
        if tid == Turret_ID:
            continue

        rt = turret_dict[tid]["r"]
        thetat = turret_dict[tid]["theta"]

        theta_cmd = aim.theta_aim_angle(r0, theta0_rad, rt, thetat)
        print(f"\nTarget turret {tid}: theta_cmd = {theta_cmd:.2f} deg")
        m1.goAngle(theta_cmd)
        time.sleep(0.5)

    print("\n=== TEST: AIM at globes (theta + phi) ===")
    for i, g in enumerate(globes, start=1):
        rt = g["r"]
        thetat = g["theta"]
        zt = g["z"]

        theta_cmd = aim.theta_aim_angle(r0, theta0_rad, rt, thetat)
        phi_cmd = aim.phi_aim_angle(r0, theta0_rad, rt, thetat, z_target=zt, z_base=0.0)

        print(f"\nGlobe {i}:")
        print(f"  theta_cmd = {theta_cmd:.2f} deg")
        print(f"  phi_raw   = {phi_cmd:.2f} deg")
       

        m1.goAngle(theta_cmd)
        m2.goAngle(phi_cmd_limited)
        time.sleep(0.75)


if __name__ == "__main__":
    # Set True ONLY on the Pi when hardware is connected
    run_test(use_real_motors=False)
