import league
import pygame


class MapParams():
    def __init__(self, floorTS, floorWidth, floorLayer, wallTS,
                 wallWidth, wallLayer, decorationTS, decorationWidth,
                 decorationLayer, decoration2Ts, decoration2Width,
                 decoration2Layer, ceilingTs, ceilingWidth, ceilingLayer):

        self.ceiling = [ceilingTs, ceilingWidth, ceilingLayer]
        self.decoration2 = [decoration2Ts, decoration2Width, decoration2Layer]
        self.decoration = [decorationTS, decorationWidth, decorationLayer]
        self.walls = [wallTS, wallWidth, wallLayer]
        self.floor = [floorTS, floorWidth, floorLayer]


class MapRenderer():
    def __init__(self, mapName, engine):
        self.engine = engine
        self.mapName = mapName
        self.all_impassables = [] # needed for collisions currently - xam

        mapDict = {
            "first floor": 1,
            "second floor": 2
        }

        selector = mapDict.get(self.mapName)

        if selector == 1:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        else:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')


    def getAllImpassables(self):
        # returns all impassable sprites, this function is only used in game.py -xam
        return self.all_impassables


    def renderBackground(self):
        floor = league.Spritesheet(self.map.floor[0], 16, self.map.floor[1])
        wall = league.Spritesheet(self.map.walls[0], 16, self.map.walls[1])
        decoration = league.Spritesheet(
            self.map.decoration[0], 16, self.map.decoration[1])
        decoration2 = league.Spritesheet(
            self.map.decoration2[0], 16, self.map.decoration2[1])

        floorLayer = league.Tilemap(self.map.floor[2], floor, layer=0)
        wallLayer = league.Tilemap(self.map.walls[2], wall, layer=1)
        decoLayer = league.Tilemap(self.map.decoration[2], decoration, layer=2)
        deco2Layer = league.Tilemap(
            self.map.decoration2[2], decoration2, layer=3)

        world_size = (floorLayer.wide*league.Settings.tile_size,
                      floorLayer.high * league.Settings.tile_size)

        self.engine.drawables.add(floorLayer.passable.sprites())
        self.engine.drawables.add(wallLayer.impassable.sprites())
        self.engine.drawables.add(decoLayer.impassable.sprites())
        self.engine.drawables.add(deco2Layer.impassable.sprites())

        # list of all impassable objects that are only used in game.py for collisions
        self.all_impassables.append(wallLayer.impassable.sprites())
        #self.all_impassables.append(decoLayer.impassable.sprites())
        #self.all_impassables.append(deco2Layer.impassable.sprites())

        return world_size


    def renderForeGround(self):
        ceiling = league.Spritesheet(self.map.ceiling[0], 16, self.map.ceiling[1])
        ceilingLayer = league.Tilemap(self.map.ceiling[2], ceiling, layer=4)
        self.engine.drawables.add(ceilingLayer.impassable.sprites())
