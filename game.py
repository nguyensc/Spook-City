#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay
from inventory import Inventory
from pickup import Pickup

"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

def getSpawnCoords(play):
    coords = play.getCoords()

    left = 16
    right = 656
    up = 16
    down = 656

    coordx = left   
    coordy = up

    xdiffLeft = abs(left - coords[0])
    xdiffRight = abs(right - coords[0])
    if(xdiffRight > xdiffLeft) :
        coordx = right
    ydiffUp = abs(up - coords[1])
    ydiffDown = abs(down - coords[1])
    if(ydiffDown > ydiffUp) :
        coordy = down

    return Player(2, coordx, coordy)

# Function to call when colliding with zombie

def main():
    e = league.Engine("Survive")
    e.init_pygame()
    floor = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 16, 8)
    walls = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 16, 23)
    floorLayer = league.Tilemap('../assets/map assets/level 1/floors.lvl', floor, layer = 1)
    wallLayer = league.Tilemap('../assets/map assets/level 1/walls.lvl', walls, layer = 2)
    b = league.Tilemap('../assets/map assets/level 1/background.lvl', floor, layer = 0)
    world_size = (floorLayer.wide*league.Settings.tile_size, floorLayer.high *league.Settings.tile_size)
    e.drawables.add(floorLayer.passable.sprites())
    e.drawables.add(wallLayer.passable.sprites())
    e.drawables.add(b.passable.sprites())  

    p = Player(2, 200, 200)

    o = Overlay(p)
    

    p.blocks.add(floorLayer.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()

    q = Player(10, 100, 100)
    q.image = p.image
    key = Pickup(2, 300, 300, p)
    
    i = Inventory(p, key)
    
    e.objects.append(p)
    e.objects.append(q)
    e.objects.append(key)

    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(o)
    e.drawables.add(i)
    e.drawables.add(key)

    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    c = league.DumbCamera(800, 600, p, e.drawables, world_size)
    
    e.objects.append(c)
    e.objects.append(o)
    e.objects.append(i)

    e.collisions[p] = (q, p.ouch)
    e.collisions[key] = (p, key.pickedUp) 

    e.zombie = getSpawnCoords(p)
    def createEnemy(self):
        temp = getSpawnCoords(p)
        temp.image = p.image
        e.drawables.add(temp)
        e.objects.append(temp)
        e.objects.append(c)

    e.makeZombie = createEnemy


    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    pygame.time.set_timer(pygame.USEREVENT, 1000 // league.Settings.gameTimeFactor)
    
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down

    #e.events[pygame.USEREVENT] = i.update
    #e.key_events[pygame.K_f] = e.makeZombie
    #e.key_events[pygame.K_f] = p.addKey

    e.events[pygame.USEREVENT + 1] = q.move_right
    
    e.events[pygame.QUIT] = e.stop 
    #add an event to spawn in a new monster every userevent then
     # change the location of the monster each time then
     # change the location based on where the player is then
     # add a spawn if a previous monster dies, which will require it's own event
     # add a spawn when the key is picked up
    e.run()

if __name__=='__main__':
    main()


