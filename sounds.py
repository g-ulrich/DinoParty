import pygame, os
from random import choice


class Sounds:
    def __init__(self):
        pygame.mixer.init()
        # music pygame object and string name
        self.music_objects = self.get_music_objects()
        self.song_obj = choice(self.music_objects)
        # self.play_song()
        # character
        self.step = pygame.mixer.Sound('assets/sounds/character/step.wav')
        self.gun_shot = pygame.mixer.Sound('assets/sounds/gun/shot.wav')
        self.gun_hit_wall = pygame.mixer.Sound('assets/sounds/gun/hit_wall.wav')
        self.gun_hit_wall.set_volume(.05)
        self.gun_farts = [pygame.mixer.Sound('assets/sounds/gun/fart.wav'), pygame.mixer.Sound('assets/sounds/gun/fart2.wav')]
        self.gun_hurt = pygame.mixer.Sound('assets/sounds/gun/hurt.wav')
        # self.step.set_volume()

    def get_music_objects(self):
        file_names = os.listdir("assets/sounds/music")
        items = []
        for name in file_names:
            items.append({'song': pygame.mixer.Sound(f"assets/sounds/music/{name}"), 'name': name})
        return items

    def skip_song(self):
        self.song_obj['song'].fadeout(1000)
        self.song_obj = choice(self.music_objects)
        self.play_song()

    def play_song(self):
        self.song_obj['song'].set_volume(.3)
        self.song_obj['song'].play(-1)

    def play_step(self):
        self.step.set_volume(choice([.2, .1]))
        self.step.play()

    def play_shot(self):
        self.gun_shot.set_volume(choice([.2, .1]))
        self.gun_shot.play()

    def play_hit_wall(self):
        self.gun_hit_wall.play()

    def play_fart(self):
        fart = choice(self.gun_farts)
        fart.play()

    def play_hurt(self):
        self.gun_hurt.set_volume(choice([.2, .1]))
        self.gun_hurt.play()

