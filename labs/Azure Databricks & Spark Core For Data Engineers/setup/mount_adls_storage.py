# Databricks notebook source
# MAGIC %md
# MAGIC # Mount Azure Datalake Storage (Service Principal)

# COMMAND ----------

dbutils.widgets.text("storage_container_name", "raw", "Storage Container Name")
dbutils.widgets.text("storage_account_name", "monitoringstaticimages", "Storage Account Name")
dbutils.widgets.text("client_id", "5fc36737-0cba-4261-acce-d798dd2826d5", "Client Id")
dbutils.widgets.text("tenant_id", "72aa0d83-624a-4ebf-a683-1b9b45548610", "Tenant Id")
dbutils.widgets.text("client_secret", "Hn0rcY-~kw~DNi2~o.ZBD7vE0~3hjaLYv3", "Client Secret")

# COMMAND ----------

storage_container_name = dbutils.widgets.get("storage_container_name")
storage_account_name = dbutils.widgets.get("storage_account_name")
client_id = dbutils.widgets.get("client_id")
tenant_id = dbutils.widgets.get("tenant_id")
client_secret = dbutils.widgets.get("client_secret")

# COMMAND ----------

config = {
  "fs.azure.account.auth.type": "OAuth",
  "fs.azure.account.oauth.provider.type": "org.apache.hadoop.fs.azurebfs.oauth2.ClientCredsTokenProvider",
  "fs.azure.account.oauth2.client.id": f"{client_id}",
  "fs.azure.account.oauth2.client.secret": f"{client_secret}",
  "fs.azure.account.oauth2.client.endpoint": f"https://login.microsoftonline.com/{tenant_id}/oauth2/token"
}

# COMMAND ----------

print(config)

# COMMAND ----------

dbutils.fs.mount(
  source = f"abfss://{storage_container_name}@{storage_account_name}.dfs.core.windows.net/",
  mount_point = f"/mnt/{storage_account_name}/{storage_container_name}",
  extra_configs = config
)

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/public/

# COMMAND ----------

# MAGIC %fs
# MAGIC ls /mnt/dmdatabricksdqxlc/bronze

# COMMAND ----------

# dbutils.fs.unmount(f"/mnt/{storage_account_name}/{storage_container_name}")
