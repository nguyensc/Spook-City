import pygame
from league import *

class Flashlight(DUGameObject):
    def __init__(self, z=0, x=0, y=0, target=None):
        super().__init__(z,x,y)
        self.delta = 512
        self.target = target
        self.x = target.x
        self.y = target.y
        self.scale = int(256 / 64);

        self.image = pygame.image.load("../assets/light assets/RadialTrapezoid.png").convert_alpha()
        self.image.fill((255, 255, 255, 100),None, pygame.BLEND_RGBA_MULT)
        self.image = pygame.transform.scale(self.image, (256, 64))
        
        self.collide = Drawable()
        self.collide.image = pygame.Surface([4,4])
        self.collide.rect = pygame.Rect(0,0,4,4)


        self.world_size = (Settings.width, Settings.height)
        self.blocks = pygame.sprite.Group()

    def lineOfSight(self, length = 0):
        xx = int(self.rect.x)
        yy = int(self.rect.y)
        n_position = (xx - length, yy)
        for i in range(length):
            self.collide.x = self.collide.rect.x = xx
            self.collide.y = self.collide.rect.y = yy

            if(pygame.sprite.spritecollideany(self.collide, self.blocks) != None):
                n_position = (xx,yy)
                break
            xx -= 1
        return n_position

    def update(self, time):
        self.x = self.target.x + 20
        self.y = self.target.y - 10
