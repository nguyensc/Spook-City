from league import *
import pygame

class BackgroundMusic():
    def __init__(self, name):
        if name == "lavender town":
            self.name = "../assets/music assets/Lavender Town.mp3"
        if name == "dream fatigue":
            self.name = "../assets/music assets/Dream Fatigue.mp3"
        
        pygame.mixer.music.load(self.name)
    
    def start_music(self):
        pygame.mixer.music.play(-1)

    def stop_music(self):
        pygame.mixer.music.fadeout(15000)
       
class Sound():
    def __init__(self):
        self.door_sound = pygame.mixer.Sound("../assets/sound effect assets/creak_x.wav")

    def play_door_sound(self):
        self.door_sound.play()