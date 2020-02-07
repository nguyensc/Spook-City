import pygame
import sys
sys.path.append('..')
import league
from player import Player
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
    q = Player(2, 300, 400)
    o = Overlay(p)
    p.rect = p.image.get_rect()
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.objects.append(l)
    e.objects.append(f)
   

    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(l)
    e.drawables.add(f)
    mapRenderer.renderForeGround()
    c = league.LessDumbCamera(720, 720, p, e.drawables, world_size)
    e.objects.append(c)
    e.light_source = l
    e.collisions[p] = (q, p.ouch)
  
    e.nospriteables.append((f, (255, 0, 0, 255)))

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