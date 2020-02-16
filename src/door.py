from league import *
import pygame
from mapRenderer import MapRenderer

class Door(Character):
    def __init__(self, z=0, x=0, y=0, engine = None):
        super().__init__(z, x, y)
        self.x = x; self.y = y;

        self.sheet = Spritesheet('../assets/map assets/container.png', 48, 1)
        self.emptyImage = pygame.image.load('../assets/map assets/containerEmpty.png').convert_alpha()
        self.sprites = self.sheet.sprites
        self.image = self.sprites[0].image
        self.image = pygame.transform.scale(self.image, (192, 192))
        self.emptyImage = pygame.transform.scale(self.emptyImage, (192, 192))

        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        self.isDoor = 1
        self.isEmpty = False
        self.engine = engine
    
    def changeRoom(self):
        self.engine.changeRoom()
        map = MapRenderer("second room", self.engine)
        map.renderBackground()
        map.renderForeGround()

    def makeEmpty(self):
        isEmpty = True
        self.contents = 0
        self.image = self.emptyImage
        return isEmpty


    def update(self, time):
        return
