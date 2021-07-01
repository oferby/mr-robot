from world import World

world = World()

# def draw():
#     world.update_display()


while True:

    obs = world.reset()
    # agent = PlanningAgent(world)

    while True:
        # action = agent.get_action(obs)
        # if action is not None:
        #     obs = world.take_action(action)
        event_info = world.handle_events()
        if event_info is not None:
            if event_info == 99:
                break

        # draw()
