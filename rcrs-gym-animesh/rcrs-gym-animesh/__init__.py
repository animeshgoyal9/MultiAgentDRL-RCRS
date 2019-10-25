import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='rcrs-gym-animesh-v0',
    entry_point='rcrs-gym-animesh.envs:RCRSEnv'
)
