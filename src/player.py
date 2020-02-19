from league import *
from math import radians, cos, sin, copysign
import pygame
from beartrap import BearTrap
from lantern import Lantern
from rancidmeat import RancidMeat


class Player(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0, enemy=None):
        super().__init__(z, x, y)
        # This unit's health
        self.health = 100
        self.heart_rate = 10 # lower = faster heart animation speed
        self.bullets = []
        self.blocks = pygame.sprite.Group() # What sprites am I not allowd to cross?
        self.interactables = pygame.sprite.Group()
        self.hazards = [] # similar to interactables but dangerous!
        self.enemies = pygame.sprite.Group()
        self.stepTile = 0
        self.direction = 0
        self.last_hit = pygame.time.get_ticks()
        self.delta = 512
        self.screen = None
        # Where the player is positioned
        self.x = x
        self.y = y
        self.camera = None

        self.items = None # set up by in engine in game.py
        self.inventory = {
            0: "None"
        }
        self.active_item = 0
        
        self.sheet = Spritesheet('../assets/map assets/sprite sheets/Horror City - Frankenstein MV/Characters/$Dr Frankenstien.png', 64, 3)
        self.sprites = self.sheet.sprites
        self.image = self.sprites[self.stepTile].image

        # timers
        self.shoot_timer = 20
        self.shoot_counter = self.shoot_timer
        self.spotted_timer = 30
        self.spotted_counter = self.spotted_timer
        self.interaction_timer = 20
        self.interaction_counter = self.interaction_timer
        self.interaction_counter_prev = -1
        self.interaction_timeout = 10
        # raycast init
        self.raycast_increments = 15
        self.raycast_points = [0 for i in range(360 // self.raycast_increments)]
        self.sight_coords = [(-1, -1), (-1, -1), (-1, -1), (-1, -1)]

        self.rect = self.image.get_rect(center=(self.x,self.y)) # the players collision mask, this determines when the player collides with things
        self.rect.width = self.rect.width // 2
        self.rect.height = self.rect.height // 2

        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        
        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collisions = []
        # For collision detection, we need to compare our sprite
        # with collideable sprites.  However, we have to remap
        # the collideable sprites coordinates since they change.
        # For performance reasons I created this sprite so we
        # don't have to create more memory each iteration of
        # collision detection.
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = pygame.Rect(0, 0, 16, 16)

        self.cpoint = Drawable()
        self.cpoint.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.cpoint.rect = pygame.Rect(0, 0, 1, 1)

        # Overlay
        self.font = pygame.font.Font('freesansbold.ttf',32)
        self.overlay = self.font.render(str(self.health) + "        4 lives", True, (0,0,0))


    def get_x(self):
        return self.rect.x


    def get_y(self):
        return self.rect.y

    def move_left(self, time):
        self.get_animation(3)
        self.direction = 1
        amount = self.delta * time
        try:
            if self.x - amount < 0:
                raise OffScreenLeftException
            else:
                self.x = self.x - amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x + amount
                    self.update(0)
        except:
            pass

    def move_right(self, time):
        self.get_animation(1)
        self.direction = 3
        self.collisions = []
        amount = self.delta * time
        try:
            if self.x + amount > self.world_size[0] - Settings.tile_size:
                raise OffScreenRightException
            else:
                self.x = self.x + amount
                self.update(0)
                while(len(self.collisions) != 0):
                    self.x = self.x - amount
                    self.update(0)
        except:
            pass

    def move_up(self, time):
        self.get_animation(0)
        self.direction = 0
        self.collisions = []
        amount = self.delta * time
        try:
            if self.y - amount < 0:
                raise OffScreenTopException
            else:
                self.y = self.y - amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y + amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def move_down(self, time):
        self.get_animation(2)
        self.collisions = []
        amount = self.delta * time
        self.stepTile = (self.stepTile + 1) % 4
        self.image = self.sprites[self.stepTile].image
        try:
            if self.y + amount > self.world_size[1] - Settings.tile_size:
                raise OffScreenBottomException
            else:
                self.y = self.y + amount
                self.update(0)
                if len(self.collisions) != 0:
                    self.y = self.y - amount
                    self.update(0)
                    self.collisions = []
        except:
            pass

    def get_animation(self, dir):
        if self.direction != dir:
            self.direction = dir
            self.stepTile = 0

        self.stepTile = ((self.stepTile + 1) % 3) + (self.direction * 3)
        self.image = self.sprites[self.stepTile].image

        
    def shoot_bullet(self, time, dir):
        if (self.shoot_counter > 0):
            return
        self.shoot_counter = self.shoot_timer

        bullet = Bullet((self.x - 32, self.y + 64), dir, 10, self.blocks)
        self.bullets.append(bullet)
    def shoot_bullet_up(self, time):
        self.shoot_bullet(time, 90)
    def shoot_bullet_down(self, time):
        self.shoot_bullet(time, 270)
    def shoot_bullet_left(self, time):
        self.shoot_bullet(time, 180)
    def shoot_bullet_right(self, time):
        self.shoot_bullet(time, 0)


    def lineofsight_raycast(self, length, direction, precise=0):
        xx = int(self.rect.x + 16); yy = int(self.rect.y + 16)
        r = radians(direction)
        dirx = int(cos(r))
        diry = int(sin(r))
        # necessary for light raycasting
        if precise:
            dirx = cos(r)
            diry = sin(r)
        # find where the raycast SHOULD end up assuming nothing blocking it
        end_position = (xx + dirx * length, yy + diry * length)
        tempx = xx; tempy = yy
        # loop through all positions in range
        for i in range(0, length, 8):
            self.cpoint.x = self.cpoint.rect.x = tempx
            self.cpoint.y = self.cpoint.rect.y = tempy
            # line of sight runs into wall
            if pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (tempx, tempy)
                break   
            # line of sight runs into enemy
            elif pygame.sprite.spritecollideany(self.cpoint, self.enemies) != None and not precise:
                # find the specific enemy that has spotted the player
                for enemy in self.enemies:
                    # check if the correct enemy has been found
                    if pygame.sprite.collide_rect(self.cpoint, enemy):
                        if not dirx:
                            self.spotted_by_enemy(enemy, 0, copysign(-1, enemy.y - self.y)) # set enemy state
                        else:
                            self.spotted_by_enemy(enemy, copysign(1, enemy.x - self.x), 0)

                end_position = (xx, yy)
                break


            tempx = xx + dirx * i
            tempy = yy + diry * i

        return end_position  

    def light_raycast(self, length):
        for i in range(0, 360, self.raycast_increments):
            direction = i
            condition0 = (self.direction == 0 and (i >= 330 or i <= 30))
            condition90 = (self.direction == 90 and (i <= 120 and i >= 60))
            condition180 = (self.direction == 180 and (i <= 210 and i >= 150))
            condition270 = (self.direction == 270 and (i <= 300 and i >= 240))
            # extend the raycast if near player movement direction
            if condition0 or condition90 or condition180 or condition270:
                ray = self.lineofsight_raycast(length * 5, direction, 1)
                self.raycast_points[i // self.raycast_increments] = ray
            else:
                ray = self.lineofsight_raycast(length, direction, 1)
                self.raycast_points[i // self.raycast_increments] = ray

    def lineofsight_right(self, length):
        self.sight_coords[0] = self.lineofsight_raycast(length, 0)
        return self.sight_coords[0]

    def lineofsight_left(self, length):
        self.sight_coords[1] = self.lineofsight_raycast(length, 180)
        return self.sight_coords[1]

    def lineofsight_up(self, length):
        self.sight_coords[2] = self.lineofsight_raycast(length, 90)
        return self.sight_coords[2]

    def lineofsight_down(self, length):
        self.sight_coords[3] = self.lineofsight_raycast(length, 270)
        return self.sight_coords[3]


    def spotted_by_enemy(self, enemy, dirx, diry):
        # the 'trapped' state is state 3, enemies should be unable to move in this case
        if enemy.state == 3:
            return
        enemy.state = 2; # enemy chase state is 2
        enemy.sight_counter = enemy.sight_timeout # reset the enemy chase timer
        enemy.target = self
        enemy.dirx = dirx # target x direction to move to
        enemy.diry = diry # target y direction to move to

        # increase heart rate and set counter for when to catch breath
        self.spotted_counter = self.spotted_timer  
        self.heart_rate = 3

        return  


    def interact(self, time):
        # check to make sure the player is in range of an interactable object
        if not pygame.sprite.spritecollideany(self, self.interactables):
            return

        # check for interaction buffer
        if self.interaction_counter > self.interaction_timer:
            return # player must wait before another action

        # set the interaction timer, must be held to complete action
        if self.interaction_counter <= 0:
            self.interaction_counter = self.interaction_timer + 10 # reset interaction timer
            self.interaction_timeout = 10
            
            # loop through the interactable sprite group
            for sprite in self.interactables:
                if pygame.sprite.collide_rect(self, sprite):
                    # check for door opening case
                    if sprite.isDoor == 1:
                        sprite.changeRoom() # run the door opening code
                        return
                    self.inventory[self.active_item] = sprite.contents
        else:
            # decrement timer
            self.interaction_counter -= 1



    def use_active_item(self, time):
        # get direction player is facing, important for placing items
        r = radians(self.direction)
        tarx = self.rect.x + int(cos(r)) * 3
        tary = self.rect.y + int(sin(r)) * 3

        # beartrap use code
        if self.inventory[self.active_item] == "beartrap":
            self.create_physical_item(0, 1, BearTrap(tarx, tary))

        # lantern use code
        elif self.inventory[self.active_item] == "lantern":
            self.create_physical_item(0, 0, Lantern(tarx - 96, tary - 96))
        
        # rancid meat
        elif self.inventory[self.active_item] == "rancidmeat":
            self.create_physical_item(0, 1, RancidMeat(tarx, tary))

        self.inventory[self.active_item] = "None" # empty out the current inventory slot


    def create_physical_item(self, impassable, hazard, item):
        if impassable:
            self.blocks.append(item)
        
        if hazard:
            self.hazards.append(item)
        # add a new object to the list of entities created from user input
        self.items.append(item) 


    def reset_all_timers(self):
        self.shoot_counter = self.shoot_timer
        self.spotted_counter = self.spotted_timer
        self.interaction_counter = self.interaction_timer

    def update(self, time):     
        if (self.sight_coords[0][0] < 0):
            # light raycasts stuff (drawing happens in engine!)
            self.light_raycast(50)

        # events which should not occur on every update call
        if time != 0:
            self.shoot_counter -= 1
            self.spotted_counter -= 1
            if self.spotted_counter <= 0:
                self.heart_rate = 10
            # necessary counter buffer so the player can't spam interactions
            # all other interaction updates occur in the interaction function
            if self.interaction_counter > self.interaction_timer:
                self.interaction_counter -= 1
            # run all line of sight raycasts
            self.lineofsight_right(200)
            self.lineofsight_left(200)
            self.lineofsight_up(200)
            self.lineofsight_down(200)
            # light raycasts stuff (drawing happens in engine!)
            self.light_raycast(50)
        # check for redundant action meter display
        elif self.interaction_counter < self.interaction_timer:
            keys_pressed = pygame.key.get_pressed() # get all pressed keys
            # check to make sure the player is still pressing the interact button
            if keys_pressed[pygame.K_e] != 1:
                # if the action meter is display (meaning the player pressed e) but has stopped pressing the interact button
                # change the counter values so that the overlay stops showing the action meter
                self.interaction_counter = self.interaction_timer + 10


        # collision stuffs
        self.collisions = []
        prevrect = (self.get_x(), self.get_y())
        self.collider.x = self.collider.rect.x = self.rect.x = self.x
        self.collider.y = self.collider.rect.y = self.rect.y = self.y
        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)


    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now

    def getX(self):
        return self.x   
    def getY(self):
        return self.y
