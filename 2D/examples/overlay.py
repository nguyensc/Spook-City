import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.image = self.font.render(str(self.player.health) + "        4 lives", True, (0,0,0))
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 10
        self.rect.x = 100
        self.rect.y = 10
        self.static = True

    def update(self, deltaTime):
        self.image = self.font.render(str(self.player.health) + "        4 lives", True, (0,0,0))
