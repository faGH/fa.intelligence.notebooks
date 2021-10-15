# Databricks notebook source
# MAGIC %md
# MAGIC # Reinforcement Learning Practical Example for Playing Mario Bros
# MAGIC | Platform | Purpose |
# MAGIC | -- | -- |
# MAGIC | Tensorflow | Base ML Library |
# MAGIC | Tensorforce | Reinforcement Learning Library |
# MAGIC | OpenAI Gym | Reinforcement Learning Environment |

# COMMAND ----------

# MAGIC %md
# MAGIC - https://github.com/tensorforce/tensorforce/tree/master/examples
# MAGIC - https://github.com/tensorforce/tensorforce/blob/master/examples/save_load_agent.py
# MAGIC - https://pypi.org/project/gym-super-mario-bros/
# MAGIC - 

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Environment

# COMMAND ----------

!pip install -U pip
!pip install -U gym
!pip install -U gym-super-mario-bros

# COMMAND ----------

from nes_py.wrappers import JoypadSpace
import gym_super_mario_bros
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT

# COMMAND ----------

env = gym_super_mario_bros.make('SuperMarioBros-v0')
env = JoypadSpace(env, SIMPLE_MOVEMENT)

# COMMAND ----------

env.observation_space.shape

# COMMAND ----------

env.action_space

# COMMAND ----------

# MAGIC %md
# MAGIC ### Train a Random Agent
# MAGIC An angent that takes random steps and record the average reward per-episode.

# COMMAND ----------

import gym

total_episodes = 200
highest_reward = 0
openai_gym_cartpole = gym.make('MountainCar-v0')

for episode in range(total_episodes):
  episode_reward = 0
  state = openai_gym_cartpole.reset()
  done = False
  
  while not done:
    state, reward, done, info = openai_gym_cartpole.step(openai_gym_cartpole.action_space.sample())
    episode_reward += reward
    
  if episode_reward > highest_reward:
    highest_reward = episode_reward

openai_gym_cartpole.close()

print(f'[RANDOM_AGENT] Total Reward: {highest_reward}')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Agent

# COMMAND ----------

!pip install -U pip
!pip install -U tensorflow
!pip install -U tensorforce

# COMMAND ----------

import tensorflow as tf
import tensorforce as tsfrc

print(f'Tensor Flow Version: {tf.__version__}')
print(f'Tensorforce Version: {tsfrc.__version__}')
print()

gpus = len(tf.config.list_physical_devices('GPU'))

if gpus > 0:
    print(f'{gpus} GPU(s) available.')
else:
    print('Using CPU (No GPUs available).')

# COMMAND ----------

from tensorforce import Agent, Environment, Runner

# COMMAND ----------

# Create a wrapped environment of the OpenAI Gym environment we defined higher up.
#environment = Environment.create(
#    environment=env, max_episode_timesteps=total_episodes
#)

# Use simple cartpole env for testing.
openai_gym_cartpole = gym.make('MountainCar-v0')
environment = Environment.create(
    environment=openai_gym_cartpole, max_episode_timesteps=total_episodes
)

# COMMAND ----------

# Create a Tensorforce agent encaptulating the observation space and action space of our wrapped environment. Sequential memory, the Adam optimizer for gradient decent and a custom network.
agent = Agent.create(
    agent='tensorforce',
    environment=environment,  # alternatively: states, actions, (max_episode_timesteps)
    memory=10000,
    update=dict(unit='timesteps', batch_size=64),
    optimizer=dict(type='adam', learning_rate=3e-4),
    policy=dict(network='auto'),
    objective='policy_gradient',
    reward_estimation=dict(horizon=20)
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Train the Agent

# COMMAND ----------

# Train Tensorforce agent for X episodes.
max_achieved_reward = 0

for _ in range(total_episodes * 3):
    # Initialize the episode.
    states = environment.reset()
    done = False
    running_reward = 0

    while not done:
        # Episode timestep
        actions = agent.act(states=states)
        states, done, reward = environment.execute(actions=actions)
        agent.observe(terminal=done, reward=reward)
        running_reward += reward
        
        if running_reward > max_achieved_reward:
          max_achieved_reward = running_reward

agent.save(directory='./test-agent', format='checkpoint', append='episodes')
agent.close()
environment.close()

print(f'[TENSORFORCE][AGENT] Achieved Reward: {max_achieved_reward} /200')

# COMMAND ----------

# MAGIC %md
# MAGIC ### Visualize Trained Model

# COMMAND ----------

openai_gym_cartpole = gym.make('CartPole-v0')
training_environment = Environment.create(
    environment=openai_gym_cartpole, max_episode_timesteps=total_episodes
)
trained_agent = Agent.load(directory='./test-agent', format='checkpoint', environment=training_environment)

runner = Runner(agent=trained_agent, environment=training_environment)
runner.run(num_episodes=total_episodes, evaluation=True)
runner.close()

# COMMAND ----------

# MAGIC %sh
# MAGIC ls ./test-agent

# COMMAND ----------


