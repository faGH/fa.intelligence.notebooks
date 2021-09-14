# Databricks notebook source
# MAGIC %md
# MAGIC # Simple Existing OpenAI Environment Demonstration
# MAGIC See: https://gym.openai.com/envs/#classic_control
# MAGIC # Steps
# MAGIC - Install OpenAI Gym
# MAGIC - Create Gym
# MAGIC - Create Loop
# MAGIC   - Take an action / step
# MAGIC   - Render the environment

# COMMAND ----------

pip install gym

# COMMAND ----------

pip install pyglet

# COMMAND ----------

# MAGIC %fs
# MAGIC apt install freeglut-devel

# COMMAND ----------

import gym

env = gym.make('CartPole-v0')
env.reset()

for _ in range(1000):
    env.render()
    env.step(env.action_space.sample()) # take a random action

env.close()

# COMMAND ----------


