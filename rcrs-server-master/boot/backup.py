# class RCRSVecEnv(VecEnv):
#     """Multi-threaded Multi-agent snake environment"""
#     metadata = {'render.modes': ['human']}

#     def __init__(self, n_envs = 1, opponents = []):
#         self.action_space = spaces.Discrete(37)
#         low = np.array([-inf]*86)
#         high = np.array([inf]*86)
#         self.observation_space = spaces.Box(low, high, dtype=np.float32, shape=None)
#         self.curr_episode = 0
#         self.n_envs = n_envs
#         self.n_opponents = len(opponents)
#         self.opponents = opponents
#         super(RCRSVecEnv, self).__init__(self.n_envs, self.observation_space, self.action_space)
#         self.reset()

#     def close(self):
#         subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/kill.sh", shell=True)

#     def step_async(self, actions):
#         self.actions = action

#     def step_wait(self):

#         dones = np.asarray([ False for _ in range(self.n_envs) ])
#         rews = np.zeros((self.n_envs))
#         state = np.asarray([ {} for _ in range(self.n_envs) ])
#         state_info = []

#         for i in range(self.n_envs):
#             if (self.curr_episode <= (MAX_TIMESTEP - 1)):
#                 rews[i] = 0
#             else:
#                 rews[i] = run_reward()*1000

#             state_info.append(run_server())
#             state_info.append(run_adf(action[i]))

#             flat_list = [item for sublist in state_info for item in sublist]
        
#             state[i] = flat_list

#             dones[i] = bool(self.curr_episode == MAX_TIMESTEP)

#             if dones[i] == True:
#                 subprocess.Popen("/u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/kill.sh", shell=True)

#             time.sleep(0.14)
            
#         return state, rews, dones, {}

#     def step(self, actions):
#         self.step_async(actions)
#         return self.step_wait()

#     def reset(self):
#         subprocess.call(['gnome-terminal', '-e', "python3 /u/animesh9/Documents/RoboCup-gRPC/rcrs-server-master/boot/launch_file.py"])

#         time.sleep(11)

#         state = np.asarray([ {} for _ in range(self.n_envs)])
#         self.curr_episode = 0

#         reset_action = [ 0 for _ in range(self.n_envs)]

#         reset = []

#         for i in range(self.n_envs):
#             reset.append(run_server())
#             reset.append(run_adf(reset_action))
#             flat_list_reset = [item for sublist in reset for item in sublist]
#             state[i] = flat_list_reset
        
#         return state

#     def get_attr(self, attr_name , indices=None):
#         return self.venv.get_attr(None, indices)

#     def set_attr(self, attr_name, value, indices=None):
#         return self.venv.set_attr(None, value, indices)

#     def env_method(self, method_name, *method_args, indices=None, **method_kwargs):
#         return self.venv.env_method(None, *method_args, indices=indices, **method_kwargs)


# def run_adf(bid):
#     global flag
#     # NOTE(gRPC Python Team): .close() is possible on a channel and should be
#     # used in circumstances in which the with statement does not fit the needs
#     # of the code.
    
#     with grpc.insecure_channel('localhost:3401') as channel:
#         stub = AgentInfo_pb2_grpc.AnimFireChalAgentStub(channel)
#     # # print for PPO2
#         # print("Current action_1 for 210552869: ", action_set_list[bid[0]])
#         # print("Current action_2 for 1962675462: ", action_set_list[bid[1]])
#         # print("-----------------------------------")
#     # print for DQN
#         # print("Current action_1 for 210552869: ", action_set_list[bid])
#         # print("Current action_2 for 1962675462: ", action_set_list[1425-bid])
#         # print("-----------------------------------")
#         response = stub.getAgentInfo(AgentInfo_pb2.ActionInfo(actions = [
#             AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[bid[1]])]))
#             # AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid[0]]), AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[bid[1]])]))
#             # AgentInfo_pb2.Action(agent_id = 2090075220, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1618773504, building_id=action_set_list[1425-bid])]))
#             # AgentInfo_pb2.Action(agent_id = 210552869, building_id=action_set_list[bid]), AgentInfo_pb2.Action(agent_id = 1962675462, building_id=action_set_list[36-bid])]))
#     agent_state_info = []

#     for i in response.agents:
#         agent_state_info.append(i.agent_id)
#         agent_state_info.append(i.x)
#         agent_state_info.append(i.y)
#         agent_state_info.append(i.water)
#         agent_state_info.append(i.hp)
#         agent_state_info.append(i.idle)
#     return agent_state_info

# def run_reward():
#     # NOTE(gRPC Python Team): .close() is possible on a channel and should be
#     # used in circumstances in which the with statement does not fit the needs
#     # of the code.
#     with grpc.insecure_channel('localhost:2213') as channel:
#         stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
#         response_reward = stub.getRewards(BuildingInfo_pb2.Empty())
#     return response_reward.reward

# def run_server():
#     # NOTE(gRPC Python Team): .close() is possible on a channel and should be
#     # used in circumstances in which the with statement does not fit the needs
#     # of the code.
#     with grpc.insecure_channel('localhost:4008') as channel:
#         stub = BuildingInfo_pb2_grpc.AnimFireChalBuildingStub(channel)
#         response = stub.getBuildingInfo(BuildingInfo_pb2.Empty())
#     building_state_info = []
#     for i in response.buildings:
#         building_state_info.append(i.fieryness)
#         building_state_info.append(i.temperature)
#         # building_state_info.append(i.building_id)
#     return building_state_info