import pygame
from math import hypot
import json
from random import randint, choice
from datetime import datetime
from fonts import Font
import numpy as np


class SpriteSheet(object):
    """ Class used to grab images out of a sprite sheet. """

    def __init__(self, file_name):
        """ Constructor. Pass in the file name of the sprite sheet. """
        # Load the sprite sheet.
        self.sprite_sheet = pygame.image.load(file_name).convert()

    def get_image(self, x, y, width, height, color_key=(0, 0, 0)):
        """ Grab a single image out of a larger spritesheet
            Pass in the x, y location of the sprite
            and the width and height of the sprite. """
        # Create a new blank image
        image = pygame.Surface([width, height]).convert()
        # Copy the sprite from the large sheet onto the smaller image
        image.blit(self.sprite_sheet, (0, 0), (x, y, width, height))
        # Assuming black works as the transparent color
        image.set_colorkey(color_key)
        # Return the image
        return image


class OceanParticleAffect:
    def __init__(self, general, num=25, primary_color=(111, 166, 165), secondary_color=(255, 255, 255)):
        self.primary_color = primary_color
        self.secondary_color = secondary_color
        self.level_rect = general.screen_surface.get_rect()
        # particle weight counter
        self.timer = datetime.now()
        self.index = 0
        # last zoom scale
        self.last_zoom_scale = 4
        self.water_speed_in_1000 = 1000
        # generate particles
        self.particles = []
        self.particles_append = self.particles.append
        self.add_particles(num)

    def add_particles(self, num, rand=True):
        for i in range(num):
            if rand:
                pos = pygame.math.Vector2((randint(self.level_rect.x, self.level_rect.w),
                                           randint(self.level_rect.y, self.level_rect.h)))
            else:
                pos = pygame.math.Vector2((self.level_rect.w + randint(1, 10),
                                           randint(self.level_rect.y, self.level_rect.h)))
            color = choice(
                [self.primary_color, self.primary_color, self.primary_color, self.secondary_color, (127, 127, 127), ])
            rand_int = randint(1, 3)
            dir = choice((['left']) + ['down', 'up'])
            self.particles_append([pygame.Rect(pos.x, pos.y, rand_int * 2, rand_int), color, dir])

    def blit_particles(self, screen_surface, zoom_scale, controls):
        for index, arr in enumerate(self.particles, 0):
            arr[0].x -= randint(1, 2) / choice([10, 100, 1000, 1000, 1000])
            if arr[2] == 'down' and choice([True, False, False, False]):
                arr[0].y += randint(0, 5) / 10000
            elif arr[2] == 'up' and choice([True, False, False, False]):
                arr[0].y -= randint(0, 5) / 10000
            if self.last_zoom_scale != zoom_scale:
                if controls.obj['1']['zoom_in']:
                    arr[0].y += zoom_scale / 5
                    # all particles above center
                    # if arr[0].y >= self.level_rect.h / 2:
                    #     arr[0].y += zoom_scale / 5
                    #     # all particles below center
                    # elif arr[0].y < self.level_rect.h / 2:
                    #     arr[0].y -= zoom_scale / 5
                if controls.obj['1']['zoom_out']:
                    # if arr[0].y < self.level_rect.h / 2:
                    #     arr[0].y += zoom_scale / 5
                    # elif arr[0].y > self.level_rect.h / 2:
                    arr[0].y -= zoom_scale / 5
            pygame.draw.rect(screen_surface, arr[1], (arr[0].x, arr[0].y, arr[0].w + (zoom_scale * 2), arr[0].h + (zoom_scale * 2)))
            if arr[0].left <= self.level_rect.left or arr[0].top <= self.level_rect.top or arr[
                0].bottom >= self.level_rect.bottom:
                try:
                    self.add_particles(1, rand=False)
                    del self.particles[index]
                except:
                    self.add_particles(1, rand=False)
                    del self.particles[index]
        self.last_zoom_scale = zoom_scale


