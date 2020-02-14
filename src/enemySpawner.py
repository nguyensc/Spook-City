# The goal for this file is to extract the logic for spawning enemies into a more basic function
# We need coordinates of the spawn for maps, some variable that describes how far the player is in the game, engine, and player
# That will be in the constructor, the main method of this file returns a new enemy that's attached to the game
import league
from player import Player
from enemy import Enemy
class EnemySpawner() :
    def __init__ (self, coordX, coordY, progress, engine, player, blocks) :
        self.X = coordX
        self.y = coordY
        self.state = progress
        self.e = engine
        self.p = player
        self.blocks = blocks
        
        def spawnEnemy(coordX, coordY, player, state):
            return Enemy(coordX, coordY, player)

        def createEnemy(self):
            temp = Enemy(z=2, x=coordX, y=coordY, player=player)
            #temp = spawnEnemy(coordX,coordY,player,progress)
            engine.drawables.add(temp)
            engine.objects.append(temp)
            player.enemy = temp
            temp.hazards = player.hazards
            temp.blocks.add(blocks)

        self.e.makeZombie = createEnemy

    
