import time as t
from datetime import datetime

from league import *
import pygame
from enemies.gremlin import Gremlin
from math import copysign, radians, cos, sin
from random import seed, randint

class Spooks(Character):
    def __init__(self, z=0, x=0, y=0, player = None, engine = None):
        super().__init__(z=z, x=x, y=y)
        self.target = player
        self.walk_speed = 1
        self.run_speed = 3
        self.move_speed = self.walk_speed
        self.engine = engine

        # state 0 => IDLE moves in circle
        # state 1 => SPAWN GREMLIN
        # state 2 => CAUGHT
        # state 3 => RUN
        self.state = 0

        self.dirx = 0
        self.diry = 0
        self.direction = 0
        self.idle_speed = 10

        self.spawntimer = 100
        self.spawncounter = self.spawntimer
        self.sight_timeout = 30
        self.sight_counter = self.sight_timeout
        self.delta = 512
        # image only a place holder
        self.image = pygame.image.load('../assets/enemy/zombie/skeleton-clothed-4.png')
        # animation for spooks goes here
        self.rect = self.image.get_rect(center=(self.x,self.y))
        self.mask = pygame.mask.from_surface(self.image)
        self.last_hit = pygame.time.get_ticks()

        self.blocks = pygame.sprite.Group()
        self.hazards_blocks = pygame.sprite.Group()
        self.hazards = player.hazards
           # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collisions = []
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = pygame.Rect((0, 0, 48, 48))

    def set_directions(self, new_dirx, new_diry):
        self.dirx = new_dirx; self.diry = new_diry;

    def new_direction(self):
        prev_dir = (self.dirx, self.diry)
        possible_dirs = [
            (-1, 0),
            (0, -1),
            (0, 1),
            (1, 0),
        ]
        valid_dirs = []
        length_dirs = len(possible_dirs) - 1

        # set up valid directions
        i = 0
        for direction in possible_dirs:
            # loop through each direction
            xx = (direction[0] * self.image.get_width()) + self.rect.x
            yy = (direction[1] * self.image.get_height()) + self.rect.y
            # move collider object there
            self.collider.rect.x = self.collider.x = xx
            self.collider.rect.y = self.collider.y = yy
            # if there is a collision, set that possible direction to None
            valid_dirs.append(pygame.sprite.spritecollideany(self.collider, self.blocks))

            self.tests[i].x = self.collider.rect.x; self.tests[i].y = self.collider.rect.y;
            i+=1

        # randomly pick valid direction to being moving

        # check if all directions are 'None', bugged
        flag = 0
        for j in range(4):
            if valid_dirs[j] != None:
                flag = 1
        if not flag:
            # if the none direction bug is encountered move towards opposite
            # direction
            self.dirx = prev_dir[0] * -1
            self.diry = prev_dir[1] * -1
            return

        # grab legit direction
        i = randint(0, length_dirs)
        for valid_dir in valid_dirs:
            if possible_dirs[i] == prev_dir:
                i = (i + randint(1, 2)) % length_dirs
                continue
            elif valid_dir != None:
                self.dirx = possible_dirs[i][0]
                self.diry = possible_dirs[i][1]
                break
            i = (i + randint(1, 2)) % length_dirs

        # reset state to patrol
        self.state = 0
        return



    def check_and_handle_timeout(self):
        # see how far the enemy has moved from the last known NON-stuck position
        self.timeout_check = (abs(self.rect.x - self.timeout_position[0]), abs(self.rect.y - self.timeout_position[1]))

        # see if timeout has been reached yet, this means the enemy has not been moving enough and must be stuck
        # in a state loop
        if self.timeout_counter <= 0:
            self.state = (self.state + 1) % 2 # change movement direction state
            self.timeout_counter = self.timeout # reset timer

        # see how far the enemy has moved since the last check, this is to see if the enemy has become
        # stuck for some reason
        elif self.timeout_check[0] >= 7 or self.timeout_check[1] >= 7:
            # reset the timeout counter if the enemy has moved enough to not be stuck
            self.timeout_counter = self.timeout
            self.timeout_position = (self.rect.x, self.rect.y) # update the position to be checked next time
        else:
            self.timeout_counter-=1

    def spawn_kids(self):

        if(self.spawncounter <= 0):
            temp = Gremlin(2, self.x, self.y, self.target, self)
            temp.blocks = self.blocks
            temp.hazards = self.hazards
            self.engine.drawables.add(temp)
            self.engine.objects.append(temp)
            self.spawncounter = 100
            self.state = 0
        else:
            self.spawncounter = self.spawncounter - 1
     

    def idle(self):
        # check for spawn timer
        if self.spawncounter <= 0:
            self.spawncounter = self.spawntimer
            self.state = 1
            return
        self.spawncounter -= 1

        # determine if the current speed is high enough to change direction
        if self.move_speed > self.idle_speed:
            self.move_speed = 0
            self.direction = (self.direction + 90) % 360 # turn direction to the left

        rads = radians(self.direction)
        dirx = int(cos(rads))
        diry = int(sin(rads))

        self.x += dirx * self.move_speed
        self.y += diry * self.move_speed
        self.move_speed += 0.5



    def chase(self):
        # when to stop chasing and give up back to patrolling
        if (self.sight_counter <= 0):
            self.move_speed = self.walk_speed
            self.state = 0
        
        # begin running instead of walking
        self.move_speed = self.run_speed
        tarx = self.x + self.move_speed * self.dirx
        tary = self.y + self.move_speed * self.diry
        # temporary direction values, will be changed if there is a potential collision
        dirx = self.dirx; diry = self.diry;

        self.collider.x = tarx; self.collider.y = tary;
        if (pygame.sprite.spritecollideany(self.collider, self.blocks) != None):
            if not self.dirx:
                dirx = copysign(1, self.target.x - self.x)
                diry *= -1
            else:
                dirx *= -1
                diry = copysign(1, self.target.y - self.y)

        # move toward specified direction
        self.x += self.move_speed * dirx
        self.y += self.move_speed * diry

        # lower the sight counter, determines when enemy loses interest
        self.sight_counter -= 1
        
        return


    def shot(self):
        now = pygame.time.get_ticks()

        if now - self.last_hit > 1000:
            self.health = self.health - 25
            self.last_hit = now

        self.image.fill(255, 0, 0, 255)

    def update(self, time):
        if time != 0:
            # patrol state
            if self.state == 0:
                self.idle()
            # new direction state
            elif self.state == 1:
                self.spawn_kids()
            # chase state
            elif self.state == 2:
                self.chase()
            elif self.state == 3:
                return

       

        self.collider.x = self.rect.x = self.x
        self.collider.y = self.rect.y = self.y
        self.collisions = []

        for hazard in self.hazards:
            if pygame.sprite.collide_rect(self, hazard):
                hazard.triggered = 1
                self.state = 3
                return


        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)

        self.sight_counter-=1