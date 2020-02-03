import league
import pygame


class MapParams():
    def __init__(self, floorTS, floorWidth, floorLayer, wallsTS,
                 wallWidth, wallLayer, decorationTS, decorationWidth,
                 decorationLayer, decoration2Ts, decoration2Width,
                 decoration2Layer, doorsTS, doorsWidth, doorLayer,
                 elevatorTS, elevatorWidth, elevatorLayer):

        self.elevatorTS = [elevatorTS, elevatorWidth]
        self.doorsTS = [doorsTS, doorsWidth]
        self.decoration2Ts = [decoration2Ts, decoration2Width]
        self.decorationTs = [decorationTS, decorationWidth]
        self.wallsTS = [wallsTS, wallWidth]
        self.floorTS = [floorTS, floorWidth]
        self.map = map


class MapRenderer():
    def __init__(self, mapName, engine, player):
        self.engine = engine
        self.mapName = mapName
        self.player = player

    def renderMap(self):

        mapDict = {
            "first floor": 1,
            "second floor": 2
        }

        currMap = mapDict.get(self.mapName)

        switcher = {
            1: MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 23, '../assets/map assets/level 1/walls.lvl'

            ),
            2: MapParams(
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl',
                '../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 8, '../assets/map assets/level 1/floors.lvl'
            )
        }

        selectedMap = switcher.get(currMap)

        for i in range(0,5):
            pos = i * 3
            sprites = league.Spritesheet(selectedMap[pos], 16, selectedMap[pos + 1])
            layer = league.Tilemap(selectedMap[pos + 2], sprites, layer = i)
            self.engine.drawables.add(layer.passable.sprites())
            self.player.blocks.add(layer.impassable)
            
            if (i == 0):
                worldSize = (layer.wide * league.Settings.tile_size, layer.high * league.Settings.tile_size)
                self.player.worldSize = worldSize
                self.player.image.get._rect()
            
