import os
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
import sqlite3
import string

#-----------------------------------------------------------------------------------------------------------------#
#SETTING UP DATABASE STUFF
#Connection and cursor
conn = sqlite3.connect('diveShop.db')
cursor = conn.cursor()

#Create Table
createTable = """CREATE TABLE IF NOT EXISTS
dive_shop_data(id INTEGER PRIMARY KEY autoincrement, shopName TEXT, shopPhone TEXT, shopEmail TEXT, shopAddress TEXT, shopWebsite TEXT)"""
cursor.execute(createTable)

#-----------------------------------------------------------------------------------------------------------------#
os.environ["PATH"] += os.pathsep + r'/Users/joshmorris/Documents/Side Projects/Ocean Explorer Jamaica/backend/scraper/chromedriver'
chrome_options = Options()
#chrome_options.add_argument("--headless")
browser = webdriver.Chrome()
#-----------------------------------------------------------------------------------------------------------------#

browser.get("https://www.padi.com/dive-shops/jamaica/?page=1")