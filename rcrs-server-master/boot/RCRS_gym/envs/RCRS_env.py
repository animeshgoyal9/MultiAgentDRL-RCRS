
from __future__ import print_function
import logging

import grpc
import AgentInfo_pb2
import AgentInfo_pb2_grpc
import BuildingInfo_pb2
import BuildingInfo_pb2_grpc

import gym
from gym import error, spaces, utils
from gym.spaces import Discrete, Tuple
from gym.utils import seeding

import logging, random
import socket, pickle, json, subprocess, ast
import numpy as np
import threading
import time, math, os
import signal, sys
import threading
from subprocess import *
from numpy import inf

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

MAX_TIMESTEP = 100

action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}  
    current_action = 0
    def __init__(self):
    # Action space for PPO
        self.action_space = spaces.MultiDiscrete([37, 37])
    # Action space for DQN
        # self.action_space = spaces.Discrete(37)
        low = np.array([0]*86)
        high = np.array([inf]*86)

        self.observation_space = spaces.Box(low, high, dtype=np.float32, shape=None)

        self.curr_episode = 0
        self.seed()


    def step(self, action):
        
        logging.basicConfig()
        
        self.curr_episode += 1
        if (self.curr_episode <= (MAX_TIMESTEP - 1)):
            self.reward = 0
        else:
            self.reward = run_reward()
        
        state_info = []
        state_info.append(run_server())
        
    # To run greedy algorithm, uncomment 

        state_info_temp = state_info[0][1::2]

        action_for_greedy_algo_A1 = int((state_info_temp.index(max(state_info_temp))))
        
        maximum=max(state_info_temp[0],state_info_temp[1]) 
        secondmax=min(state_info_temp[0],state_info_temp[1]) 
          
        for i in range(2,len(state_info_temp)): 
            if state_info_temp[i]>maximum: 
                secondmax=maximum
                maximum=state_info_temp[i] 
            else: 
                if state_info_temp[i]>secondmax: 
                    secondmax=state_info_temp[i] 

        action_for_greedy_algo_A2 = int((state_info_temp.index(secondmax)))
        action = [action_for_greedy_algo_A1+1, action_for_greedy_algo_A2+1]
        
        state_info.append(run_adf(action))

        flat_list = [item for sublist in state_info for item in sublist]
        
        self.state = flat_list

    # Actions for PPO
        # self.current_action_1 = action[0]
        # self.current_action_2 = action[1]


        # print("Current Action_1: ", self.current_action_1)
        # print("Current Action_2: ", self.current_action_2)
        # print("Current State: ", self.state)
        # print("Current Episode: ", self.curr_episode)
        
        done = bool(self.curr_episode == MAX_TIMESTEP)
        if done == True:
            subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/kill.sh", shell=True)
    # Timer for 100 ms 
        time.sleep(0.14)
    # Timer for 1000 ms
        # time.sleep(1.3)
    # Timer for 10000 ms
        # time.sleep(10)
    # For cross checking
        # int(input("pause.."))
        return np.array(self.state), self.reward, done , {}

    def reset(self):
        subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/launch_file.py"])
    # Timer for 100 ms 
        time.sleep(11)
    # Timer for 1000 ms
        # time.sleep(13)
    # Timer for 10000 ms
        # time.sleep(25)
        self.curr_episode = 0
    # Reset Action for PPO
        reset_action = [0, 0]
    # Reset action for DQN
        # reset_action = 0

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
    
    with grpc.insecure_channel('localhost:3400') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
    # print for PPO2
        print("Current action_1 for 210552869: ", action_set_list[bid[0]])
        print("Current action_2 for 1962675462: ", action_set_list[bid[1]])
        print("-----------------------------------")
    # print for DQN
        # print("Current action_1 for 210552869: ", action_set_list[bid])
        # print("Current action_2 for 1962675462: ", action_set_list[36-bid])
        # print("-----------------------------------")
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
            AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[bid[1]])]))
            # AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[36-bid])]))
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
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:2212') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
    return response_reward.reward

def run_server():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:4007') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    building_state_info = []

    for i in response.buildings:
        building_state_info.append(i.fieryness)
        building_state_info.append(i.temperature)
        # building_state_info.append(i.building_id)
    return building_state_info
