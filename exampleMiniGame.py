# import pygame
# from assets import DinoDemoAssets
# from player import Player
# from datetime import datetime
# from blit_queue import GraphicsQueue
#
#
# class DinoDemo:
#     def __init__(self, colors, sounds):
#         # mouse visibility
#         self.sounds = sounds
#         self.graphics_queue = GraphicsQueue()
#         self.colors = colors
#         self.assets = DinoDemoAssets()
#         self.level_img = self.assets.level_images[0]
#         self.level_img_index = 0
#         self.level_img_timer = datetime.now()
#         self.level_rect = self.level_img.get_rect()
#         self.walls = self.level_walls()
#         self.screen_fill_color = (92, 105, 159)
#         # init player one (max two players)
#         self.p1 = Player(1, self.sounds)
#         self.p2 = Player(2, self.sounds)
#         # TODO add method to check if two players
#         self.two_players = True
#         # empty rect for queue
#         self.empty_rect = pygame.Rect(0, 0, 0, 0)
#
#         # test
#         self.guns = self.assets.guns
#
#     def level_walls(self):
#         """
#         - specific borders designed to stop player movement and other movable objects
#         """
#         r = self.level_rect
#         m1, m2 = 18, 4
#         main = pygame.Rect(r.x + m1 + 2, r.y + m1 + m2 - 5, r.w - (m1 * 2) - 2, r.h - (m1 * 2) - 1)
#         walls = {
#             'border': main
#             # 'obstacle': pygame.Rect(r.centerx - 19, r.centery - 6, 30, 29)
#         }
#         return walls
#
#     def update_player(self, surface, controls):
#         queue1 = self.p1.update(surface, controls, self.walls, collidables=[self.p2.torso_rect])
#         if self.two_players:
#             queue2 = self.p2.update(surface, controls, self.walls, collidables=[self.p1.torso_rect])
#         else:
#             queue2 = []
#
#         return queue1 + queue2
#
#     def blit_level(self, surface, controls):
#         level_queue = []
#         if (datetime.now() - self.level_img_timer).total_seconds() > .8:
#             self.level_img_timer = datetime.now()
#             self.level_img_index = self.level_img_index + 1 if self.level_img_index < len(
#                 self.assets.level_images) - 1 else 0
#         self.level_img = self.assets.level_images[self.level_img_index]
#         level_queue.append({'layer': -100, 'type': 'image', 'image': self.level_img, 'color': (0, 0, 0), 'rect': self.empty_rect,
#                       'pos': (0, 0), 'radius': 0})
#         level_queue.append({'layer': -99, 'type': 'image', 'image': self.assets.level_wall_upper, 'color': (0, 0, 0), 'rect': self.empty_rect,
#                       'pos': (0, 0), 'radius': 0})
#         level_queue.append({'layer': 100, 'type': 'image', 'image': self.assets.level_wall_bottom, 'color': (0, 0, 0),
#                       'rect': self.empty_rect,
#                       'pos': (0, 0), 'radius': 0})
#         # returns queued objects to blit, it proper order
#         queued_list_obj = self.update_player(surface, controls)
#         # essential class for blitting queued objects in order..
#         self.graphics_queue.blit_queue(surface, queued_list_obj + level_queue)
#
#     def blit_walls(self, surface):
#         for key, rect in self.walls.items():
#             if "obstacle" in key:
#                 pygame.draw.rect(surface, self.colors.red, rect)
#             elif "border" in key:
#                 pygame.draw.rect(surface, self.colors.blue, rect, 1)
#
#     def update(self, surface, controls):
#         self.blit_level(surface, controls)
#         self.blit_walls(surface)
#         self.p1.blit_player_rects(surface)
#         self.p2.blit_player_rects(surface)
#
