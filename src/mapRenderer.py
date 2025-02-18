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
        self.all_impassables = []  # needed for collisions currently - xam

        mapDict = {
            "first room": 1,
            "second room": 2,
            "third room": 3,
            "fourth room": 4,
            "fifth room": 5
        }

        selector = mapDict.get(self.mapName)

        if selector == 1:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 1/decoration 1.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 1/decoration 2.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/ceiling.lvl')

        if selector == 2:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 2/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 2/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 2/decoration 1.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 2/decoration 2.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 2/ceiling.lvl')

        if selector == 3:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 3/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 3/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 3/decoration 1.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 3/decoration 2.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 3/ceiling.lvl')

        if selector == 4:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 4/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 4/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 4/decoration 1.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 4/decoration 2.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 4/ceiling.lvl')

        if selector == 5:
            self.map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 5/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 5/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 5/decoration 1.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileB_PHC_Interior-Hospital.png', 16, '../assets/map assets/level 5/decoration 2.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 5/ceiling.lvl')

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

        self.engine.mapDrawables.add(floorLayer.passable.sprites())
        self.engine.mapDrawables.add(wallLayer.impassable.sprites())
        self.engine.mapDrawables.add(decoLayer.impassable.sprites())
        self.engine.mapDrawables.add(deco2Layer.impassable.sprites())

        # list of all impassable objects that are only used in game.py for collisions

        return world_size

    def renderForeGround(self):
        ceiling = league.Spritesheet(
            self.map.ceiling[0], 16, self.map.ceiling[1])
        ceilingLayer = league.Tilemap(self.map.ceiling[2], ceiling, layer=4)

        self.engine.mapDrawables.add(ceilingLayer.impassable.sprites())
        self.all_impassables.append(ceilingLayer.impassable.sprites())
