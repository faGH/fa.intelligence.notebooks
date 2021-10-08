# Databricks notebook source
# MAGIC %md
# MAGIC # Tensorflow Agents Example

# COMMAND ----------

# MAGIC %md
# MAGIC ### Install Dependencies

# COMMAND ----------

!pip install --upgrade pip
!pip install tensorflow==2.6
!pip install tf_agents

# COMMAND ----------

# MAGIC %md
# MAGIC ### Import Dependencies

# COMMAND ----------

import tensorflow as tf

from tf_agents.agents.dqn import dqn_agent
from tf_agents.environments import suite_gym
from tf_agents.environments import tf_py_environment
from tf_agents.eval import metric_utils
from tf_agents.metrics import tf_metrics
from tf_agents.networks import sequential
from tf_agents.policies import random_tf_policy
from tf_agents.replay_buffers import tf_uniform_replay_buffer
from tf_agents.trajectories import trajectory
from tf_agents.specs import tensor_spec
from tf_agents.utils import common

# COMMAND ----------

# MAGIC %md
# MAGIC ### Custom Environment

# COMMAND ----------

class ExampleEnv(tf_agents.py_environment.PyEnvironment):
  def observation_specs(self): #"Defines the Observations"
  def action_specs(self): #"Defines the Actions"
  
  def _reset(self): #"Reset the environment to an initial state / observation."
    #...
  
  def _step(self, action): #"Apply the Action to the Environment and return the next observation's time_step(reward, observation)"
    if is_final(self.state):
      return self.reset()
    
    observation, reward = self._apply_action(action)
    
    return TimeStep(observation, reward)

# COMMAND ----------


