import pygame
import sys
sys.path.append('..')
import league
from player import Player
from mapRenderer import MapRenderer
from overlay import Overlay
from enemies.enemySpawner import EnemySpawner
from interactables.createInteract import createInteract
from door import Door
from rooms import Room
from audio import BackgroundMusic

def main() :
    e = league.Engine("Spook City")
    e.init_pygame()
    timer = pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    count = 0

    p = Player(1, 400, 300)
    spawner = EnemySpawner(e,p)
    crate = createInteract(e,p)

    spawner.createEnemy(2,128,128)
    crate.createLanternContainer(2,128,300)
    crate.createBeartrapContainer(2,256,300)

    mapRenderer = MapRenderer("first room", e)
    world_size = mapRenderer.renderBackground()
    p.world_size = world_size
    mapRenderer.renderForeGround()
    d = Door(2, 300, 4, 300, 416, "second room", e)
    e.light_points = p.raycast_points
    e.player = p
    overlay = Overlay(p)
    e.overlay = overlay
    e.objects.append(p)
    e.objects.append(overlay)
    e.objects.append(d)

    # any objects to be created on the fly
    p.items = e.dynamic_instances
    p.interactables.add(d)

    # add all drawables
    e.drawables.add(p)
    e.drawables.add(d)
    mapRenderer.renderForeGround()

    p.resetx = 300
    p.resety = 416

    bgm = BackgroundMusic("lavender town")
    bgm.start_music()
  
    # add all impassable sprites to classes which need them
    for impassable in mapRenderer.getAllImpassables():
        p.blocks.add(impassable)

    # create room object in engine
    e.room = Room(p, e, overlay)
    p.room = e.room

    e.key_events[pygame.K_a] = p.move_left
    e.key_events[pygame.K_d] = p.move_right
    e.key_events[pygame.K_w] = p.move_up
    e.key_events[pygame.K_s] = p.move_down
    e.key_events[pygame.K_e] = p.interact
    e.key_events[pygame.K_SPACE] = p.use_active_item
    e.key_events[pygame.K_ESCAPE] = e.stop
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()