import math
from aim import Aim

# Create Aim object with known parameters
aim = Aim(
    calib_theta_deg=0.0,
    calib_phi_deg=0.0,
    laser_height_m=7.62  # 3 inches
)

# Fixed turret position
r0 = 3
theta0 = 0.0      # radians
z_base = 0.0

print("\n--- Phi Angle Test ---")
print("Ctrl+C to exit\n")

while True:
    try:
        r = float(input("Target radius r (m): "))
        z = float(input("Target height z (m): "))

        phi = aim.phi_aim_angle(
            r0=r0,
            theta0=theta0,
            rt=r,
            thetat=0.0,          # straight ahead
            z_target_m=z,
            z_base_m=z_base
        )

        phi_limited = aim.phi_limit(phi)

        print(f"→ Raw φ (deg):     {phi:.2f}")
        print(f"→ Limited φ (deg): {phi_limited:.2f}\n")

    except KeyboardInterrupt:
        print("\nExiting phi test.")
        break
