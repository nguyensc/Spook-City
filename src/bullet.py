import pygame
from league import Drawable
from math import copysign, cos, sin, radians

class Bullet:
	def __init__(self, start_position, end_position):
		self.start_position = start_position
		self.end_position = end_position
		self.x = end_position[0]
		self.y = end_position[1]

		self.tag = None

		self.red = 255
		self.green = 255
		self.blue = 0
		self.alpha = 255
		self.delta_alpha = 10 # how much to change the transparency by
		self.colors = (self.red, self.green, self.blue, self.alpha)

		self.width = start_position[0] - end_position[0]
		self.height = start_position[1] - end_position[1]
		self.minsize = 5

		w = max(abs(self.width), self.minsize)
		h = max(abs(self.height), self.minsize)
		self.surf = pygame.Surface([w, h]).convert_alpha()
		self.rect = pygame.Rect((0, 0, w, h))
		self.surf.fill(self.colors)


	def set_colors(self, new_colors):
		self.red = max(0, new_colors[0])
		self.green = max(0, new_colors[1])
		self.blue = max(0, new_colors[2])
		self.alpha = max(0, new_colors[3])
		self.colors = (self.red, self.green, self.blue, self.alpha)

	def delete(self):
		del self

	def make_surf(self, w, h):
		self.surf = pygame.Surface([w, h]).convert_alpha()
		self.rect = pygame.Rect((0, 0, w, h))
		self.surf.fill(self.colors)

	def update(self):
		# rebuild surface with any new color/size values
		w = max(abs(self.width), self.minsize)
		h = max(abs(self.height), self.minsize)
		self.make_surf(w, h)



