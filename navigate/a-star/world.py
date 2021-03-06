import random

import numpy as np
import pygame

pygame.init()

WHITE = (255, 255, 255)
GREY = (20, 20, 20)
LIGHT_GREY = (211, 211, 211)
BLACK = (0, 0, 0)
PURPLE = (100, 0, 100)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE_INT = 16777215
BLACK_INT = 0

ROBOT_SIZE = 20
STEP_SIZE = 5

WORLD_SIZE = (800, 800)
screen = pygame.display.set_mode(WORLD_SIZE)

pygame.display.set_caption("A* Simulator")

done = False

CELL_SIZE = 50
cols = int(WORLD_SIZE[0] / CELL_SIZE)
rows = int(WORLD_SIZE[1] / CELL_SIZE)

stack = []


class Cell:
    def __init__(self, x, y, grid):
        global CELL_SIZE
        self.x = x * CELL_SIZE
        self.y = y * CELL_SIZE
        self.grid = grid

        self.visited = False
        self.current = False

        self.walls = [True, True, True, True]  # top , right , bottom , left

        # neighbors
        self.neighbors = []

        self.top = 0
        self.right = 0
        self.bottom = 0
        self.left = 0

        self.next_cell = 0

    def draw(self):
        if self.current:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, CELL_SIZE, CELL_SIZE))
        elif self.visited:
            pygame.draw.rect(screen, WHITE, (self.x, self.y, CELL_SIZE, CELL_SIZE))

            if self.walls[0]:
                pygame.draw.line(screen, BLACK, (self.x, self.y), ((self.x + CELL_SIZE), self.y), 1)  # top
            if self.walls[1]:
                pygame.draw.line(screen, BLACK, ((self.x + CELL_SIZE), self.y), ((self.x + CELL_SIZE), (self.y + CELL_SIZE)),
                                 1)  # right
            if self.walls[2]:
                pygame.draw.line(screen, BLACK, ((self.x + CELL_SIZE), (self.y + CELL_SIZE)), (self.x, (self.y + CELL_SIZE)),
                                 1)  # bottom
            if self.walls[3]:
                pygame.draw.line(screen, BLACK, (self.x, (self.y + CELL_SIZE)), (self.x, self.y), 1)  # left

    def checkNeighbors(self):
        # print("Top; y: " + str(int(self.y / width)) + ", y - 1: " + str(int(self.y / width) - 1))
        if int(self.y / CELL_SIZE) - 1 >= 0:
            self.top = self.grid[int(self.y / CELL_SIZE) - 1][int(self.x / CELL_SIZE)]
        # print("Right; x: " + str(int(self.x / width)) + ", x + 1: " + str(int(self.x / width) + 1))
        if int(self.x / CELL_SIZE) + 1 <= cols - 1:
            self.right = self.grid[int(self.y / CELL_SIZE)][int(self.x / CELL_SIZE) + 1]
        # print("Bottom; y: " + str(int(self.y / width)) + ", y + 1: " + str(int(self.y / width) + 1))
        if int(self.y / CELL_SIZE) + 1 <= rows - 1:
            self.bottom = self.grid[int(self.y / CELL_SIZE) + 1][int(self.x / CELL_SIZE)]
        # print("Left; x: " + str(int(self.x / width)) + ", x - 1: " + str(int(self.x / width) - 1))
        if int(self.x / CELL_SIZE) - 1 >= 0:
            self.left = self.grid[int(self.y / CELL_SIZE)][int(self.x / CELL_SIZE) - 1]
        # print("--------------------")

        if self.top != 0:
            if not self.top.visited:
                self.neighbors.append(self.top)
        if self.right != 0:
            if not self.right.visited:
                self.neighbors.append(self.right)
        if self.bottom != 0:
            if not self.bottom.visited:
                self.neighbors.append(self.bottom)
        if self.left != 0:
            if not self.left.visited:
                self.neighbors.append(self.left)

        if len(self.neighbors) > 0:
            self.next_cell = self.neighbors[random.randrange(0, len(self.neighbors))]
            return self.next_cell
        else:
            return False


