import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging, random


# MAX_TIMESTEP = 300

# action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
#                     950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)



# class RCRSenv(gym.Env):
#     metadata = {'render.modes' : None}
#     def __init__(self):
        
#         self.action_space = spaces.Discrete(len(action_set_list))
        
#         high = np.array([np.inf]*6)
#         self.observation_space = spaces.Box(-high, high, dtype=np.float32, shape=None)

#         self.curr_episode = 0
#         self.action_episode_memory = []
#         self.seed()

#     def step(self, action):

#         self.curr_episode += 1

#         reward = self._get_reward()

#         if self.curr_episode == MAX_TIMESTEP:
#           print("Episode completed")
#           self.action_episode_memory += 1
#           print("Action Count")
        
#         state = self._take_action(action)

#         return state, reward, self.curr_episode , {}

#     def _take_action(self, action):
#         # Socket
#         return np.array([53695, 107356, 10000, 0, 10000, 15000])

#     def _get_reward(self):
# #       # Socket
#         reward = 0.95
#         return reward

#     def reset(self):
#         self.curr_episode = 0
#         self.action_episode_memory.append([])

#         return self.step(255)[0]

#     # def _render(self, mode='human', close=False):
#     #     return None 

#     def seed(self, seed = None):
#         self.np_random, seed = seeding.np_random(seed)
#         return [seed]

import os, subprocess, time, signal
import gym, numpy as np
from gym import error, spaces
from gym import utils
from gym.utils import seeding
import logging, random
import socket, pickle, json, subprocess, ast
from subprocess import *
import numpy as np
import threading 

port = [2211, 2025, 4011] 
ss = []

def createSocket(port): 
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind(('localhost', port))
    s.listen(5)
    return s


def readMessage(s):
    while True:
        c, addr = s.accept()
        print ("Socket Up and running with a connection from ",addr)
        rcvdData = c.recv(1024)
        final = bytes(rcvdData).decode("utf-8")
        print(final)


        if len(final) < 50:
          print("************************This is the Rewards************************")
          print(float(final))
        else:
          final_3 = list(final.split("|"))
          state = final_3[0]
            
          state = state.replace('[','')
          state = state.replace(',','')
          state = state.replace(']','')
          state = list(state.split(" "))
          state = state[:-1]
          state_list = [int(i) for i in state]

          action = final_3[1]
          action = action.replace('[','')
          action = action.replace(',','')
          action = action.replace(']','')
          action = list(action.split(" "))
          action = action[1:]
          action_list = [int(i) for i in action]
          print("************************This is the State space************************")
          print(state_list)
          print("************************This is the Action space***********************")
          print(action_list)

          c.close()
          return state_list, action_list

# if __name__ == "__main__":
    
    
#     for s in ss:
#         t = threading.Thread(target=readMessage, args=(s,))
#         t.start()

MAX_TIMESTEP = 300

action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)

current_action =  0

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}
    def __init__(self):
        for p in port:
            ss.append(createSocket(p));

        self.action_space = spaces.Discrete(len(action_set_list))
        
        high = np.array([np.inf]*6)
        self.observation_space = spaces.Box(-high, high, dtype=np.float32, shape=None)

        self.curr_episode = 0
        self.action_episode_memory = []
        self.seed()

    def step(self, action):

        self.curr_episode += 1

        reward = self._get_reward()

        if self.curr_episode == MAX_TIMESTEP:

          print("Episode completed")
          self.action_episode_memory += 1
          print("Action Count")
        
        state = self._take_action(action)
        current_action = action
        print(action_set_list[action])
        return state, reward, self.curr_episode , {}

    def _take_action(self, action):
        # Socket
        while True:
            c, addr = ss[1].accept()
            print ("Socket Up and running with a connection from ",addr)
            rcvdData = c.recv(1024)
            final = bytes(rcvdData).decode("utf-8")
            print(final)

        return np.array([53695, 107356, 10000, 0, 10000, 15000])

    def _get_reward(self):
#       # Socket
        while True:
            c, addr = ss[0].accept()
            print ("Socket Up and running with a connection from ",addr)
            rcvdData = c.recv(1024)
            final = bytes(rcvdData).decode("utf-8")
            print(final)
        reward = int(final)
        return reward

    def reset(self):
        self.curr_episode = 0
        self.action_episode_memory.append([])

        return self.step(current_action)[0]

    # def _render(self, mode='human', close=False):
    #     return None 

    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]