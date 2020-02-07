import abc
import os

os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"
import pygame
from .settings import *


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
        self.nospriteables = {} # explained further in graphics.py

        # defaults
        self.title = title
        self.running = False
        self.clock = None 
        self.events = {}
        self.key_events = {}
        self.key_events[Settings.statistics_key] = self.toggle_statistics
        self.objects = []
        self.drawables = pygame.sprite.LayeredUpdates()
        self.screen = None
        self.real_delta_time = 0
        self.visible_statistics = False
        self.statistics_font = None
        self.collisions = {}
        self.overlay = None
        self.light_source = None

    def init_pygame(self):
        """This function sets up the state of the pygame system,
        including passing any specific settings to it."""
        # Startup the pygame system
        pygame.init()
        # Create our window
        self.screen = pygame.display.set_mode((Settings.width, Settings.height))
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
        # Set the repeat delay for key presses
        pygame.key.set_repeat(Settings.key_repeat)
        # Create statistics font
        self.statistics_font = pygame.font.Font(None,30)

    def run(self):
        """The main game loop.  As close to our book code as possible."""
        self.running = True
        while self.running:
            # The time since the last check
            now = pygame.time.get_ticks()
            self.real_delta_time = now - self.last_checked_time
            self.last_checked_time = now
            self.game_delta_time = self.real_delta_time * (0.001 * Settings.gameTimeFactor)

            # Wipe screen
            self.screen.fill(Settings.fill_color)
            
            # Process inputs
            self.handle_inputs()

            # Update game world
            # Each object must have an update(time) method
            self.check_collisions()
            for o in self.objects:
                o.update(self.game_delta_time)

            # Generate outputs
            #d.update()
            #dark = pygame.Surface((720, 720))
            #dark.fill(pygame.color.Color('Grey'))
            


<<<<<<< HEAD
=======
            self.drawables.draw(self.screen)
>>>>>>> ba50b5c6f9e171556b67bdf457dcf42071ff2fe6
            # Show statistics?
            if self.visible_statistics:
                self.show_statistics()
            
            # Show overlay?
            if self.overlay:
                self.show_overlay()
            #dark.blit(self.light_source.image, (self.objects[0].rect.x, self.objects[0].rect.y))
            #self.screen.blit(dark, (0, 0), special_flags=pygame.BLEND_RGBA_SUB)

            for rect, color in self.extra_rect_drawables:
                pygame.draw.rect(self.screen, color, rect, 3)

            # draw projectiles
            for p in self.projectiles:
                
                # otherwise see if the projectile is done
                if p.alpha <= 0:
                    self.projectiles.remove(p)
                    p.delete() # destroy the projectile memory
                    continue

                self.screen.blit(p.surf, (p.x, p.y)) # display the bullet
                p.update() # updates any values for the projectile to progress
                new_alpha = p.alpha - p.delta_alpha # increase the transparency
                p.set_colors((p.red, p.green - 5, 0, new_alpha)) # move colors towards white

            # Could keep track of rectangles and update here, but eh.
            pygame.display.flip()

            # Frame limiting code
            self.clock.tick(Settings.fps)

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
        statistics_string = statistics_string +  " FPS: " + str(int(self.clock.get_fps()))
        fps = self.statistics_font.render(statistics_string, True, Settings.statistics_color)
        self.screen.blit(fps, (10, 10))
    
    def show_overlay(self):
        self.screen.blit(self.overlay, Settings.overlay_location)

    def stop(self, time):
        self.running = False

    def end(self, time):
        pygame.quit()

    def handle_inputs(self):
        events = pygame.event.get()
        for event in events:
            # left mouse button presse
            if event.type in self.events.keys():
                self.events[event.type](self.game_delta_time)

        # handle key pressed events
        pressed_keys = pygame.key.get_pressed() # get all pressed keys
        # if a key with an event is pressed do the event
        for key_event in  self.key_events.keys():
            # check if a key with an event is pressed
            if (pressed_keys[key_event]):
                self.key_events[key_event](self.game_delta_time) # run the event associated with the key