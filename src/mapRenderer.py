import league
import pygame
from tmxloader import TiledRenderer


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

        selector = mapDict[currMap]

        if (selector == 1) {
            e.
        }
        else if (selector == 2) {

        }
        else if (selector == 3) {
            
        }
        else if (selector == 4) {
            
        }
        else if (selector == 5) {
            
        }
        else if (selector == 6) {
            
        }
        else {

        }