import pygame

class Node:
	def __init__(self, parent, x=0, y=0, w=32, h=32):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.neighbors = []
