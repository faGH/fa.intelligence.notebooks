# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion of JSON Files

# COMMAND ----------

constructors_file_path = "/mnt/dmdatabricksdqxlc/raw/constructors.json"
drivers_file_path = "/mnt/dmdatabricksdqxlc/raw/drivers.json"
races_file_path = "/mnt/dmdatabricksdqxlc/raw/results.json"
pit_stops_file_path = "/mnt/dmdatabricksdqxlc/raw/pit_stops.json"
qualifying_file_path = "/mnt/dmdatabricksdqxlc/raw/qualifying/qualifying_split_*.json"

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DateType

# COMMAND ----------

constructors_schema = "constructorId INT, constructorRef STRING, name STRING, url STRING"
driver_name_schema = StructType(fields = [
  StructField("forename", StringType(), True),
  StructField("surname", StringType(), True)
])
drivers_schema = StructType(fields = [
  StructField("driverId", IntegerType(), False),
  StructField("driverRef", StringType(), True),
  StructField("number", IntegerType(), True),
  StructField("name", driver_name_schema),
  StructField("dob", DateType(), True),
  StructField("nationality", StringType(), True),
  StructField("url", StringType(), True)
])
races_schema = "resultId INT, raceId INT, driverId INT, constructorId INT, number INT, grid INT, position INT, positionText STRING, positionOrder INT, points DOUBLE, laps INT, time STRING, milliseconds INT, fastestLap INT, rank INT, fastestLapTime STRING, fastestLapSpeed STRING, statusId INT"
pit_stops_schema = StructType(fields=[StructField("raceId", IntegerType(), False),
                                      StructField("driverId", IntegerType(), True),
                                      StructField("stop", StringType(), True),
                                      StructField("lap", IntegerType(), True),
                                      StructField("time", StringType(), True),
                                      StructField("duration", StringType(), True),
                                      StructField("milliseconds", IntegerType(), True)
                                     ])
qualifying_schema = StructType(fields=[StructField("qualifyId", IntegerType(), False),
                                      StructField("raceId", IntegerType(), False),
                                      StructField("driverId", IntegerType(), False),
                                      StructField("constructorId", IntegerType(), False),
                                      StructField("number", IntegerType(), True),
                                      StructField("position", IntegerType(), True),
                                      StructField("q1", StringType(), True),
                                      StructField("q2", StringType(), True),
                                      StructField("q3", StringType(), True)
                                     ])

# COMMAND ----------

constructors_df = spark \
  .read \
  .schema(constructors_schema) \
  .json(constructors_file_path)
drivers_df = spark \
  .read \
  .schema(drivers_schema) \
  .json(drivers_file_path)
races_df = spark \
  .read \
  .schema(races_schema) \
  .json(races_file_path)
pit_stops_df = spark \
  .read \
  .schema(pit_stops_schema) \
  .option("multiLine", True) \
  .json(pit_stops_file_path)
qualifying_df = spark \
  .read \
  .schema(qualifying_schema) \
  .option("multiLine", True) \
  .json(qualifying_file_path)

display(qualifying_df)
display(constructors_df)
display(drivers_df)
display(races_df)
display(pit_stops_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Transform DataFrame

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, col, concat, lit

# COMMAND ----------

constructors_df_transformed = constructors_df \
  .withColumnRenamed("constructorId", "constructor_id") \
  .withColumnRenamed("constructorRef", "constructor_ref") \
  .drop("url") \
  .withColumn("ingestion_date", current_timestamp())
drivers_df_transformed = drivers_df \
  .withColumnRenamed("driverId", "driver_id") \
  .withColumnRenamed("driverRef", "driver_ref") \
  .drop("url") \
  .withColumn("name", concat(col("name.forename"), lit(" "), col("name.surname"))) \
  .withColumn("ingestion_date", current_timestamp())
races_df_transformed = races_df \
  .withColumnRenamed("resultId", "result_id") \
  .withColumnRenamed("raceId", "race_id") \
  .withColumnRenamed("driverId", "driver_id") \
  .withColumnRenamed("constructorId", "constructor_id") \
  .withColumnRenamed("positionText", "position_text") \
  .withColumnRenamed("positionOrder", "position_order") \
  .withColumnRenamed("fastestLap", "fastest_lap") \
  .withColumnRenamed("fastestLapTime", "fastest_lap_time") \
  .withColumnRenamed("fastestLapSpeed", "fastest_lap_speed") \
  .withColumn("ingestion_date", current_timestamp()) \
  .drop("statusId")
pit_stops_df_transformed = pit_stops_df \
  .withColumnRenamed("raceId", "race_id") \
  .withColumnRenamed("driverId", "driver_id") \
  .withColumn("ingestion_date", current_timestamp())
qualifying_df_transformed = qualifying_df \
  .withColumnRenamed("raceId", "race_id") \
  .withColumnRenamed("qualifyId", "qualifying_id") \
  .withColumnRenamed("driverId", "driver_id") \
  .withColumnRenamed("constructorId", "constructor_id") \
  .withColumn("ingestion_date", current_timestamp())

display(constructors_df_transformed)
display(drivers_df_transformed)
display(races_df_transformed)
display(pit_stops_df_transformed)
display(qualifying_df_transformed)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write to File

# COMMAND ----------

constructors_output_directory = "/mnt/dmdatabricksdqxlc/bronze/constructors/"
drivers_output_directory = "/mnt/dmdatabricksdqxlc/bronze/drivers/"
races_output_directory = "/mnt/dmdatabricksdqxlc/bronze/results/"
pit_stops_output_directory = "/mnt/dmdatabricksdqxlc/bronze/pit_stops/"
qualifying_output_directory = "/mnt/dmdatabricksdqxlc/bronze/qualifying/"

constructors_df_transformed.write.mode("overwrite").parquet(constructors_output_directory)
drivers_df_transformed.write.mode("overwrite").parquet(drivers_output_directory)
races_df_transformed.write.mode("overwrite").partitionBy("race_id").parquet(races_output_directory)
pit_stops_df_transformed.write.mode("overwrite").parquet(pit_stops_output_directory)
qualifying_df_transformed.write.mode("overwrite").parquet(qualifying_output_directory)

# COMMAND ----------


