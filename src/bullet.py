import pygame
import league
from light import Light
from math import cos, sin, radians, floor
from random import randint

class Bullet:
	def __init__(self, position=(0,0), direction=90, speed=1, blocks=None):
		self.x = position[0]
		self.y = position[1]
		self.direction = direction
		self.blocks = blocks
		self.displayed = 0
		self.destroyed = 0

		newdir = direction + randint(-8, 5)
		rads = radians(newdir)
		self.hspeed = (floor(cos(rads)*10) / 10) * speed
		self.vspeed = (floor(sin(rads)*10) / 10) * speed

		self.image = pygame.image.load("../assets/projectiles/bullet.png").convert_alpha()
		self.image = pygame.transform.scale(self.image, (16,16))
		self.image = pygame.transform.rotate(self.image, newdir + 90)

		self.rect = self.image.get_rect()

		self.wall_collider = league.Drawable()
		self.wall_collider.image = pygame.Surface((self.rect.height, self.rect.width))
		self.wall_collider.rect = pygame.Rect((0, 0, 16, 16))

	def move(self):
		x = self.x + self.hspeed * 2
		y = self.y - self.vspeed * 2
		
		# should check for collisions here
		if self.destroyed:
			return

		self.destroyed = self.check_wall_collision()

		self.x = self.rect.x = x
		self.y = self.rect.y = y

	def check_wall_collision(self):
		# all enemy collisions occur in the enemy class
		for sprite in self.blocks:
			self.wall_collider.x = sprite.x
			self.wall_collider.y = sprite.y

			if pygame.sprite.spritecollideany(self, self.blocks):
				return 1
		return 0

	def update(self):
		self.move()