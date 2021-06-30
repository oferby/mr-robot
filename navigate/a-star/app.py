from world import World
from agents import SimpleAgent

world = World()
agent = SimpleAgent()


def draw():
    world.update_display()


while True:

    obs, reward, done = world.reset()

    while not done:
        action = agent.get_action(obs)
        if action is not None:
            print('action:', action)
            if action == 99:
                break
            else:
                obs, reward, done = world.take_action(action)
                agent.get_feedback(obs, action, reward, done)
            draw()

        if done:
            break
