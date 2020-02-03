#!/usr/bin/env python3

import pygame
import sys
sys.path.append('..')
import league
from player import Player
from overlay import Overlay 

from mapRenderer import MapRenderer
"""This file is garbage. It was a hastily coded mockup
to demonstrate how to use the engine.  We will be creating
a Game class that organizes this code better (and is
reusable).
"""

# Function to call when colliding with zombie

def main():
    e = league.Engine("Survive")
    e.init_pygame()
    p = Player(2, 400, 300)
    renderer = MapRenderer("first floor", e, p)
    renderer.renderMap()
    o = Overlay(p)
     q = Player(10, 100, 100)
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(o)
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)
    
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
