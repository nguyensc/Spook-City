import pygame
from league import *

class Flashlight(DUGameObject):
    def __init__(self, z=0, x=0, y=0, target=None):
        super().__init__(z,x,y)
        self.delta = 512
        self.target = target
        self.x = target.x
        self.y = target.y
        self.scale = int(256 / 64)

        self.image = pygame.image.load("../assets/light assets/RadialTrapezoid.png").convert_alpha()
        self.image.fill((255, 255, 255, 255),None, pygame.BLEND_RGBA_MULT)
        self.image = pygame.transform.scale(self.image, (128, 64))

        self.world_size = (Settings.width, Settings.height)
        self.blocks = pygame.sprite.Group()


    def update(self, time):
        self.x = self.target.rect.x + 30
        self.y = self.target.rect.y - 10
