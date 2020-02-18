import pygame
import league
from mapRenderer import MapRenderer

def main(self, player = None, engine = None, overlay = None):

    self.player = player
    self.engine = engine
    self.overlay = overlay

    
    map = MapRenderer("first floor", self.engine)
    map.renderBackground()
    map.renderForeGround()