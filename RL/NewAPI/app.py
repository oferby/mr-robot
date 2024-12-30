import gym
import agents

env = gym.make("LunarLander-v2", render_mode="human")
observation = env.reset(seed=42)

agent = agents.TD3Agent(4, 8)

for i in range(100):

    while True:
        action = agent.get_action(observation)
        observation_, reward, terminated, truncated = env.step(action)
        agent.observe(observation, action, observation_, reward, terminated)

        if terminated or truncated:
            observation = env.reset()
            break

        observation = observation_

env.close()
