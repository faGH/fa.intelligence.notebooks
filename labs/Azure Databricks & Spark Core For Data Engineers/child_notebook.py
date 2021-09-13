# Databricks notebook source
dbutils.widgets.help()

# COMMAND ----------

dbutils.widgets.text("input", "", "Send the parameter value")

# COMMAND ----------

print("Example child notebook.")

# COMMAND ----------

input = dbutils.widgets.get("input")
dbutils.notebook.exit("Done with param " + input)

# COMMAND ----------


