import pygame
from assets import Colors, PlayerAssets, WalkingEffect
from datetime import datetime
from random import randint


class Player:
    """
    Update method returns queue to be displayed from minigame class calling it.
    """

    def __init__(self, player_num, sounds, spawn_pos):
        self.sounds = sounds
        self.colors = Colors()
        self.assets = PlayerAssets(player_num)
        self.rect = pygame.Rect(spawn_pos.x, spawn_pos.y, 24, 24)
        self.feet_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 17, 12, 5)
        self.body_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 4, 12, 18)
        self.torso_rect = pygame.Rect(self.rect.x + 6, self.rect.y + 12, 12, 10)
        self.img = self.assets.dino_idle[0]
        self.direction = pygame.math.Vector2()
        self.last_direction = pygame.math.Vector2(1, 0)
        self.walk_speed = 1
        self.run_speed = 2
        # player 1 or 2 indexes
        self.player_num = f"{player_num}"
        self.sprite_move_i = 0  # 7
        self.sprite_idle_i = 0  # 4
        self.sprite_hit_i = 0  # 2
        self.facing_right = True
        # only left or right.
        self.facing_up = False
        self.facing_down = False
        # timers to slow the speed of sprite updates
        self.idle_timer = datetime.now()
        self.walk_timer = datetime.now()
        self.walk_sound_timer = datetime.now()
        self.run_timer = datetime.now()
        self.hit_timer = datetime.now()
        # player walking affect
        self.moving_dust = WalkingEffect()
        # empty rect for queue
        self.empty_rect = pygame.Rect(0, 0, 0, 0)

    def update_sprite(self, running):
        walking = True if not running and self.direction != (0, 0) else False
        running = True if running else False
        hit = False  # add hit method here
        # respawn = False  # add respawn method here
        if self.facing_right and self.direction.x == -1:
            self.sprite_move_i = 0  # 7
            self.sprite_idle_i = 0  # 4
            self.sprite_hit_i = 0  # 2
        elif not self.facing_right and self.direction.x == 1:
            self.sprite_move_i = 0  # 7
            self.sprite_idle_i = 0  # 4
            self.sprite_hit_i = 0  # 2
        if self.direction.x == -1:
            self.facing_right = False
        elif self.direction.x == 1:
            self.facing_right = True
        if self.direction.y == -1:
            self.facing_up = True
            self.facing_down = False
        elif self.direction.y == 1:
            self.facing_up = False
            self.facing_down = True
        # if running adjust body rect
        if running:
            self.body_rect.y = self.rect.y + 7
            self.body_rect.h = 15
        else:
            self.body_rect.y = self.rect.y + 4
            self.body_rect.h = 18

        if walking and self.direction != (0, 0):
            if (datetime.now() - self.walk_timer).total_seconds() > .08:
                self.walk_timer = datetime.now()
                if (datetime.now() - self.walk_sound_timer).total_seconds() > .16:
                    self.walk_sound_timer = datetime.now()
                    self.sounds.play_step()
                if self.facing_right:
                    self.img = self.assets.dino_walk[self.sprite_move_i]
                    self.sprite_move_i = self.sprite_move_i + 1 if self.sprite_move_i < len(
                        self.assets.dino_walk) - 1 else 0
                else:
                    self.img = self.assets.dino_walk_flip[self.sprite_move_i]
                    self.sprite_move_i = self.sprite_move_i + 1 if self.sprite_move_i < len(
                        self.assets.dino_walk) - 1 else 0

        elif running and self.direction != (0, 0):
            if (datetime.now() - self.run_timer).total_seconds() > .06:
                self.run_timer = datetime.now()
                if (datetime.now() - self.walk_sound_timer).total_seconds() > .08:
                    self.walk_sound_timer = datetime.now()
                    self.sounds.play_step()
                if self.facing_right:
                    self.img = self.assets.dino_run[self.sprite_move_i]
                    self.sprite_move_i = self.sprite_move_i + 1 if self.sprite_move_i < len(
                        self.assets.dino_run) - 1 else 0
                else:
                    self.img = self.assets.dino_run_flip[self.sprite_move_i]
                    self.sprite_move_i = self.sprite_move_i + 1 if self.sprite_move_i < len(
                        self.assets.dino_run) - 1 else 0

        elif hit:
            if (datetime.now() - self.hit_timer).total_seconds() > .15:
                self.hit_timer = datetime.now()
                if self.facing_right:
                    self.img = self.assets.dino_hit[self.sprite_hit_i]
                    self.sprite_hit_i = self.sprite_hit_i + 1 if self.sprite_hit_i < len(
                        self.assets.dino_hit) - 1 else 0
                else:
                    self.img = self.assets.dino_hit_flip[self.sprite_hit_i]
                    self.sprite_hit_i = self.sprite_hit_i + 1 if self.sprite_hit_i < len(
                        self.assets.dino_hit) - 1 else 0
        else:
            # idle
            if (datetime.now() - self.idle_timer).total_seconds() > .2:
                self.idle_timer = datetime.now()
                if self.facing_right:
                    self.img = self.assets.dino_idle[self.sprite_idle_i]
                    self.sprite_idle_i = self.sprite_idle_i + 1 if self.sprite_idle_i < len(
                        self.assets.dino_idle) - 1 else 0
                else:
                    self.img = self.assets.dino_idle_flip[self.sprite_idle_i]
                    self.sprite_idle_i = self.sprite_idle_i + 1 if self.sprite_idle_i < len(
                        self.assets.dino_idle) - 1 else 0

    def set_movement(self, controls, level_walls, movable_object_array):
        hit_vector = self.check_walls(level_walls)
        hit_vector2 = self.check_movable_objects(movable_object_array)
        running = True if controls.obj[self.player_num]['run'] else False
        speed = self.run_speed if running else self.walk_speed
        self.direction.x = 0
        self.direction.y = 0
        if controls.obj[self.player_num]['up'] and hit_vector.y != -1 and hit_vector2.y != -1:
            self.direction.x = 0
            self.direction.y = -1
            # speed = self.run_speed - .5 if running else self.walk_speed
        if controls.obj[self.player_num]['down'] and hit_vector.y != 1 and hit_vector2.y != 1:
            self.direction.x = 0
            self.direction.y = 1
            # speed = self.run_speed - .5 if running else self.walk_speed
        if controls.obj[self.player_num]['left'] and hit_vector.x != -1 and hit_vector2.x != -1:
            self.direction.x = -1
            self.direction.y = 0
        if controls.obj[self.player_num]['right'] and hit_vector.x != 1 and hit_vector2.x != 1:
            self.direction.x = 1
            self.direction.y = 0
        if self.direction.x != 0:
            self.last_direction.x = self.direction.x
        self.update_sprite(running)
        self.update_rects(self.direction * speed)

    def update_rects(self, move):
        # image rect
        self.rect.x += move.x
        self.rect.y += move.y
        # custom rect for feet
        self.feet_rect.x += move.x
        self.feet_rect.y += move.y
        # custom rect for entire upright body (not running)
        self.body_rect.x += move.x
        self.body_rect.y += move.y
        # torso only
        self.torso_rect.x += move.x
        self.torso_rect.y += move.y

    def check_movable_objects(self, rects):
        """
        check against torso_rect
        """
        hit = pygame.math.Vector2()
        for rect in rects:
            if rect.collidepoint(self.torso_rect.midtop):
                hit.y = -1
            if rect.collidepoint(self.torso_rect.midbottom):
                hit.y = 1
            if rect.collidepoint(self.torso_rect.midright):
                hit.x = 1
            if rect.collidepoint(self.torso_rect.midleft):
                hit.x = -1
        return hit

    def check_walls(self, level_walls):
        # right left up down
        hit = pygame.math.Vector2()
        for key, rect in level_walls.items():
            if "obstacle" in key:
                if rect.collidepoint(self.feet_rect.midtop):
                    hit.y = -1
                if rect.collidepoint(self.feet_rect.midbottom):
                    hit.y = 1
                if rect.collidepoint(self.feet_rect.midright):
                    hit.x = 1
                if rect.collidepoint(self.feet_rect.midleft):
                    hit.x = -1
            elif "border" in key:
                if not rect.collidepoint(self.feet_rect.midtop):
                    hit.y = -1
                if not rect.collidepoint(self.feet_rect.midbottom):
                    hit.y = 1
                if not rect.collidepoint(self.feet_rect.midright):
                    hit.x = 1
                if not rect.collidepoint(self.feet_rect.midleft):
                    hit.x = -1
        return hit

    def blit_player_rects(self, surface):
        """
        - used for debug
        """
        # pygame.draw.rect(surface, self.colors.red, self.rect, 1)
        pygame.draw.rect(surface, self.colors.green, self.body_rect, 1)
        # pygame.draw.rect(surface, self.colors.black, self.torso_rect, 1)
        # pygame.draw.rect(surface, self.colors.blue, self.feet_rect, 1)

    def update(self, surface, controls, level_walls, collidables=[]):
        self.set_movement(controls, level_walls, collidables)
        dust_path_queue = self.moving_dust.update_effect(surface, self.feet_rect, self.direction)
        # add dino image and dino shadow image to queue
        return dust_path_queue + [
            {'layer': 3, 'type': 'image', 'image': self.assets.dino_shadow, 'color': (0, 0, 0),
             'rect': self.empty_rect, 'pos': self.rect.topleft, 'radius': 0},
            {'layer': 4, 'type': 'image', 'image': self.img, 'color': (0, 0, 0), 'rect': self.empty_rect,
             'pos': self.rect.topleft, 'radius': 0}
        ]
