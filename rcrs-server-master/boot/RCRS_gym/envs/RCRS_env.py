
from __future__ import print_function
import logging

import grpc

import AgentInfo_pb2
import AgentInfo_pb2_grpc
import BuildingInfo_pb2
import BuildingInfo_pb2_grpc

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
import time, math
from numpy import inf
import time, os 
import signal, sys
import threading
# import psutil


MAX_TIMESTEP = 100

action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}  
    current_action = 0
    def __init__(self):
        self.action_space = spaces.Discrete(37)
        
        low = np.array([0]*116)
        high = np.array([inf]*116)

        self.observation_space = spaces.Box(low, high, dtype=np.float32, shape=None)

        self.curr_episode = 0
        self.seed()


    def step(self, action):
        
        logging.basicConfig()
        
        self.curr_episode += 1
        self.reward = run_reward()
        state_info = []

        state_info.append(run_server())
        state_info.append(run_adf(action))

        flat_list = [item for sublist in state_info for item in sublist]
        
        self.state = flat_list

        self.current_action = action

        # print("Current Action: ", self.current_action)
        # print("Current State: ", self.state)
        print("Current Episode: ", self.curr_episode)
        
        done = bool(self.reward == 0 or self.curr_episode == MAX_TIMESTEP)
        if done == True:
            os.system("for pid in $(ps -ef | grep 'start-comprun'); do kill -2 $pid; done")

        time.sleep(1)
        return np.array(self.state), self.reward, done , {}

    def reset(self):
        subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/delete_master.py"])
        time.sleep(15)
        self.curr_episode = 0
        reset_action = 0
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
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:9090') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
        print("Current action: ", action_set_list[bid])
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
            AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[len(action_set_list) - bid -1])]))
    # print(response.agents)
    agent_state_info = []

    for i in response.agents:
        agent_state_info.append(i.agent_id)
        agent_state_info.append(i.x)
        agent_state_info.append(i.y)
        agent_state_info.append(i.water)
        agent_state_info.append(i.hp)
    return agent_state_info

def run_reward():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:2212') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        # response = stub.getBuildingInfo(BuildingInfo_pb2.BuildingInfo(buildings = [
            # BuildingInfo_pb2.Building(fieryness = 1, temperature=1, building_id = 1), BuildingInfo_pb2.Building(fieryness = 2, temperature=2, building_id = 2)]))
        response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
    # print(response_reward.reward)
    return response_reward.reward

def run_server():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:4007') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        # response = stub.getBuildingInfo(BuildingInfo_pb2.BuildingInfo(buildings = [
            # BuildingInfo_pb2.Building(fieryness = 1, temperature=1, building_id = 1), BuildingInfo_pb2.Building(fieryness = 2, temperature=2, building_id = 2)]))
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    building_state_info = []

    for i in response.buildings:
        building_state_info.append(i.fieryness)
        building_state_info.append(i.temperature)
        building_state_info.append(i.building_id)
    # print(fieryness_values
    return building_state_info
    print("*******************************************")

# if __name__ == '__main__':
#     logging.basicConfig()
#     state_info = []
#     while True:
#         run_adf(253)
#         run_reward()
#         run_server()
#         state_info.append(run_server())
#         # state_info.append(run_adf(249))
#         flat_list = [item for sublist in state_info for item in sublist]
#         print(flat_list)
#         time.sleep(4)
