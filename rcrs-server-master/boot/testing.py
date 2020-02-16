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

# from stable_baselines.common.policies import MlpPolicy, MlpLstmPolicy, FeedForwardPolicy
from stable_baselines.deepq.policies import MlpPolicy
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

class DQN(CustomPolicy):
    def __init__(self):
        super(DQN, self).__init__()

    def learn(self, total_timesteps, callback=None, log_interval=100, tb_log_name="DQN",
              reset_num_timesteps=True, replay_wrapper=None):

        new_tb_log = self._init_num_timesteps(reset_num_timesteps)

        with SetVerbosity(self.verbose), TensorboardWriter(self.graph, self.tensorboard_log, tb_log_name, new_tb_log) \
                as writer:
            self._setup_learn()

            # Create the replay buffer
            if self.prioritized_replay:
                self.replay_buffer = PrioritizedReplayBuffer(self.buffer_size, alpha=self.prioritized_replay_alpha)
                if self.prioritized_replay_beta_iters is None:
                    prioritized_replay_beta_iters = total_timesteps
                else:
                    prioritized_replay_beta_iters = self.prioritized_replay_beta_iters
                self.beta_schedule = LinearSchedule(prioritized_replay_beta_iters,
                                                    initial_p=self.prioritized_replay_beta0,
                                                    final_p=1.0)
            else:
                self.replay_buffer = ReplayBuffer(self.buffer_size)
                self.beta_schedule = None

            if replay_wrapper is not None:
                assert not self.prioritized_replay, "Prioritized replay buffer is not supported by HER"
                self.replay_buffer = replay_wrapper(self.replay_buffer)

            # Create the schedule for exploration starting from 1.
            self.exploration = LinearSchedule(schedule_timesteps=int(self.exploration_fraction * total_timesteps),
                                              initial_p=self.exploration_initial_eps,
                                              final_p=self.exploration_final_eps)

            episode_rewards = [0.0]
            episode_successes = []
            obs = self.env.reset()
            reset = True
            F = 0


            for _ in range(total_timesteps):
                if callback is not None:
                    # Only stop training if return value is False, not when it is None. This is for backwards
                    # compatibility with callbacks that have no return statement.
                    if callback(locals(), globals()) is False:
                        break
                # Take action and update exploration to the newest value
                kwargs = {}
                if not self.param_noise:
                    update_eps = self.exploration.value(self.num_timesteps)
                    update_param_noise_threshold = 0.
                else:
                    update_eps = 0.
                    # Compute the threshold such that the KL divergence between perturbed and non-perturbed
                    # policy is comparable to eps-greedy exploration with eps = exploration.value(t).
                
                    update_param_noise_threshold = \
                        -np.log(1. - self.exploration.value(self.num_timesteps) +
                                self.exploration.value(self.num_timesteps) / float(self.env.action_space.n))
                    kwargs['reset'] = reset
                    kwargs['update_param_noise_threshold'] = update_param_noise_threshold
                    kwargs['update_param_noise_scale'] = True

                # Check if agent is busy or idle
                while (check_busy_idle() == 0):
                    with self.sess.as_default():
                        action = self.act(np.array(obs)[None], update_eps=update_eps, **kwargs)[0]
                    env_action = action
                    reset = False
                    new_obs, rew, done, info = self.env.step(env_action)
                    F = F + rew         

                # Store transition in the replay buffer.
                self.replay_buffer.add(obs, action, F, new_obs, float(done))
                obs = new_obs

                if writer is not None:
                    ep_rew = np.array([F]).reshape((1, -1))
                    ep_done = np.array([done]).reshape((1, -1))
                    total_episode_reward_logger(self.episode_reward, ep_rew, ep_done, writer,
                                                self.num_timesteps)

                episode_rewards[-1] += F

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

    # Kill the process once training and testing is done
subprocess.Popen("/u/animesh9/Documents/MultiAgentDRL-RCRS/rcrs-server-master/boot/kill.sh", shell=True)
