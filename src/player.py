from league import *
import pygame
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
        self.last_hit = pygame.time.get_ticks()
        self.delta = 512
        self.screen = None
        # Where the player is positioned
        self.x = x
        self.y = y
        self.camera = None
        
        self.sheet = Spritesheet('../assets/player/Black/player_idle.png', 48, 1)
        self.sprites = self.sheet.sprites
        self.image = self.sprites[0].image

        # timers
        self.shoot_timer = 20
        self.shoot_counter = self.shoot_timer
        self.spotted_timer = 30
        self.spotted_counter = self.spotted_timer

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


    def spotted_by_enemy(self, enemy, dirx, diry):
        enemy.state = 2; # enemy chase state is 2
        enemy.sight_counter = enemy.sight_timeout # reset the enemy chase timer
        enemy.target = self
        enemy.dirx = dirx # target x direction to move to
        enemy.diry = diry # target y direction to move to

        # increase heart rate and set counter for when to catch breath
        self.spotted_counter = self.spotted_timer  
        self.heart_rate = 3

        return


    def lineofsight_right(self, length):
        xx = int(self.rect.x); yy = int(self.rect.y);
        end_position = (xx + length, yy)

        for i in range(length):
            self.cpoint.x = self.cpoint.rect.x = xx
            self.cpoint.y = self.cpoint.rect.y = yy

            # line of sight runs into enemy
            if self.enemy.rect.collidepoint(xx, yy):
                self.spotted_by_enemy(self.enemy, -1, 0) # set enemy state
                end_position = (xx, yy)
                break
            # line of sight runs into wall
            elif pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (xx, yy)
                break
            xx += 16

        self.sight_coords[0] = end_position
        return end_position


    def lineofsight_left(self, length):
        xx = int(self.rect.x); yy = int(self.rect.y)
        end_position = (xx - length, yy)

        for i in range(length):
            self.cpoint.x = self.cpoint.rect.x = xx
            self.cpoint.y = self.cpoint.rect.y = yy

            # line of sight runs into enemy
            if self.enemy.rect.collidepoint(xx, yy):
                self.spotted_by_enemy(self.enemy, 1, 0) # set enemy state
                end_position = (xx, yy)
                break
            # line of sight runs into wall
            elif pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (xx, yy)
                break
            xx -= 16

        self.sight_coords[1] = end_position
        return end_position


    def lineofsight_up(self, length):
        xx = int(self.rect.x); yy = int(self.rect.y)

        end_position = (xx, yy - length)

        for i in range(length):
            self.cpoint.x = self.cpoint.rect.x = xx
            self.cpoint.y = self.cpoint.rect.y = yy

            # line of sight runs into enemy
            if self.enemy.rect.collidepoint(xx, yy):
                self.spotted_by_enemy(self.enemy, 0, 1) # set enemy state
                end_position = (xx, yy)
                break
            # line of sight runs into wall
            elif pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (xx, yy)
                break
            yy -= 8

        self.sight_coords[2] = end_position
        return end_position


    def lineofsight_down(self, length):
        xx = int(self.rect.x); yy = int(self.rect.y)
        end_position = (xx, yy + length)

        for i in range(length):
            self.cpoint.x = self.cpoint.rect.x = xx
            self.cpoint.y = self.cpoint.rect.y = yy

            # line of sight runs into enemy
            if self.enemy.rect.collidepoint(xx, yy):
                self.spotted_by_enemy(self.enemy, 0, -1) # set enemy state
                end_position = (xx, yy)
                break
            # line of sight runs into wall
            elif pygame.sprite.spritecollideany(self.cpoint, self.blocks) != None:
                end_position = (xx, yy)
                break
            yy += 8

        self.sight_coords[3] = end_position
        return end_position




    def spotted_by_enemy(self, enemy, dirx, diry):
        enemy.state = 2; # enemy chase state is 2
        enemy.sight_counter = enemy.sight_timeout # reset the enemy chase timer
        enemy.target = self
        enemy.dirx = dirx # target x direction to move to
        enemy.diry = diry # target y direction to move to

        # increase heart rate and set counter for when to catch breath
        self.spotted_counter = self.spotted_timer  
        self.heart_rate = 3

        return


    

    def update(self, time):      
        '''
        xx = self.x; yy = self.y;
        for i in range(100):
            self.cpoint.rect.x = xx; self.cpoint.rect.y = yy;
            xx-=1
            if self.enemy.rect.collide(self.cpoint.x, self.cpoint.y) != None:
                printd("hit")
                break '''
        if time != 0:
            self.shoot_counter -= 1
            self.spotted_counter -= 1
            if self.spotted_counter <= 0:
                self.heart_rate = 10

        
        self.lineofsight_right(400)
        self.lineofsight_left(400)
        self.lineofsight_up(200)
        self.lineofsight_down(200)
        

        self.collisions = []
        prevrect = (self.rect.x, self.rect.y)
        self.collider.x = self.collider.rect.x = self.rect.x = self.x;
        self.collider.y = self.collider.rect.y = self.rect.y = self.y;

        self.rect.x += 8; self.rect.y += 8;

        for sprite in self.blocks:
            self.collider.rect.x = sprite.x
            self.collider.rect.y = sprite.y
            if pygame.sprite.collide_rect(self, self.collider):
                self.collisions.append(sprite)
        
        #self.collider.x += 5; self.collider.y+= 5;
        #self.rect.x = prevrect[0]; self.rect.y = prevrect[1]
        
        #pygame.display.flip()

    def ouch(self):
        now = pygame.time.get_ticks()
        if now - self.last_hit > 1000:
            self.health = self.health - 10
            self.last_hit = now

    def getX(self):
        return self.x   
    def getY(self):
        return self.y
