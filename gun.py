from datetime import datetime
import pygame
from assets import GunAssets, get_angle
from random import choice


class Gun:
    def __init__(self, player_num, level_rect, sounds):
        self.sounds = sounds
        self.player_num = player_num
        self.level_rect = level_rect
        self.assets = GunAssets()
        self.all_guns = self.assets.all_guns
        self.gun_img = self.all_guns[2]
        self.rect = self.gun_img.get_rect()
        self.torso_rect_offset = pygame.math.Vector2((-7, -9))
        # bullets will be 5 bullets, due to smoke affect that follows bullets
        self.max_bullets = 10
        self.bullet_speed = 2
        self.bullets = []
        self.bullet_timer = datetime.now()
        self.last_bullet_direction = pygame.math.Vector2()
        # fake rect
        self.empty_rect = pygame.Rect(0, 0, 0, 0)

    def delete_bullet_obj_by_index(self, b_index):
        try:
            del self.bullets[b_index]
        except:
            del self.bullets[b_index]

    def update_bullet_hits(self, b_obj, b_index, r):
        self.bullets[b_index]['hit'] += 1
        if self.bullets[b_index]['hit'] == 1:
            self.sounds.play_hit_wall()
            # add bullet bounce affect
            self.bullets.append({'layer': 100, 'type': 'circle', 'image': False, 'color': (255, 255, 255),
                                 'rect': b_obj['rect'],
                                 'pos': b_obj['pos'],
                                 'radius': 5, 'angle': b_obj['angle'], 'dir': b_obj['dir'], 'hit': 0, 'width': 0})
            if b_obj['rect'].left <= r.left:
                self.bullets[b_index]['angle'] = (b_obj['angle'][0] * -1, b_obj['angle'][1])
            elif b_obj['rect'].right >= r.right:
                self.bullets[b_index]['angle'] = (b_obj['angle'][0] * -1, b_obj['angle'][1])
            elif b_obj['rect'].bottom >= r.bottom:
                self.bullets[b_index]['angle'] = (b_obj['angle'][0], b_obj['angle'][1] * -1)
            elif b_obj['rect'].top <= r.top:
                self.bullets[b_index]['angle'] = (b_obj['angle'][0], b_obj['angle'][1] * -1)
        elif self.bullets[b_index]['hit'] == 2:
            self.sounds.play_fart()
            # add bullet bounce affect
            self.bullets.append({'layer': 100, 'type': 'circle', 'image': False, 'color': (255, 255, 255),
                                 'rect': b_obj['rect'], 'pos': b_obj['pos'], 'radius': 5,
                                 'angle': b_obj['angle'], 'dir': b_obj['dir'], 'hit': 0, 'width': 0})
            self.delete_bullet_obj_by_index(b_index)

    def update_bullets(self, walls, controls, slope, crosshair_pos, gun_pos, gun_img, character_direction,
                       moving_obj_classes=[]):
        # add bullet if space is press
        if controls.obj[self.player_num]['space']:
            # check bullet timer and add bullets
            if (datetime.now() - self.bullet_timer).total_seconds() > .2:
                self.bullet_timer = datetime.now()
                if len(self.bullets) < self.max_bullets:
                    self.sounds.play_shot()
                    gun_rect = pygame.Rect(gun_pos[0] + 8, gun_pos[1] + 8, 2, 2)
                    gun_pos = pygame.math.Vector2((gun_pos[0] + 8, gun_pos[1] + 8))
                    # bullet image
                    self.bullets.append(
                        {'layer': -1, 'type': 'image', 'image': self.assets.bullet, 'color': (38, 43, 68),
                         'rect': gun_rect, 'pos': gun_pos, 'radius': 0,
                         'angle': slope, 'dir': character_direction.x, 'hit': 0})
                    # init explosion out of gun, gets deleted really quickly.
                    self.bullets.append({'layer': 100, 'type': 'circle', 'image': False, 'color': (255, 255, 255),
                                         'rect': gun_rect, 'pos': gun_pos, 'radius': 5,
                                         'angle': slope, 'dir': character_direction.x, 'hit': 0, 'width': 0})

        # update existing bullets

        for b_index, b_obj in enumerate(self.bullets, 0):
            # bullet is a circle
            if b_obj['type'] == 'image':
                # move bullet
                if choice([True, False, False]):
                    if character_direction.x == -1:
                        pos = (b_obj['pos'][0] + (b_obj['angle'][0] * 3), b_obj['pos'][1] + (b_obj['angle'][1] * 3))
                    else:
                        pos = (b_obj['pos'][0] - (b_obj['angle'][0] * 3), b_obj['pos'][1] - (b_obj['angle'][1] * 3))
                    self.bullets.append({'layer': 1, 'type': 'circle', 'image': False, 'color': (255, 255, 255),
                                         'rect': self.empty_rect, 'pos': pos, 'radius': 3,
                                         'angle': slope, 'dir': character_direction.x, 'hit': 0, 'width': 0})
                b_obj['pos'] += [(i * self.bullet_speed) * b_obj['dir'] for i in b_obj['angle']]
                b_obj['rect'].centerx = b_obj['pos'][0]
                b_obj['rect'].centery = b_obj['pos'][1]
                # check bullets against borders and obstacles
                for key, rect in walls.items():
                    if key == "border_bullets":
                        if not rect.colliderect(b_obj['rect']):
                            self.update_bullet_hits(b_obj, b_index, rect)
                    if "obstacle" in key:
                        if rect.colliderect(b_obj['rect']):
                            self.update_bullet_hits(b_obj, b_index, rect)
            elif b_obj['type'] == 'circle':
                b_obj['radius'] -= 1
                if b_obj['radius'] <= 0:
                    self.delete_bullet_obj_by_index(b_index)
            for c_index, c_obj in enumerate(moving_obj_classes, 0):
                if b_obj['rect'].colliderect(c_obj.body_rect):
                    if not self.assets.explosion1.start:
                        self.assets.explosion1.initiate(b_obj['pos'])
                    else:
                        self.assets.explosion2.initiate(b_obj['pos'])
                    c_obj.update_hit()
                    self.sounds.play_hurt()
                    self.delete_bullet_obj_by_index(b_index)
        explosion_queue = self.assets.explosion1.iterate()
        return self.bullets + explosion_queue

    def update(self, walls, body_rect, torso_rect, zoom_scale, character_direction, controls, moving_obj_classes=[]):
        """
        - Called from minigame class
        """
        # crosshair stuff
        x, y = controls.obj[self.player_num]['motion']
        # x, y = pygame.mouse.get_pos()
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
        bullets_list = self.update_bullets(walls, controls, slope, end_pos, gun_pos, gun_img, character_direction,
                                           moving_obj_classes)
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