class World:

    def __init__(self):
        self.agent_location = None
        self.background = None
        self.target_location = None
        self.turn = None
        self.max_turns = None
        self.is_mdp = False
        self.draw_central_agent = False
        self.target_location = None
        self.planned_positions = []
        self.path = None

        pygame.font.init()
        self.font = pygame.font.SysFont('David', 20)

    def reset(self):
        self.agent_location = []
        self.target_location = None
        self.planned_positions = []
        self.path = []
        self.create()
        self.init_agent_location()
        self.background = np.copy(self.get_surface())
        self.turn = 0
        self.max_turns = 2000
        self.draw()

        # obs
        return self.get_partial_obs_for_agent()

    @staticmethod
    def get_surface():
        return pygame.surfarray.pixels2d(screen)

    def draw(self):
        pygame.surfarray.blit_array(pygame.display.get_surface(), self.background)

        for p in self.planned_positions:
            self.draw_rec(p[0], p[1], ROBOT_SIZE, LIGHT_GREY)

        half_size = ROBOT_SIZE // 2
        for p in self.path:
            self.draw_rec(p[0] - half_size, p[1] - half_size, ROBOT_SIZE, GREY)

        self.draw_rec(self.agent_location[0], self.agent_location[1], ROBOT_SIZE, BLUE)

        if self.draw_central_agent:
            x, y = self.get_agent_location()
            self.draw_rec(x - 1, y - 1, 2, RED)

        if self.target_location:
            self.draw_rec(self.target_location[0] - (ROBOT_SIZE // 2), self.target_location[1] - (ROBOT_SIZE // 2),
                          ROBOT_SIZE, RED)

        pygame.display.flip()

    def take_action(self, a):

        new_pos = [x for x in self.agent_location]

        # up
        if a == 0:
            new_pos[1] = new_pos[1] - STEP_SIZE
        # right
        elif a == 1:
            new_pos[0] = new_pos[0] + STEP_SIZE
        # down
        elif a == 2:
            new_pos[1] = new_pos[1] + STEP_SIZE
        # left
        elif a == 3:
            new_pos[0] = new_pos[0] - STEP_SIZE
        elif a == 98:
            self.draw_central_agent = not self.draw_central_agent

        if self.check_valid_action(new_pos, a):
            self.agent_location = new_pos
            self.draw()

        self.turn += 1
        if self.turn > self.max_turns:
            print('Max turns reached')
            return self.get_obs(), -1, True

        return self.get_obs()

    @staticmethod
    def draw_rec(x, y, size, color):
        pygame.draw.rect(screen, color, pygame.Rect(x, y, size, size))

    def draw_text(self, text, position):
        txt = self.font.render(text, True, RED)
        screen.blit(txt, position)

    @staticmethod
    def update_display():
        pygame.display.update()

    def get_obs(self):
        if self.is_mdp:
            return self.get_surface().copy()
        return self.get_partial_obs_for_agent()

    def check_valid_action(self, new_location, a):
        surface = self.get_surface()
        if not all([True if x > 1 else False for x in new_location]):
            return False

        if a == 1 and new_location[0] + ROBOT_SIZE > WORLD_SIZE[0]:
            return False
        if a == 2 and new_location[1] + ROBOT_SIZE > WORLD_SIZE[1]:
            return False

        s = []
        if a == 0:
            # print(new_location[0], new_location[0] + ROBOT_SIZE, new_location[1])
            s = surface[new_location[0]: new_location[0] + ROBOT_SIZE,
                new_location[1]: new_location[1] + STEP_SIZE]
            # print(s)

        elif a == 1:
            s = surface[new_location[0] + ROBOT_SIZE - STEP_SIZE:new_location[0] + ROBOT_SIZE,
                new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        elif a == 2:
            s = surface[new_location[0]:new_location[0] + ROBOT_SIZE,
                new_location[1] + ROBOT_SIZE - STEP_SIZE: new_location[1] + ROBOT_SIZE]
            # print(s)

        elif a == 3:
            s = surface[new_location[0]:new_location[0] + STEP_SIZE, new_location[1]: new_location[1] + ROBOT_SIZE]
            # print(s)

        if self.check_surface(s, np.size(s)):
            return False

        return True

    def check_surface_for_central_position(self, x, y):
        size = ROBOT_SIZE // 2
        if (x - size) < 0 or (x + size) > WORLD_SIZE[0] or (y - size) < 0 or (y + size) > WORLD_SIZE[1]:
            return True
        s = self.get_surface()[x - size: x + size, y - size: y + size]
        return self.check_surface(s, np.size(s))

    def check_surface_for_position(self, x, y, size=ROBOT_SIZE):
        s = self.get_surface()[x: x + size, y: y + size]
        return self.check_surface(s, np.size(s))

    @staticmethod
    def check_surface(s, size):
        s = np.reshape(s, (size,))
        if any(x == BLACK_INT for x in s):
            return True

    def get_partial_obs_for_agent(self):
        x, y = self.get_agent_location()
        return self.get_partial_obs(x, y)

    def get_agent_location(self):
        x = int(self.agent_location[0] + ROBOT_SIZE // 2)
        y = int(self.agent_location[1] + ROBOT_SIZE // 2)
        return x, y

    def get_partial_obs(self, x, y):
        surface = self.get_surface()
        sensors = [0, 0, 0, 0]
        _x = x - (ROBOT_SIZE // 2)
        while True:
            if _x == 0 or surface[_x, y] == BLACK_INT:
                sensors[0] = x - _x - (ROBOT_SIZE // 2)
                break
            _x -= 1

        _x = x + (ROBOT_SIZE // 2)
        while True:

            if (_x == WORLD_SIZE[0] - 1) or surface[_x, y] == BLACK_INT:
                sensors[2] = _x - x - (ROBOT_SIZE // 2)
                break
            _x += 1

        _y = y - (ROBOT_SIZE // 2)
        while True:
            if _y == 0 or surface[x, _y] == BLACK_INT:
                sensors[1] = y - _y - (ROBOT_SIZE // 2)
                break
            _y -= 1

        _y = y + (ROBOT_SIZE // 2)
        while True:
            if (_y >= WORLD_SIZE[1] - 1) or surface[x, _y] == BLACK_INT:
                sensors[3] = _y - y - (ROBOT_SIZE // 2)
                break
            _y += 1

        return sensors

    @staticmethod
    def remove_walls(current_cell, next_cell):
        x = int(current_cell.x / CELL_SIZE) - int(next_cell.x / CELL_SIZE)
        y = int(current_cell.y / CELL_SIZE) - int(next_cell.y / CELL_SIZE)
        if x == -1:  # right of current
            current_cell.walls[1] = False
            next_cell.walls[3] = False
        elif x == 1:  # left of current
            current_cell.walls[3] = False
            next_cell.walls[1] = False
        elif y == -1:  # bottom of current
            current_cell.walls[2] = False
            next_cell.walls[0] = False
        elif y == 1:  # top of current
            current_cell.walls[0] = False
            next_cell.walls[2] = False

    def create(self):
        grid = []

        for y in range(rows):
            grid.append([])
            for x in range(cols):
                grid[y].append(Cell(x, y, grid))

        current_cell = grid[0][0]
        next_cell = 0

        # -------- Main Program Loop -----------
        while not done:
            # --- Main event loop

            screen.fill(GREY)

            current_cell.visited = True
            current_cell.current = True

            for y in range(rows):
                for x in range(cols):
                    grid[y][x].draw()

            next_cell = current_cell.checkNeighbors()

            if next_cell:
                current_cell.neighbors = []

                stack.append(current_cell)

                self.remove_walls(current_cell, next_cell)

                current_cell.current = False

                current_cell = next_cell

            elif len(stack) > 0:
                current_cell.current = False
                current_cell = stack.pop()

            elif len(stack) == 0:
                break

    def init_agent_location(self):
        while True:
            i = np.random.randint(0, 4)
            if i == 0:
                y = np.random.randint(10, WORLD_SIZE[1] - 1)
                if not self.check_surface_for_position(5, y, ROBOT_SIZE):
                    self.agent_location = [5, y]
                    break
            elif i == 1:
                y = np.random.randint(10, WORLD_SIZE[1] - 1)
                if not self.check_surface_for_position(5, y, ROBOT_SIZE):
                    self.agent_location = [WORLD_SIZE[0] - ROBOT_SIZE - 2, y]
                    break

    def set_target_location(self, location):
        x, y = location
        if not self.check_surface_for_position(x - (ROBOT_SIZE // 2), y - (ROBOT_SIZE // 2), ROBOT_SIZE):
            self.target_location = [x, y]
            self.draw()
            return True
        return False

    def remove_target_location(self):
        self.target_location = None

    def add_to_planned_positions(self, position):
        self.planned_positions.append([position[0] - (ROBOT_SIZE // 2), position[1] - (ROBOT_SIZE // 2)])
        self.draw()

    @staticmethod
    def is_overlap(pos1, pos2):

        r_size = ROBOT_SIZE // 2

        rec1 = pygame.rect.Rect(pos1[0] - r_size, pos1[1] - r_size, ROBOT_SIZE, ROBOT_SIZE)
        rec2 = pygame.rect.Rect(pos2[0] - r_size, pos2[1] - r_size, ROBOT_SIZE, ROBOT_SIZE)

        return rec1.colliderect(rec2)

    def reset_planned(self):
        self.planned_positions = []
        self.path = []
        self.draw()

    def draw_path(self, path):
        self.path = path
        self.draw()