class PlayerAssets:
    def __init__(self, player_num):
        # player bubbles
        self.sheet_bubble = SpriteSheet('assets/dinoSprites/p1p2bubbles.png')
        self.p1_bubble = self.sheet_bubble.get_image(0, 0, 14, 14)
        self.p2_bubble = self.sheet_bubble.get_image(0, 14, 14, 14)
        self.p1_bubble_rect = self.p1_bubble.get_rect()
        self.p2_bubble_rect = self.p2_bubble.get_rect()
        # no conversion to keep transparency
        self.dino_shadow = pygame.image.load('assets/dinoSprites/shadow.png')
        # blue dino for player 1 and red for player 2
        idle, walk, hit, white, run = self.get_sprite_list(
            'assets/dinoSprites/blue' if player_num == 1 else 'assets/dinoSprites/red')
        self.dino_idle, self.dino_walk, self.dino_hit, self.dino_all_white, self.dino_run = idle, walk, hit, white, run
        self.dino_idle_flip = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in idle]
        self.dino_walk_flip = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in walk]
        self.dino_hit_flip = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in hit]
        self.dino_all_white_flip = pygame.transform.flip(white, flip_x=True, flip_y=False)
        self.dino_run_flip = [pygame.transform.flip(i, flip_x=True, flip_y=False) for i in run]

    def read_json_file(self, path):
        output = ""
        with open(path) as f:
            for line in f:
                output += line
        return json.loads(output)

    def get_sprite_list(self, path):
        sheet = SpriteSheet(f"{path}/dino.png")
        sheet_map = self.read_json_file(f"{path}/dino.json")
        frames = [sheet_map['frames'][key]['frame'] for key in sheet_map['frames'].keys()]
        images = [sheet.get_image(i['x'], i['y'], i['w'], i['h'], color_key=(0, 0, 0)) for i in frames]
        return images[0:4], images[5:11], images[14:16], images[16], images[18:24]


class WalkingEffect:
    """
    - All items blitted are queued are accessed by self.queue
    """

    def __init__(self):
        self.white = (255, 255, 255)
        self.light_gray = (225, 225, 225)
        # self.green_gray = (137, 142, 79)
        self.green_gray = (132, 137, 77)
        self.items = []
        self.step = []
        self.smoke_timer = datetime.now()
        self.step_timer = datetime.now()
        self.step_index = 0
        # emprty rect for queue
        self.empty_rect = pygame.Rect(0, 0, 0, 0)

    def update_effect(self, surface, rect, direction):
        """
        :param surface:
        :param rect - from feet of character:
        :param moving - vector direction:
        :return:
        """
        queue = []
        queue_append = queue.append
        # calculate character steps
        if (datetime.now() - self.step_timer).total_seconds() > .05:
            self.step_timer = datetime.now()
            self.step_index += 1
            if direction.y == 0:
                xy = pygame.math.Vector2((0, 0 if self.step_index % 2 == 0 else 1))
                self.step.append({'pos': rect.center - xy, 'dt': datetime.now()})
            elif direction.x == 0:
                xy = pygame.math.Vector2((0 if self.step_index % 2 == 0 else 1, 0))
                self.step.append({'pos': rect.center + xy, 'dt': datetime.now()})
        for i, v in enumerate(self.step, 0):
            # add foot steps to queue
            queue_append({'layer': 0, 'type': 'rect', 'image': False, 'color': self.green_gray,
                          'rect': pygame.Rect(v['pos'][0], v['pos'][1], 2, 2), 'pos': (0, 0), 'radius': 0})
            if (datetime.now() - v['dt']).total_seconds() > 3:
                del self.step[i]
        # calculate character dust
        if (datetime.now() - self.smoke_timer).total_seconds() > randint(5, 8) / 70 and direction != (0, 0):
            self.smoke_timer = datetime.now()
            rand_int = randint(2, 3)
            rand_x, rand_y = rect.centerx - (direction.x * 7), rect.centery - randint(0, 4)
            self.items.append(
                {'center': (rand_x, rand_y), 'radius': rand_int, 'color': choice([self.white, self.light_gray])})
        for i, v in enumerate(self.items, 0):
            self.items[i]['radius'] -= .1 if direction == (0, 0) else .2
            # add large white circle and small gray circle to queue
            queue_append({'layer': 0, 'type': 'circle', 'image': False, 'color': v['color'], 'rect': self.empty_rect,
                          'pos': v['center'], 'radius': v['radius'], 'width': 0})
            queue_append(
                {'layer': 0, 'type': 'circle', 'image': False, 'color': self.light_gray, 'rect': self.empty_rect,
                 'pos': v['center'], 'radius': v['radius'] - 1, 'width': 0})
            if v['radius'] <= 0.0:
                del self.items[i]
        return queue


