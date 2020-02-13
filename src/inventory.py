import league
import pygame

class Inventory(league.DUGameObject):
    def __init__(self, player, pickup=None):
        super().__init__(self)
        self._layer = 1001
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf', 32)
        self.image = pygame.image.load('../assets/overlay assets/Hearts/basic/heart.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = 10
        self.y = 10
        self.rect.x = 100
        self.rect.y = 10
        self.static = True
        #self.pickup = pickup

    def update(self, deltaTime):
        if(len(self.player.items) > 0) :
            self.image =  pygame.image.load('../assets/inventory assets/key.png').convert_alpha()
            self.image = pygame.transform.scale(self.image, (64, 64))
            #self.pickup.kill()