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

from stable_baselines.common.vec_env import DummyVecEnv, VecNormalize, VecEnv
from stable_baselines import PPO2, DQN, A2C, DDPG
from stable_baselines import results_plotter
from stable_baselines.bench import Monitor
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines.ddpg import AdaptiveParamNoiseSpec

import warnings
warnings.filterwarnings("ignore", category=DeprecationWarning) 


total_timesteps_to_learn =      2500 # 50 episodes
total_timesteps_to_predict =    2500 # 50 episodes
algo_used =                     "PPO2"
training_iterations =           20
testing_iterations =            20


if (algo_used == "PPO2"):
    from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, FeedForwardPolicy
else:
    from stable_baselines.deepq.policies import MlpPolicy

# Directory 
hostname = socket.gethostname()
# Parent Directory path 
parent_dir = sys.path[0]
# Path 
path = os.path.join(parent_dir, hostname) 
# os.mkdir(path) 
path_for_kill_file = os.path.join(parent_dir, "kill.sh")
columns = ['Mean Rewards', 'Standard deviation']
df = pd.DataFrame(columns=columns)


env = gym.make('RCRS-v2')
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: env]) 
# Automatically normalize the input features
env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           net_arch=[dict(pi=[256, 256, 64, 64],
                                                          vf=[256, 256, 64, 64])], 
                                           feature_extraction="mlp")

model = PPO2(CustomPolicy, env, verbose=1, learning_rate=0.0025,  n_steps = 256)

for k in range(training_iterations):
    # Train the agent
    model.learn(total_timesteps=int(total_timesteps_to_learn))
    # Saving the model 
    
    model.save("{}_{}_{}_{}".format("rcrs_wgts", k, algo_used, hostname))
    subprocess.Popen(path_for_kill_file, shell=True)

for j in range(testing_iterations):
    # Load the trained agent
    model = PPO2.load("{}_{}_{}_{}".format("rcrs_wgts", j, algo_used, hostname))

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