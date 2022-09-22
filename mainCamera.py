import pygame
from miniGameHandler import Handler
from assets import CameraAssets


class SpriteGroup(pygame.sprite.Group):
    def __init__(self, general, colors):
        super().__init__()
        self.sounds = general.sounds
        self.general = general
        self.colors = colors
        self.assets = CameraAssets()

        # camera zoom
        self.zoom_scale = 4

        # level assets
        self.handler = Handler(self.general, self.colors)
        self.level_rect = self.handler.level_rect
        self.level_vector = pygame.math.Vector2(self.level_rect.size)
        self.level_vector_zoomed = self.level_vector * self.zoom_scale

        # create new surface for camera and keep all colors.
        self.screen_surface = self.general.screen_surface
        self.screen_surface_size = pygame.math.Vector2(self.screen_surface.get_size())
        self.camera_surface = pygame.Surface(self.level_rect.size, pygame.SRCALPHA)

    def get_camera_zoom(self, controls):
        if self.level_vector_zoomed.x >= self.screen_surface_size.x or self.level_vector_zoomed.y >= self.screen_surface_size.y:
            self.zoom_scale -= 0.02
        if controls.obj['1']['zoom_out']:
            self.zoom_scale += 0.02
        if controls.obj['1']['zoom_in']:
            self.zoom_scale -= 0.02
        self.zoom_scale = 2 if self.zoom_scale <= 2 else self.zoom_scale
        # self.zoom_scale = 6 if self.zoom_scale >= 6 else self.zoom_scale
        self.level_vector_zoomed = pygame.math.Vector2(self.level_rect.size) * self.zoom_scale

    def blit_screen_surface(self, controls):
        self.get_camera_zoom(controls)
        scaled_camera_surf = pygame.transform.scale(self.camera_surface, self.level_vector_zoomed)
        half_screen = pygame.math.Vector2(self.screen_surface_size) / 2
        # applies scaled camera surface to center of main screen
        self.screen_surface.blit(scaled_camera_surf, (half_screen.x - (self.level_vector_zoomed.x / 2),
                                                      half_screen.y - (self.level_vector_zoomed.y / 2)))
        self.blit_fps(self.screen_surface)
        self.blit_zoom(self.screen_surface, controls)

    def blit_fps(self, surface):
        text = self.assets.font.bold.render(f"FPS: {round(self.general.clock.get_fps(), 2)}", True, self.colors.white)
        surface.blit(text, (10, surface.get_height() - 10 - text.get_height()))

    def blit_zoom(self, surface, controls):
        if controls.obj['1']['zoom_out'] or controls.obj['1']['zoom_in']:
            text = self.assets.font.bold.render(f"Zoom: {round(self.zoom_scale, 2)}", True, self.colors.white)
            surface.blit(text, (10, surface.get_height() - 10 - (text.get_height() * 2)))

    # def blit_message(self, surface):
    #     """
    #     blit message splits message up into smaller messages if \n is mentioned
    #     """
    #     array = self.message.split("\n")
    #     queue = []
    #     queue_append = queue.append
    #     y_vector = pygame.math.Vector2()
    #     # queue_append({'layer': 7, 'type': 'rect', 'image': 0, 'color': (0, 0, 0),
    #     #               'rect': self.assets.wooden_sign_rect,
    #     #               'pos': level_rect.center, 'radius': 0})
    #     for index, message in enumerate(array, 0):
    #         text = self.assets.font.bold.render(f"{self.message}", True, (255, 255, 255))
    #         y_vector.y = text.get_height() * index + 3
    #         queue_append({'layer': 8, 'type': 'image', 'image': text, 'color': (0, 0, 0),
    #                   'rect': text.get_rect(),
    #                   'pos': surface. + y_vector, 'radius': 0})

    def camera(self, controls):
        # show defined fill color for level.
        self.general.screen_surface.fill(self.handler.mini_game.screen_fill_color)

        # update mini game.
        self.handler.mini_game.update(self.camera_surface, controls, self.zoom_scale)

        self.blit_screen_surface(controls)
        controls.blit_controller_message()


        # message block
        # r = pygame.Rect(200, self.screen_surface_size[1] - 200, self.screen_surface_size[0] - 400, 190)
        # pygame.draw.rect(self.screen_surface, (200, 200, 200), r)
        # r = pygame.Rect(205, self.screen_surface_size[1] - 195, self.screen_surface_size[0] - 410, 180)
        # pygame.draw.rect(self.screen_surface, (255, 255, 255), r)

        # self.assets.cross.update(self.screen_surface)
