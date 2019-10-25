import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging


# core modules
import logging.config
import math
import pkg_resources
import random

# 3rd party modules
from gym import spaces
import cfg_load
import gym
import numpy as np

# path = 'config.yaml'  # always use slash in packages
# filepath = pkg_resources.resource_filename('rcrs_gym_animesh', path)
# config = cfg_load.load(filepath)
# logging.config.dictConfig(config['LOGGING'])

class RCRSenv(gym.Env):
	metadata = {'render.modes' : ['human']}

	def __init__(self):
		# Reference: https://github.com/MartinThoma/banana-gym/blob/master/gym_banana/envs/banana_env.py
		self.observation_space = spaces.Discrete(8)
		# Reference: https://github.com/openai/gym/blob/master/gym/spaces/multi_discrete.py
		self.action_space = spaces.Discrete(36)

		self._action_set = action_function
		# General variables
		self._take_action = _action_set[0]

		# Store what the agent tried
		self.curr_episode = -1
		self.action_episode_memory = []

    def step(self, action):
    	
    	"""
        The agent takes a step in the environment.
        Parameters
        ----------
        action : int
        Returns
        -------
        ob, reward, episode_over, info : tuple
            ob (object) :
                an environment-specific object representing your observation of
                the environment.
            reward (float) :
                amount of reward achieved by the previous action. The scale
                varies between environments, but the goal is always to increase
                your total reward.
            episode_over (bool) :
                whether it's time to reset the environment again. Most (but not
                all) tasks are divided up into well-defined episodes, and done
                being True indicates the episode has terminated. (For example,
                perhaps the pole tipped too far, or you lost your last life.)
            info (dict) :
                 diagnostic information useful for debugging. It can sometimes
                 be useful for learning (for example, it might contain the raw
                 probabilities behind the environment's last state change).
                 However, official evaluations of your agent are not allowed to
                 use this for learning.
        """
        if self.curr_episode == 300 or self._get_reward == 0:
            raise RuntimeError("Episode is done")
        self.curr_step += 1
        self._take_action(action)
        reward = self._get_reward()
        ob = self._get_state()
        return ob, reward, self.curr_step, {}

    def _take_action(self, a):

        action = _action_set[a] # This is from the rcrs simulator

        return action

    def _get_reward(self):
        """Reward is given for a sold banana."""
        self.reward = reward_function # This is from the rcrs simulator
        return reward

    def reset(self):
        """
        Reset the state of the environment and returns an initial observation.
        Returns
        -------
        observation (object): the initial observation of the space.
        """
        self.curr_step = -1
        self.curr_episode += 1
        self.action_episode_memory.append([])
        self._take_action([0])

        return self._get_state()

    def _render(self, mode='human', close=False):
        return

    def _get_state(self):
        """Get the observation."""
        self.ob = state_list # This is from the rcrs simulator
        return ob

    def seed(self, seed):
        random.seed(seed)
        np.random.seed


