import logging
from gym.envs.registration import register

logger = logging.getLogger(__name__)

register(
    id='BasicRoulette-v0',
    entry_point='basic_roulette.envs:BasicRoulette',
    timestep_limit=1000,
    reward_threshold=1.0,
    nondeterministic = True,
)