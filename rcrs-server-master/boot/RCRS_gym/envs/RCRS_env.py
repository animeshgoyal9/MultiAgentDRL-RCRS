from __future__ import print_function
import logging

import grpc
import AgentInfo_pb2
import AgentInfo_pb2_grpc
import BuildingInfo_pb2
import BuildingInfo_pb2_grpc

import gym
from gym import error, spaces, utils
from gym.spaces import Discrete, Tuple, Box, MultiDiscrete
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
import collections

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy
# from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize, VecEnv
from stable_baselines import PPO2, DQN
# from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines import DDPG
from stable_baselines.ddpg import AdaptiveParamNoiseSpec

MAX_TIMESTEP = 100
n_agents  = 2

# action_set_list = np.array([55296,55298,55299,40964,26631,53257,49162,53258,36875,57356,55308,57358,24591,57359,55311,55312,57362,28690,57364,32789,57365,51225,55322,57371,57372,55324,34845,55325,40993,57378,36898,30754,49187,57379,53283,43044,53284,53285,24616,53288,55336,55337,53291,55339,53292,55340,57389,57391,57392,57394,55346,57395,55347,51253,53303,55353,55354,43067,30779,34876,55356,53309,55357,57406,53310,36927,24640,41024,57408,26688,57409,38978,28742,53319,53320,51276,34899,30804,36950,45142,53334,32855,57431,53336,41049,49241,53337,39001,57434,57435,43102,26719,53347,57444,53349,53350,57447,57448,57449,57450,53356,45165,53357,34926,41072,49264,39024,53363,53364,43127,32888,53371,53377,53378,45188,53380,53381,39049,34955,53391,51344,30864,53393,24722,53394,53396,53397,53399,43160,53400,45211,37020,47261,32926,28831,55457,34980,39076,24745,41134,43183,53423,53425,53426,45236,30900,53429,49336,55490,53444,55492,55493,53446,41159,55495,43208,55498,45259,30923,55499,55502,55504,55505,37081,28891,53472,53473,53474,53475,51428,53476,53477,53478,53479,55527,53480,53481,35050,55530,55533,41198,55535,26864,33010,37108,39157,55542,47351,55543,55545,55546,55548,53501,55549,53502,43264,55559,55562,45323,55564,55565,24846,53520,33041,53522,53523,55571,55572,30999,43289,53534,53536,53537,49443,53539,55587,53540,41254,55590,55593,51498,55594,55596,57645,53549,55597,31022,57647,43312,53553,53554,35123,26932,55604,55606,55607,57657,49466,57659,53563,57660,53564,57662,57663,57665,55617,57666,55619,55620,57669,31045,57670,53575,57672,57673,35146,29002,53578,57675,57676,53580,53581,57678,55630,57679,43343,53584,55632,55633,53587,57685,57688,57689,57691,57692,53597,47456,53602,29027,53603,31078,41320,33129,26986,53610,55659,55660,55661,57711,57712,57718,47481,55674,57725,57726,55678,51583,53631,27009,53633,39297,41346,29058,53634,24964,53637,55685,55686,53639,55687,57736,53640,55688,57738,53642,57739,43403,53645,53646,45456,55702,27032,51608,53656,55705,53658,31130,53659,41373,57757,57758,35230,53662,55712,29089,57762,33187,57764,53668,57765,53669,53672,55721,53674,55722,49579,55724,53677,55725,57774,53678,57775,51631,55727,31153,27059,57781,37301,57782,57783,55740,35261,33214,55743,55744,49602,51654,53702,39366,53704,53705,27082,53707,53710,53711,31184,55762,45524,53718,33239,53719,49625,53721,53722,29147,39389,37342,57823,43488,53728,53729,53732,53733,53735,53736,55784,55786,45547,55787,55789,55790,53743,53745,53746,49652,53748,55796,37365,53749,55797,31225,35323,53755,55803,53756,55804,55805,53759,45570,53762,55811,53764,55812,29190,53768,53771,53777,53778,49683,33300,31252,37398,55835,55836,25118,53791,53794,39461,53798,55846,27175,29223,55847,49704,33323,53804,53805,55853,55854,53808,47667,55859,53814,53815,53817,53820,35389,53821,55869,29246,45630,55870,37439,39488,55873,27202,53827,55875,53828,55876,53834,53835,55886,55887,53841,53842,53844,47700,53845,25174,39511,55897,55898,43613,55904,53857,55905,53858,53861,53864,53865,55917,55918,29296,53875,37493,53877,53878,53880,53881,55930,53884,53886,53889,53890,55938,31363,53892,53893,47749,29319,53895,53896,53898,49807,25233,51857,53905,53906,55954,45715,55957,53910,55959,55962,55963,53916,53917,31389,35486,39585,49834,25260,53935,37557,27319,55991,39608,35513,47802,55994,53948,29373,53949,55997,53951,43712,53952,56000,49857,56002,56003,41673,53962,37580,53964,33485,53965,47825,25299,35541,31447,43741,29408,41700,47848,53993,25322,33514,53994,53995,53996,53997,53998,31472,54001,45810,54004,39668,49915,43773,29437,54015,54017,54018,27395,33547,31503,25366,49946,47906,39715,54056,54057,33578,45868,56109,23343,56111,56112,54066,54067,25397,43831,35640,54077,54079,47935,54080,33601,56130,23366,54092,54093,43854,29519,54096,54098,54099,56148,56149,39766,41817,27481,56157,56160,47970,56162,56163,56166,54119,23399,54120,54121,56169,54122,54123,29548,37741,27502,56175,41840,25459,54133,54135,54136,39801,47993,33659,50046,23424,54146,54148,56196,27525,54149,56197,41863,56200,56201,54156,54158,54159,25488,48016,43922,31635,56211,33684,45972,54165,39830,56214,23447,54168,50073,54169,27548,56221,54174,56223,54176,56224,54179,56227,37797,56229,54182,56230,25511,54183,48039,56231,54185,54186,45995,54188,54189,23470,50098,56244,54198,56246,56247,54201,56249,54202,56250,29628,56252,54205,56253,54207,54208,56257,46018,54210,41923,54213,56261,25542,54214,56263,50121,33738,31691,56270,56271,43986,54229,54232,46041,54233,56283,56284,33759,54239,54240,31714,35811,54243,37861,56294,56296,44009,54249,56297,54250,56299,54252,56300,54253,56301,56302,56303,46064,56304,31739,33788,25600,54272,41985,44034,54275,50181,54277,54278,56327,56328,54281,56329,35851,54283,27661,37902,54286,46095,54287,54290,31762,56338,54293,56341,56342,33815,54295,54296,42010,39964,54302,54303,29729,54306,54307,44069,54309,54310,23590,27688,54313,54314,31793,42037,33848,25658,44092,54332,56380,54333,56381,54335,54336,56387,56388,56389,54345,56395,54348,56396,54349,56398,56399,35921,48210,44115,56405,56406,33879,50264,56410,56413,56414,40034,56420,56421,37990,56423,56424,48233,35946,25710,56430,56431,56433,56434,38013,48256,56448,56450,56451,29832,44169,56459,31884,27791,54415,48279,46236,56479,54432,54435,44196,54436,56485,54438,56486,36007,25768,42153,54441,54442,56492,56493,27822,56495,48304,56496,29873,54449,54450,44217,56507,33980,56508,56510,36032,56513,40131,23749,38087,29896,56520,56521,31946,27851,46285,54479,52432,54482,34003,56532,54485,54486,42199,56535,54488,54489,44250,54490,40154,54491,54492,56541,54494,48350,56542,36063,54495,38112,31969,56548,54501,56549,27878,54502,29927,46312,54504,56552,54505,54507,56555,54508,54510,54511,54513,54514,54516,54517,25846,54519,54520,54522,54523,44285,48381,38143,56576,52482,23811,56579,27909,56582,56585,54539,54540,56588,42253,56591,52496,56592,52497,48404,54551,54554,25883,27934,23838,54561,40226,54567,42280,46376,52521,52522,52525,29997,54573,34094,52526,54574,48431,54577,25910,54583,54584,54586,38203,23867,54588,36158,32062,40258,30020,34121,36181,48470,27992,52568,52569,32089,52570,38234,30043,23899,54625,52581,34150,50534,52582,54639,54640,38257,30066,54642,32114,54643,54646,48502,54648,54649,54651,25980,54652,23932,54658,54659,38280,32137,44426,52620,52621,52623,46481,23955,50580,52630,54683,36253,52638,38303,42401,44449,54689,54690,52645,54694,46504,23976,40360,52651,54700,50605,54701,54707,54708,52665,52666,48570,52667,54716,23997,52672,40385,52674,52675,50628,52676,54724,30150,54726,54727,42440,54729,54730,54733,54739,54740,36309,52693,54742,54743,52696,52697,54745,40409,54746,24028,50657,38369,54755,32228,54758,54759,46570,30189,54766,54767,52720,40432,34289,52721,52722,26099,52723,52729,54777,44538,54779,54780,50688,52738,38402,32260,54790,54791,46601,26124,36369,30225,54801,34322,52755,54803,52756,54804,50713,54810,52765,38429,52766,52767,52768,42529,54817,54818,32291,54821,54823,40488,34345,46634,54826,54827,54830,54831,50736,26161,54834,44599,38456,54840,54841,54842,36411,32316,34368,54852,40516,54854,54855,24141,52814,50767,54865,54867,54868,52821,30295,28249,52825,52826,54874,46684,40541,26207,34399,32351,54885,54886,54888,54889,50798,30318,28272,46707,32374,48761,34426,40570,54908,54909,52866,52867,50821,52875,44684,52876,52877,38541,36499,24211,34453,40598,56983,28313,56985,56986,26269,52895,52896,50850,56995,30373,56998,56999,57001,36522,57004,40621,57005,52911,52912,28337,52913,52914,57014,24248,54969,54970,32442,57018,52923,48827,52924,57020,57021,38596,42695,30407,54984,36553,28362,52940,54988,52941,52942,54990,40654,52943,54993,32465,52949,55000,26329,44761,55001,24285,50910,55007,55008,28385,46818,57061,57062,55016,32488,55022,55023,55029,55030,28408,44792,42745,57081,57084,46847,32511,57087,55040,48896,55042,57090,55043,57091,53005,55053,53006,53007,55055,53008,55056,28435,38677,34587,55072,53027,55075,53028,53029,55077,55078,55080,55081,55083,48939,28460,55084,36654,30510,38714,32571,44860,55100,42813,55102,55103,40767,55105,55108,55109,46921,55115,55116,38735,55119,32594,55125,55126,34649,55132,55133,48990,44895,55136,55138,55139,36712,38760,26473,30569,32617,28524,55158,49015,55160,55161,55163,55164,55166,55167,55169,55170,32642,24452,36749,55181,55183,40847,51088,55184,55190,49046,53143,55191,24477,44961,55201,55203,36772,55204,26534,38822,53159,55207,55208,53161,53162,42924,32688,49073,53172,53173,53174,55226,55227,26560,38849,32711,49096,42955,47051,55246,55247,34775,55255,57305,57307,57308,55261,55262,24543,38880,55265,45027,57318,55272,55273,47082,57325,53234,55282,53235,57331,53236,57332,53237,55285,53238,55286,53239,57335,24568,57336,32762,45054], dtype = object)


