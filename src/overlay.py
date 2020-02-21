import league
import pygame

class Overlay(league.DUGameObject):
    def __init__(self, player):
        super().__init__(self)
        self._layer = 1000
        self.player = player
        self.image = pygame.Surface([480, 480]).convert_alpha()
        self.image.fill((255,255,255,0))
        self.rect = self.image.get_rect()
        self.x = 100
        self.y = 10
        self.rect.x = 100
        self.rect.y = 10
        self.static = True

        # set up any text display stuffs
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.text = self.font.render(str(self.player.health) + "        4 lives", True, (255,255,255))

        # set up action meter for user interaction
        self.action_meter_sheet = league.Spritesheet("../assets/player/action_meter.png", 16, 3)
        self.action_meter_sprites = self.action_meter_sheet.sprites
        self.action_meter_index = 0
        self.action_meter_len = len(self.action_meter_sprites) - 2
        self.action_meter_animation_speed = self.player.interaction_timer // self.action_meter_len + 3
        self.action_meter_animation_counter = self.action_meter_animation_speed

        # set up inventory gui stuffs
        self.ui_box = pygame.image.load("../assets/overlay assets/ui_box.png")
        self.item_icons = [
            pygame.image.load('../assets/game objects/beartrap.png').convert_alpha(),
            pygame.image.load('../assets/game objects/lantern.png').convert_alpha(),
            pygame.image.load('../assets/game objects/rancidmeat.png').convert_alpha()
        ]



    def action_meter_updater(self):
        # if the player is attempting to interact, draw the action meter
        self.action_meter_image = self.action_meter_sprites[self.action_meter_index].image.convert_alpha()
        self.action_meter_image = pygame.transform.scale(self.action_meter_image, (32, 32))
        self.image.blit(self.action_meter_image, (self.player.x, self.player.y))
        
        # check when to animate next sprite
        if self.action_meter_animation_counter <=  0:
            self.action_meter_index = min(self.action_meter_len, self.action_meter_index + 1) # increment the current image index to get next sprite
            self.action_meter_animation_counter = self.action_meter_animation_speed
        else: self.action_meter_animation_counter -= 1
        
    def update(self, deltaTime):
        self.image.fill((255,255,255,0))
        
        self.text = self.font.render(str(self.player.health) + "        4 lives", True, (255,255,255))
        
        # draw ui box
        self.ui_box = pygame.image.load("../assets/overlay assets/ui_box.png")
        self.ui_box = pygame.transform.scale(self.ui_box, (480, 48))
        
        # draw selected active 
        # beartrap case
        if self.player.inventory[self.player.active_item] == "beartrap":
            selected_item = self.item_icons[0]
            self.ui_box.blit(pygame.transform.scale(selected_item, (48, 48)).convert_alpha(), (0, 4))
        # lantern case
        elif self.player.inventory[self.player.active_item] == "lantern":
            selected_item = self.item_icons[1]
            self.ui_box.blit(pygame.transform.scale(selected_item, (48, 48)).convert_alpha(), (0, 4))
        # rancid meat case
        elif self.player.inventory[self.player.active_item] == "rancidmeat":
            selected_item = self.item_icons[2]
            self.ui_box.blit(pygame.transform.scale(selected_item, (48, 48)).convert_alpha(), (0, 4))


        # when the user is performing an interaction,. show the action meter
        if self.player.interaction_counter < self.player.interaction_timer:
            self.action_meter_updater()
        else:
            # reset the action meter image index when no interaction occuring
            self.action_meter_index = 0
            self.action_meter_animation_counter = self.action_meter_animation_speed

        # render all constant gui elements
        self.image.blit(self.text, (0, 0))
        self.image.blit(self.ui_box, (0, 0))

