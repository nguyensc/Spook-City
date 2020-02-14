from league import *
import pygame


class Light(DUGameObject):
    def __init__(self, z=0,x=0,y=0, target=None, scale=170):
        super().__init__(z,x,y)
        self.delta = 512
        self.target = target
        self.x = target.x
        self.y = target.y

        self.image = pygame.image.load("../assets/light assets/Radial4.png").convert_alpha()
        self.image.fill((255, 255, 255, 100),None, pygame.BLEND_RGBA_MULT)
        self.image = pygame.transform.scale(self.image, (scale,scale))
        self.rect = self.image.get_rect()
        self.mask = pygame.mask.from_surface(self.image)
                  
        self.blocks = pygame.sprite.Group()

  
    def update(self, time):
        self.x = self.target.x
        self.y = self.target.y
        self.rect.x = self.target.x - 60
        self.rect.y = self.target.y - 65

    
    
        