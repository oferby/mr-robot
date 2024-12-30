import abc
import numpy as np
from numpy_ringbuffer import RingBuffer
import tensorflow as tf
from tensorflow import keras as K


class ReplayBuffer:
    def __init__(self, max_size=10000):
        self.storage = []
        self.max_size = max_size
        self.ptr = 0

    class __Full:
        def add(self, transition):
            self.storage[self.ptr] = transition

            if (self.ptr + 1) == self.max_size:
                self.ptr = 0
            else:
                self.ptr += 1

        def sample(self, batch_size):
            ind = np.random.randint(0, len(self.storage), size=batch_size)
            states, actions, next_states, rewards, dones = [], [], [], [], []
            for i in ind:
                state, action, next_state, reward, done = self.storage[i]
                states.append(state)
                actions.append(action)
                next_states.append(next_state)
                rewards.append(reward)
                dones.append(done)
            return states, actions, next_states, rewards, dones

    def add(self, transition):
        self.storage.append(transition)
        self.ptr += 1
        if len(self.storage) == self.max_size:
            self.__class__ = self.__Full
            self.ptr = 0

    def sample(self, batch_size):
        ind = np.random.randint(0, len(self.storage), size=batch_size)
        states, actions, next_states, rewards, dones = [], [], [], [], []
        for i in ind:
            state, action, next_state, reward, done = self.storage[i]
            states.append(state)
            actions.append(action)
            next_states.append(next_state)
            rewards.append(reward)
            dones.append(done)
        return states, actions, next_states, rewards, dones


class AbstractAgent:

    def __init__(self, action_space, state_space):
        self.actions = action_space
        self.states = state_space
        self.memory = ReplayBuffer()

    @abc.abstractmethod
    def get_action(self, state):
        pass

    @abc.abstractmethod
    def observe(self, state, action, new_state, reward, done):
        pass


class RandomAgent(AbstractAgent):
    def __init__(self, action_space, state_space):
        super().__init__(action_space, state_space)
        self.cumulative_reward = 0

    def get_action(self, state):
        return np.random.randint(0, self.actions - 1)

    def observe(self, state, action, new_state, reward, done):
        self.cumulative_reward += reward
        state = [round(o, 2) for o in state]
        new_state = [round(o, 2) for o in new_state]
        print(
            'state: {}, \naction: {}, \nnew_state: {}, \nreward: {}, cumulative: {}, done: {}'.format(state, action,
                                                                                                      new_state, reward,
                                                                                                      self.cumulative_reward,
                                                                                                      done))
        print('\n')
        if done:
            self.cumulative_reward = 0


class Actor:
    def __init__(self, action_dim, max_action):
        self.max_action = max_action
        self.model = K.Sequential([
            K.layers.Dense(400, activation='relu'),
            K.layers.Dense(300, activation='relu'),
            K.layers.Dense(action_dim, activation='tanh')
        ])

    def forward(self, x):
        return self.model(x) * self.max_action


class Critic:
    def __init__(self, state_dim, action_dim):
        self.model = K.Sequential([
            K.layers.Dense(400, activation='relu'),
            K.layers.Dense(300, activation='relu'),
            K.layers.Dense(1),
        ])

        self.model.compile(optimizer='Adam', loss='MeanSquaredError')

        self.target = K.Sequential([
            K.layers.Dense(400, activation='relu'),
            K.layers.Dense(300, activation='relu'),
            K.layers.Dense(1),
        ])

        self.target.compile(optimizer='Adam', loss='MeanSquaredError')

    def forward(self, x, u):
        x = np.concatenate((x, u), axis=1)
        return self.model(x), self.target(x)

    def Q1(self, x, u):
        x = np.concatenate((x, u), axis=1)
        return self.model(x)


class TD3Agent(AbstractAgent):
    def __init__(self, action_space, state_space, max_action=1):
        super().__init__(action_space, state_space)
        self.actor_model = Actor(action_space, max_action)
        self.actor_target = Actor(action_space, max_action)
        x = tf.ones((1, state_space))
        self.actor_model.forward(x)
        self.actor_target.forward(x)

        self.actor_target.model.set_weights(self.actor_model.model.weights)

        self.step = 0

    def get_action(self, state):
        x = K.backend.constant(state, shape=(1, 8))
        actions = self.actor_model.forward(x).numpy()
        best_action = np.argmax(actions)
        return best_action

    def observe(self, state, action, new_state, reward, done):
        self.memory.add((state, action, new_state, reward, done))
        self.step += 1
        if self.step == 1000:
            print('training...')
            self.train()
            self.step = 0

    def train(self):
        samples = self.memory.sample(64)
        states, actions, next_states, rewards, dones = samples
        states = K.backend.constant(states)
        actions = K.backend.constant(actions)
        next_states = K.backend.constant(next_states)
        rewards = K.backend.constant(rewards)
        dones = K.backend.constant(dones)




