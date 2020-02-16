import gym
import RCRS_gym

import os
import numpy as np
import shutil
import sys
import socket
from scipy import stats
import pandas as pd
from openpyxl import Workbook 
import matplotlib.pyplot as plt
import time
from datetime import date, datetime
import subprocess
from subprocess import *

from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, FeedForwardPolicy
# from stable_baselines.deepq.policies import MlpPolicy
from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize, VecEnv
from stable_baselines import PPO2, DQN, A2C
# from stable_baselines.common.evaluation import evaluate_policy
from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
# from stable_baselines import DDPG
from stable_baselines.ddpg import AdaptiveParamNoiseSpec


import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# Directory 
hostname = socket.gethostname()
# Parent Directory path 
parent_dir = sys.path[0]
# Path 
path = os.path.join(parent_dir, hostname) 
# os.mkdir(path) 
path_for_kill_file = os.path.join(parent_dir, "kill.sh")


env = gym.make('RCRS-v2')
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: env]) 
# Automatically normalize the input features
env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

columns = ['Mean Rewards', 'Standard deviation']
df = pd.DataFrame(columns=columns)

total_timesteps_to_learn =      100 # 50 episodes
total_timesteps_to_predict =    100 # 50 episodes
algo_used =                     "A2C"


class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           net_arch=[dict(pi=[256, 256, 64, 64],
                                                          vf=[256, 256, 64, 64])], 
                                           feature_extraction="mlp")

model = A2C(CustomPolicy, env, verbose=1, learning_rate=0.0025,  n_steps = 256)

for k in range(1):
    # Train the agent
    model.learn(total_timesteps=int(total_timesteps_to_learn))
    # Saving the model 
    
    model.save("{}_{}_{}_{}".format("rcrs_wgts", k, algo_used, hostname))
    subprocess.Popen(path_for_kill_file, shell=True)

for j in range(1):
    # Load the trained agent
    model = A2C.load("{}_{}_{}_{}".format("rcrs_wgts", j, algo_used, hostname))

    # Reset the environment
    obs = env.reset()
    # Create an empty list to store reward values 
    final_rewards = []
    for _ in range(total_timesteps_to_predict):
        # predict the values
        action, _states = model.predict(obs)
        obs, rewards, dones, info = env.step(action)
        if dones == True:
            final_rewards.append(rewards)
    # Print the mean reward
    print(np.mean(final_rewards))
    # Print the standard deviation of reward
    print(np.std(final_rewards))
    # Create a DataFrame to save the mean and standard deviation
    df = df.append({'Mean Rewards': np.mean(final_rewards), 'Standard deviation': np.std(final_rewards)}, ignore_index=True)
    
    df.to_csv("{}_{}_{}".format(1, algo_used, "MeanAndStdReward.csv", sep=',',index=True))
    
    subprocess.Popen(path_for_kill_file, shell=True)
subprocess.Popen(path_for_kill_file, shell=True)