import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging, random


MAX_TIMESTEP = 300

action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)


action_set = { i : action_set_list[i] for i in range(0, len(action_set_list) ) }

class RCRSenv(gym.Env):
    metadata = {'render.modes' : ['human']}
    def __init__(self):
        # Reference: https://github.com/MartinThoma/banana-gym/blob/master/gym_banana/envs/banana_env.py
        self.observation_space = spaces.Discrete(8)
        # Reference: https://github.com/openai/gym/blob/master/gym/spaces/multi_discrete.py
        self.action_space = spaces.Discrete(36)

        # self.actionCounts = { i : 0 for i in range(0, len(action_set_list) ) }
    
#       self._action_set = action_function # Actual 
        
        # General variables
        # self._take_action = self._action_set[0]

        # Store what the agent tried
        self.curr_episode = 0
        self.action_episode_memory = []

    def step(self, action):
        
        # self.actionCounts[action] += 1
        self._take_action(action)
        self.curr_episode += 1

        reward = self._get_reward()

        if self.curr_episode == MAX_TIMESTEP:
          print("Episode completed")
          self.action_episode_memory += 1
          print("Action Count")
        ob = self._get_state()
        return ob, reward, self.curr_episode , {}

    def _take_action(self, action):

        action_tobe_taken = action_set_list[action] # This is from the rcrs simulator

        return action_tobe_taken

    def _get_reward(self):
#         self.reward = reward_function # This is from the rcrs simulator
        reward = 0.95
        return reward

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        Returns
        -------
        observation (object): the initial observation of the space.
        """
        # self.t = 0
        self.curr_episode = 0
        self.action_episode_memory.append([])
        # self._take_action(a)

        return self._get_state()

    def _render(self, mode='human', close=False):
        return

    def _get_state(self):
        """Get the observation."""
#         self.ob = state_list # This is from the rcrs simulator
        self.ob = np.array([210552869, 53695, 107356, 10000, 0, 10000, 0, 15000], dtype=object)
        
        return self.ob

    def seed(self, seed):
        random.seed(seed)
        np.random.seed




