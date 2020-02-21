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
        self.current_room = 1
        self.room_lanterns = {
            "1": [],
            "2": []
        }    

    def build_room(self, objects, enemies, map_renderer, room_number):
        map_renderer.renderBackground()
        
        # update room number, used with lanterns
        self.current_room = room_number
        # build all renderable objects, used with engine and others
        for o in objects:
            self.engine.objects.append(o)
            self.player.interactables.add(o)
            self.engine.drawables.add(o)
        # build all enemies
        for e in enemies:
            self.engine.objects.append(e)
            self.player.enemies.add(e)
            self.engine.drawables.add(e)
        # recreate lanterns for lantern persistance
        lanterns = self.room_lanterns[str(self.current_room)]
        self.player.lanterns = lanterns
        for lantern in lanterns:
            self.player.create_physical_item(0, 0, lantern)
        # add all impassable sprites to classes which need them
        for impassable in map_renderer.getAllImpassables():
            self.player.blocks.add(impassable)
        map_renderer.renderForeGround()



    def room1(self):
        m = MapRenderer("first room", self.engine)
        objects = []
        # set up doors
        d0 = Door(2, 300, 4, 300, 416, "second room", self.engine)
        # set up containers
        c0 = Container(2, 100, 16, "lantern")
        c1 = Container(2, 364, 16, "beartrap")
        c2 = Container(2, 316, 264, "rancidmeat")
        # add all the above set up objects into the array
        objects = [d0, c0, c1, c2]
        # set up enemies
        enemies = []
        # build room 1
        self.build_room(objects, enemies, m, 1)
        


    def room2(self):
        m = MapRenderer("second room", self.engine)
        objects = []     
        # set up doors
        d0 = Door(2, 300, 432, 300, 32, "first room", self.engine)
        # set up lootable containers
        c0 = Container(2, 100, 16, "lantern")
        c1 = Container(2, 316, 264, "beartrap")
        # add all the above set up objects into the array
        objects = [d0, c0, c1]
        # set up enemies
        e0 = Bogey(2, 100, 150, self.player)
        enemies = [e0]
        # build room 2
        self.build_room(objects, enemies, m, 2)