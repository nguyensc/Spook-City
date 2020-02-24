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
    e = league.Engine("Survive")
    e.init_pygame()
    timer = pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    count = 0

    p = Player(1, 240, 300)
    
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

    # creation of enemies
    spawner = EnemySpawner(e,p)

    # crate spawner
    crate = createInteract(e,p)

    spawner.createSpooks(2,100,120)
    crate.createBeartrapContainer(2,250,300)
    
  

    # any objects to be created on the fly
    p.items = e.dynamic_instances
    p.interactables.add(d)

    # extra rects to draw debug only ! (for now)
    e.extra_rect_drawables.append((p.rect, (255, 0, 0)))
    e.extra_rect_drawables.append((p.collider.rect, (0, 255, 0)))

    # add all drawables
    e.drawables.add(p)
    e.drawables.add(d)
    mapRenderer.renderForeGround()


    #bgm = BackgroundMusic("lavender city")
    #bgm.start_music()
  
    # add all impassable sprites to classes which need them
    for impassable in mapRenderer.getAllImpassables():
        p.blocks.add(impassable)
   

    zombieTimer = 60000 #Change this to change spawn rate of the zombie
    pygame.time.set_timer(pygame.USEREVENT, zombieTimer // league.Settings.gameTimeFactor)

    # create room object in engine
    e.room = Room(p, e, overlay)
    
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