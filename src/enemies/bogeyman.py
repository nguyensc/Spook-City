import time as t
from datetime import datetime

from league import *
import pygame
from math import copysign
from random import seed, randint

class Enemy(Character):
    """This is a sample class for a player object.  A player
    is a character, is a drawable, and an updateable object.
    This class should handle everything a player does, such as
    moving, throwing/shooting, collisions, etc.  It was hastily
    written as a demo but should direction.
    """
    def __init__(self, z=0, x=0, y=0, player=None):
        super().__init__(z, x, y)
        # This unit's attributes
        self.health = 100
        self.walk_speed = 1
        self.run_speed = 2
        self.move_speed = self.walk_speed # the current movement speed

        # state 0 -> PATROL
        # state 1 -> DECIDE DIRECTION
        # state 2 -> CHASE
        self.state = 0
        self.player = player
        self.target = self.player
        self.dirx = 0
        self.diry = 1

        # timeout movement values
        self.timeout = 10
        self.timeout_counter = self.timeout
        self.timeout_position = (self.rect.x, self.rect.y)
        # player spotted timeout (how long to chase for)
        self.sight_timeout = 30
        self.sight_counter = self.sight_timeout

        # Last time I was hit
        self.last_hit = pygame.time.get_ticks()
        # A unit-less value.  Bigger is faster.
        self.delta = 512
        # Where the player is positioned
        self.x = x
        self.y = y
        # The image to use.  This will change frequently
        # in an animated Player class.
        self.image = pygame.image.load('../assets/skeleton-clothed-1.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (64, 64))
        self.rect = self.image.get_rect(center=(self.x, self.y))
        self.rect.width *= 1 / 2; self.rect.height *= 1 / 2;
        self.mask = pygame.mask.from_surface(self.image)
        self.aggro = pygame.mixer.Sound('../assets/enemy/zombie/bogeyagro')

        # How big the world is, so we can check for boundries
        self.world_size = (Settings.width, Settings.height)
        
        # What sprites am I not allowd to cross?
        self.blocks = pygame.sprite.Group()
        self.hazards = None
        self.hazard_blocks = pygame.sprite.Group()

        # Which collision detection function?
        self.collide_function = pygame.sprite.collide_rect
        self.collisions = []
        self.collider = Drawable()
        self.collider.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.collider.rect = pygame.Rect((0, 0, 48, 48))

        self.test = Drawable()
        self.test.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.test.rect = self.image.get_rect()

        self.test1 = Drawable()
        self.test1.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.test1.rect = self.image.get_rect()

        self.test2 = Drawable()
        self.test2.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.test2.rect = self.image.get_rect()

        self.test3 = Drawable()
        self.test3.image = pygame.Surface([Settings.tile_size, Settings.tile_size])
        self.test3.rect = self.image.get_rect()

        self.tests = [self.test, self.test1, self.test2, self.test3]


        # SEED SET HERE MIGHT NEED TO CHANGE LATER
        seed(datetime.now())


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


    def move(self):
        # state machine -> updates self.dirx and self.diry (the direction of movement)
        self.x += self.move_speed * self.dirx
        self.y += self.move_speed * self.diry 

        # collision handling
        while len(self.collisions) != 0:
            # move in opposite x/y directions
            # will not be moved if direction if 0
            self.x -= self.dirx * 20
            self.y -= self.diry * 20 # move in opposite y direction

            self.update(0) # update to recheck collisions
            
            # set state to new direction
            self.state = 1
        return

    def chase(self):
        # when to stop chasing and give up back to patrolling
        if (self.sight_counter <= 0):
            self.move_speed = self.walk_speed
            self.state = 0
        
        # begin running instead of walking
        self.move_speed = self.run_speed
        self.aggro.play()
        tarx = self.x + self.move_speed * self.dirx
        tary = self.y + self.move_speed * self.diry
        # temporary direction values, will be changed if there is a potential collision
        dirx = self.dirx; diry = self.diry;

        self.collider.x = tarx; self.collider.y = tary;
        if pygame.sprite.spritecollideany(self.collider, self.blocks) != None:
            if self.dirx < self.diry:
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
                self.move()
            # new direction state
            elif self.state == 1:
                self.new_direction()
            # chase state
            elif self.state == 2:
                self.chase()
       

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
