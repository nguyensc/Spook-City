from .settings import *
from .engine import *
from .game_objects import *

import csv
import math
import os
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
import league

class Camera(UGameObject):
    def __init__(self, width, height, center_on, drawables, world_size):
        self.width = width
        self.height = height
        self.center_on = center_on
        self.drawables = drawables
        self.x = self.center_on.x
        self.y = self.center_on.y
        self.world_size = world_size

    def update(self, deltaTime):
        pass

class DumbCamera(Camera):
    def update(self, time):
        self.x = self.center_on.x
        self.y = self.center_on.y
        offset_x = - (self.x - (self.width // 2))
        offset_y = - (self.y - (self.height // 2))
        
        for d in self.drawables:
            d.rect.x = d.x + offset_x
            d.rect.y = d.y + offset_y

class LessDumbCamera(Camera):
    def update(self, time):
        if self.center_on.x - self.width // 2 > 0 and self.center_on.x + self.width // 2 < self.world_size[0] - Settings.tile_size:
            self.x = self.center_on.x
        if self.center_on.y - self.height // 2 > 0 and self.center_on.y + self.height // 2 < self.world_size[1] - Settings.tile_size:
            self.y = self.center_on.yls
        offset_x = - (self.x - (self.width // 2))
        offset_y = - (self.y - (self.height // 2))
        
        for d in self.drawables:
            if hasattr(d, 'static'):
                continue
            d.rect.x = d.x + offset_x
            d.rect.y = d.y + offset_y

class Tilemap:
    """An object that represents an MxN list of tiles.  Give x, y
    returns various pieces of information about that tile, such as
    the image to draw, etc.

    Fields:
    path - A path to the file that holds the tilemap data.  Structure described below.
    spritesheet - The spritesheet from which to get the images for the tiles.
    tile_size - The number of pixels wide and high (we are forcing squares) per tile.
    wide - The number of tiles wide the map holds.
    high - The number of tiles vertically the map holds.
    world - The MxN list of tile numbers.
    sprites - The sprites for drawing the world.

    File structure:
    A tilemap file begins with the width (an integer) of the map (in tiles, not pixels), a newline,
    the height (an integer; again in tiles, not pixels), followed by a comma-separated list of lists
    of integers that represent the sprite number from the spritesheet.  For instance,

    5
    7
    1, 1, 1, 1, 2, 1, 1
    1, 1, 1, 1, 2, 1, 1
    1, 1, 1, 2, 1, 2, 1
    1, 1, 1, 2, 1, 2, 2
    2, 2, 2, 2, 1, 2, 2
    """
    def __init__(self, path, spritesheet, tile_size = Settings.tile_size, layer = 0):
        self.path = path
        self.spritesheet = spritesheet
        self.tile_size = tile_size
        self.layer = layer
        self.world = []
        self.passable = pygame.sprite.Group()
        self.impassable = pygame.sprite.Group()
        self.__parse()

    def __parse(self):
        """This function begins the process of (attempting) to
        parse a level file.  The structure of the file is described above.
        """
        #default image for replacing tiles with blank images
        defaultImg = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 16, 1)
        
        with open(self.path, 'r') as f:
            reader = csv.reader(f)
            contents = list(reader)
        # How many tiles wide is our world?
        self.wide = int(contents[0][0])
        # And how tall?
        self.high = int(contents[1][0])
        # Sprite numbers for all tiles are in the
        # multidimensional list "world".
        self.world = contents[2:]
        a = 0

        skipVal = 555

        for i in self.world:
            b = 0
            for j in i:
                x = b * self.spritesheet.tile_size
                y = a * self.spritesheet.tile_size
                num = int(j)
                    
                if (num == skipVal):
                    base_sprite = defaultImg.sprites[25]
                else:
                    if num < 0:
                        base_sprite = self.spritesheet.sprites[abs(num)]
                    else:
                        base_sprite = self.spritesheet.sprites[num]
                
                sprite = Drawable(self.layer)
                sprite.image = base_sprite.image

                # Set rectangle coords (using top-left coords here)
                rect = sprite.image.get_rect() 
                rect.x = x
                rect.y = y
                sprite.x = x
                sprite.y = y
                sprite.rect = rect
                if num < 0:
                    self.impassable.add(sprite)
                else:
                    self.passable.add(sprite)
                b = b + 1
            a = a + 1

class Spritesheet:
    """An object that represents a spritesheet and provides
    methods to access individual sprites from it.

    There are better ways to create spritesheets.  This code does
    not allow for packed sprites for instance.  Instead, it forces
    sprites to be in nice, tiled squares.

    Fields:
    path - The path to the spritesheet file.
    tile_size - The number of pixels wide and high the sprites are.  We are forcing square tiles for this engine.
    per_row - The number of sprites per row on the spritesheet.
    width - Number of pixels wide of the spritesheet image.
    height - Number of pixels high of the spritesheet image.
    sprites - A single-dimensional list of the sprites from the sheet.
    """
    def __init__(self, path, tile_size, per_row):
        self.path = path
        self.sheet = pygame.image.load(self.path).convert_alpha()
        self.tile_size = tile_size
        self.per_row = per_row
        self.width, self.height = self.sheet.get_size()
        self.sprites = self.__split_up()

    def __split_up(self):
        # This function splits the sheet up into equal-sized chunks,
        # and returns a list of the chunks.
        sprites = []
        for i in range((self.width * self.height) // (Settings.tile_size * Settings.tile_size)):
                image = self.__get_image_num(i)
                sprites.append(image)
        return sprites

    def __get_image_num(self, num):
        # This function copies an MxM image from x, y
        # to a new Sprite and returns it.
        y = self.tile_size * (num  // self.per_row)
        x = self.tile_size * (num  % self.per_row)
        sprite = Drawable()
        sprite.image = pygame.Surface((self.tile_size, self.tile_size)).convert_alpha()
        sprite.image.fill((128,128,128,0))
        sprite.image.blit(self.sheet, (0, 0), (x, y, x + self.tile_size, y + self.tile_size))
        return sprite

class Spritesheet_Ext:
    """An object that represents a spritesheet and provides
    methods to access individual sprites from it.

    There are better ways to create spritesheets.  This code does
    not allow for packed sprites for instance.  Instead, it forces
    sprites to be in nice, tiled squares.

    Fields:
    path - The path to the spritesheet file.
    tile_size - The number of pixels wide and high the sprites are.  We are forcing square tiles for this engine.
    per_row - The number of sprites per row on the spritesheet.
    width - Number of pixels wide of the spritesheet image.
    height - Number of pixels high of the spritesheet image.
    sprites - A single-dimensional list of the sprites from the sheet.
    """
    def __init__(self, path, tile_width, tile_height, per_row, paddingX = 0, paddingY = 0, scaleResolution = [-1, -1], scale = 1):
        self.path = path

        if scaleResolution != [-1, -1]:
            image = pygame.image.load(self.path)
            image = pygame.transform.scale(image, (scaleResolution[0], scaleResolution[1]))
        else:
            image = pygame.image.load(self.path)
            
        self.sheet = image.convert_alpha()
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.per_row = per_row
        self.width, self.height = self.sheet.get_size()
        self.paddingX = paddingX
        self.paddingY = paddingY
        self.scale = scale
        self.scaleResolution = scaleResolution
        self.sprites = self.__split_up()

    def __split_up(self):
        # This function splits the sheet up into equal-sized chunks,
        # and returns a list of the chunks.
        sprites = []
        for i in range((self.tile_width * self.tile_height) // int((self.scale * (Settings.tile_size * Settings.tile_size)))):
                image = self.__get_image_num(i)
                sprites.append(image)
        return sprites

    def __get_image_num(self, num):
        # This function copies an MxM image from x, y
        # to a new Sprite and returns it.
        y = (self.tile_height * (num  // self.per_row)) + self.paddingY
        x = (self.tile_width * (num  % self.per_row)) + self.paddingX
        sprite = Drawable()
        sprite.image = pygame.Surface((self.tile_width, self.tile_height)).convert_alpha()
        sprite.image.fill((128,128,128,0))
        sprite.image.blit(self.sheet, (0, 0), (x, y, x + self.tile_width, y + self.tile_height))
        return sprite