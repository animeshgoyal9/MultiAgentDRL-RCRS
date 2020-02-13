import gym
import RCRS_gym

import os
import numpy as np
import shutil
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


# Create log dir
log_dir = "/u/animesh9/Documents/MultiAgentDRL-RCRS//plots/"
os.makedirs(log_dir, exist_ok=True)
# Create and wrap the environment
env = gym.make('RCRS-v2')
env = Monitor(env, log_dir, allow_early_resets=True)
# The algorithms require a vectorized environment to run
env = DummyVecEnv([lambda: env]) 
# Automatically normalize the input features
env = VecNormalize(env, norm_obs=True, norm_reward=False, clip_obs=10.)

# Add some param noise for exploration
# param_noise = AdaptiveParamNoiseSpec(initial_stddev=0.1, desired_action_stddev=0.1)
# Because we use parameter noise, we should use a MlpPolicy with layer normalization

now = datetime.now()
dt_string = now.strftime("%d/%m/%Y")
columns = ['Mean Rewards', 'Standard deviation']
df = pd.DataFrame(columns=columns)

total_timesteps_to_learn =      2500 # 50 episodes
total_timesteps_to_predict =    2500 # 50 episodes
algo_used =                     "A2C"


# Custom MLP policy of three layers of size 128 each
class CustomPolicy(FeedForwardPolicy):
    def __init__(self, *args, **kwargs):
        super(CustomPolicy, self).__init__(*args, **kwargs,
                                           net_arch=[dict(pi=[256, 256, 64, 64],
                                                          vf=[256, 256, 64, 64])], 
                                           feature_extraction="mlp")


# for i in range(2):
# model = DQN(MlpPolicy, env, verbose=1, learning_rate=0.0025, tensorboard_log = "./ppo2_rcrs_tensorboard/", batch_size = 64)
model = A2C(CustomPolicy, env, verbose=1, learning_rate=0.0025, tensorboard_log = "./ppo2_rcrs_tensorboard/", n_steps = 256)
# model = PPO2.load("rcrs_wgts_18_PPO2.pkl")
# obs = env.reset()

for k in range(25):
    # Train the agent
    model.learn(total_timesteps=int(total_timesteps_to_learn))
    # Saving the model
    model.save("{}_{}_{}".format("rcrs_wgts", k, algo_used))

    subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-server-master/boot/kill.sh", shell=True)



for j in range(25):
    # Load the trained agent
    model = A2C.load("{}_{}_{}".format("rcrs_wgts", j, algo_used))
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
    # # Create a dataframe to save the mean and standard deviation
    # df2 = pd.DataFrame([np.mean(final_rewards), stats.sem(final_rewards)], index = ['Rewards', 'Standard Error'])
    # Convert to csv
    df.to_csv("{}_{}_{}".format(1, algo_used, "MeanAndStdReward.csv", sep=',',index=True))
    # # Convert to excel
    # df2.to_excel("{}_{}_{}".format(j+1, algo_used, "MeanAndStdReward.xlsx" ))

    subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-server-master/boot/kill.sh", shell=True)

    # Kill the process once training and testing is done
subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-server-master/boot/kill.sh", shell=True)