# Databricks notebook source
# MAGIC %md
# MAGIC # Check General Library Versions

# COMMAND ----------

# MAGIC %md
# MAGIC ### Tensorflow

# COMMAND ----------

import sys
import tensorflow.keras
import pandas as pd
import sklearn as sk
import tensorflow as tf

print(f"Tensorflow Version: {tf.__version__}")

gpu_count = len(tf.config.list_physical_devices('CPU'))

print('GPU(s) are', "available ({0} GPU)".format(gpu_count) if gpu_count > 0 else "NOT AVAILABLE")

# COMMAND ----------


