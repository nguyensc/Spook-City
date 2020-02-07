import pygame
from league import Drawable
from math import copysign, cos, sin, radians

class Smoke:
	def __init__(self, start_position, end_position, delay):
		self.start_position = start_position
		self.end_position = end_position
		self.x = end_position[0]
		self.y = end_position[1]
		self.delay = delay

		self.red = 128
		self.green = 128
		self.blue = 0
		self.alpha = 32
		self.delta_alpha = 1 # how much to change trasnparency by
		self.colors = (self.red, self.green, self.blue, 1)

		self.width = start_position[0] - end_position[0]
		self.height = start_position[1] - end_position[1]
		self.minsize = 5

		self.delta_width = 1
		self.delta_height = 0

		# either width or height will stay constant based on desired direction
		# only specified through endpoints
		w = max(abs(self.width), self.minsize)
		h = max(abs(self.height), self.minsize)

		# whichever (w or h) is constant should get bigger, to act like smoke
		if (w == self.minsize):
			self.delta_height = 1
		else:
			self.delta_width = 1

		self.surf = pygame.Surface([w, h]).convert_alpha()
		self.surf.fill(self.colors)


	def set_colors(self, new_colors):
		if self.delay <= 0:
			self.red = max(0, new_colors[0])
			self.green = max(0, new_colors[1])
			self.blue = max(0, new_colors[2])
			self.alpha = max(0, new_colors[3])
			self.colors = (self.red, self.green, self.blue, self.alpha)

	def delete(self):
		del self

	def make_surf(self, w, h):
		self.surf = pygame.Surface([w, h]).convert_alpha()
		self.surf.fill(self.colors)

	def update(self):
		print(self.delay)
		if self.delay > 0:
			self.delay -= 1
			return

		self.red = 200
		self.green = 200
		self.blue = 200

		self.delta_width += min(2, self.delta_width * 1)
		self.delta_height += min(2, self.delta_height * 1)

		# rebuild surface with any new color/size values
		w = max(abs(self.width + self.delta_width), self.minsize)
		h = max(abs(self.height + self.delta_height), self.minsize)
		self.make_surf(w, h)



