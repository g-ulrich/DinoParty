import pygame


class Controls:
    def __init__(self):
        pygame.joystick.init()
        self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count()) if
                          "xbox" in pygame.joystick.Joystick(i).get_name().lower()]
        self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"
        self.obj = {'pressed': [],
                    '1': {'up': False, 'down': False, 'right': False,
                           'left': False, 'space': False, 'run': False, 'esc': False,
                           'restart': False, 'zoom_in': False, 'zoom_out': False},
                    '2': {'up': False, 'down': False, 'right': False,
                           'left': False, 'space': False, 'run': False, 'esc': False,
                           'restart': False, 'zoom_in': False, 'zoom_out': False}
                    }

    def start_rumble(self, duration=1):
        [i.rumble(1.0, 1.0, duration) for i in self.joysticks]

    def stop_rumble(self):
        [i.stop_rumble() for i in self.joysticks]

    def update_joysticks(self, event):
        if event.type == pygame.JOYDEVICEADDED:
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"
        if event.type == pygame.JOYDEVICEREMOVED:
            self.joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
            self.controller_type = [i.get_name() for i in self.joysticks][0] if self.joysticks else "Keyboard"

    def activated_pressed(self, pressed):
        # computer keys pressed
        self.obj['pressed'] = pressed
        if not self.joysticks:
            # player 1
            self.obj['1']['left'] = True if pressed[pygame.K_LEFT] else False
            self.obj['1']['down'] = True if pressed[pygame.K_DOWN] else False
            self.obj['1']['up'] = True if pressed[pygame.K_UP] else False
            self.obj['1']['right'] = True if pressed[pygame.K_RIGHT] else False
            self.obj['1']['run'] = True if pressed[pygame.K_c] else False
            self.obj['1']['space'] = True if pressed[pygame.K_SPACE] else False

            # player 2
            self.obj['2']['left'] = True if pressed[pygame.K_a] else False
            self.obj['2']['down'] = True if pressed[pygame.K_s] else False
            self.obj['2']['up'] = True if pressed[pygame.K_w] else False
            self.obj['2']['right'] = True if pressed[pygame.K_d] else False
            self.obj['2']['run'] = True if pressed[pygame.K_z] else False
            self.obj['2']['space'] = True if pressed[pygame.K_x] else False

            # both p1 and p2
            if pressed[pygame.K_r]:
                self.obj['1']['restart'] = True
                self.obj['2']['restart'] = True
            else:
                self.obj['1']['restart'] = False
                self.obj['2']['restart'] = False
            if pressed[pygame.K_1]:
                self.obj['1']['zoom_in'] = True
                self.obj['2']['zoom_in'] = True
            else:
                self.obj['1']['zoom_in'] = False
                self.obj['2']['zoom_in'] = False
            if pressed[pygame.K_2]:
                self.obj['1']['zoom_out'] = True
                self.obj['2']['zoom_out'] = True
            else:
                self.obj['1']['zoom_out'] = False
                self.obj['2']['zoom_out'] = False
            if pressed[pygame.K_ESCAPE]:
                self.obj['1']['esc'] = True
                self.obj['2']['esc'] = True
            else:
                self.obj['1']['esc'] = False
                self.obj['2']['esc'] = False

    def activated_controler(self, event):
        # xbox controller
        if self.joysticks:
            if event.type == pygame.JOYBUTTONDOWN:
                player_num = event.joy + 1
                if event.button == 1:
                    self.obj[f'{player_num}']['space'] = True
                if event.button == 3:
                    self.obj[f'{player_num}']['run'] = True
                if event.button == 4:
                    self.obj[f'{player_num}']['zoom_in'] = True
                if event.button == 5:
                    self.obj[f'{player_num}']['zoom_out'] = True
                if event.button == 6:
                    self.obj[f'{player_num}']['esc'] = True
                if event.button == 7:
                    self.obj[f'{player_num}']['restart'] = True
            if event.type == pygame.JOYBUTTONUP:
                player_num = event.joy + 1
                if event.button == 1:
                    self.obj[f'{player_num}']['space'] = False
                if event.button == 3:
                    self.obj[f'{player_num}']['run'] = False
                if event.button == 4:
                    self.obj[f'{player_num}']['zoom_in'] = False
                if event.button == 5:
                    self.obj[f'{player_num}']['zoom_out'] = False
                if event.button == 6:
                    self.obj[f'{player_num}']['esc'] = False
                if event.button == 7:
                    self.obj[f'{player_num}']['restart'] = False
            if event.type == pygame.JOYHATMOTION:
                # d pad
                player_num = event.joy + 1
                self.obj[f'{player_num}']['right'] = True if event.value == (1, 0) else False
                self.obj[f'{player_num}']['left'] = True if event.value == (-1, 0) else False
                self.obj[f'{player_num}']['up'] = True if event.value == (0, 1) else False
                self.obj[f'{player_num}']['down'] = True if event.value == (0, -1) else False