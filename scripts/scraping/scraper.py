from selenium import *
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import time
import json
import os.path
import sys
import pickle



if len(sys.argv) > 1:
     searchTerm = str(sys.argv[1])
else:
    searchTerm = "laptop"

'''
class toJSON:
    StoreName = ''
    products = []

class product:
    url = ''
    upc = ''
    name = ''
    #category_id = pass
    #subcategory_id = pass
    description = ''
    #keyword = []
    img_url = []

def resetProduct(p: product):
    p.url = ''
    p.upc = ''
    p.description = ''
    #p.keyword = []
    img_url = ''

'''
PATH = "C:\Program Files\chromedriver\chromedriver.exe"
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option ("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options = options)

stealth(driver,
      languages = ["en-US", "en"],
      vendor="Google Inc",
      platform="Win32",
      webgl_cendor="Intel Inc.",
      renderer="Intel Iris OpenGL Engine",
      fix_hairline=True,
      )


toJSON = {
    "store": "Texas State Bookstore",
    "products":  []
}
prodTemplate = {
    "url": None,
    "upc": None,
    "name": None,
    "description": None,
    "img_url": None
}
def resetTemplate(a: prodTemplate):
    a["url"] = None
    a["upc"] = None
    a["name"] = None
    a["description"] = None
    a["img_url"] = None

ERROR = 0

url = "https://www.bkstr.com/texasstatestore/"
#url = "https://www.walmart.com/"


# with open("cookies2.txt") as f:
#      data = json.load(f)
#      data = json.dumps(data)
#data = data.replace("[", '').replace("]", '')
#print(data)
#data = data.split("},")

driver.get(url + "404")
cookies = pickle.load(open("cookies.pkl", "rb"))
for cookie in cookies:
    driver.add_cookie(cookie)


search = WebDriverWait(driver, 40).until(
        EC.element_to_be_clickable((By.NAME, "searchValue"))
)
#search = driver.find_element(By.NA
#ME, "searchValue")
search.send_keys(searchTerm)
search.send_keys(Keys.RETURN)

time.sleep(3)
search_page = driver.current_url
products = driver.find_elements(By.CLASS_NAME, "product-tile__photo")
#products = driver.find_elements(By.XPATH, 
#"/html[1]/body[1]/ef-root[1]/ef-store[1]/ef-category-landing-page[1]/main[1]/div[2]/div[1]/div[2]/div[1]/ef-category-results-section[1]/div[1]/div[2]"
#)
print('found products')
num = len(products)


scraped = 0

while scraped < num:
        try:
            if scraped > 3:
                #ActionChains(driver)\
                #   .scroll_to_element(products[scraped])\
                #   .perform()
                i = scraped//4
                while i != 0:
                    driver.execute_script("window.scrollBy(0,500)", "")
                    i-=1

            products[scraped].click()
            local_product = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "pdp-container"))
            )
            #local_product = driver.find_element(By.CLASS_NAME, "pdp-container")
            local_url = driver.current_url
            name = local_product.find_element(By.CLASS_NAME, "h4")
            
            images = driver.find_element(By.CLASS_NAME, "product-image")
            image_url = images.find_element(By.CSS_SELECTOR, "body.brand--store2119:nth-child(2) section.pdp-summary.page-full-width div.pdp-container div.pdp-hero:nth-child(3) ef-product-hero-carousel:nth-child(1) div.product-preview div.product-image picture:nth-child(1) > img.d-none.d-print-block:nth-child(2)")
            image_url = image_url.get_attribute('src')
            price = local_product.find_element(By.CLASS_NAME, "price.regular")
            
            temp = {
                "url": local_url,
                "upc": None,
                "name": name.text,
                "price": price.text,
                #"category_ID": 
                #"subcategory_ID":
                #"keywords": 
                "img_url": image_url
            }
            toJSON["products"].append(temp)
            del temp
            driver.back()
            WebDriverWait(driver, 10).until(
                EC.url_changes(local_url)
            )
            time.sleep(2)
            products = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.CLASS_NAME, "product-tile__photo"))
            )
            products = driver.find_elements(By.CLASS_NAME, "product-tile__photo")
            scraped = scraped +1
        except Exception as e:
            ERROR +=1
            print(e)
            if ERROR > 1:
                driver.get(search_page)
                products = driver.find_elements(By.CLASS_NAME, "product-tile__photo")
                continue

        


       
            file = json.dumps(toJSON, indent = 4)
            current_time = time.ctime()
            timeCode = str(current_time[11]) + str(current_time[12]) + str(current_time[14]) + str(current_time[15]) + str(current_time[17]) + str(current_time[18]) 

            filename = ("%s%s-%d"%(searchTerm, timeCode, scraped))
            f = open(filename + ".json", "x")

            f.write(file)
            f.close
            print("%d items scraped"%(scraped))