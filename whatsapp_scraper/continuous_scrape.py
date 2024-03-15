# here looking at changing this so rather than the flask app doing everything, there is a python script that is hosted which runs periodically 
#continually scraping the data and updating the db, and then a simpler flask app that just pulls data from the db and presents a map.. reducing complexity 
# at the front end. how log in server side? for now can just do it on the computer and scan whatsapp. figure other ways later.

# and can put in a docker container i think? separately, so container for python script which just runs and updates. separate container with flask
# app in it which draws from the other guy.

import sys
from link_device import link_device
from update_map import update_map
import sqlite3
import os
import time
from datetime import datetime
from threading import Thread
from queue import Queue
import shutil
from time import sleep


# import selenium  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException



# time imports
from dateutil.parser import parse
import time

# alterations to chromedriver to allow it to run headless, 
chrome_options = webdriver.ChromeOptions()
chrome_options.add_argument("--no-sandbox")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# this to solve issue of headless browser using old chrome or something?
chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

# this is to save the user data between sessions to avoid logging in each time
chrome_options.add_argument('--user-data-dir=./User_Data')



# connect to stations database
conn = sqlite3.connect("stations.db")
cursor = conn.cursor()

# initiate driver
global driver
driver = webdriver.Chrome(options=chrome_options)

# get whatsapp webpage
driver.get("https://web.whatsapp.com/") 

#TODO put in a scoll down chats bit here, for personal phone swamping whatsapp chats

# check for station checks first, because user data should be keeping it logged in.
element_locator = (By.XPATH, '//span[text() = "Station Checks"]')
try:
    station_checks = WebDriverWait(driver, 60).until(
    EC.visibility_of_element_located(element_locator)
)
    # initiate update
    print("station checks found - initiating update")
    update_map(driver)
    print("update complete - exiting")
    driver.quit()
    sys.exit()

# link device if no stationchecks
except TimeoutException:
    print("couldnt find stationchecks")
    driver.save_screenshot("thiswhereimat.png")
    link_device(driver)

# then intitate update map
update_map(driver)
print("update complete - exiting")
driver.quit()
sys.exit()