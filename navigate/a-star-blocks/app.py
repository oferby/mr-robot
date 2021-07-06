from world import World
from agents import PlanningAgent

world = World()

while True:

    obs = world.reset()
    agent = PlanningAgent(world.get_final_state(), obs)

    while True:
        action = agent.get_action(obs)
        if action is not None:
            obs = world.take_action(action)
        event_info = world.handle_events()
        if event_info is not None:
            if event_info == 99:
                break
