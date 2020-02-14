from league import *
import pygame

''' the first active (usable) item '''
class RancidMeat():
    def __init__(self, x=0, y=0):    

        self.sheet = Spritesheet('../assets/rancid_meat.png', 32, 1)
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.x = x - self.rect.width // 2
        self.y = y + self.rect.height // 2

        self.rect.x = self.x + self.rect.width // 3
        self.rect.y = self.y + self.rect.height // 3
        self.rect.width = self.rect.width // 5
        self.rect.height = self.rect.height // 5

        # a separate collision rectangle for the area of effect (think of this like strength of smell for attracting baddies)
        self.aoe_rect = (self.rect.x, self.rect.y, 128, 128) 

        self.triggered = 0
        self.isLightSource = 0
        self.fortitude = 100 # how long can the rancid meat last against an enemy ripping it apart

        self.sprite_speed = 3
        self.sprite_speed_counter = 0      


    def update(self):
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        return
