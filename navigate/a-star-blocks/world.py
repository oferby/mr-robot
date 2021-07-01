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
FONT = pygame.font.SysFont('David', 20)


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
            elif k == 112:
                return 1, 97
    return


class World:

    def __init__(self):
        self.background = None
        self.state = None
        self.reset()

    def reset(self):
        self.background = np.copy(self.get_surface())
        self.state = np.array([[0, 1, 2], [3, 4, 5], [6, 7, 8]])
        self.draw()

    def draw(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        for i in range(3):
            for j in range(3):
                self.draw_rec_outline(i * BLOCK_SIZE, j * BLOCK_SIZE, BLOCK_SIZE, BLACK, 3)
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

    @staticmethod
    def update_display():
        pygame.display.update()

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def take_action(self, action):
        pass

    def handle_events(self):
        event = get_event()
        if event:
            is_kb_event, event_info = event
            if is_kb_event:
                return event_info
            else:
                # mouse event
                print(event_info)
                pass
        return
