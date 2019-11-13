
from __future__ import print_function
import logging

import grpc

import PyRL_pb2
import PyRL_pb2_grpc

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

MAX_TIMESTEP = 300

action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}
    # x = 0
    # v = 0   
    current_action = 0
    def __init__(self):
        # Add the bash start-comprun.sh command here
        # self.goal_position = 0.5
        # self.goal_velocity = 0
        self.action_space = spaces.Discrete(36)
        
        low = np.array([0, inf])
        high = np.array([0, inf])
        
        self.observation_space = spaces.Box(low, high, dtype=np.float32, shape=None)

        self.curr_episode = 0
        self.seed()


    def step(self, action):
        
        self.curr_episode += 1
        # Take the input of reward from gRPC
        reward = -1
        self.current_action = action
        logging.basicConfig()
        self.x, self.v = run(action)
        
        print("Current Action: ", self.current_action)
        print("Current Location: ", self.x, ", ", self.v)

        self.state = (self.x, self.v)
        print("Current Episode: ", self.curr_episode)
        
        done = bool(self.reward == 0 or self.curr_episode == MAX_TIMESTEP)
        # done = bool(self.x >= 0.5)
        return np.array(self.state), reward, done , {}

    def reset(self):
        # Add the sh kill.sh command here
        self.curr_episode = 0
        
        reset_action = 3
        self.x, self.v = run(reset_action)
        print("Reset Location: ", self.x, ", ", self.v)
        self.state = (self.x, self.v)
        return np.array(self.state) 

    def seed(self, seed = None):
        self.np_random, seed = seeding.np_random(seed)
        return [seed]

def run_adf():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:9090') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
            AgentInfo_pb2.Action(agent_id = 1, building_id=1), AgentInfo_pb2.Action(agent_id = 2, building_id=2)]))
    print(response.agents)

def run_server():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:2212') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        # response = stub.getBuildingInfo(BuildingInfo_pb2.BuildingInfo(buildings = [
            # BuildingInfo_pb2.Building(fieryness = 1, temperature=1, building_id = 1), BuildingInfo_pb2.Building(fieryness = 2, temperature=2, building_id = 2)]))
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    print(response.buildings)

if __name__ == '__main__':
    logging.basicConfig()
    run_adf()
    run_server()
