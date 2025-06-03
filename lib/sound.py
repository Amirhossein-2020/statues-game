import pygame
import os

class SoundManager:
    def __init__(self, DB):
        pygame.mixer.init()
        self.sounds = {
            "idle": self.load_sound(DB.audioListPath["music"][0]),
            "moving": self.load_sound(DB.audioListPath["sound effect"][3]),
            "frozen": self.load_sound(DB.audioListPath["sound effect"][2]),
            "countdown": self.load_sound(DB.audioListPath["sound effect"][0]),
            "eliminated": self.load_sound(DB.audioListPath["sound effect"][1]),
        }

    def load_sound(self, path):
        try:
            return pygame.mixer.Sound(path)
        except pygame.error as e:
            print(f"[ERROR] Could not load sound {path}: {e}")
            return None

    def stop_all(self):
        pygame.mixer.stop()

    def play(self, sound_name, loop=False):
        self.stop_all()
        sound = self.sounds.get(sound_name)
        if sound:
            try:
                sound.play(loops=-1 if loop else 0)
            except pygame.error as e:
                print(f"[ERROR] Failed to play sound '{sound_name}': {e}")
        else:
            print(f"[WARNING] Sound '{sound_name}' not found.")