from league import *
import pygame

class Pickup(DUGameObject):
    def __init__(self, z=0, x=0, y=0):
        super().__init__(z, x, y)

        self.last_hit = pygame.time.get_ticks()

        self.x = x
        self.y = y

        self.image = pygame.image.load('../assets/inventory assets/key.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()

        self.blocks = pygame.sprite.Group()

        self.collide_function = pygame.sprite.collide_circle
        self.collisions = []


        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = self.collider.image.get_rect()
    
    def pickedUp(self) :
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            print("picked up key")
            self.image = pygame.image.load('../assets/overlay assets/Hearts/basic/heart.png').convert_alpha()
            self.x = -100
            self.y = -100

        #this is super hacky. SEt it to blank and throw it off the screen
    
    def update(self, time):
        self.rect.x = self.x
        self.rect.y = self.y
        self.collisions = []
        for sprite in self.blocks:
            self.collider.rect.x= sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
