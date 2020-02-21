import pygame
import league
from mapRenderer import MapRenderer
from door import Door
from container import Container
from bogey import Bogey

class Room:
    def __init__(self, player = None, engine = None, overlay = None):
        self.player = player
        self.engine = engine
        self.overlay = overlay    


    def room1(self):
        m = MapRenderer("first room", self.engine)
        m.renderBackground()
       
        # set up doors
        d = Door(2, 300, 4, 300, 416, "second room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)
        # set up lootable containers
        containers = [
            Container(2, 100, 16, "lantern"),
            Container(2, 364, 16, "beartrap"),
            Container(2, 316, 264, "rancidmeat")
            ]
        for container in containers:
            self.engine.objects.append(container)
            self.player.interactables.add(container)
            self.engine.drawables.add(container)

        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)


    def room2(self):
        m = MapRenderer("second room", self.engine)
        m.renderBackground()
        
        # set up doors
        d = Door(2, 300, 432, 300, 16, "first room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)
        # set up lootable containers
        containers = [
            Container(2, 100, 16, "lantern"),
            Container(2, 316, 264, "beartrap")
            ]
        for container in containers:
            self.engine.objects.append(container)
            self.player.interactables.add(container)
            self.engine.drawables.add(container)
        # set up enemies
        b = Bogey(2, 100, 150, self.player)
        self.engine.objects.append(b)
        self.player.enemies.add(b)
        self.engine.drawables.add(b)

        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)