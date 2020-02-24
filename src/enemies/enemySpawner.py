# The goal for this file is to extract the logic for spawning enemies into a more basic function
# We need coordinates of the spawn for maps, some variable that describes how far the player is in the game, engine, and player
# That will be in the constructor, the main method of this file returns a new enemy that's attached to the game
import league
from player import Player
from enemies.spooks import Spooks
from enemies.abbot import abbot
from enemies.enemy import Enemy
from enemies.gremlin import Gremlin

class EnemySpawner() :
    def __init__ (self, engine=None, player=None) :
        self.e = engine
        self.p = player
        self.blocks = player.blocks
    
    def createSpooks(self, z, x, y):
        temp = Spooks(z, x, y, self.p, self.e)
        temp.blocks = self.blocks
        temp.hazards = self.p.hazards
        self.p.enemies.add(temp)
        self.e.drawables.add(temp)
        self.e.objects.append(temp)

    def createAbbot(self, z, x, y):
        temp = abbot(z,x,y, self.p)
        temp.blocks = self.blocks
        temp.hazards = self.p.hazards
        self.p.enemies.add(temp)
        self.e.drawables.add(temp)
        self.e.objects.append(temp)

    def createEnemy(self, z,x,y):
        temp = Enemy(z,x,y,self.p)
        temp.blocks = self.blocks
        temp.hazards = self.p.hazards
        self.p.enemies.add(temp)
        self.e.drawables.add(temp)
        self.e.objects.append(temp)


    
