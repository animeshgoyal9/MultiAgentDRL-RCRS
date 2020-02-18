from __future__ import print_function
import logging

import grpc
import sys
import socket, os
sys.path.append(os.path.join(sys.path[0], "../../PyRCRSClient/RCRS_gRPC_Client"))
import AgentInfo_pb2
import AgentInfo_pb2_grpc
import BuildingInfo_pb2
import BuildingInfo_pb2_grpc

import gym
from gym import error, spaces, utils
from gym.spaces import Discrete, Tuple, Box, MultiDiscrete
from gym.utils import seeding

import logging, random, socket, pickle, json, subprocess, ast
import numpy as np
import threading
import time, math
import signal
from subprocess import *
from numpy import inf
import collections

# map_used = "Small"
map_used = "Big"
algo_used = "PPO2"

if (map_used == 'Small'):
    MAX_TIMESTEP = 100
    n_agents  = 2  
    action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)
else:
    MAX_TIMESTEP = 250
    n_agents  = 4
    action_set_list = np.array([55887, 55875, 32789, 26534, 50850, 55870, 56223, 56229, 56214, 55917, 55962, 55898, 33041, 25233, 27992, 
                                33041, 56246, 55859, 55762, 55632, 35851, 39766, 35851, 36181, 42695, 53898, 48470, 35921, 53948, 32688, 
                                55606, 37342, 51857, 45972, 54494, 53426, 32855, 32762, 54508, 24141, 53719, 56395, 53581, 49264, 45054, 
                                52924, 25658, 52940, 57434, 52875, 33514, 55115, 53473, 52674, 52949, 29373, 41923, 51225, 50767, 51583, 
                                44069, 52941, 54540, 57762, 41320, 50628, 25174, 56302, 53998, 55604, 47082, 56160, 32351, 23899, 41346, 
                                55796, 33187, 25322, 57434, 25600, 52768, 52895, 48827, 53472, 24452, 50628, 34587, 44961, 23838, 38143, 
                                54554, 32260, 33514, 37861, 31635, 54625, 49857, 44250, 29873, 42010, 53603])

    # action_set_list = np.array([55887, 55875])

#Directory 
hostname = socket.gethostname()
# Parent Directory path 
parent_dir = sys.path[0]
# Path 
path = os.path.join(parent_dir, hostname) 
path_for_kill_file = os.path.join(parent_dir, "kill.sh")
string_for_launch_file = "python3" + " " + sys.path[0] + "/launch_file.py"

len_action_list = len(action_set_list)

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}  
    current_action = 0
    def __init__(self):
        if (algo_used == "PPO2"):
            self.action_space = MultiDiscrete([len(action_set_list)]*n_agents)
        else:
            self.action_space = Discrete(len_action_list*len_action_list)
        low = np.array([-inf]*2876)
        high = np.array([inf]*2876)
        # low = np.array([-inf]*n_agents*(len_action_list+6))
        # high = np.array([inf]*n_agents*(len_action_list+6))
        self.observation_space = Box(low, high, dtype=np.float32, shape=None)
        self.curr_episode = 0
        self.seed()


    def step(self, action):
        
        logging.basicConfig()
        
        self.curr_episode += 1
        print(self.curr_episode)
        state_info = []
        state_info.append(run_server())
        
        fieryeness_counter = np.array(state_info[0][0::2])
        appending_list = []
        for i in fieryeness_counter:
            if 0 <= i <= 2:
                appending_list.append(float(10/len(fieryeness_counter)))
            elif 3 <= i <= 5:
                appending_list.append(float(5/len(fieryeness_counter)))
            else:
                appending_list.append(float(-10/len(fieryeness_counter)))
        
        self.reward = sum(appending_list)
        print(self.reward)
        
    # To run greedy algorithm, uncomment 

        # state_info_temp = state_info[0][1::2]

        # action_for_greedy_algo_A1 = int((state_info_temp.index(max(state_info_temp))))
        
        # maximum=max(state_info_temp[0],state_info_temp[1]) 
        # secondmax=min(state_info_temp[0],state_info_temp[1]) 
          
        # for i in range(2,len(state_info_temp)): 
        #     if state_info_temp[i]>maximum: 
        #         secondmax=maximum
        #         maximum=state_info_temp[i] 
        #     else: 
        #         if state_info_temp[i]>secondmax: 
        #             secondmax=state_info_temp[i] 

        # action_for_greedy_algo_A2 = int((state_info_temp.index(secondmax)))
        # action = [action_for_greedy_algo_A1+1, action_for_greedy_algo_A2+1]

        state_info.append(run_adf(action))
        print("Action for 210552869" ,   action_set_list[action[0]])
        print("Action for 1618773504" ,  action_set_list[action[1]])
        print("Action for 1535509101" ,  action_set_list[action[2]])
        print("Action for 1127234487" ,  action_set_list[action[3]])
        print("-----------------------------------------------")
        flat_list = [item for sublist in state_info for item in sublist]
        
        self.state = flat_list

        done = bool(self.curr_episode == MAX_TIMESTEP)
        if done == True:
            subprocess.Popen(path_for_kill_file, shell=True)
        if (map_used == 'Small'):
            time.sleep(0.14)
        else:
            time.sleep(0.19)
        return np.array(self.state), self.reward, done , {}

    def reset(self):
        subprocess.run(['gnome-terminal', '-e', string_for_launch_file])
        if (map_used == 'Small'):
            time.sleep(11)
        else:
            time.sleep(14)
        self.curr_episode = 0
        # if (algo_used == "PPO2"):
        #     reset_action = [0]*n_agents
        # else:
        #     reset_action = 0
        reset_action = [0]*n_agents
        reset = []
        reset.append(run_server())
        reset.append(run_adf(reset_action))

        flat_list_reset = [item for sublist in reset for item in sublist]

        self.state = flat_list_reset
        return np.array(self.state) 

    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]


def run_adf(bid):
    global flag
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    
    with grpc.insecure_channel('localhost:3902') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
            # AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid//len_action_list]), 
            # AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[bid%len_action_list])]))

            AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid[0]]), 
            AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[bid[1]]),
            AgentInfo_pb2.Action(agent_id = 1535509101, building_id=action_set_list[bid[2]]), 
            AgentInfo_pb2.Action(agent_id = 1127234487, building_id=action_set_list[bid[3]])]))
            # AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[1425-bid])]))
            # AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[bid[1]])]))
            
    agent_state_info = []

    for i in response.agents:
        agent_state_info.append(i.agent_id)
        agent_state_info.append(i.x)
        agent_state_info.append(i.y)
        agent_state_info.append(i.water)
        agent_state_info.append(i.hp)
        agent_state_info.append(i.idle)
    return agent_state_info

def run_reward():
    with grpc.insecure_channel('localhost:2214') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
    return response_reward.reward

def run_server():
    with grpc.insecure_channel('localhost:4009') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    building_state_info = []
    for i in response.buildings:
        building_state_info.append(i.fieryness)
        building_state_info.append(i.temperature)
        # building_state_info.append(i.building_id)
    return building_state_info

