import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='rcrs_gym_animesh-v0',
    entry_point='rcrs_gym_animesh.envs:RCRSEnv',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)