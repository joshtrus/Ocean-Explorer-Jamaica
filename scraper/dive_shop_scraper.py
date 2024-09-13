import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sqlite3
import string

#-----------------------------------------------------------------------------------------------------------------#
#SETTING UP DATABASE 
#Connection and cursor
conn = sqlite3.connect('diveShop.db')
cursor = conn.cursor()

#Create Table
createTable = """CREATE TABLE IF NOT EXISTS
dive_shop_data(id INTEGER PRIMARY KEY autoincrement, shopName TEXT, shopPhone TEXT, shopEmail TEXT, shopParish TEXT, shopAddress TEXT, shopWebsite TEXT, activityType TEXT)"""
cursor.execute(createTable)

#-----------------------------------------------------------------------------------------------------------------#
os.environ["PATH"] += os.pathsep + r'/Users/joshmorris/Documents/Side Projects/Ocean Explorer Jamaica/scraper/chromedriver'
chrome_options = Options()
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome()
#-----------------------------------------------------------------------------------------------------------------#
shop_name = []
shop_phone = []
sho_email = []
shop_address = []
shop_website = []
p = 0



for x in range(1,3):
    browser.get(f"https://www.padi.com/dive-shops/jamaica/?page={x}")
    p += 1 
    
    for x in range(1,21):
        name = browser.find_element("xpath", 
                                    f"""/html/body/section/div[3]/div[1]/div[2]/div/div[3]/a[{x}]/p[2]""")
        name = name.text
        print(name)

        
