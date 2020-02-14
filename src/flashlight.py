import pygame
from league import *

class Flashlight(DUGameObject):
    def __init__(self, z=0, x=0, y=0, target=None):
        super().__init__(z,x,y)
        self.delta = 512
        self.target = target
        self.x = target.x
        self.y = target.y
        self.scale = int(256 / 64)

        self.pic = pygame.image.load("../assets/light assets/RadialTrapezoid.png").convert_alpha()
        self.pic.fill((255, 255, 255, 255),None, pygame.BLEND_RGBA_MULT)
        self.pic = pygame.transform.scale(self.pic, (128, 64))

        self.originalWidth = self.pic.get_width()
        self.width = self.originalWidth 
        self.currentWidth = self.width

        self.image = pygame.Surface([self.originalWidth , self.pic.get_height()]).convert_alpha()

        
        self.rect = self.image.get_rect(center=(target.x, target.y))
        self.rect.x = self.width
        self.mask = pygame.mask.from_surface(self.image)
    
        self.collide = Drawable()
        self.collide.image = pygame.Surface([self.originalWidth , self.image.get_height()])
        self.collide.rect = self.pic.get_rect() 

        self.world_size = (Settings.width, Settings.height)
        self.blocks = pygame.sprite.Group()


    def lineOfSight(self, length = 0):
        xx = int(self.rect.x)
        yy = int(self.rect.y)
        n_position = (xx - length, yy)
        for i in range(length):
            self.collide.x = self.collide.rect.x = xx
            self.collide.y = self.collide.rect.y = yy

            if(pygame.sprite.spritecollideany(self.collide, self.blocks) != None):
                n_position = (xx,yy)
                break
            xx -= 1
        return n_position
    

    def check_collision(self):
        target_face = 0
        collision_width = 0
        collision_occurred_flag = 0

        wallx = 0
        overlap = 0
        newWidth = self.originalWidth

        if(pygame.sprite.collide_mask(self, self.target.enemy)):
            overlap_mask = self.mask.overlap_mask(self.target.enemy.mask, (0,0))
            print("collide")


        for sprite in self.blocks:
            self.collide.rect.x = sprite.x
            self.collide.rect.y = sprite.y

            if pygame.sprite.collide_rect(self, self.collide):
                wallx = sprite.x
                overlap = self.originalWidth - (self.x - wallx)
                break
        
        newWidth = self.originalWidth - overlap
        self.width = abs(newWidth)


    def update(self, time):
        self.x = self.target.x + 20
        self.y = self.target.y - 10

        self.y += 16

        self.rect.x = self.x
        self.rect.y = self.y
        self.rect.width = self.originalWidth


        # a collision safety buffer, don't want collisions to begin too soon
        if pygame.time.get_ticks() > 1000:
            self.check_collision()

        self.pic = pygame.transform.scale(self.pic, (128, 64))
        self.image = pygame.Surface([1000, self.pic.get_height()]).convert_alpha()
        self.image.fill((0,0,0,0))

        self.collide.rect.width = self.width
        self.collide.width = self.width

        self.image.blit(self.pic, (0, 0), area=(0, 0, self.width, self.pic.get_height()))