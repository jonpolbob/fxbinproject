from selenium import webdriver
import selenium
import win32gui
import re
import os
import zipfile
import ntplib,datetime
import time
import threading


global pairs
timeout=60

# personalisation des options(rep de download et adresse vers chromdriver
options = webdriver.ChromeOptions()
prefs = {"download.default_directory": "c:/tmp"}
options.add_experimental_option("prefs", prefs)
chromedriver = "c:/windows/system32/chromedriver.exe"
driver = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)
driver.set_page_load_timeout(timeout)
URL = "https://deal.ig.com/platform/index.htm?201702141508"

driver.get(URL)
