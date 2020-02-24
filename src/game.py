import pygame
import sys
sys.path.append('..')
import league
from player import Player
from enemy import Enemy
from mapRenderer import MapRenderer
from light import Light
from flashlight import Flashlight
from overlay import Overlay
from container import Container
from enemySpawner import EnemySpawner
from door import Door
from rooms import Room
from audio import BackgroundMusic

def getSpawnCoords(play): #CoordX, coordY, some indicator for progress through the game, 
    left = 16
    right = 656
    up = 16
    down = 656

    coordx = left   
    coordy = up

    xdiffLeft = abs(left - play.getX())
    xdiffRight = abs(right - play.getX())
    if(xdiffRight > xdiffLeft) :
        coordx = right
    ydiffUp = abs(up - play.getY())
    ydiffDown = abs(down - play.getY())
    if(ydiffDown > ydiffUp) :
        coordy = down

    return Enemy(2, 100, 100, play)

def main() :
    e = league.Engine("Survive")
    e.init_pygame()
    timer = pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // league.Settings.gameTimeFactor)
    count = 0

    p = Player(1, 240, 300)
    
    mapRenderer = MapRenderer("fourth room", e)
    world_size = mapRenderer.renderBackground()
    p.world_size = world_size
    mapRenderer.renderForeGround()
    l = Light(20, 0, 0, p)
    #f = Flashlight(200, 500, 2, p)
    d = Door(2, 300, 4, 300, 416, "first room", e)
    e.light_points = p.raycast_points

    #e.flashlight = f
    e.light_source = l
    e.player = p

    overlay = Overlay(p)
    e.overlay = overlay

    enemy = Enemy(2, 100, 150, p)
    p.enemies.add(enemy)

    container1 = Container(2, 100, 64, "lantern")
    container2 = Container(2, 300, 64, "beartrap")
    container3 = Container(2, 316, 264, "rancidmeat")

    e.objects.append(p)
    e.objects.append(enemy)
    e.objects.append(l)
    #e.objects.append(f)
    e.objects.append(overlay)
    e.objects.append(container1)
    e.objects.append(container2)
    e.objects.append(container3)
    e.objects.append(d)

    # any objects to be created on the fly
    p.items = e.dynamic_instances
    enemy.hazards = p.hazards
    p.interactables.add(container1)
    p.interactables.add(container2)
    p.interactables.add(container3)
    p.interactables.add(d)

    # extra rects to draw debug only ! (for now)
    e.extra_rect_drawables.append((p.rect, (255, 0, 0)))
    e.extra_rect_drawables.append((p.collider.rect, (0, 255, 0)))
    e.extra_rect_drawables.append((enemy.rect, (0, 0, 255)))
    for test in enemy.tests: 
        e.drawables.add(test)
        e.extra_rect_drawables.append((test.rect, (255, 0, 255)))
    e.extra_rect_drawables.append(((p.x, p.y, 32, 32), (200, 255, 150)))

    # add all drawables
    e.drawables.add(p)
    e.drawables.add(enemy)
    e.drawables.add(l)
    #e.drawables.add(f)
    e.drawables.add(container1)
    e.drawables.add(container2)
    e.drawables.add(container3)
    e.drawables.add(d)

    mapRenderer.renderForeGround()

    spawner = EnemySpawner(100, 100, 0, e, p, p.blocks)

    bgm = BackgroundMusic("lavender town")
    bgm.start_music()
  
    # add all impassable sprites to classes which need them
    for impassable in mapRenderer.getAllImpassables():
        p.blocks.add(impassable)
        enemy.blocks.add(impassable)
        #f.blocks.add(impassable)

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
    e.events[pygame.USEREVENT] = e.makeZombie
    e.events[pygame.QUIT] = e.stop
    e.run()

if __name__=='__main__':
    main()