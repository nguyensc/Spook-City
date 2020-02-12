from league import *
import pygame

''' the first active (usable) item '''
class BearTrap():
    def __init__(self, x=0, y=0):    

        self.sheet = Spritesheet('../assets/beartrap.png', 32, 2)
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.rect = self.image.get_rect()

        self.x = x - self.rect.width // 2
        self.y = y + self.rect.height // 2

        self.rect.x = self.x
        self.rect.y = self.y

        self.triggered = 0
        self.isLightSource = 0

        self.sprite_speed = 3
        self.sprite_speed_counter = 0

    def animate(self):
        # check the timing and see if ready to switch to next image index
        if self.sprite_speed_counter <= 0:
            self.image_index = min(self.image_index + 1, 3) 
            self.sprite_speed_counter = self.sprite_speed
        else:
            self.sprite_speed_counter -= 1       


    def update(self):
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))

        if self.triggered:
            self.animate()
        return
