from datetime import datetime
import pygame
from assets import GunAssets, get_angle
from random import choice


class Gun:
    def __init__(self, player_num, level_rect):
        self.player_num = player_num
        self.level_rect = level_rect
        self.assets = GunAssets()
        self.all_guns = self.assets.all_guns
        self.gun_img = self.all_guns[3]
        self.rect = self.gun_img.get_rect()
        self.torso_rect_offset = pygame.math.Vector2((-5, -7))
        # bullets
        self.max_bullets = 5
        self.bullet_speed = 1
        self.bullets = []
        self.bullet_timer = datetime.now()
        self.last_bullet_direction = pygame.math.Vector2()
        # fake rect
        self.empty_rect = pygame.Rect(0, 0, 0, 0)

    def update_bullet_hits(self, b_obj, b_index, r):
        self.bullets[b_index]['hit'] += 1
        print(self.bullets[b_index]['hit'])
        if self.bullets[b_index]['hit'] == 1:
            print("------------")
            print(self.bullets[b_index]['pos'], self.bullets[b_index]['dir'], self.bullets[b_index]['angle'])
            # if r.left <= lr.left:
            #     self.dir = pygame.math.Vector2((self.dir.x * -1, self.dir.y))
            # elif r.right >= lr.right:
            #     self.dir = pygame.math.Vector2((self.dir.x * -1, self.dir.y))
            # elif r.bottom >= lr.bottom:
            #     self.dir = pygame.math.Vector2((self.dir.x, self.dir.y * -1))
            # elif r.top <= lr.top:
            #     self.dir = pygame.math.Vector2((self.dir.x, self.dir.y * -1))
            if b_obj['pos'].x > r.midleft[0] or b_obj['pos'] < r.midright[0]:
                self.bullets[b_index]['angle'] = (self.bullets[b_index]['angle'][0] * -1, self.bullets[b_index]['angle'][1])
            if b_obj['pos'].y > r.midtop[1] or b_obj['pos'].y < r.midbottom[1]:
                self.bullets[b_index]['angle'] = (self.bullets[b_index]['angle'][0] * -1, self.bullets[b_index]['angle'][1] * -1)
            print(self.bullets[b_index]['pos'], self.bullets[b_index]['dir'], self.bullets[b_index]['angle'])
        elif self.bullets[b_index]['hit'] == 2:
            try:
                del self.bullets[b_index]
            except:
                del self.bullets[b_index]

    def update_bullets(self, walls, controls, slope, crosshair_pos, gun_pos, character_direction, moving_obj_classes=[]):
        # add bullet if space is press
        if controls.obj[self.player_num]['space']:
            # check bullet timer and add bullets
            if (datetime.now() - self.bullet_timer).total_seconds() > .2:
                self.bullet_timer = datetime.now()
                if len(self.bullets) < self.max_bullets:
                    self.bullets.append({'layer': 2, 'type': 'circle', 'image': False, 'color': (38, 43, 68),
                                         'rect': pygame.Rect(crosshair_pos[0], crosshair_pos[1], 4, 3),
                                         'pos': pygame.math.Vector2((gun_pos[0] + 8, gun_pos[1] + 8)),
                                         'radius': 1, 'angle': slope, 'dir': character_direction.x, 'hit': 0})
                    self.bullets.append({'layer': 2, 'type': 'rect', 'image': False, 'color': (0, 255, 0),
                                         'rect': pygame.Rect(gun_pos[0] + 8, gun_pos[1] + 8, 4, 3),
                                         'pos': pygame.math.Vector2((crosshair_pos[0], crosshair_pos[1])),
                                         'radius': 0, 'angle': slope, 'dir': character_direction.x, 'hit': 0})
        # update existing bullets
        for b_index, b_obj in enumerate(self.bullets, 0):
            # bullet is a circle
            if b_obj['type'] == 'circle':
                # move bullet
                b_obj['pos'] += [(i * self.bullet_speed) * b_obj['dir'] for i in b_obj['angle']]
                # check bullets against borders and obstacles
                for key, rect in walls.items():
                    if key == "border_bullets":
                        if not rect.collidepoint(b_obj['pos']):
                            self.update_bullet_hits(b_obj, b_index, rect)
                    if "obstacle" in key:
                        if rect.collidepoint(b_obj['pos']):
                            self.update_bullet_hits(b_obj, b_index, rect)
            if b_obj['type'] == 'rect':
                # move bullet
                x, y = [(i * self.bullet_speed) * b_obj['dir'] for i in b_obj['angle']]
                b_obj['rect'].centerx += x
                b_obj['rect'].centery += y
                # check bullets against borders and obstacles
                for key, rect in walls.items():
                    if key == "border_bullets":
                        if not rect.colliderect(b_obj['rect']):
                            print("hit")
                            # self.update_bullet_hits(b_obj, b_index, rect)
                    if "obstacle" in key:
                        if rect.colliderect(b_obj['rect']):
                            print("hit")
                            # self.update_bullet_hits(b_obj, b_index, rect)

                # for c_index, c_obj in enumerate(moving_obj_classes, 0):
                #     if self.bullets[b_index]['rect'].colliderect(c_obj.body_rect):
                #         print("hit")

        return self.bullets

    def update(self, walls, body_rect, torso_rect, zoom_scale, character_direction, controls, moving_obj_classes=[]):
        """
        - Called from minigame class
        """
        # crosshair stuff
        x, y = pygame.mouse.get_pos()
        # close if follows mouse movement but is off because of different dimensions of level and window
        end_pos = (x - self.level_rect.w) / zoom_scale, (y - self.level_rect.h) / zoom_scale
        start_pos = self.level_rect.x + torso_rect.centerx, self.level_rect.y + torso_rect.centery
        # self.assets.cross_hair.update(surface, end_pos)
        cross_hair_array = self.assets.cross_hair.update(end_pos, self.level_rect)
        # gun stuff
        self.rect.center = torso_rect.center + self.torso_rect_offset
        gun_pos = self.rect.center
        if character_direction.x == -1:
            gun_img = pygame.transform.flip(self.gun_img, True, False)
            self.torso_rect_offset.x = -7
            angle, slope = get_angle(end_pos, start_pos)
        else:
            # last character direction 1 is set in the init of player class
            gun_img = self.gun_img
            self.torso_rect_offset.x = -5
            angle, slope = get_angle(start_pos, end_pos)
        # angles gun based on cross hairs
        gun_img = pygame.transform.rotate(gun_img, angle)
        # update bullets trajectory, deletion, creation, and collision is handled in the minigame class
        bullets_list = self.update_bullets(walls, controls, slope, end_pos, gun_pos, character_direction, moving_obj_classes)
        # -1 makes sure the gun is behind the player
        return [
                   #    {'layer': -1 if character_direction.x == -1 else 6,
                   #  'type': 'image', 'image': self.assets.bullet, 'color': (0, 0, 0),
                   #  'rect': self.assets.bullet_rect, 'pos': (0, 0), 'radius': 0},
                   # {'layer': -1 if character_direction.x == -1 else 5,
                   #  'type': 'rect', 'image': False, 'color': (0, 255, 0),
                   #  'rect': self.assets.bullet_rect, 'pos': (0, 0), 'radius': 1},
                   {'layer': -1 if character_direction.x == -1 else 5,
                    'type': 'image', 'image': gun_img, 'color': (0, 0, 0),
                    'rect': self.rect, 'pos': gun_pos, 'radius': 0}] + cross_hair_array + bullets_list
