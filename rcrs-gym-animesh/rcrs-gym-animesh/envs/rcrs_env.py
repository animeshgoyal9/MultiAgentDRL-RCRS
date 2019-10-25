import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging

logger = logging.getlogger(__name__)

class RCRSenv(gym.Env):
	metadata = {'render.modes' : ['human']}

	def __init__(self):
		
		self.observation_space = spaces.MultiDiscrete((40))
		# Reference: https://github.com/openai/gym/blob/master/gym/spaces/multi_discrete.py
		self.action_space = spaces.MultiDiscrete((20))
		self.viewer = None
		self.server_process = None
        self.server_port = None
        self.prev_reward = []
        # Reference: https://github.com/openai/gym/blob/master/gym/envs/box2d/lunar_lander.py
        self.reset()

    def seed(self, seed = None):
    	self.np_random, seed = seeding.np_random(seed)
    	return [seed]

    def reset(self):
    	self.initial_pos_FB = [255]


    def step(self, action):
    	self.previous_state = self.state # keep a record of the previous state
    	state, self.untransformed_state = self.__generate_state()  # Generate state
    	self.state = state # keep a record of the new state

    	# Rewards for RL
    	reward = self.__compute_rewards()

    	return state, reward, done, {} 

    def demo_rcrs_gym(env, seed=None, render= False):
    	env.seed(seed)

    def render(self):
     	pass

    if __name__ == '__main__':
     	main()


