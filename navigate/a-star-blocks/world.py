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


def get_neighbors(current):
    neighbors = []
    zero_location = np.where(current == 0)[0][0]
    if zero_location == 0:
        actions = [1, 3]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 1:
        actions = [0, 2, 4]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 2:
        actions = [1, 5]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 3:
        actions = [0, 4, 6]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 4:
        actions = [1, 3, 5, 7]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 5:
        actions = [2, 4, 8]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 6:
        actions = [3, 7]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 7:
        actions = [4, 6, 8]
        add_neigbor(neighbors, actions, current)
    elif zero_location == 8:
        actions = [5, 7]
        add_neigbor(neighbors, actions, current)

    return neighbors


def add_neigbor(neighbors, actions, current):
    for action in actions:
        s = np.copy(current)
        World.get_state_for_action(s, action)
        neighbors.append(s)


class World:

    def __init__(self):
        self.background = None
        self.state = None
        self.build_background()
        self.final_state = np.arange(9)

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

        for i in range(40):
            neighbors = get_neighbors(self.state)
            r = np.random.randint(0, len(neighbors))
            self.state = neighbors[r]

        print("init state: {}".format(self.state))

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

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    # action is the number of the box 0-8
    # returns obs, reward, done
    def take_action(self, action):

        World.get_state_for_action(self.state, action)
        self.draw()
        return self.check_reward()

    @staticmethod
    def get_state_for_action(state, action):
        if action == 0:
            if state[1] == 0:
                state = World.switch_state(state, 1, 0)
            elif state[3] == 0:
                state = World.switch_state(state, 3, 0)
        elif action == 1:
            if state[0] == 0:
                state = World.switch_state(state, 0, 1)
            elif state[2] == 0:
                state = World.switch_state(state, 2, 1)
            elif state[4] == 0:
                state = World.switch_state(state, 4, 1)
        elif action == 2:
            if state[1] == 0:
                state = World.switch_state(state, 1, 2)
            elif state[5] == 0:
                state = World.switch_state(state, 2, 5)
        elif action == 3:
            if state[0] == 0:
                state = World.switch_state(state, 3, 0)
            elif state[4] == 0:
                state = World.switch_state(state, 3, 4)
            elif state[6] == 0:
                state = World.switch_state(state, 6, 3)
        elif action == 4:
            if state[1] == 0:
                state = World.switch_state(state, 1, 4)
            elif state[3] == 0:
                state = World.switch_state(state, 3, 4)
            elif state[5] == 0:
                state = World.switch_state(state, 5, 4)
            elif state[7] == 0:
                state = World.switch_state(state, 7, 4)
        elif action == 5:
            if state[2] == 0:
                state = World.switch_state(state, 2, 5)
            elif state[4] == 0:
                state = World.switch_state(state, 4, 5)
            elif state[8] == 0:
                state = World.switch_state(state, 6, 5)
        elif action == 6:
            if state[3] == 0:
                state = World.switch_state(state, 3, 6)
            elif state[7] == 0:
                state = World.switch_state(state, 7, 6)
        elif action == 7:
            if state[6] == 0:
                state = World.switch_state(state, 6, 7)
            elif state[4] == 0:
                state = World.switch_state(state, 4, 7)
            elif state[8] == 0:
                state = World.switch_state(state, 8, 7)
        elif action == 8:
            if state[5] == 0:
                state = World.switch_state(state, 5, 8)
            elif state[7] == 0:
                state = World.switch_state(state, 7, 8)

        return state

    def check_reward(self):
        if np.array_equal(self.final_state, self.state):
            return np.copy(self.state), 100, True
        else:
            return np.copy(self.state), -1, False

    @staticmethod
    def switch_state(state, x, y):
        tmp = state[x]
        state[x] = state[y]
        state[y] = tmp
        return state

    def get_final_state(self):
        return np.copy(self.final_state)

    def handle_events(self):
        event = get_event()
        if event:
            is_kb_event, event_info = event
            if is_kb_event:
                if event_info < 9:
                    return self.take_action(event_info)
                return event_info
            else:
                # mouse event
                print(event_info)
                pass
        return
