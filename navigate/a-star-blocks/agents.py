import sys
import numpy as np
import heapq
import world


class PlanningAgent:

    def __init__(self, final_state, init_state):
        self.final_state = final_state
        self.init_state = None

        self.priority_q = None
        self.open_set = None
        self.close_set = None
        self.f_score = None
        self.g_score = None
        self.come_from = None
        self.path = None

        self.reset(init_state)

    def reset(self, obs):
        self.init_state = obs

        self.priority_q = []
        self.open_set = set()
        self.close_set = set()
        self.f_score = {}
        self.g_score = {}
        self.come_from = {}
        self.path = None

        self.plan_with_a_star(np.copy(self.init_state), np.copy(self.final_state))
        print("plan finished")
        print("path: {}".format(self.path))

    def plan_with_a_star(self, start, end):
        print("planning.....")

        heapq.heappush(self.priority_q, (0, start.tolist()))

        self.open_set.add(str(start))
        self.g_score[str(start)] = 0
        self.f_score[str(start)] = self.get_h(start)

        while len(self.open_set) > 0:
            current = heapq.heappop(self.priority_q)
            print("current: {}".format(current))
            current_p, current_loc = current
            current_loc = np.array(current_loc)
            self.open_set.remove(str(current_loc))

            if np.array_equal(current_loc, end):
                self.path = self.return_path(current_loc)
                return

            neighbors = world.get_neighbors(current_loc)

            for neighbor in neighbors:
                tentative_score = self.get_g(current_loc) + 1
                if tentative_score < self.get_g(neighbor):
                    self.come_from[str(neighbor)] = current_loc
                    self.g_score[str(neighbor)] = tentative_score

                    score = self.g_score[str(neighbor)] + self.get_h(neighbor)
                    self.f_score[str(neighbor)] = score

                    if str(neighbor) not in self.open_set:
                        self.open_set.add(str(neighbor))
                        print(self.priority_q)
                        print(score, neighbor)
                        heapq.heappush(self.priority_q, (score, neighbor.tolist()))

    def get_h(self, state):

        h = 0
        for i, s in enumerate(state):
            x1 = s // 3
            y1 = s % 3
            x2 = i // 3
            y2 = i % 3
            a1 = np.array([x1, y1])
            a2 = np.array([x2, y2])
            h += np.linalg.norm(a1 - a2)
        return h

    def get_g(self, node):
        s = str(node)
        if s in self.g_score:
            return self.g_score[s]
        return sys.maxsize

    def return_path(self, last_loc):
        path = []
        current = last_loc
        path.insert(0, current)
        while str(current) in self.come_from:
            current = self.come_from[str(current)]
            path.insert(0, current)

        return path

    def get_action(self, obs):
        pass
