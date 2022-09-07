import pygame


class Font:
    def __init__(self, size=15):
        # heart1 - U+005E
        # heart2 - U+005F
        # twitter - U+0060
        # patreon - U007B
        # facebook - U007C
        # twitch - U007D
        # smile1 - U007E
        # smile2 - U00A1
        # smile3 - U00A2
        # pacghost - U00A3
        # bob - U00A4
        # skull - U20A0
        self.bold = pygame.font.Font('assets/fonts/mago3.ttf', size)
