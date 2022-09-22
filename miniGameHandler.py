import pygame
from dinoDemo import DinoDemo
from assets import OceanParticleAffect
from blit_queue import GraphicsQueue


class Handler:
    def __init__(self, general, colors):
        self.sounds = general.sounds
        self.general = general
        self.colors = colors
        self.queue = GraphicsQueue()
        self.mini_game = DinoDemo(general, self.colors, self.sounds)
        self.level_rect = self.mini_game.level_rect

    def update_mini_game(self, screen_surface):
        """
        - Update from home screen, only change if player selects new mini game.
        """
        pass
        # self.mini_game = DinoDemo()
        # self.level_rect = self.mini_game.level_rect