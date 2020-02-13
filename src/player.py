from league import *
from math import radians, cos, sin, copysign
import pygame
from beartrap import BearTrap
from lantern import Lantern
from bullet import Bullet


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
        self.interactables = pygame.sprite.Group()
        self.hazards = [] # similar to interactables but dangerous!

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
        
        self.sheet = Spritesheet('../assets/player/Black/player_idle.png', 48, 1)
        self.sprites = self.sheet.sprites
        self.image = self.sprites[0].image

        # timers
        self.shoot_timer = 20
        self.shoot_counter = self.shoot_timer
        self.spotted_timer = 30
        self.spotted_counter = self.spotted_timer
        self.interaction_timer = 20
        self.interaction_counter = self.interaction_timer

        self.rect = pygame.Rect((8, 8, 20, 20)) # the players collision mask, this determines when the player collides with things
        self.enemy = enemy;
        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
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

        self.sight_coords = [(-1, -1), (-1, -1), (-1, -1), (-1, -1)]


    def get_x(self):
        return self.rect.x


    def get_y(self):
        return self.rect.y


    def move_left(self, time):
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
        amount = self.delta * time
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


    def lineofsight_raycast(self, length, direction):
        xx = int(self.rect.x); yy = int(self.rect.y)
        r = radians(direction)
        dirx = int(cos(r))
        diry = int(sin(r))
        end_position = (xx + dirx * length, yy + diry * length)

        for i in range(length):
            self.cpoint.x = self.cpoint.rect.x = xx
            self.cpoint.y = self.cpoint.rect.y = yy

            # line of sight runs into enemy
            if self.enemy.rect.collidepoint(xx, yy):
                if not dirx:
                    self.spotted_by_enemy(self.enemy, 0, copysign(-1, self.enemy.y - self.y)) # set enemy state
                else:
                    self.spotted_by_enemy(self.enemy, copysign(1, self.enemy.x - self.x), 0)

                end_position = (xx, yy)
                break
            # line of sight runs into wall
            elif pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (xx, yy)
                break     
            xx += dirx * 2
            yy += diry * 2
        return end_position  

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
        # check for interaction buffer
        if self.interaction_counter > self.interaction_timer:
            return # player must wait before another action

        # set the interaction timer, must be held to complete action
        if self.interaction_counter <= 0:
            self.interaction_counter = self.interaction_timer + 10 # reset interaction timer
            print("hit")
            # loop through the interactable sprite group
            for sprite in self.interactables:
                if pygame.sprite.collide_rect(self, sprite):
                    print("interaction triggered!  ", sprite.contents)
                    self.inventory[self.active_item] = sprite.contents
                    sprite.makeEmpty()
        else:
            # decrement timer
            self.interaction_counter -= 1

    def use_active_item(self, time):
        # beartrap use code
        if self.inventory[self.active_item] == "beartrap":
            self.create_physical_item(0, 1, BearTrap(self.x, self.y))

        # lantern use code
        elif self.inventory[self.active_item] == "lantern":
            self.create_physical_item(0, 0, Lantern(self.x, self.y))

        self.inventory[self.active_item] = "None" # empty out the current inventory slot


    def create_physical_item(self, impassable, hazard, item):
        if impassable:
            self.blocks.append(item)
        
        if hazard:
            self.hazards.append(item)
        # add a new object to the list of entities created from user input
        self.items.append(item) 

    def update(self, time):      
        print(self.interaction_counter)

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

            self.lineofsight_right(400)
            self.lineofsight_left(400)
            self.lineofsight_up(200)
            self.lineofsight_down(200)
        else:
            self.interaction_counter_prev = self.interaction_counter
            # check for redundant action meter display
            if self.interaction_counter_prev == self.interaction_counter and self.interaction_counter != self.interaction_timer:
                self.interaction_counter = self.interaction_timer + 10

        self.collisions = []
        prevrect = (self.get_x(), self.get_y())
        self.collider.x = self.collider.rect.x = self.rect.x = self.x;
        self.collider.y = self.collider.rect.y = self.rect.y = self.y;            

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
