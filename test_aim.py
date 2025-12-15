import math
from aim import Aim

aim = Aim(calib_theta_deg=0.0)

while True:
    print("\n--- New Test ---")

    r0 = float(input("Your turret radius: "))
    theta0_deg = float(input("Your turret angle (deg): "))

    rt = float(input("Target turret radius: "))
    thetat_deg = float(input("Target turret angle (deg): "))

    theta0_rad = math.radians(theta0_deg)
    thetat_rad = math.radians(thetat_deg)

    result = aim.turret_aim_angle(r0, theta0_rad, rt, thetat_rad)

    print(f"→ Aim angle: {result:.2f} degrees")
