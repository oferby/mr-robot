from world import World
from agents import SimpleAgent, PlanningAgent

world = World()


def draw():
    world.update_display()


while True:

    obs = world.reset()
    agent = PlanningAgent(world)

    while True:
        action = agent.get_action(obs)
        if action is not None:
            print('action:', action)
            if action == 99:
                break
            else:
                obs = world.take_action(action)
            draw()
