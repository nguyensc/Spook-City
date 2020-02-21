from league import *
import pygame

class RancidMeat():
    def __init__(self, x=0, y=0):    

        self.sheet = Spritesheet('../assets/game objects/rancidmeat.png', 32, 4)
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(x, y))
        self.x = x - self.rect.width // 2
        self.y = y + self.rect.height // 2
        self.rect.x = self.x + self.rect.width // 3
        self.rect.y = self.y + self.rect.height // 3
        self.rect.width = self.rect.width // 5
        self.rect.height = self.rect.height // 5
        self.light = pygame.image.load("../assets/light assets/redlight.png").convert_alpha()
        self.light = pygame.transform.scale(self.light, (96, 96))

        # a separate collision rectangle for the area of effect (think of this like strength of smell for attracting baddies)
        self.aoe_rect = self.image.get_rect(center=(self.rect.x, self.rect.y))
        self.aoe_rect.width = 128
        self.aoe_rect.height = 128
        self.aoe_rect.x -= self.aoe_rect.width // 3
        self.aoe_rect.y -= self.aoe_rect.height // 3

        self.triggered = 0
        self.isLightSource = 1
        self.fortitude = 100 # how long can the rancid meat last against an enemy ripping it apart
        self.destroyed = 0
        self.image_timer = 2
        self.image_counter = 0
        self.image_number = 16

    def animate(self):
        # check the timing and see if ready to switch to next image index
        if self.image_counter <= 0:
            self.image_index = (self.image_index + 1) % self.image_number
            self.image_counter = self.image_timer
        else:
            self.image_counter -= 1       


    def aoe(self, target):
        # check end condition (target is at the core rect)
        if pygame.sprite.collide_rect(self, target):
            target.state = 3 # render the target useless
            self.fortitude -= 5
        # attract target inside of aoe_rect toward core rect
        else:
            target.target = self


    def update(self):
        if self.fortitude <= 0:
            self.destoryed = 1
            return
        self.image = self.sprites[self.image_index].image.convert_alpha()
        self.image = pygame.transform.scale(self.image, (48, 48))
        self.animate()
        return
