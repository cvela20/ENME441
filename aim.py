# Aim Class
# Cameron Vela, Lucas Billington, Vraj Patel

import math

class Aim:

	def __init__(self, calib_theta_deg = 0.0, calib_phi_deg=0.0, laser_height =0.0):
		self.calib_theta_deg = calib_theta_deg
		self.calib_phi_deg = calib_phi_deg
		self.laser_height = laser_height

	def convert_coordinates(self, r, theta_rad):
		x = r * math.cos(theta_rad)
		y = r * math.sin(theta_rad)

		return x, y


	def theta_aim_angle(self, r0, theta0, rt, thetat):
		x0, y0 = self.convert_coordinates(r0, theta0)
		xt, yt = self.convert_coordinates(rt, thetat)

		dx = xt - x0
		dy = yt - y0

		aim_abs = math.degrees(math.atan2(dy, dx)) % 360
		center_abs = math.degrees(math.atan2(-y0, -x0)) % 360

		theta_deg = (aim_abs - center_abs - self.calib_theta_deg) % 360

		return theta_deg

	def phi_aim_angle(self, r0, theta0, rt, thetat, z_target):
		x0, y0 = self.convert_coordinates(r0, theta0)
		xt, yt = self.convert_coordinates(rt, thetat)

		z0 = self.laser_height

		dx = xt-x0
		dy = yt-y0
		dz = z_target - z0

		horiz_dist = math.sqrt(dx*dx + dy*dy)

		phi_deg = math.degrees(math.atan2(dz, horiz_dist))

		return phi_deg


