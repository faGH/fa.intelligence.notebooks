# Databricks notebook source
# MAGIC %md
# MAGIC # Ingestion of CSV Files

# COMMAND ----------

# MAGIC %md
# MAGIC #### Check File Mounts

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/dmdatabricksdqxlc/raw/

# COMMAND ----------

# MAGIC %md
# MAGIC #### Read the CSV file using the Spark DataFrame Reader API
# MAGIC - https://spark.apache.org/docs/latest/api/python/reference/pyspark.sql.html#input-and-output

# COMMAND ----------

from pyspark.sql.types import StructType, StructField, IntegerType, StringType, DoubleType

# COMMAND ----------

circuit_schema = StructType(fields = [
  StructField("circuitId", IntegerType(), False),
  StructField("circuitRef", StringType(), True),
  StructField("name", StringType(), True),
  StructField("location", StringType(), True),
  StructField("country", StringType(), True),
  StructField("lat", DoubleType(), True),
  StructField("lng", DoubleType(), True),
  StructField("alt", IntegerType(), True),
  StructField("url", StringType(), True)
])
race_schema = StructType(fields = [
  StructField("raceId", IntegerType(), False),
  StructField("year", IntegerType(), True),
  StructField("round", IntegerType(), True),
  StructField("circuitId", IntegerType(), False),
  StructField("name", StringType(), True),
  StructField("date", StringType(), True),
  StructField("time", StringType(), True),
  StructField("url", StringType(), True)
])
lap_times_schema = StructType(fields = [
  StructField("raceId", IntegerType(), False),
  StructField("driverId", IntegerType(), False),
  StructField("lap", IntegerType(), True),
  StructField("position", IntegerType(), True),
  StructField("time", StringType(), True),
  StructField("milliseconds", IntegerType(), True)
])

# COMMAND ----------

circuits_file_path = "/mnt/dmdatabricksdqxlc/raw/circuits.csv"
races_file_path = "/mnt/dmdatabricksdqxlc/raw/races.csv"
lap_times_file_path = "/mnt/dmdatabricksdqxlc/raw/lap_times/lap_times_split_*.csv"
circuits_df = spark \
  .read \
  .option("header", True) \
  .schema(circuit_schema) \
  .csv(circuits_file_path)
races_df = spark \
  .read \
  .option("header", True) \
  .schema(race_schema) \
  .csv(races_file_path)
lap_times_df = spark \
  .read \
  .schema(lap_times_schema) \
  .csv(lap_times_file_path)

# COMMAND ----------

# circuits_df.show()
display(circuits_df)
display(races_df)
display(lap_times_df)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Drop Columns We Don't Need

# COMMAND ----------

from pyspark.sql.functions import col

# COMMAND ----------

circuits_selected = circuits_df \
  .select(col("circuitId"), col("circuitRef"), col("name"), col("location"), col("country"), col("lat"), col("lng"), col("alt"))
races_selected = races_df \
  .select(col("raceId"), col("year"), col("round"), col("circuitId"), col("name"), col("date"), col("time"))

display(circuits_selected)
display(races_selected)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Rename Columns

# COMMAND ----------

circuits_renamed = circuits_selected \
  .withColumnRenamed("circuitId", "circuit_id") \
  .withColumnRenamed("circuitRef", "circuit_ref") \
  .withColumnRenamed("lat", "latitude") \
  .withColumnRenamed("lng", "longitude") \
  .withColumnRenamed("alt", "altitude")
races_renamed = races_selected \
  .withColumnRenamed("raceId", "race_id") \
  .withColumnRenamed("year", "race_year") \
  .withColumnRenamed("circuitId", "circuit_id")
lap_times_renamed = lap_times_df \
  .withColumnRenamed("raceId", "race_id") \
  .withColumnRenamed("driverId", "driver_id")

display(lap_times_renamed)
display(circuits_renamed)
display(races_renamed)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Add New Column

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, to_timestamp, concat, lit

# COMMAND ----------

circuits_final = circuits_renamed.withColumn("ingestion_date", current_timestamp())
races_final = races_renamed \
  .withColumn("race_timestamp", to_timestamp(concat(col("date"), lit(" "), col("time")), "yyyy-MM-dd HH:mm:ss")) \
  .withColumn("ingestion_date", current_timestamp()) \
  .drop("date") \
  .drop("time")
lap_times_final = lap_times_renamed \
  .withColumn("ingestion_date", current_timestamp()) \

display(lap_times_final)
display(circuits_final)
display(races_final)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Write Data to Filesystem (With Partitioning)

# COMMAND ----------

final_circuits_directory_path = "/mnt/dmdatabricksdqxlc/bronze/circuits"
circuits_final.write.mode("overwrite").parquet(final_circuits_directory_path)

final_races_directory_path = "/mnt/dmdatabricksdqxlc/bronze/races"
races_final \
  .write \
  .mode("overwrite") \
  .partitionBy("race_year") \
  .parquet(final_races_directory_path)

final_lap_times_directory_path = "/mnt/dmdatabricksdqxlc/bronze/lap_times"
lap_times_final \
  .write \
  .mode("overwrite") \
  .parquet(final_lap_times_directory_path)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/dmdatabricksdqxlc/bronze/

# COMMAND ----------

circuits_df = spark.read.parquet(final_circuits_directory_path)
races_df = spark.read.parquet(final_races_directory_path)

display(circuits_df)
display(races_df)

# COMMAND ----------


