from dateutil.parser import parse
import datetime
from bs4 import BeautifulSoup

# import selenium  
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.actions.wheel_input import ScrollOrigin
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException

import sqlite3

def update_map(driver):
    # connecting db
    conn = sqlite3.connect("stations.db")
    cursor = conn.cursor()

    # navigate to web page
    print("IN THE SCRAPE FUNCTION NOW")
    element_locator = (By.XPATH, '//span[text() = "Station Checks"]')

    try:
        station_checks = WebDriverWait(driver, 15).until(
        EC.visibility_of_element_located(element_locator)
    )
    except TimeoutException:
        print("couldnt find stationchecks")
        driver.save_screenshot("thiswhereimat.png")         
        driver.get("https://web.whatsapp.com/") 

    # assuming logging in has been done
    
    # find appropriate groupchat on page and click         
    try:
        station_checks = WebDriverWait(driver, 20).until(
        EC.visibility_of_element_located(element_locator)
    )
    except TimeoutException:
        print("couldnt find stationchecks")
        driver.save_screenshot("thiswhereimat.png")
        return False

    # click on station checks chat.
    station_checks.click()

    # finding day to check from - setting 5 days priot (maybe excessive)
    day_name = (datetime.datetime.now() - datetime.timedelta(days=5)).strftime('%A').upper()

    # scrolling up in whatsap chat
    loop = False
    counter = 0
    
    while loop == False:
        try:
            counter +=1
            today = driver.find_element(by=By.XPATH, value =f'//span[text() = "{day_name}"]')
            print ("scrolling up complete")
            loop = True
        except NoSuchElementException:
            print("not found, scrolling up")
            iframe = driver.find_element(by=By.XPATH, value ='//div[@class = "n5hs2j7m oq31bsqd gx1rr48f qh5tioqs"]')
            scroll_origin = ScrollOrigin.from_element(iframe)
            ActionChains(driver)\
            .scroll_from_origin(scroll_origin, 0, -10000)\
            .perform()

    print(" try statement passed, scrolling done, initiating scrape")
    

    ''' beginning scrape '''
    # make soup object out of page with stations on it
    page = driver.page_source
    soup = BeautifulSoup(page, "html.parser")

    #find the lowest container that holds all the information to scrape
    tab_index = soup.find('div', class_= 'n5hs2j7m oq31bsqd gx1rr48f qh5tioqs')

    # find the deepest div type containing both the date and the place number and iterate through them
    date_content = tab_index.find_all('div', class_='copyable-text')
    
    for div in date_content:
            
            # extract date
            contains_date = div['data-pre-plain-text']
            parsed_date = parse(contains_date,fuzzy=True)
            date = str(parsed_date.date())
            print(f"the date is: {date}")
        
            # extract station ID
            station_id = None
            spans = div.find_all('span', class_= None)                
            for span in spans:            
                station_ids = cursor.execute('SELECT station_id FROM stations')
                for row in station_ids:
                    if (str(row[0]) in span.text.strip()):                        
                        station_id = row[0]
                        int(station_id)
                    else:
                        continue
            print("station code is:", station_id)
                

            # update db to include the date last checked, and below to calculate the time since last checked. could combine to one line maybe?
            cursor.execute("UPDATE stations SET last_checked = ? WHERE station_id = ?", (date, station_id,))
            conn.commit()
    cursor.execute("UPDATE stations SET days_since = CAST(julianday('now') - julianday(last_checked) AS INTEGER);")     
    cursor.execute("UPDATE stations SET timestamp = datetime('now');")
    conn.commit()
    print("station last checked updated")

    return