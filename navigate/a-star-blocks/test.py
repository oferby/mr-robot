import numpy as np


def get_h(state):
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


print(get_h([1, 0, 8, 3, 4, 5, 6, 7, 2]))
