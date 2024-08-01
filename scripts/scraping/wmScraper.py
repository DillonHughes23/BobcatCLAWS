from selenium import *
from selenium.common.exceptions import *
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
from random import random
from random import randint
import random



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
def scrapePage(search_page):
    try:
        shelfs = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-stack-index]")))
        shelfs = driver.find_elements(By.CSS_SELECTOR, "div[data-stack-index]")
        #driver.find_elements(By.CSS_SELECTOR, "div[data-stack-index]")
        #index = [0,2]
        for x in range(len(shelfs)):
            shelfs = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-stack-index]")))
            shelfs = driver.find_elements(By.CSS_SELECTOR, "div[data-stack-index]")
            products = shelfs[x].find_elements(By.TAG_NAME, "a")
            print(len(products), " products found on shelf ", x)
            for y in range(1): #len(products)
                shelfs = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-stack-index]")))
                shelfs = driver.find_elements(By.CSS_SELECTOR, "div[data-stack-index]")
                products = shelfs[x].find_elements(By.TAG_NAME, "a")
                products[y].click()
                checkCaptcha()
                scrapeItem()
                driver.get(search_page)
                print("Search Page 2: " + search_page)
                checkCaptcha()    
    except TimeoutException:
        driver.get(search_page)
    except ElementNotInteractableException as e:
        scraped += 1
    except StaleElementReferenceException:
        driver.get(search_page)
        
    except NoSuchElementException as e:
        scraped +=1
        driver.back()
    except ElementClickInterceptedException as e:
        scraped += 1
    except Exception as e:
        ERROR += 1
        if ERROR > 1:
            driver.back()
            ERROR = 0
            scraped +=1
        print("Something didn't work")
        print(e)


def scrapeItem ():
    try:
        WebDriverWait(driver, 3).until(EC.presence_of_element_located((By.ID, "main-title")))
        name = driver.find_element(By.ID, "main-title")
        price = driver.find_element(By.XPATH, "//*[@id='maincontent']/section/main/div[2]/div[2]/div/div[2]/div/div[2]/div/div/span[1]/span[2]/span")
        image_url = driver.find_element(By.CSS_SELECTOR, "div.flex.flex-column.min-vh-100.shadow-2 div.flex.flex-column.flex-auto.relative.z-0 div.flex-auto.relative.z-1:nth-child(2) div.main-content.mw1660.center main.ph4.min-vh-100 div.flex.undefined.flex-column.h-100:nth-child(2) div.h-100.relative:nth-child(2) div.w_KPWk.w_GxNv.flex-row.undefined div.w_aoqv.w_wRee.w_p0Zv:nth-child(1) div.flex.undefined.flex-column.h-100 div.h-100.relative section.flex.items-center:nth-child(1) div.ma2.relative div.container.overflow-y-hidden.mt2.mb0:nth-child(2) div.tc.b--white.ba.bw1.b--blue.mb2.overflow-hidden.br3:nth-child(1) button.pa0.ma0.bn.bg-white.b--white.pointer div.relative > img:nth-child(1)")
   
    except NoSuchElementException:
        driver.back()
        return
    except TimeoutException:
        driver.back()
        return
    except Exception as e:
        raise

    

    temp = {
    "url": driver.current_url,
    "upc": None,
    "name": name.text,
    "price": price.text,
    #"category_ID": 
    #"subcategory_ID":
    #"keywords": 
    "img_url": image_url.get_attribute('src')
    }

    toJSON["products"].append(temp)
    del temp




# def scrapeShelf(shelf):
#     try:
#         shelf = shelf
#         products = shelf.find_elements(By.CLASS_NAME, "mb0 ph1 pa0-xl bb b--near-white w-25")
#         print(len(products), " found on shelf")
#         for product in products:
#             product.click()
#             scrapeItem()
#             driver.back()
#     except Exception:
#         raise

def nextPage(search_page):
    driver.get( search_page)
    checkCaptcha()
    button = driver.find_element(By.CSS_SELECTOR, "a[aria-label='Next Page']")
    button.click()
    checkCaptcha()
    time.sleep(2)
    search_page = driver.current_url
    return search_page
    print("SEARCH PAGE: " + search_page)


def checkCaptcha():
    random.seed(time.ctime())
    ox = randint(-5, 5)
    oy = randint(-5,5)
    variance = random.random()
    try:
        page_title = driver.title
        if "Robot" in page_title:
            print("Captcha Page detected")
            action = ActionChains(driver)
            button = driver.find_element(By.ID, "px-captcha")
            action.move_to_element_with_offset(button, ox, oy)
            action.click_and_hold()
            action.perform()
            time.sleep(8 + 3*variance)
            action.release(button)
            action.perform()
            time.sleep(.2)
            action.release(button)
            captcha = WebDriverWait(driver, 4).until_not(EC.title_contains, "Robot")
            driver.refresh()
        if driver.find_elements(By.ID, "px-captcha"):
            print("Captcha Frame Detected")
            action = ActionChains(driver)
            button = driver.find_element(By.ID, "px-captcha")
            action.move_to_element_with_offset(button, ox, oy)
            action.click_and_hold()
            action.perform()
            time.sleep(8 + 3*variance)
            action.release(button)
            action.perform()
            time.sleep(.2)
            action.release(button)
            captcha = WebDriverWait(driver, 4).until_not(EC.presence_of_element_located((By.ID, "px-captcha")))
            driver.refresh()
    except TimeoutException:
        driver.refresh()
        checkCaptcha()
        
        


PATH = "C:\Program Files\chromedriver\chromedriver.exe"
options = Options()
options.add_argument("start-maximized")
options.add_experimental_option("detach", True)
options.add_experimental_option ("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options = options)
action = ActionChains(driver)

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

ERROR = 0
driver.implicitly_wait(3)
#url = "https://www.bkstr.com/texasstatestore/home"
url = "https://www.walmart.com/"

driver.get(url)

checkCaptcha()
search = WebDriverWait(driver, 3).until(
        EC.element_to_be_clickable((By.NAME, "q"))
)

#search = driver.find_element(By.NAME, "searchValue")
search.send_keys(searchTerm)
search.send_keys(Keys.RETURN)
checkCaptcha()
search_page = WebDriverWait(driver, 1).until(EC.presence_of_element_located((By.CSS_SELECTOR, "div[data-stack-index]")))
search_page = driver.current_url
scraped = 0
page = 1
try:
    print("Starting")
    scrapePage(search_page)

    while page < 25:
        search_page = nextPage(search_page)
        page += 1
        scrapePage(search_page)
    
        


except Exception as e:
    print(e)
    print("One or more actions failed")
    #driver.close()
finally:
    scraped = len(toJSON["products"])
    file = json.dumps(toJSON, indent = 4)
    current_time = time.ctime()
    print(current_time)
    timeCode = str(current_time[11]) + str(current_time[12]) + str(current_time[14]) + str(current_time[15]) + str(current_time[17]) + str(current_time[18]) 
    filename = ("%s%s-%d"%(searchTerm, timeCode, scraped))
    f = open(filename + ".json", "x")

    f.write(file)
    f.close
    print("%d items scraped"%(scraped))
            
        
       

