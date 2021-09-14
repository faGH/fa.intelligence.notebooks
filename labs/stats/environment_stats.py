# Databricks notebook source
import sys
import tensorflow.keras
import pandas as pd
import sklearn as sk
import tensorflow as tf

print(f"Tensorflow Version: {0}"

gpu_count = len(tf.config.list_physical_devices('CPU'))

print('GPU is', "available ({0} GPU)".format(gpu_count) if gpu_count > 0 else "NOT AVAILABLE")

# COMMAND ----------


