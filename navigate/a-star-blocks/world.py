import sys
import random
import numpy as np
import pygame

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
LIGHT_GREY = (211, 211, 211)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE_INT = 16777215
BLACK_INT = 0

WORLD_SIZE = (300, 300)
BLOCK_SIZE = 100

pygame.init()
screen = pygame.display.set_mode(WORLD_SIZE)
screen.fill(WHITE)
pygame.display.set_caption("A* Block Simulator")
pygame.font.init()
FONT = pygame.font.SysFont('David', 30)


def get_event():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_event = pygame.mouse.get_pos()
            return 0, mouse_event

        elif event.type == pygame.KEYUP:
            k = event.key
            # print('key:', k)
            # q
            if k == 113:
                sys.exit()

            if k == 1073741906:
                return 1, 0
            elif k == 1073741905:
                return 1, 2
            elif k == 1073741903:
                return 1, 1
            elif k == 1073741904:
                return 1, 3
            # r
            elif k == 114:
                return 1, 99
            # s
            elif k == 115:
                return 1, 98
            # p
            elif k == 1073741922:
                return 1, 0
            elif k == 1073741913:
                return 1, 1
            elif k == 1073741914:
                return 1, 2
            elif k == 1073741915:
                return 1, 3
            elif k == 1073741916:
                return 1, 4
            elif k == 1073741917:
                return 1, 5
            elif k == 1073741918:
                return 1, 6
            elif k == 1073741919:
                return 1, 7
            elif k == 1073741920:
                return 1, 8


    return


class World:

    def __init__(self):
        self.background = None
        self.state = None
        self.build_background()
        self.final_state = np.array(9)

    def reset(self):
        self.randomize_state()
        self.draw()
        return np.copy(self.state)

    def build_background(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), np.copy(self.get_surface()))

        for i in range(3):
            for j in range(3):
                self.draw_rec_outline(i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLACK, 3)

        self.background = np.copy(self.get_surface())

    def randomize_state(self):
        self.state = np.arange(9)
        np.random.shuffle(self.state)

    def draw(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)
        for i in range(3):
            for j in range(3):
                middle_pos = BLOCK_SIZE // 2
                current_state = self.state.flatten()

                if current_state[i * 3 + j] != 0:
                    self.draw_text(str(current_state[i * 3 + j]),
                                   (j * BLOCK_SIZE + middle_pos, i * BLOCK_SIZE + middle_pos),
                                   RED)

        pygame.display.flip()

    @staticmethod
    def draw_rec(x, y, size, color):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))

    @staticmethod
    def draw_rec_outline(x, y, size, color, border_size):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size), border_size)

    def draw_text(self, text, position, color):
        txt = FONT.render(text, True, color, WHITE)
        screen.blit(txt, position)

    # @staticmethod
    # def update_display():
    #     pygame.display.update()

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    # action is the number of the box 0-8
    # returns obs, reward, done
    def take_action(self, action):
        if action == 0:
            if self.state[1] == 0:
                self.switch_state(1, 0)
                self.draw()
            elif self.state[3] == 0:
                self.switch_state(3, 0)
                self.draw()
        elif action == 1:
            if self.state[0] == 0:
                self.switch_state(0, 1)
                self.draw()
            elif self.state[2] == 0:
                self.switch_state(2, 1)
                self.draw()
            elif self.state[4] == 0:
                self.switch_state(4, 1)
                self.draw()
        elif action == 2:
            if self.state[1] == 0:
                self.switch_state(1, 2)
                self.draw()
            elif self.state[5] == 0:
                self.switch_state(2, 5)
                self.draw()
        elif action == 3:
            if self.state[0] == 0:
                self.switch_state(3, 0)
                self.draw()
            elif self.state[4] == 0:
                self.switch_state(3, 4)
                self.draw()
            elif self.state[6] == 0:
                self.switch_state(6, 3)
                self.draw()
        elif action == 4:
            if self.state[1] == 0:
                self.switch_state(1, 4)
                self.draw()
            elif self.state[3] == 0:
                self.switch_state(3, 4)
                self.draw()
            elif self.state[5] == 0:
                self.switch_state(5, 4)
                self.draw()
            elif self.state[7] == 0:
                self.switch_state(7, 4)
                self.draw()
        elif action == 5:
            if self.state[2] == 0:
                self.switch_state(2, 5)
                self.draw()
            elif self.state[4] == 0:
                self.switch_state(4, 5)
                self.draw()
            elif self.state[8] == 0:
                self.switch_state(6, 5)
                self.draw()
        elif action == 6:
            if self.state[3] == 0:
                self.switch_state(3, 6)
                self.draw()
            elif self.state[7] == 0:
                self.switch_state(7, 6)
                self.draw()
        elif action == 7:
            if self.state[6] == 0:
                self.switch_state(6, 7)
                self.draw()
            elif self.state[4] == 0:
                self.switch_state(4, 7)
                self.draw()
            elif self.state[8] == 0:
                self.switch_state(8, 7)
                self.draw()
        elif action == 8:
            if self.state[5] == 0:
                self.switch_state(5, 8)
                self.draw()
            elif self.state[7] == 0:
                self.switch_state(7, 8)
                self.draw()

            return self.check_reward()

    def check_reward(self):
        if np.equal(self.final_state, self.state):
            return np.copy(self.state), 100, True
        else:
            return np.copy(self.state), -1, False

    def switch_state(self, x, y):
        tmp = self.state[x]
        self.state[x] = self.state[y]
        self.state[y] = tmp

    def handle_events(self):
        event = get_event()
        if event:
            is_kb_event, event_info = event
            if is_kb_event:
                return self.take_action(event_info)
            else:
                # mouse event
                print(event_info)
                pass
        return
