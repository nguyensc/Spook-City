from league import *
import pygame
from mapRenderer import MapRenderer

class Door(Character):
    def __init__(self, z=0, x=0, y=0, warpx=0, warpy=0, connected_room=None, engine=None):
        super().__init__(z, x, y)
        self.x = x; self.y = y
        self.warpx = warpx; self.warpy = warpy
        self.sheet = Spritesheet_Ext('../assets/map assets/sprite sheets/Hospital Tiles/!$Elevator Doors-Alt.png', 48, 32, 2)
        self.emptyImage = pygame.image.load('../assets/map assets/containerEmpty.png').convert_alpha()
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y
        self.animation_timer = 3
        self.animation_counter = self.animation_timer
        self.isDoor = 1
        self.isLightSource = 1
        self.light = pygame.image.load("../assets/light assets/orangelight.png").convert_alpha()
        self.light = pygame.transform.scale(self.light, (128, 128))
        self.light_offsetx = 24
        self.light_offsety = 24
        self.glow = -1
        self.transform = (128, 128)
        self.open = 0
        self.engine = engine
        self.engine.dynamic_instances.append(self)
        # parse connected room
        self.room_num = 0
        if connected_room == "first room":
            self.room_num = 1
        elif connected_room == "second room":
            self.room_num = 2
        elif connected_room == "third room":
            self.room_num = 3
        elif connected_room == "fourth room":
            self.room_num = 4
        elif connected_room == "fifth room":
            self.room_num = 5
    
    def changeRoom(self):
        # begin the animation process of opening the door
        self.open = 1

    def update(self, time=0):
        # must be animated all the way
        if self.open:
            if self.image_index >= 5:
                # invoke engine's change room capabilities 
                self.engine.player.x = self.warpx
                self.engine.player.y = self.warpy
                self.engine.changeRoom(self.room_num)
                del self
                return
            # will only hit if the full animation has played (thanks modulo operator %)
            elif self.animation_counter <= 0:
                self.image_index = min(self.image_index + 1, 5)
                self.animation_counter = self.animation_timer
            self.animation_counter -= 1

        # display updated image
        self.image = self.sprites[self.image_index].image
        self.image = pygame.transform.scale(self.image, (64, 64))

        self.light = pygame.transform.scale(self.light, self.transform)


        return
