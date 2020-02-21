from league import *
import pygame
from math import copysign
from random import seed, randint

class Bogey(Character):
    """
    Moves like a knight from chess
    Does not begin moving until player is in certain range
    """
    def __init__(self, z=0, x=0, y=0, player=None):
        super().__init__(z, x, y)
        # This unit's attributes
        self.health = 100
        self.walk_speed = 1
        self.run_speed = 2
        self.move_speed = self.walk_speed # the current movement speed

        # state 0 -> IDLE
        # state 1 -> PATROL ANGLE
        self.state = 0
        self.player = player
        self.target = self.player
        self.dirx = 0
        self.diry = 1

        # player spotted timeout (how long to chase for)
        self.sight_timeout = 30
        self.sight_counter = self.sight_timeout
        self.delta = 512
        self.x = x
        self.y = y
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.sheet = Spritesheet('../assets/character assets/bogey/Idle.png', 150, 2)
        self.sprites = self.sheet.sprites
        self.image_index = 0
        self.image = self.sprites[self.image_index].image
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.width *= 1 / 2; self.rect.height *= 1 / 2;
        
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        self.hazards = []
        self.hazard_blocks = pygame.sprite.Group()

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collisions = []
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = pygame.Rect((0, 0, 48, 48))


    def move(self):
        # state machine -> updates self.dirx and self.diry (the direction of movement)
        self.x += self.move_speed * self.dirx
        self.y += self.move_speed * self.diry 

        '''
        # collision handling
        while len(self.collisions) != 0:
            # move in opposite x/y directions
            # will not be moved if direction if 0
            self.x -= self.dirx * 20
            self.y -= self.diry * 20 # move in opposite y direction

            self.update(0) # update to recheck collisions
            
            # set state to new direction
            self.state = 1
        '''

        return


    def chase(self):
        return

    def idle(self):
        return



    def update(self, time):
        if time != 0:
            # patrol state
            if self.state == 0:
                self.idle()
       
        self.collider.x = self.rect.x = self.x
        self.collider.y = self.rect.y = self.y
        self.collisions = []

        for hazard in self.hazards:
            # check if hazard has an area of effect
            if hasattr(hazard, "aoe_rect"):
                # run aoe code
                hazard.aoe(self)
                print(hazard.fortitude)
                if hazard.fortitude <= 0:
                    self.target = self.player
                    del hazard

            elif pygame.sprite.collide_rect(self, hazard) and not hazard.triggered:
                hazard.triggered = 1
                self.state = 3
                return


        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

        self.sight_counter-=1
