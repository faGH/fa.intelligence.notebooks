# Databricks notebook source
# MAGIC %md
# MAGIC # Selenium Demo
# MAGIC How to use Selenium with Python. Notebooks in particular.
# MAGIC - https://selenium-python.readthedocs.io/api.html#module-selenium.webdriver.chrome.webdriver

# COMMAND ----------

# MAGIC %md
# MAGIC #### Install Dependencies

# COMMAND ----------

!pip install selenium

# COMMAND ----------

CHROMEDRIVER_PATH = "."

# COMMAND ----------

from urllib.request import urlopen
from io import BytesIO
from zipfile import ZipFile

def download_and_unzip(url, extract_to):
  http_response = urlopen(url)
  zipfile = ZipFile(BytesIO(http_response.read()))
  zipfile.extractall(path=extract_to)

# COMMAND ----------

download_and_unzip("https://chromedriver.storage.googleapis.com/95.0.4638.17/chromedriver_linux64.zip", CHROMEDRIVER_PATH)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Create Driver

# COMMAND ----------

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

options = Options()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

# COMMAND ----------

# MAGIC %md
# MAGIC #### Perform a Simple Set of Operations

# COMMAND ----------

# Step 2) Navigate to Facebook
browser.get("http://www.facebook.com")
# Step 3) Search & Enter the Email or Phone field & Enter Password
username = browser.find_element_by_id("email")
password = browser.find_element_by_id("pass")
submit   = browser.find_element_by_id("loginbutton")
username.send_keys("YOUR EMAILID")
password.send_keys("YOUR PASSWORD")
# Step 4) Click Login
submit.click()
wait = WebDriverWait( browser, 5 )
page_title = browser.title
assert page_title == "Facebook"