class Explosion:
    def __init__(self, width=15, radius=1, color=(255, 255, 255), sec_color=(255, 200, 200)):
        self.color = color
        self.start = False
        self.width = width
        self.exp_index = -1
        self.center = pygame.math.Vector2()
        self.radius = radius
        self.second_color = sec_color
        self.hit_box_rect = pygame.Rect(0, 0, 0, 0)
        self.empty_rect = pygame.Rect(0, 0, 0, 0)

    def initiate(self, center_pos):
        self.center.x = center_pos[0]
        self.center.y = center_pos[1]
        self.start = True
        self.exp_index = 0

    def iterate(self, offset=(0, 0)):
        queue = {'layer': -100, 'type': 'circle', 'image': False, 'color': (255, 255, 255),
                 'rect': self.empty_rect, 'pos': self.center,
                 'radius': 0, 'angle': (0, 0), 'dir': -1, 'hit': 0, 'width': 0}
        if self.start:
            if self.width >= 1:
                complete_offset = self.center - offset
                self.radius += round(self.exp_index)
                self.width -= round(self.exp_index)
                self.exp_index = self.exp_index + .08 if self.width > 3 else self.exp_index + .01
                queue = {'layer': 99, 'type': 'circle', 'image': False,
                         'color': choice([self.color, self.second_color]),
                         'rect': self.empty_rect, 'pos': self.center if offset != (0, 0) else complete_offset,
                         'radius': self.radius, 'angle': (0, 0), 'dir': -1, 'hit': 0, 'width': self.width}
                self.hit_box_rect.x = complete_offset[0] - (self.radius / 2)
                self.hit_box_rect.y = complete_offset[1] - (self.radius / 2)
                self.hit_box_rect.w = self.radius
                self.hit_box_rect.h = self.radius

            elif self.width <= 0:
                self.start = False
                self.width = 15
                self.exp_index = 0
                self.center = pygame.math.Vector2()
                self.radius = 1
        return [queue]


class Colors:
    def __init__(self):
        self.red = (255, 0, 0)
        self.green = (0, 255, 0)
        self.blue = (0, 0, 255)
        self.light_yellow = (244, 255, 69)
        self.green_forest = (85, 128, 85)
        self.green_plains = (139, 145, 80)
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)

    def flash(self):
        return choice([self.white, self.light_yellow, self.red])


class WallAssets:
    def __init__(self):
        pass


class DecorationAssets:
    def __init__(self):
        # font
        self.font = Font(15)
        # wooden sign with width
        self.wooden_sign = pygame.image.load('assets/levels/decoration/wooden_sign.png').convert()
        self.wooden_sign.set_colorkey((0, 0, 0))
        self.wooden_sign_on_rock = pygame.image.load('assets/levels/decoration/sign_on_rock.png').convert()
        self.wooden_sign_on_rock.set_colorkey((0, 0, 0))
        self.grass_sheet = SpriteSheet('assets/levels/decoration/grass.png')
        self.grass = self.grass_sheet.get_image(0, 0, 7, 7).convert()
        self.grass.set_colorkey((255, 255, 255))
        self.grass1 = self.grass_sheet.get_image(7, 0, 7, 7).convert()
        self.grass1.set_colorkey((255, 255, 255))
        self.grass2 = self.grass_sheet.get_image(14, 0, 7, 7).convert()
        self.grass2.set_colorkey((255, 255, 255))
        self.grass3 = self.grass_sheet.get_image(21, 0, 7, 7).convert()
        self.grass3.set_colorkey((255, 255, 255))
        self.grass4 = self.grass_sheet.get_image(28, 0, 7, 7).convert()
        self.grass4.set_colorkey((255, 255, 255))
        self.grass5 = self.grass_sheet.get_image(35, 0, 7, 7).convert()
        self.grass5.set_colorkey((255, 255, 255))
        self.grasses = [self.grass, self.grass1, self.grass2, self.grass4, self.grass5] + ([self.grass3] * 20)


class ControlsAssets:
    def __init__(self):
        self.font = Font(40)
        self.large_font = Font(50)


class DinoDemoAssets:
    def __init__(self, general):
        self.guns = GunAssets()
        self.particles = OceanParticleAffect(general)
        self.decorations = DecorationAssets()
        self.level_images = [
            pygame.image.load('assets/levels/demo/demo0.png'),
            pygame.image.load('assets/levels/demo/demo1.png'),
            pygame.image.load('assets/levels/demo/demo2.png'),
            pygame.image.load('assets/levels/demo/demo3.png')
        ]
        self.level_wall_upper = pygame.image.load('assets/levels/demo/upper_wall.png').convert()
        self.level_wall_upper.set_colorkey((0, 0, 0))
        self.level_wall_bottom = pygame.image.load('assets/levels/demo/bottom_wall.png').convert()
        self.level_wall_bottom.set_colorkey((0, 0, 0))


