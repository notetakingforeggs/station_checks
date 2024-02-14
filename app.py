# here looking at changing this so rather than the flask app doing everything, there is a python script that is hosted which runs periodically 
#continually scraping the data and updating the db, and then a simpler flask app that just pulls data from the db and presents a map.. reducing complexity 
# at the front end. how log in server side? for now can just do it on the computer and scan whatsapp. figure other ways later.

# and can put in a docker container i think? separately, so container for python script which just runs and updates. separate container with flask
# app in it which draws from the other guy.


from map import map
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
#chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-gpu")
# this to solve issue of headless browser using old chrome or something?
chrome_options.add_argument("user-agent=User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

# this is to save the user data between sessions to avoid logging in each time
chrome_options.add_argument('--user-data-dir=./User_Data')



# connect to stations database
conn = sqlite3.connect("stations.db")
cursor = conn.cursor()


global driver
driver = webdriver.Chrome(options=chrome_options)


# if not driver check for station checks then initate link device function
print("IN THE SCRAPE FUNCTION NOW")
driver.get("https://web.whatsapp.com/") 


if not os.path.exists("static/QR.png"):
    print("no QR and User data present, using as standin for logged in")
    link_device(driver)
    
    # check for appropriate groupchat on page and click         
element_locator = (By.XPATH, '//span[text() = "Station Checks"]')
try:
    station_checks = WebDriverWait(driver, 20).until(
    EC.visibility_of_element_located(element_locator)
)
except TimeoutException:
    print("couldnt find stationchecks")
    driver.save_screenshot("thiswhereimat.png")
    link_device(driver)


# else intitate infinite loop of update stations

while True:
    update_map(driver)
    sleep() 


    
# If QR already exists just remove data? allows to log in as someone else?
#TODO here either make sessions so that log in turns to log out if already logged in
if os.path.exists("static/QR.png"):
    print("QR and User data present, using as standin for logged in")
    os.remove("static/QR.png")
    shutil.rmtree("User_Data")
    errormsg1 = "device was already linked, now unlinked so try again"

# wait for QR existence and render 'scanme' template
print("also checking for QR")
counter = 0
while not os.path.exists("static/QR.png"):
    print("no QR yet")
    time.sleep(5)
    counter +=1
    if counter >= 6:                
        print("taking too long to log in")         
        #TODO make and error page like apology       
         
    
#return qr for scanning    
print("returning scanme.html")

              


    
    # check for log in (user data and QR presence)
    if not os.path.exists("static/QR.png"):
        print("No QR, not logged in")
        return render_template("apology.html", content = "No QR not logged in")
    if (update_map(driver)):
        return redirect("/map")
    else:
        return render_template("apology.html", content = "stationchecks not found, are you sure you have linked an appropriate device?")
    # TODO better to just prevent the user from being able to access the update button if not logged in.
   
@app.route("/repopulate")
def repopulate():
    return render_template("apology.html", content = "under construction")
        