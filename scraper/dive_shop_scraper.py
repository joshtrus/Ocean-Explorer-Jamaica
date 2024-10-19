from selenium import webdriver                           # so we can instantiate a WebDriver
from selenium.webdriver.common.keys import Keys          # let's us 'type' things in the browser (i.e. in the searchbar)
from selenium.webdriver.chrome.options import Options    # so we can configure our WebDriver settings (e.g. how verbose it should be)
from selenium.webdriver.common.by import By              # to let selenium find elements *by* different identifiers (e.g. by class)
import time
from selenium.webdriver.support.ui import WebDriverWait  
from selenium.webdriver.support import expected_conditions as EC
import uuid
from boto3 import resource
from boto3.dynamodb.conditions import Attr, Key
from datetime import datetime


# SETTING UP BROWSER
#-------------------------------------------------------------------
chrome_options = Options()
# chrome_options.add_argument("--headless")
chrome_options.add_experimental_option("detach", True)
chrome_options.add_argument("--log-level=3")
prefs = {"profile.default_content_setting_values.notifications" : 2}
chrome_options.add_experimental_option("prefs",prefs)
browser = webdriver.Chrome(options=chrome_options)
browser.set_window_size(1080, 960)
#-------------------------------------------------------------------
shop_table = resource('dynamodb').Table('dive_shop_details')

def store_dive_shop(table, name, details):
    response = table.put_item(
        Item={
            'shop_id': details['id'],  #partition key
            'name': name,
            'address': details['address'],
            'activity': details['activity'],
            'image_url': details['image_url'],
            'created_date': datetime.now().isoformat()
        }
    )
    print(f'Insert response: {response}')



def get_shop_details():
    padi_url = "https://www.padi.com/dive-shops/jamaica/?page=1"
    browser.get(padi_url)

    shop_details_dict = {} 
    for x in range(1, 21):
        raw_name = browser.find_element(By.XPATH, f"""//*[@id="dsl-list"]/div/div[3]/a[{x}]/p[2]""")
        name = raw_name.text

        raw_address = browser.find_element(By.XPATH, f'''//*[@id="dsl-list"]/div/div[3]/a[{x}]/p[3]''')
        address = raw_address.text

        activity = "No activity listed"  
        try:
            # Try to get the activity from div[3]
            raw_activity = browser.find_element(By.XPATH, f"""//*[@id="dsl-list"]/div/div[3]/a[{x}]/div[3]/div[3]/p[2]""")
            activity = raw_activity.text
        except Exception:
            try:
                # If that fails, try div[2]
                raw_activity = browser.find_element(By.XPATH, f"""//*[@id="dsl-list"]/div/div[3]/a[{x}]/div[2]/div[3]/p[2]""")
                activity = raw_activity.text
            except Exception:
                activity = "No activity listed"  # Keep the default if still not found
    
        try:
            image_url = browser.find_element(By.XPATH, f"""//*[@id="dsl-list"]/div/div[3]/a[{x}]/div[1]/div/div[2]/div/div[1]/div/picture/img""").get_attribute('src')
        except Exception:
            image_url = None


        shop_id = str(uuid.uuid4())



        shop_details = {
            'id': shop_id, 
            'address': address,
            'activity': activity,
            'image_url': image_url
        }

        shop_details_dict[name] = shop_details
    return shop_details_dict


if __name__ == "__main__":

    shop_details = get_shop_details()

    for name, details in shop_details.items():
        store_dive_shop(shop_table, name, details)




