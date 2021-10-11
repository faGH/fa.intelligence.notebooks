# Databricks notebook source
# MAGIC %md
# MAGIC # Solution to Rendering an OpenAI Gym Environment Inline
# MAGIC The aim of this notebook is to demistify Reinforcement Learning. To expose how simple it really is to get going. Make these systems as accessible to non-AI/ML developers as possible.
# MAGIC 
# MAGIC ### Resources
# MAGIC - https://gym.openai.com/docs/#environments
# MAGIC - https://keras-rl.readthedocs.io/en/latest/agents/overview/
# MAGIC 
# MAGIC ### TODO
# MAGIC - Refactor this notebook into nicely abstracted utilities that we can use to spin up RL agents with ease for any environment / problem domain.
# MAGIC - Create and showcase a custom environment creation and being navigated by the RL agent.

# COMMAND ----------

# MAGIC %md
# MAGIC ### Install Dependencies

# COMMAND ----------

#RUN /databricks/python3/bin/pip install --upgrade pip
#RUN /databricks/python3/bin/pip install pandas
#RUN /databricks/python3/bin/pip install urllib3
#RUN /databricks/python3/bin/pip install gym
#RUN /databricks/python3/bin/pip install tensorflow
#RUN /databricks/python3/bin/pip install tf-agents
#RUN /databricks/python3/bin/pip install install keras-rl2
#RUN /databricks/python3/bin/pip install plotly
#RUN /databricks/python3/bin/pip install opencv-python
#RUN /databricks/python3/bin/pip install opencv-contrib-python
#RUN /databricks/python3/bin/pip install av
#RUN /databricks/python3/bin/pip install pyvirtualdisplay
#RUN /databricks/python3/bin/pip install box2d
#RUN /databricks/python3/bin/pip install pyglet
#RUN /databricks/python3/bin/pip install ale-py
#RUN /databricks/python3/bin/pip install pyopengl

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Virtual Display

# COMMAND ----------

import matplotlib.pyplot as plt
from pyvirtualdisplay import Display

display = Display(visible=0, size=(1400, 900))
display.start()

from IPython import display

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Utilities

# COMMAND ----------

class OpenAIGymSessionVideo:
  def __init__(self, environment):
    self.environment = environment
    self.frames = []
    
  def renderAndCapture(self, epoch_id):
    from PIL import Image
    import base64
    from io import BytesIO

    three_d_rgb_array = self.environment.render(mode='rgb_array')
    image = Image.fromarray(three_d_rgb_array, 'RGB')
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')

    import numpy as np
    import cv2
    import io
    import os
    
    video_fps = 30
    video_codec = cv2.VideoWriter_fourcc(*'MP4V')
    video_output = cv2.VideoWriter(f'{epoch_id}.mp4', video_codec, video_fps, image.size)

    for frame in self.frames:
      video_output.write(frame)

    video_output.release()
    # Convert the video to codecs web supports.
    os.system(f"ffmpeg -i {epoch_id}.mp4 -vcodec libx264 {epoch_id}.web.mp4")
    
    self.frames = []
    video = io.open(f'{epoch_id}.web.mp4', 'r+b').read()
    encoded_video = base64.b64encode(video)
    base64_video = encoded_video.decode('utf-8')
    video_tag =f'<video controls loop autoplay width="250px" height="200px"><source src="data:video/mp4;base64,{base64_video}" type="video/mp4" /></video>'
    
    displayHTML(video_tag)
    
  def capture(self):
    from PIL import Image
    import base64
    from io import BytesIO

    three_d_rgb_array = self.environment.render(mode='rgb_array')
    image = Image.fromarray(three_d_rgb_array, 'RGB')
    image_buffer = BytesIO()
    image.save(image_buffer, format='PNG')
    
    import numpy as np
    import cv2
    
    im_arr = np.frombuffer(image_buffer.getvalue(), dtype=np.uint8)
    self.frames.append(cv2.imdecode(im_arr, flags=cv2.IMREAD_COLOR))

# COMMAND ----------

class OpenAIGymSession:
  def __init__(self, environment_name):
    self.environment_name = environment_name
    
  def start(self, episodes, max_epochs=-1):
    import gym
    import uuid

    session_id = uuid.uuid4()
    env = gym.make(self.environment_name)
    env_display = OpenAIGymSessionVideo(env)

    # For each iteration we want to run.
    for episode in range(episodes):
      env.reset()
        
      episodes_id = uuid.uuid4()
      current_epoch = 0
      # Take an initial random action / step.
      action = env.action_space.sample()
      observation, reward, done, info = env.step(action)
      
      # Run the loop again if the environment is not done.
      while not(done):
        current_epoch += 1

        # Break out of the loop if we have reached max_epochs with no done status.
        if max_epochs > -1 and current_epoch >= max_epochs:
          # Render last image of this iteration.
          env_display.renderAndCapture(episodes_id)
          return
        
        # Take next action / step.
        action = env.action_space.sample()
        observation, reward, done, info = env.step(action)
        env_display.capture()
      # Render last image of this iteration.
      env_display.renderAndCapture(episodes_id)
    env.close()

