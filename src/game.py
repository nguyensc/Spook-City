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
<<<<<<< HEAD
    floor = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA5_PHC_Interior-Hospital.png', 16, 8)
    walls = league.Spritesheet('../assets/map assets/sprite sheets/Hospital Tiles/TileA4_PHC_Interior-Hospital.png', 16, 23)
    floorLayer = league.Tilemap('../assets/map assets/level 1/floors.lvl', floor, layer = 0)
    wallLayer = league.Tilemap('../assets/map assets/level 1/walls.lvl', walls, layer = 1)
    b = league.Tilemap('../assets/map assets/level 1/background.lvl', floor, layer = 0)
    world_size = (floorLayer.wide*league.Settings.tile_size, floorLayer.high *league.Settings.tile_size)
    e.drawables.add(floorLayer.passable.sprites())
    e.drawables.add(wallLayer.passable.sprites())
    e.drawables.add(b.passable.sprites()) 

    p = Player(1, 400, 300)
    l = Light(1, 0, 0, p)
    p.blocks.add(wallLayer.impassable)
    f = Flashlight(200, 500, 2, p)
    q = Player(2, 300, 400)
    o = Overlay(p)
    f.blocks.add(wallLayer.impassable)
    p.world_size = world_size
=======
    p = Player(1, 400, 300)
    map = MapRenderer("first floor", e)
    world_size = map.renderBackground()
    p.world_size = world_size
    l = Light(20, 0, 0, p)
    f = Flashlight(200, 500, 2, p)
    q = Player(2, 300, 400)
    o = Overlay(p)
>>>>>>> ba50b5c6f9e171556b67bdf457dcf42071ff2fe6
    p.rect = p.image.get_rect()
    q.image = p.image
    e.objects.append(p)
    e.objects.append(q)
    e.objects.append(l)
    e.objects.append(f)
   

    e.drawables.add(p)
    e.drawables.add(q)
    e.drawables.add(l)
<<<<<<< HEAD
    e.drawables.add(f)    

    c = league.LessDumbCamera(league.Settings.height, league.Settings.width, p, e.drawables, world_size)
=======
    e.drawables.add(f)
    map.renderForeGround()
    c = league.LessDumbCamera(720, 720, p, e.drawables, world_size)
>>>>>>> ba50b5c6f9e171556b67bdf457dcf42071ff2fe6
    e.objects.append(c)
    e.light_source = l
<<<<<<< HEAD
    e.flashlight = f  

=======
>>>>>>> ba50b5c6f9e171556b67bdf457dcf42071ff2fe6
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