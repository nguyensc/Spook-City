import league
import pygame

class MapParams():
    def __init__(self, floorTS, floorWidth, floorLayer, wallTS,
                 wallWidth, wallLayer, decorationTS, decorationWidth,
                 decorationLayer, decoration2Ts, decoration2Width,
                 decoration2Layer, doorsTS, doorsWidth, doorLayer,
                 elevatorTS, elevatorWidth, elevatorLayer):

        self.elevator = [elevatorTS, elevatorWidth, elevatorLayer]
        self.doors = [doorsTS, doorsWidth, doorLayer]
        self.decoration2 = [decoration2Ts, decoration2Width, decoration2Layer]
        self.decoration = [decorationTS, decorationWidth, decorationLayer]
        self.walls = [wallTS, wallWidth, wallLayer]
        self.floor = [floorTS, floorWidth, floorLayer]
        self.map = map


class MapRenderer():
    def __init__(self, mapName, engine):
        self.engine = engine
        self.mapName = mapName

    def renderMap(self):

        mapDict = {
            "first floor": 1,
            "second floor": 2
        }

        selector = mapDict.get(self.mapName)
        
        if selector == 1:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        if selector == 2:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        if selector == 3:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        if selector == 4:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        if selector == 5:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        if selector == 6:
            map = MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        else:
            map=MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl')

        floor = league.Spritesheet(map.floor[0], 16, map.floor[1])
        wall = league.Spritesheet(map.walls[0], 16, map.walls[1])
        decoration = league.Spritesheet(map.decoration[0], 16, map.decoration[1])
        decoration2 = league.Spritesheet(map.decoration2[0], 16, map.decoration2[1])
        doors = league.Spritesheet(map.doors[0], 16, map.doors[1])
        elevator = league.Spritesheet(map.elevator[0], 16, map.elevator[1])
        
        floorLayer = league.Tilemap(map.floor[2], floor, layer = 0)
        wallLayer = league.Tilemap(map.walls[2], wall, layer = 1)
        decoLayer = league.Tilemap(map.decoration[2], decoration, layer = 2)
        deco2Layer = league.Tilemap(map.decoration2[2], decoration2, layer = 3)
        doorLayer = league.Tilemap(map.doors[2], doors, layer = 4)
        elevatorLayer = league.Tilemap(map.elevator[2], elevator, layer = 5)
        
        world_size = (floorLayer.wide*league.Settings.tile_size, floorLayer.high *league.Settings.tile_size)

        self.engine.drawables.add(floorLayer.passable.sprites())
        self.engine.drawables.add(wallLayer.impassable.sprites())
        self.engine.drawables.add(decoLayer.impassable.sprites())
        self.engine.drawables.add(deco2Layer.impassable.sprites())
        self.engine.drawables.add(doorLayer.impassable.sprites())
        self.engine.drawables.add(elevatorLayer.impassable.sprites())
        return world_size
