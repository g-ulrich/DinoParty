import pygame
from dinoDemo import DinoDemo


class Handler:
    def __init__(self, general, colors):
        self.sounds = general.sounds
        self.general = general
        self.colors = colors
        self.mini_game = DinoDemo(self.colors, self.sounds)
        self.level_rect = self.mini_game.level_rect

    def update_mini_game(self):
        """
        - Update from home screen, only change if player selects new mini game.
        """
        pass
        # self.mini_game = DinoDemo()
        # self.level_rect = self.mini_game.level_rect