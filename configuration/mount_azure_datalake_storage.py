# Databricks notebook source
# MAGIC %md
# MAGIC # Mount Azure Datalake Storage (Service Principal)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Input Widgets for Notebook

# COMMAND ----------

dbutils.widgets.text("storage_container_name", "AZURE_STORAGE_CONTAINER_NAME", "Storage Container Name")
dbutils.widgets.text("storage_account_name", "AZURE_STORAGE_ACCOUNT_NAME", "Storage Account Name")
dbutils.widgets.text("client_id", "AZURE_SERVICE_PRINCIPAL_CLIENT_ID", "Client Id")
dbutils.widgets.text("tenant_id", "AZURE_SERVICE_PRINCIPAL_TENANT_ID", "Tenant Id")
dbutils.widgets.text("client_secret", "AZURE_SERVICE_PRINCIPAL_CLIENT_SECRET", "Client Secret")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Grab Input Values from Widgets

# COMMAND ----------

storage_container_name = dbutils.widgets.get("storage_container_name")
storage_account_name = dbutils.widgets.get("storage_account_name")
client_id = dbutils.widgets.get("client_id")
tenant_id = dbutils.widgets.get("tenant_id")
client_secret = dbutils.widgets.get("client_secret")

# COMMAND ----------

# MAGIC %md
# MAGIC ### Setup Mounting Configuration

# COMMAND ----------

config = {
  "fs.azure.account.auth.type": "OAuth",
  "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
  "fs.azure.account.oauth2.client.id": f"{client_id}",
  "fs.azure.account.oauth2.client.secret": f"{client_secret}",
  "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

# COMMAND ----------

# MAGIC %md
# MAGIC ### Perform Mount

# COMMAND ----------

dbutils.fs.mount(
  source = f"abfss://{storage_container_name}@{storage_account_name}.dfs.core.windows.net/",
  mount_point = f"/mnt/{storage_account_name}/{storage_container_name}",
  extra_configs = config
)

# COMMAND ----------

# MAGIC %md
# MAGIC ### Confirm Mount Succeeded

# COMMAND ----------

# MAGIC %fs
# MAGIC ls mnt/

# COMMAND ----------

# MAGIC %md
# MAGIC ### Allow Run as Child Notebook
# MAGIC Here we return from the notebook's execution so that if this notebook is being called by a parent, it can understand when it's done.

# COMMAND ----------

dbutils.notebook.exit(f"{storage_account_name}/{storage_container_name} mounted.")

# COMMAND ----------


