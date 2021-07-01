from world import World

world = World()

while True:

    obs = world.reset()
    # agent = PlanningAgent(world)

    while True:
        # action = agent.get_action(obs)
        # if action is not None:
        #     obs = world.take_action(action)
        world.handle_events()
