# Databricks notebook source
# MAGIC %md
# MAGIC # Databricks Utilities
# MAGIC - Filesystem Utilities
# MAGIC - Notebook Utilities
# MAGIC - Magic Commands
# MAGIC - Secrets

# COMMAND ----------

# MAGIC %fs
# MAGIC ls

# COMMAND ----------

dbutils.fs.ls('/')

# COMMAND ----------

for folder_name in dbutils.fs.ls('/'):
  print(folder_name)

# COMMAND ----------

dbutils.fs.help()

# COMMAND ----------

dbutils.fs.help("mount")

# COMMAND ----------

dbutils.notebook.help()

# COMMAND ----------

child_response = dbutils.notebook.run("./child_notebook", 10, {"input":"passed param demo."})

# COMMAND ----------

print(child_response)

# COMMAND ----------

# MAGIC %pip install pandas

# COMMAND ----------

dbutils.secrets.help()

# COMMAND ----------

dbutils.secrets.listScopes()

# COMMAND ----------

dbutils.secrets.list("ai-secrets")

# COMMAND ----------

example_password = dbutils.secrets.get("ai-secrets", "ExamplePassword")

print(example_password)

# COMMAND ----------