action_set_list = np.array([255, 960, 905, 934, 935, 936, 937, 298, 938, 939, 940, 941, 942, 943, 944, 945, 946, 947, 948, 949, 
                    950, 951, 247, 952, 248, 953, 249, 954, 250, 955, 251, 956, 957, 253, 958, 254, 959], dtype = object)

class RCRSenv(gym.Env):
    metadata = {'render.modes' : None}  
    current_action = 0
    def __init__(self):
    # Action space for PPO
        self.action_space = MultiDiscrete([len(action_set_list), len(action_set_list)])
    # Action space for DQN
        # self.action_space = Discrete(len(action_set_list))

        low = np.array([-inf]*n_agents*(len(action_set_list)+6))
        high = np.array([inf]*n_agents*(len(action_set_list)+6))
        self.observation_space = Box(low, high, dtype=np.float32, shape=None)
        self.curr_episode = 0
        self.seed()


    def step(self, action):
        
        logging.basicConfig()
        
        self.curr_episode += 1
        # if (self.curr_episode <= (MAX_TIMESTEP - 1)):
        #     self.reward = 0
        # else:
        #     self.reward = run_reward()
        print(self.curr_episode)
        state_info = []
        state_info.append(run_server())

        fieryeness_counter = collections.Counter(state_info[0][0::2])
        
        for key, value in fieryeness_counter.items():
            if 0 <= key <= 2:
                fieryeness_counter[key] = (value*10)/len(state_info[0][0::2])
            elif 3 <= key <= 5:
                fieryeness_counter[key] = value*(-5)/len(state_info[0][0::2])
            else:
                fieryeness_counter[key] = value*(-10)/len(state_info[0][0::2])
        
        self.reward = sum(fieryeness_counter.values())
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

        flat_list = [item for sublist in state_info for item in sublist]
        
        self.state = flat_list

        done = bool(self.curr_episode == MAX_TIMESTEP)
        if done == True:
            subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/kill.sh", shell=True)
    # Timer for 100 ms 
        time.sleep(0.14)
    # Timer for 1000 ms
        # time.sleep(1.3)
    # Timer for 10000 ms
        # time.sleep(10)
    # Timer for berlin map
        # time.sleep(0.19)
        # time.sleep(0.012)
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
    # # Reset action for DQN
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
    
    with grpc.insecure_channel('localhost:3401') as channel:
        stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
    # # print for PPO2
        print("Current action_1 for 210552869: ", action_set_list[bid[0]])
        print("Current action_2 for 1962675462: ", action_set_list[bid[1]])
        print("-----------------------------------")
    # print for DQN
        # print("Current action_1 for 210552869: ", action_set_list[bid])
        # print("Current action_2 for 1962675462: ", action_set_list[len(action_set_list)-1-bid])
        # print("-----------------------------------")
        response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
            AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[bid[1]])]))
            # AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[bid[1]])]))
            # AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[1425-bid])]))
            # AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[len(action_set_list)-1-bid])]))
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
    with grpc.insecure_channel('localhost:2213') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
    return response_reward.reward

def run_server():
    # NOTE(gRPC Python Team): .close() is possible on a channel and should be
    # used in circumstances in which the with statement does not fit the needs
    # of the code.
    with grpc.insecure_channel('localhost:4008') as channel:
        stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
        response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
    building_state_info = []
    for i in response.buildings:
        building_state_info.append(i.fieryness)
        building_state_info.append(i.temperature)
        # building_state_info.append(i.building_id)
    return building_state_info

