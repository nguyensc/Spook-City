from league import *
import pygame

class Container(Character):
    def __init__(self, z=0, x=0, y=0, contents=None):
        super().__init__(z, x, y)
        self.x = x; self.y = y;

        self.sheet = Spritesheet('../assets/map assets/container.png', 48, 1)
        self.emptyImage = pygame.image.load('../assets/map assets/containerEmpty.png').convert_alpha()
        self.sprites = self.sheet.sprites
        self.image = self.sprites[0].image
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.emptyImage = pygame.transform.scale(self.emptyImage, (96, 96))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.contents = contents
        self.isEmpty = False


    '''
    def animate(self):
        # check the timing and see if ready to switch to next image index
        if self.sprite_speed_counter <= 0:
            self.image_index = min(self.image_index + 1, 3) 
            self.sprite_speed_counter = self.sprite_speed
        else:
            self.sprite_speed_counter -= 1       
    '''
    def makeEmpty(self):
        isEmpty = True
        self.contents = 0
        self.image = self.emptyImage
        return isEmpty


    def update(self, time):
        return
