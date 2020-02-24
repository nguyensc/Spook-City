from league import *
import pygame

''' an active (usable) item just like beartrap '''
class Lantern():
    def __init__(self, x=0, y=0):    

        self.sheet = Spritesheet('../assets/game objects/lantern.png', 48, 1)
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = pygame.Rect((0, 0, 48, 48))
        self.x = x
        self.y = y
        self.rect.x = self.x
        self.rect.y = self.y

        self.triggered = 0
        self.isLightSource = 1
        self.light = pygame.image.load('../assets/light assets/Radial4.png').convert_alpha()
        self.light = pygame.transform.scale(self.light, (256, 256))
        self.light_offsetx = 24
        self.light_offsety = 24
        self.sprite_speed = 3
        self.sprite_speed_counter = 0

    def animate(self):
        # check the timing and see if ready to switch to next image index
        if self.sprite_speed_counter <= 0:
            self.image_index = (self.image_index + 1) % 7 
            self.sprite_speed_counter = self.sprite_speed
        else:
            self.sprite_speed_counter -= 1    

    def update(self):
        self.image = pygame.Surface([256, 256]).convert_alpha()
        self.image.fill((255,255,255,0))

        self.lantern = self.sprites[self.image_index].image.convert_alpha()
        self.lantern = pygame.transform.scale(self.lantern, (48, 48))

        self.image.blit(self.lantern, (64, 64))

        return
