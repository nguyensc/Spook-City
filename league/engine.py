from .settings import *
import pygame
import abc
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"


class Engine:
    """Engine is the definition of our game engine.  We want it to
    be as game agnostic as possible, and will try to emulate code
    from the book as much as possible.  If there are deviations they
    will be noted here.

    Fields:
    title - The name of the game.
    running - Whether or not the engine is currently in the main game loop.
    clock - The real world clock for elapsed time.
    events - A dictionary of events and handling functions.
    objects - A list of updateable game objects.
    drawable - A list of drawable game objects.
    screen - The window we are drawing upon.
    real_delta_time - How much clock time has passed since our last check.
    game_delta_time - How much game time has passed since our last check.
    visible_statistics - Whether to show engine statistics statistics.
    """

    def __init__(self, title):
        # vars added by max (enemy stuff, bullet stuff, and collision stuff)
        self.extra_rect_drawables = []
        self.extra_line_drawables = []
        self.projectiles = []
        self.nospriteables = []
        self.player = None
        self.dynamic_instances = []
        self.light_points = []  # used for raycasting light
        self.room = None

        self.title = title
        self.running = False
        self.clock = None
        self.events = {}
        self.key_events = {}
        self.key_events[Settings.statistics_key] = self.toggle_statistics
        self.objects = []
        self.drawables = pygame.sprite.LayeredUpdates()
        self.mapDrawables = pygame.sprite.LayeredUpdates()
        self.screen = None
        self.window = None
        self.real_delta_time = 0
        self.visible_statistics = False
        self.statistics_font = None
        self.collisions = {}
        self.overlay = None
        self.light_source = None
        self.flashlight = None

        self.currangle = 0

    def init_pygame(self):
        """This function sets up the state of the pygame system,
        including passing any specific settings to it."""
        # Startup the pygame system
        pygame.init()
        # Create our window
        self.screen = pygame.display.set_mode(
            (Settings.width, Settings.height))
        # Set the title that will display at the top of the window.
        pygame.display.set_caption(self.title)
        # Create the clock
        self.clock = pygame.time.Clock()
        self.last_checked_time = pygame.time.get_ticks()
        # Startup the joystick system
        pygame.joystick.init()
        # For each joystick we find, initialize the stick
        for i in range(pygame.joystick.get_count()):
            pygame.joystick.Joystick(i).init()
        print("controllers connected: " + str(pygame.joystick.get_count()))
        # Set the repeat delay for key presses
        pygame.key.set_repeat(Settings.key_repeat)
        # Create statistics font
        self.statistics_font = pygame.font.Font(None, 30)

    def changeRoom(self, room_num):
        self.drawables.empty()
        self.mapDrawables.empty()
        self.objects = []
        self.dynamic_instances = []
        # resetup player
        self.drawables.add(self.player)
        self.objects.append(self.player)
        self.player.enemies.empty()
        self.player.reset_all_timers()
        self.player.blocks.empty()
        self.player.interactables.empty()
        self.player.items = self.dynamic_instances
        # resetup overlay
        self.objects.append(self.overlay)
        # init room
        if room_num == 1:
            self.room.room1()
        elif room_num == 2:
            self.room.room2()
        elif room_num == 3:
            self.room.room3()
        elif room_num == 4:
            self.room.room4()
        elif room_num == 5:
            self.room.room5()

    def run(self):
        """The main game loop.  As close to our book code as possible."""
        self.running = True
        while self.running:
            # The time since the last check
            now = pygame.time.get_ticks()
            self.real_delta_time = now - self.last_checked_time
            self.last_checked_time = now
            self.game_delta_time = self.real_delta_time * \
                (0.001 * Settings.gameTimeFactor)

            # Wipe screen
            self.screen.fill(Settings.fill_color)

            # Process inputs
            self.handle_inputs()

            # Update game world
            # Each object must have an update(time) method
            self.check_collisions()
            for o in self.objects:
                o.update(self.game_delta_time)

            self.mapDrawables.draw(self.screen)

            # Show statistics?
            if self.visible_statistics:
                self.show_statistics()

            # set up fog-of-war
            fog = pygame.Surface((Settings.width, Settings.height))
            fog.fill(pygame.color.Color(30, 30, 30))

            # draw player light onto
            light = pygame.Surface((480, 480)).convert_alpha()
            light.fill((255, 255, 255, 0))
            light_polygon = []
            for coords in self.light_points:
                light_polygon.append(coords)
            # must convert list -> typle for use in draw_polygon

            pygame.draw.polygon(light, (255, 255, 196, 128),
                                tuple(light_polygon))
            fog.blit(light, (0, 0))

            # draw any runtime instances created by the player
            for i in self.dynamic_instances:
                i.update()
                # all item type objects must have an isLightSource attribute
                if i.isLightSource:
                    fog.blit(i.light, (i.x - i.light_offsetx,
                                       i.y - i.light_offsety))
                # run area of effect code if the dynamic instance has an aoe
                # if hasattr(i, "aoe_rect"):
                #pygame.draw.rect(self.screen, (255,255,128,255), i.aoe_rect, 5)
                # render the actual physical item
                self.screen.blit(i.image, (i.x, i.y))
                #pygame.draw.rect(self.screen, (255,255,128,255), i.rect, 5)

            # drawables all go ontop of dynamic instances
            self.drawables.draw(self.screen)

            #fog.blit(self.light_source.image, self.light_source.rect)
            #fog.blit(self.flashlight.image, self.flashlight.rect)
            self.screen.blit(fog, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)

            # show display ontop of fog
            if self.overlay:
                self.show_overlay()

            # Could keep track of rectangles and update here, but eh.
            pygame.display.flip()

            # Frame limiting code
            self.clock.tick(Settings.fps)

    def rotate_image_center(self, img, angle, pos):
        w, h = img.get_size()

        box = [pygame.math.Vector2(p)
               for p in [(0, 0), (w, 0), (w, -h), (0, -h)]]
        box_rotate = [p.rotate(angle) for p in box]

        min_box = (min(box_rotate, key=lambda p: p[0])[
                   0], min(box_rotate, key=lambda p: p[1])[1])
        max_box = (max(box_rotate, key=lambda p: p[0])[
                   0], max(box_rotate, key=lambda p: p[1])[1])

        pivot = pygame.math.Vector2(w/5, -h/2)
        pivot_rotate = pivot.rotate(angle)
        pivot_move = pivot_rotate - pivot

        origin = (pos[0] + min_box[0] - pivot_move[0],
                  pos[1] - max_box[1] + pivot_move[1])

        rotated_image = pygame.transform.rotate(img, angle)
        return (rotated_image, origin)

    def check_collisions(self):
        for i in self.collisions.keys():
            if pygame.sprite.collide_rect(i, self.collisions[i][0]):
                self.collisions[i][1]()

    def add_group(self, group):
        self.drawables.add(group.sprites())

    def toggle_statistics(self):
        self.visible_statistics = not self.visible_statistics

    def show_statistics(self):
        statistics_string = "Version: " + str(Settings.version)
        statistics_string = statistics_string + \
            " FPS: " + str(int(self.clock.get_fps()))
        fps = self.statistics_font.render(
            statistics_string, True, Settings.statistics_color)
        self.screen.blit(fps, (10, 10))

    def show_overlay(self):
        self.screen.blit(self.overlay.image, Settings.overlay_location)

    def stop(self, time):
        self.running = False

    def end(self, time):
        pygame.quit()

    def handle_inputs(self):
        for event in pygame.event.get():
            if event.type in self.events.keys():
                self.events[event.type](self.game_delta_time)
            if event.type == pygame.KEYDOWN:
                if event.key in self.key_events.keys():
                    self.key_events[event.key](self.game_delta_time)
