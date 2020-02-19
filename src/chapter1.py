import pygame
import league
from mapRenderer import MapRenderer

def main(self, player = None, engine = None, overlay = None):

    self.player = player
    self.engine = engine
    self.overlay = overlay

    
    map = MapRenderer("second floor", self.engine)
    map.renderBackground()

    self.engine.light_points = self.player.raycast_points
    self.engine.drawables.add(self.player)
    self.engine.objects.append(self.player)
    self.engine.objects.append(self.overlay)

    map.renderForeGround()

    return None