# COMMAND ----------

class OpenAIGymSessionForModel:
  def __init__(self, environment_name):
    self.environment_name = environment_name
    
  def start(self, model, episodes=1, max_epochs=-1):
    import gym
    import uuid

    session_id = uuid.uuid4()
    env = gym.make(self.environment_name)
    env_display = OpenAIGymSessionVideo(env)

    # For each iteration we want to run.
    for episode in range(episodes):
      initial_observation = env.reset()
        
      episodes_id = uuid.uuid4()
      current_epoch = 0
      # Take an initial random action / step.
      action = model.forward(initial_observation)
      observation, reward, done, info = env.step(action)
      
      # Run the loop again if the environment is not done.
      while not(done):
        current_epoch += 1

        # Break out of the loop if we have reached max_epochs with no done status.
        if max_epochs > -1 and current_epoch >= max_epochs:
          # Render last image of this iteration.
          env_display.renderAndCapture(episodes_id)
          return
        
        # Take next action / step.
        action = model.forward(observation)
        observation, reward, done, info = env.step(action)
        env_display.capture()
      # Render last image of this iteration.
      env_display.renderAndCapture(episodes_id)
    env.close()

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Environment
# MAGIC Our utilities support rendering various OpenAI Gym environments. See https://gym.openai.com/envs/#classic_control for more.

# COMMAND ----------

episodes = 1;
env_name = "LunarLander-v2"
session = OpenAIGymSession(env_name)

session.start(episodes);

# COMMAND ----------

episodes = 1
env_name = "CartPole-v1"
session = OpenAIGymSession(env_name)

session.start(episodes);

# COMMAND ----------

# MAGIC %md
# MAGIC ### Custom Environment

# COMMAND ----------

import gym
from gym import spaces

# Simple environment taking a discrete and continuious action.
class AdditionCompetitionEnv(gym.Env):
  """Custom Environment that follows gym interface"""
  metadata = {'render.modes': ['human']}

  def __init__(self):
    super(AdditionCompetitionEnv, self).__init__()

    self.state = 0
    # 0) Sutract 1, 1) Add 1
    self.action_space = gym.spaces.Discrete(3)
    self.observation_space = gym.spaces.Discrete(1)

  def step(self, action):
    if action == 0:
        self.state -= 1
    elif action == 2:
        self.state += 1
    
    done = self.state <= 200 or self.state >= 200
    info = {}
    
    return self.state, self.state, done, info
  def reset(self):
    # Reset the state of the environment to an initial state
    #self.state = 0
    
    return self.state

# COMMAND ----------

# MAGIC %md
# MAGIC ### Introducting a Deep Q Network

# COMMAND ----------

import numpy as np
import gym

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Activation, Flatten
from tensorflow.keras.optimizers import Adam

from rl.agents.dqn import DQNAgent
from rl.policy import BoltzmannQPolicy
from rl.memory import SequentialMemory

ENV_NAME = 'LunarLander-v2'

# Get the environment and extract the number of actions.
env = gym.make(ENV_NAME)
np.random.seed(123)
env.seed(123)
env = AdditionCompetitionEnv()
nb_actions = env.action_space.n

# Next, we build a very simple model. This is the network structure.
model = Sequential()
model.add(Flatten(input_shape=(1,) + env.observation_space.shape))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(16))
model.add(Activation('relu'))
model.add(Dense(nb_actions))
model.add(Activation('linear'))
print(model.summary())

memory = SequentialMemory(limit=50000, window_length=1)
policy = BoltzmannQPolicy()
dqn = DQNAgent(model=model, nb_actions=nb_actions, memory=memory, nb_steps_warmup=10,
               target_model_update=1e-2, policy=policy)
dqn.compile(Adam(learning_rate=1e-3), metrics=['mae'])

# Start the training.
dqn.fit(env, nb_steps=50000, visualize=False, verbose=2)

# Persist the model state.
dqn.save_weights(f'dqn_{ENV_NAME}_weights.h5f', overwrite=True)

# Test the model 
dqn.test(env, nb_episodes=5, visualize=False)

# COMMAND ----------

# Get the initial observations from a reset environment. (From it's initial state)
initial_observation = env.reset()
# Ask the model what the next action should be in the environment's action_space. This is an index that can be passed to env.step to take the action which would in turn return a new observation which we can look through till the environment is done etc.
next_action = dqn.forward(initial_observation)

# COMMAND ----------

initial_observation

# COMMAND ----------

next_action

# COMMAND ----------

# We can take the action suggested by the model and get a observation among other things back which we can then use in a loop.
observation, reward, done, info = env.step(dqn.forward(initial_observation))

print(env.step(dqn.forward(initial_observation)))

# COMMAND ----------

# Trained model making action decisions.
env_name = "LunarLander-v2"
session = OpenAIGymSessionForModel(env_name)

session.start(dqn);

# COMMAND ----------


