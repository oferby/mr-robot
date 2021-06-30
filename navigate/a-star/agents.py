import sys

from abc import abstractmethod
import numpy as np
import pygame
import heapq

import world

SENSOR_NOISE = 20.0


def kb_action():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        if event.type == pygame.MOUSEBUTTONUP:
            mouse_event = pygame.mouse.get_pos()

        elif event.type == pygame.KEYUP:
            k = event.key
            # print('key:', k)
            # q
            if k == 113:
                sys.exit()

            if k == 1073741906:
                return 0
            elif k == 1073741905:
                return 2
            elif k == 1073741903:
                return 1
            elif k == 1073741904:
                return 3
            # r
            elif k == 114:
                return 99
            # s
            elif k == 115:
                return 98
            # p
            elif k == 112:
                return 97
    return


class Agent:
    @abstractmethod
    def get_action(self, obs):
        pass

    def set_target(self, target_location):
        pass


class SimpleAgent(Agent):

    def get_action(self, obs):
        return kb_action()

    def set_target(self, target_location):
        pass


class PlanningAgent(Agent):

    def __init__(self, world):
        self.world = world
        self.active = False
        self.target_location = None
        self.path = None
        self.plan_completed = False

        self.priority_q = None
        self.open_set = None
        self.close_set = None
        self.f_score = None
        self.g_score = None
        self.come_from = None

        self.reset()

    def reset(self):
        self.priority_q = []
        self.open_set = set()
        self.close_set = set()
        self.f_score = {}
        self.g_score = {}
        self.come_from = {}
        self.active = True
        self.plan_completed = False
        self.path = None

    def get_action(self, obs):

        event = self.get_event()

        if event:
            return event

        if self.active and self.plan_completed:
            pass

        return

    def plan_path(self):
        start = self.get_agent_location()
        heapq.heappush(self.priority_q, (0, start))

        self.open_set.add(str(start))
        self.g_score[str(start)] = 0
        self.f_score[str(start)] = self.get_h(start)

        while len(self.open_set) > 0:
            current = heapq.heappop(self.priority_q)
            current_p, current_loc = current
            self.open_set.remove(str(current_loc))

            if self.world.is_overlap(current_loc, self.target_location):
                self.path = self.return_path(current_loc)
                self.world.draw_path(self.path)
                return

            neighbors = self.get_neighbors(current_loc)

            for neighbor in neighbors:

                self.world.add_to_planned_positions(neighbor)

                tentative_score = self.get_g(current_loc) + 1
                if tentative_score < self.get_g(neighbor):
                    self.come_from[str(neighbor)] = current_loc
                    self.g_score[str(neighbor)] = tentative_score

                    score = self.g_score[str(neighbor)] + self.get_h(neighbor)
                    self.f_score[str(neighbor)] = score

                    if str(neighbor) not in self.open_set:
                        self.open_set.add(str(neighbor))
                        heapq.heappush(self.priority_q, (score, neighbor))

    def get_neighbors(self, current):
        neighbors = []
        step_size = world.STEP_SIZE * 4

        loc = current.copy()
        loc[0] -= step_size
        if not self.world.check_surface_for_central_position(loc[0], loc[1]):
            neighbors.append(loc)

        loc = current.copy()
        loc[0] += step_size
        if not self.world.check_surface_for_central_position(loc[0], loc[1]):
            neighbors.append(loc)

        loc = current.copy()
        loc[1] -= step_size
        if not self.world.check_surface_for_central_position(loc[0], loc[1]):
            neighbors.append(loc)

        loc = current.copy()
        loc[1] += step_size
        if not self.world.check_surface_for_central_position(loc[0], loc[1]):
            neighbors.append(loc)

        return neighbors

    def return_path(self, last_loc):
        path = []
        current = last_loc
        path.insert(0, current)
        while str(current) in self.come_from:
            current = self.come_from[str(current)]
            path.insert(0, current)

        return path


    def add_location_to_open_set(self, location):
        heapq.heappush(self.priority_q, (0, location))
        self.open_set.add(location)

    def add_location_to_closed_set(self, location):
        self.close_set.add(location)

    def get_h(self, location):
        x_, y_ = location
        a = np.array([x_, y_])
        b = np.array(self.target_location)
        return np.linalg.norm(a - b)

    def get_g(self, node):
        s = str(node)
        if s in self.g_score:
            return self.g_score[s]
        return sys.maxsize

    def get_agent_location(self):
        loc = self.world.get_agent_location()
        x, y = loc
        return [x, y]

    def set_target(self, target_location):
        self.reset()
        self.world.reset_planned()
        self.target_location = target_location
        print("target set to: {}".format(target_location))
        self.plan_path()

    def get_event(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()

            if event.type == pygame.MOUSEBUTTONUP:
                location = pygame.mouse.get_pos()
                self.world.set_target_location(location)
                self.set_target(location)
                return

            elif event.type == pygame.KEYUP:
                k = event.key
                # print('key:', k)
                # q
                if k == 113:
                    sys.exit()

                if k == 1073741906:
                    return 0
                elif k == 1073741905:
                    return 2
                elif k == 1073741903:
                    return 1
                elif k == 1073741904:
                    return 3
                # r
                elif k == 114:
                    return 99
                # s
                elif k == 115:
                    return 98
                # p
                elif k == 112:
                    return 97
        return
