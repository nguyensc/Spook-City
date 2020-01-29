from league import *
import pygame


class Light(Character):
    def __init__(self, x=0, y=0, z=0, target=None):
        super().__init__(x, y, z)
        self.delta = 512
        self.target = target
        self.x = target.x
        self.y = target.y
        self.scale = int(256 / 64);

        self.image = pygame.image.load("../assets/light assets/Radial4.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (256,256))
        
    
        self.world_size = (Settings.width, Settings.height)
        self.blocks = pygame.sprite.Group()

  
    def update(self, time):
        self.x = (self.target.rect.x - self.scale) - 120; self.y = self.target.rect.y - 120;
        