import pygame
import os

class SoundManager:
    def __init__(self, base_path="assets/sounds"):
        pygame.mixer.init()
        self.sounds = {
            "idle": self.load_sound(base_path, "idling.wav"),
            "moving": self.load_sound(base_path, "moving.wav"),
            "frozen": self.load_sound(base_path, "freezing.wav"),
            "countdown": self.load_sound(base_path, "countdown.wav"),
            "eliminated": self.load_sound(base_path, "elimination.wav"),
        }

    def load_sound(self, base_path, filename):
        full_path = os.path.join(base_path, filename)
        try:
            return pygame.mixer.Sound(full_path)
        except pygame.error as e:
            print(f"[ERROR] Could not load sound {filename}: {e}")
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