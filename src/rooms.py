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
        self.current_room = 1


    def room1(self):
        m = MapRenderer("first room", self.engine)
        m.renderBackground()
        self.current_room = 1
        self.player.resetx = 300
        self.player.resety = 416
       
        # set up doors
        d = Door(2, 300, 4, 300, 416, "second room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)

        # set up enemy and lootable container
        self.spawner.createEnemy(2,128,128)
        self.crate.createLanternContainer(2,160,340)
        self.crate.createBeartrapContainer(2,256,300)
    
        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)


    def room2(self):
        m = MapRenderer("second room", self.engine)
        m.renderBackground()
        self.current_room = 2
        self.player.resetx = 300
        self.player.resety = 416

        
        # set up doors
        d = Door(2, 300, 432, 300, 16, "third room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)

        # set up container and enemy
        self.crate.createLanternContainer(2,387,328)
        self.crate.createBeartrapContainer(2,330,332)
        self.spawner.createEnemy(2,386,183)
        self.spawner.createEnemy(2,60,71)

        # door to next room
        d2 = Door(2,61,189,413,65,"third room", self.engine)
        print("changing room")
        self.engine.drawables.add(d2)
        self.engine.objects.append(d2)
        self.player.interactables.add(d2)
        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)

    def room3(self):
        m = MapRenderer("third room", self.engine)
        m.renderBackground()
        self.current_room = 3

        
        # set up doors
        d = Door(2, 413, 65, 300, 16, "second room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)

        # set up container and enemy
        self.spawner.createAbbot(2,82,399)
        self.crate.createBeartrapContainer(2,200,70)

        d2 = Door(2,300,300,52,56,"fourth room", self.engine)
        self.engine.drawables.add(d2)
        self.engine.objects.append(d2)
        self.player.interactables.add(d2)
        
        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)
    
    def room4(self):
        m = MapRenderer("fourth room", self.engine)
        m.renderBackground()
        self.current_room = 4

        
        # set up doors
        d = Door(2, 52, 56, 300, 16, "third", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)

        # set up container and enemy
        self.crate.createRancidMeatContainer(2,234,66)
        self.spawner.createAbbot(2,352,376)


        d2 = Door(2,17,195,50,416,"fifth room", self.engine)
        self.engine.drawables.add(d2)
        self.engine.objects.append(d2)
        self.player.interactables.add(d2)
        
        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)
    
    def room5(self):
        m = MapRenderer("fifth room", self.engine)
        m.renderBackground()
        self.current_room = 5

        
        # set up doors
        d = Door(2, 50, 416, 17, 195, "fourth room", self.engine)
        self.engine.objects.append(d)
        self.player.interactables.add(d)
        self.engine.drawables.add(d)

        # set up container and enemy
        self.crate.createBeartrapContainer(2,259,334)
        self.spawner.createSpooks(2,226,130)

        
        m.renderForeGround()

        # add all impassable sprites to classes which need them
        for impassable in m.getAllImpassables():
            self.player.blocks.add(impassable)