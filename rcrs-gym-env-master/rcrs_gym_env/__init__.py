from gym.envs.registration import register

register(
	id='rcrs-gym-env-v0',
	entry_point='rcrs_gym_env.envs:RCRSEnv'
)
