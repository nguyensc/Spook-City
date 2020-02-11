import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player
        self.image = pygame.Surface([720, 720]).convert_alpha()
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 10
        self.rect.x = 100
        self.rect.y = 10
        self.static = True


        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render(str(self.player.health) + "        4 lives", True, (0,0,0))

        self.ui_box = pygame.image.load("../assets/overlay assets/ui_box.png")
        self.item_icons = [
            pygame.image.load('../assets/icons/beartrap.png').convert_alpha()
        ]

        
    def update(self, deltaTime):
        self.image = pygame.Surface([720, 720]).convert_alpha()
        self.image.fill((255,255,255,0))
        
        self.text = self.font.render(str(self.player.health) + "        4 lives", True, (0,0,0))
        
        # draw ui box
        self.ui_box = pygame.image.load("../assets/overlay assets/ui_box.png")
        self.ui_box = pygame.transform.scale(self.ui_box, (64, 64))
        
        # draw selected active 
        if self.player.inventory[self.player.active_item] == "beartrap":
            selected_item = self.item_icons[0]
            self.ui_box.blit(pygame.transform.scale(selected_item, (64, 64)).convert_alpha(), (0, 4))

        self.image.blit(self.text, (0, 0))
        self.image.blit(self.ui_box, (0, 0))
