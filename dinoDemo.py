import pygame
from assets import DinoDemoAssets
from player import Player
from datetime import datetime
from blit_queue import GraphicsQueue
from random import choice, randint
from gun import Gun


class DinoDemo:
    def __init__(self, general, colors, sounds):
        # mouse visibility
        self.general = general
        self.sounds = sounds
        self.sounds.play_demo_song()
        self.graphics_queue = GraphicsQueue()
        self.colors = colors
        self.assets = DinoDemoAssets(general)
        self.level_img = self.assets.level_images[0]
        self.level_img_index = 0
        self.level_img_timer = datetime.now()
        self.level_rect = self.level_img.get_rect()
        self.gun = Gun("1", self.level_rect, self.sounds)
        # sign offset from center
        self.sign_offset = pygame.math.Vector2((--10, 20))
        self.walls = self.level_walls()
        self.sign_x_timer = datetime.now()
        # empty rect for queue
        self.empty_rect = pygame.Rect(0, 0, 0, 0)
        self.grasses = self.level_grass()
        self.screen_fill_color = (92, 105, 159)
        # init player one (max two players)
        self.p1 = Player(1, self.sounds, self.level_rect.topleft + pygame.math.Vector2((30, 30)))
        self.p2 = Player(2, self.sounds, self.level_rect.bottomleft + pygame.math.Vector2((30, -60)),
                         disable_movement=True)
        # TODO add method to check if two players
        self.two_players = True
        # need cross hair
        self.need_cross_hair = True

    def level_walls(self):
        """
        - specific borders designed to stop player movement and other movable objects
        """
        r = self.level_rect
        sign_r = self.assets.decorations.wooden_sign_on_rock.get_rect()
        m1, m2 = 18, 4
        main = pygame.Rect(r.x + m1 + 2, r.y + m1 + m2 - 5, r.w - (m1 * 2) - 2, r.h - (m1 * 2) - 1)
        walls = {
            'border': main,
            'border_bullets': pygame.Rect(r.x + m1 + 2, r.y + m1 + m2 - 13, r.w - (m1 * 2) - 2, r.h - (m1 * 2) + 8),
            'obstacle_stone_sign': pygame.Rect(r.centerx + sign_r.x - self.sign_offset.x,
                                               r.centery + sign_r.y - self.sign_offset.y + 12,
                                               sign_r.w, sign_r.h - 12)
        }
        return walls

    def level_grass(self):
        grass = []
        grass_append = grass.append
        for i in range(15):
            grass_append({'layer': -1, 'type': 'image', 'image': choice(self.assets.decorations.grasses),
                          'color': (0, 0, 0), 'rect': self.empty_rect,
                          'pos': (randint(20, self.level_rect.bottomright[0] - 20),
                                  randint(20, self.level_rect.bottomright[1] - 20)), 'radius': 0})
        return grass

    def update_player(self, surface, controls):
        queue1 = self.p1.update(surface, controls, self.walls,
                                collidables=[self.p2.torso_rect] if self.two_players else [])
        if self.two_players:
            queue2 = self.p2.update(surface, controls, self.walls,
                                    collidables=[self.p1.torso_rect])
        else:
            queue2 = []

        return queue1 + queue2

    def blit_wood_sign(self, controls):
        # wooden sign with message
        if self.p1.body_rect.colliderect(self.walls['obstacle_stone_sign']):
            if controls.joysticks:
                controls.update_controller_message("Controls",
                    "Welcome to the demo!" +
                    "\nPress (Y) to run." +
                    "\nPress (B) to shoot." +
                    "\nRight bumper zooms screen in." +
                    "\nLeft bumper zooms screen out." +
                    "\nPress the back button to go to main menu. :)"
                )
            else:
                controls.update_controller_message("Controls",
                    "Welcome to the demo!" +
                    "\nPlayer 1 uses [C] to run and player 2 uses [Z]." +
                    "\nPlayer 1 uses [SPACE] to shoot and player 2 uses [X]." +
                    "\nPress [2] to zoom screen in." +
                    "\nPress [1] to zoom screen out." +
                    "\nPress the ESC button to go to main menu. :)"
                )
        sign = [
            {'layer': 99, 'type': 'image', 'image': self.assets.decorations.wooden_sign_on_rock, 'color': (0, 0, 0),
             'rect': self.assets.decorations.wooden_sign_on_rock.get_rect(),
             'pos': self.level_rect.center - self.sign_offset, 'radius': 0}
        ]
        return sign

    def blit_level(self, surface, controls, zoom_scale):
        level_queue = []
        if (datetime.now() - self.level_img_timer).total_seconds() > .8:
            self.level_img_timer = datetime.now()
            self.level_img_index = self.level_img_index + 1 if self.level_img_index < len(
                self.assets.level_images) - 1 else 0
        self.level_img = self.assets.level_images[self.level_img_index]
        level_queue.append(
            {'layer': -100, 'type': 'image', 'image': self.level_img, 'color': (0, 0, 0), 'rect': self.empty_rect,
             'pos': (0, 0), 'radius': 0})
        level_queue.append({'layer': -99, 'type': 'image', 'image': self.assets.level_wall_upper, 'color': (0, 0, 0),
                            'rect': self.empty_rect,
                            'pos': (0, 0), 'radius': 0})
        level_queue.append({'layer': 100, 'type': 'image', 'image': self.assets.level_wall_bottom, 'color': (0, 0, 0),
                            'rect': self.empty_rect,
                            'pos': (0, 0), 'radius': 0})
        # wooden sign with message
        queued_wooden_sign = self.blit_wood_sign(controls)
        # returns queued objects to blit, it proper order
        queued_list_obj = self.update_player(surface, controls)
        # blit guns
        queue_gun_list = self.gun.update(self.walls, self.p1.body_rect, self.p1.torso_rect, zoom_scale,
                                         self.p1.last_direction, controls,
                                         moving_obj_classes=[self.p2] if self.two_players else [])
        # essential class for blitting queued objects in order..
        self.graphics_queue.blit_queue(
            surface, queued_list_obj + queue_gun_list + level_queue + queued_wooden_sign + self.grasses)

    def blit_walls_rects(self, surface):
        for key, rect in self.walls.items():
            if "obstacle" in key:
                pygame.draw.rect(surface, self.colors.red, rect, 1)
            elif "border" in key:
                pygame.draw.rect(surface, self.colors.blue, rect, 1)

    def blit_ocean_particles(self, zoom_scale, controls):
       self.assets.particles.blit_particles(self.general.screen_surface, zoom_scale, controls)

    def update(self, surface, controls, zoom_scale):
        self.blit_level(surface, controls, zoom_scale)
        self.blit_ocean_particles(zoom_scale, controls)



        # self.blit_dotted_line_and_cross_hair(surface, zoom_scale, self.p1.torso_rect)

        # self.blit_walls_rects(surface)
        # self.p1.blit_player_rects(surface)
        # self.p2.blit_player_rects(surface)
