#!/usr/bin/env python3
import pygame
import sys
sys.path.append('..')
import league
from player import Player
from enemy import Enemy
from overlay import Overlay

def main():
    e = league.Engine("Sigrid's Quest")
    e.init_pygame()

    sprites = league.Spritesheet('./assets/base_chip_pipo.png', league.Settings.tile_size, 8)
    t = league.Tilemap('./assets/world.lvl', sprites, layer = 1)
    b = league.Tilemap('./assets/background.lvl', sprites, layer = 0)

    world_size = (t.wide*league.Settings.tile_size, t.high *league.Settings.tile_size)
    e.drawables.add(t.passable.sprites())
    e.drawables.add(b.passable.sprites()) 

    enemy = Enemy(2, 100, 100)
    enemy.blocks.add(t.impassable)

    p = Player(2, 400, 300, enemy)
    p.blocks.add(t.impassable)
    p.world_size = world_size
    p.rect = p.image.get_rect()

    o = Overlay(p, e.screen)
    c = league.LessDumbCamera(800, 600, p, e.drawables, world_size, e.nospriteables)
    #c = league.DumbCamera(800, 600, p, e.drawables, world_size)

    e.drawables.add(p)
    e.drawables.add(p.collider)
    e.drawables.add(enemy)
    e.drawables.add(enemy.collider)
    e.drawables.add(o)

    # projectiles pre-added
    e.projectiles = p.bullets

    # extra rects to draw debug only ! (for now)
    e.extra_rect_drawables.append((p.rect, (255, 0, 0)))
    e.extra_rect_drawables.append((p.collider.rect, (0, 255, 0)))
    e.extra_rect_drawables.append((enemy.rect, (0, 0, 255)))

    for test in enemy.tests:
        e.drawables.add(test)
        e.extra_rect_drawables.append((test.rect, (255, 0, 255)))

    e.extra_rect_drawables.append(((p.x, p.y, 32, 32), (200, 255, 150)))
    
    e.objects.append(enemy)
    e.objects.append(c)
    e.objects.append(o)
    e.objects.append(p)

    #e.collisions[p] = (enemy, p.ouch) 
    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    
    # player input set up
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.key_events[pygame.K_UP] = p.shoot_bullet_up
    '''
    e.key_events[pygame.K_DOWN] = p.shoot_bullet_down
    e.key_events[pygame.K_RIGHT] = p.shoot_bullet_right
    e.key_events[pygame.K_LEFT] = p.shoot_bullet_left '''

    e.events[pygame.QUIT] = e.stop # elegant quit

    e.run() # begin game loop

if __name__=='__main__':
    main()
