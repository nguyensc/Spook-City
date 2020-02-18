import pygame
import league
from mapRenderer import MapRenderer

def main(self, player = None, engine = None, overlay = None):

    self.player = player
    self.engine = engine
    self.overlay = overlay

    
    map = MapRenderer("second floor", self.engine)
    map.renderBackground()
    d = Door(2, 300, 4, engine)
    engine.objects.append(d)
    player.interactables.add(d)
    engine.drawables.add(d)


    map.renderForeGround()