class GunAssets:
    def __init__(self):
        self.explosion1 = Explosion()
        self.explosion2 = Explosion()
        self.colors = Colors()
        self.cross_hair = CrossHairsByPos()
        self.bullet_sheet = SpriteSheet('assets/bullet.png')
        self.bullet = self.bullet_sheet.get_image(0, 0, 16, 16)
        self.bullet_rect = pygame.Rect(9, 4, 4, 3)
        self.sheet = SpriteSheet('assets/guns.png')
        scale = 12
        self.gun1 = pygame.transform.scale(self.sheet.get_image(0, 0, 16, 16), (scale, scale))
        self.gun2 = pygame.transform.scale(self.sheet.get_image(16, 0, 16, 16), (scale, scale))
        self.gun3 = pygame.transform.scale(self.sheet.get_image(0, 16, 16, 16), (scale, scale))
        self.gun4 = pygame.transform.scale(self.sheet.get_image(16, 16, 16, 16), (scale, scale))
        self.all_guns = [self.gun1, self.gun2, self.gun3, self.gun4]


class CrossHairs:
    def __init__(self):
        pygame.mouse.set_visible(False)
        self.timer = datetime.now()
        self.inner_rect = pygame.Rect(0, 0, 5, 5)
        self.outer_rect = pygame.Rect(0, 0, 21, 21)
        self.outer_rect_index = 3
        self.dotted_line_offset = pygame.math.Vector2((0, 3))
        # self.center_offset = pygame.math.Vector2((-30, -50))

    def update(self, surface):
        self.inner_rect.center = pygame.mouse.get_pos()
        self.outer_rect.center = self.inner_rect.center
        pygame.draw.rect(surface, (255, 255, 255), self.inner_rect)
        if (datetime.now() - self.timer).total_seconds() > .3:
            self.timer = datetime.now()
            if self.outer_rect_index < 5:
                self.outer_rect_index += 1
            else:
                self.outer_rect_index = 3
        pygame.draw.rect(surface, (255, 255, 255), self.outer_rect, self.outer_rect_index)


class CrossHairsByPos:
    def __init__(self, size=1):
        pygame.mouse.set_visible(False)
        self.size = size
        self.timer = datetime.now()
        self.inner_rect = pygame.Rect(0, 0, 1, 1)
        self.outer_rect = pygame.Rect(0, 0, 7, 7)
        self.outer_rect_index = 1
        self.dotted_line_offset = pygame.math.Vector2((0, 3))
        self.pos = (0, 0)

    def hit_boundary(self, level_rect, pos):
        if not level_rect.collidepoint((pos[0], pos[1] + 4)):
            return True
        if not level_rect.collidepoint((pos[0], pos[1] - 4)):
            return True
        if not level_rect.collidepoint((pos[0] + 4, pos[1])):
            return True
        if not level_rect.collidepoint((pos[0] - 4, pos[1])):
            return True
        return False

    def update(self, pos, level_rect):
        # if not self.hit_boundary(level_rect, pos):
        #     # update self.pos if boundary not hit
        #     self.pos = pos
        self.inner_rect.center = pos
        self.outer_rect.center = self.inner_rect.center
        if (datetime.now() - self.timer).total_seconds() > .6:
            self.timer = datetime.now()
            if self.outer_rect_index <= 1:
                self.outer_rect_index += 1
            else:
                self.outer_rect_index = 1
        return [{'layer': 1000, 'type': 'rect', 'image': False, 'color': (255, 255, 255),
                 'rect': self.inner_rect, 'pos': (0, 0), 'radius': 0},
                {'layer': 1000, 'type': 'rect', 'image': False, 'color': (255, 255, 255),
                 'rect': self.outer_rect, 'pos': (0, 0), 'radius': self.outer_rect_index}]


class CameraAssets:
    def __init__(self):
        self.font = Font(25)


class Point:
    def __init__(self, point):
        self.x = point[0]
        self.y = point[1]
        self.slope = 0

    def __add__(self, other):
        return Point((self.x + other.x, self.y + other.y))

    def __sub__(self, other):
        return Point((self.x - other.x, self.y - other.y))

    def __mul__(self, scalar):
        return Point((self.x * scalar, self.y * scalar))

    def __truediv__(self, scalar):
        if scalar == 0:
            scalar = .01
        return Point((self.x / scalar, self.y / scalar))

    def __len__(self):
        return int(hypot(self.x, self.y))

    def get(self):
        return (self.x, self.y)


def get_angle(start_pos, end_pos):
    origin = Point(start_pos)
    target = Point(end_pos)
    displacement = target - origin
    length = len(displacement)
    slope = displacement / length
    start = origin + (slope * 0)
    end = origin + (slope * (int(length) + 1))
    start = start.get()
    end = end.get()
    return np.rad2deg(np.arctan2(end[1] - start[1], end[0] - start[0])) * -1, slope.get()
