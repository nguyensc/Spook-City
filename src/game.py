#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay
from light import Light
from flashlight import Flashlight

"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie

def main():
    e = league.Engine("Survive")
    e.init_pygame()
    floor = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 16, 8)
    walls = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 16, 23)
    floorLayer = league.Tilemap('../assets/map assets/level 1/floors.lvl', floor, layer = 1)
    wallLayer = league.Tilemap('../assets/map assets/level 1/walls.lvl', walls, layer = 1)
    b = league.Tilemap('../assets/map assets/level 1/background.lvl', floor, layer = 1)
    world_size = (floorLayer.wide*league.Settings.tile_size, floorLayer.high *league.Settings.tile_size)
    e.drawables.add(floorLayer.passable.sprites())
    e.drawables.add(wallLayer.passable.sprites())
    e.drawables.add(b.passable.sprites()) 
    p = Player(1, 400, 300)
    l = Light(200, 500, 1, p)
    f = Flashlight(200, 500, 1, p)
    q = Player(2, 300, 400)
    o = Overlay(p)
    p.world_size = world_size
    p.rect = p.image.get_rect()
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.objects.append(l)
    e.objects.append(f)
    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(o)
    e.drawables.add(l)
    e.drawables.add(f)
    c = league.LessDumbCamera(720, 720, p, e.drawables, world_size)
    e.objects.append(c)
    e.objects.append(o)

    e.collisions[p] = (q, p.ouch) 
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.events[pygame.USEREVENT + 1] = q.move_right
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()
