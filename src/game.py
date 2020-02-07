import pygame
import sys
sys.path.append('..')
import league
from player import Player
from enemy import Enemy
from overlay import Overlay 
from mapRenderer import MapRenderer
from light import Light
from flashlight import Flashlight
from overlay import Overlay

def main() :
    e = league.Engine("Survive")
    e.init_pygame()
    timer = pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    count = 0
    p = Player(1, 400, 300)
    mapRenderer = MapRenderer("first floor", e)
    world_size = mapRenderer.renderBackground()
    p.world_size = world_size

    l = Light(20, 0, 0, p)
    f = Flashlight(200, 500, 2, p)
    e.flashlight = f
    e.light_source = l

    o = Overlay(p)

    p.rect = p.image.get_rect()

    enemy = Enemy(2, 100, 100)
    p.enemy = enemy

    e.objects.append(p)
    e.objects.append(enemy)
    e.objects.append(l)
    e.objects.append(f)
   
    p.enemy = enemy

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

    e.drawables.add(p)
    e.drawables.add(enemy)
    e.drawables.add(l)
    e.drawables.add(f)

    mapRenderer.renderForeGround()

    c = league.LessDumbCamera(720, 720, p, e.drawables, world_size)
    e.objects.append(c)
    #e.collisions[p] = (q, p.ouch)
  
    # draws the flashlight collision rectangle
    e.nospriteables.append((f, (255, 0, 0, 255)))

    # add all impassable sprites to classes which need them
    for impassable in mapRenderer.getAllImpassables():
        p.blocks.add(impassable)
        enemy.blocks.add(impassable)

    pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()
