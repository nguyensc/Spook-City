import pygame
import league
from mapRenderer import MapRenderer
from door import Door
from interactables.createInteract import createInteract
from enemies.enemySpawner import EnemySpawner

class Room:
    def __init__(self, player = None, engine = None, overlay = None):
        self.player = player
        self.engine = engine
        self.overlay = overlay
        self.crate = createInteract(engine, player)
        self.spawner = EnemySpawner(engine,player)


    def room1(self):
        m = MapRenderer("first room", self.engine)
        m.renderBackground()
       
        # set up doors
        d = Door(2, 300, 4, 300, 416, "second room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)
        # set up lootable containers
        self.crate.createBeartrapContainer(2,100,16)
        self.crate.createLanternContainer(2,364,16)
        self.crate.createRandcidMeatContaier(2,316,264)
    
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
        self.crate.createLanternContainer(2,100,16)
        self.crate.createBeartrapContainer(2,316,264)
        # set up enemies
        self.spawner.createEnemy(2,100,200)

        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)