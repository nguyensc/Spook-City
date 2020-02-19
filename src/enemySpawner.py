# The goal for this file is to extract the logic for spawning enemies into a more basic function
# We need coordinates of the spawn for maps, some variable that describes how far the player is in the game, engine, and player
# That will be in the constructor, the main method of this file returns a new enemy that's attached to the game
import league
from player import Player
from enemy import Enemy
from gremlin import gremlin
class EnemySpawner:
    def __init__ (self, coordX, coordY, progress, engine, player, blocks) :
        self.x = coordX
        self.y = coordY
        self.state = progress
        self.e = engine
        self.p = player
        self.blocks = blocks
        
    def spawnEnemy(self, coordX, coordY, player, state):
        return Enemy(coordX, coordY, player)

    def createEnemy(self):
        self.temp = Enemy(2, self.x, self.y, self.p)
        self.e.drawables.add(self.temp)
        self.e.objects.append(self.temp)
        self.p.enemies.add(self.temp)
        self.temp.hazards = self.p.hazards
        self.temp.blocks.add(self.blocks)

    def createGremlin(self, creator):
        self.temp = gremlin(2, self.x, self.y, self.p, creator)
        self.e.drawables.add(self.temp)
        self.e.objects.append(self.temp)
        self.p.enemies.add(self.temp)
        self.temp.hazards = self.p.hazards
        self.temp.blocks.add(self.blocks)

        

    
