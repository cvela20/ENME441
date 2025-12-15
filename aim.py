import math

class Aim:

	def __init__(self, calib_theta_deg = 0.0):
		self.calib_theta_deg = calib_theta_deg

	def polar_to_cart(self, r, theta_rad):
		x = r * math.cos(theta_rad)
		y = r * math.sin(theta_rad)

		return x, y


	def theta_aim_angle(self, r0, theta0, rt, thetat):
		x0, y0 = self.polar_to_cart(r0, theta0)
		xt, yt = self.polar_to_cart(rt, thetat)

		dx = xt - x0
		dy = yt - y0

		aim_theta = math.degrees(math.atan2(dy, dx))
		aim_theta = (aim_theta - self.calib_theta_deg) % 360

		return aim_theta


if __name__ == "__main__":
    a = Aim(calib_theta_deg=0.0)

    # Place your turret at r=300, theta=0 rad (point on +x axis)
    r0, t0 = 300.0, 0.0

    # Target turret at r=300, theta=pi/2 rad (point on +y axis)
    rt, tt = 300.0, math.pi/2

    ang = a.theta_aim_angle(r0, t0, rt, tt)
    print("Aim angle (deg):", ang)