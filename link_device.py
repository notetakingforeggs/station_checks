import os
# import selenium  

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException


def link_device(driver):
    # navigate to web page
    print("In the link function now")
    driver.get("https://web.whatsapp.com/") 
    

    #QR retrieval (in the same function to avoid log in issues) 
    print("getting webpage and initiating qr retrieval")

    # locate QR code element on page  
    element_locator = (By.XPATH, '/html/body/div[1]/div/div[2]/div[3]/div[1]/div/div/div[2]/div/canvas')
    try:
        QR = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(element_locator)
    )
        print("QR should be visible, screenshot now")

        # screenshot QR   
        QR.screenshot('static/QR.png')
                        
        # wait for presence of station checks chat to evaluate success QR scan - up to 60s 
        element_locator_2 = (By.XPATH, '//span[text() = "Station Checks"]')
        try:
            station_checks = WebDriverWait(driver, 20).until(
            EC.visibility_of_element_located(element_locator_2)
        )
        # return false if QR code is not scanned, or station chats not present in whatssapp account
        except TimeoutException:
            print("no QR, logged in?")
            return False      
        print("link_device is returning true")       
        return True
    except TimeoutException:
        print("no QR found... logged in already perhaps?")
    return False

    
        
