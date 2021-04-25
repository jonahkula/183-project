from selenium import webdriver
from selenium_stealth import stealth
from constants import *
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import TimeoutException, NoSuchElementException

PATH = r"/mnt/c/Users/Omelc/Downloads/chromedriver.exe" # change the path to where your chromedriver is currently located for now

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options, executable_path=PATH) # the type of webdriver will be decided by browser.js once the front-end portion works

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win64",
)

def clickable_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT).until(EC.element_to_be_clickable((element_type, locator)))

def presence_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT).until(EC.presence_of_element_located((element_type, locator)))

driver.get("https://www.walgreens.com/findcare/vaccination/covid-19")

current_button = None
if STATE == "New Hampshire":
    current_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/section/section/section[1]/div/section/section[2]/section/div[2]/a")
elif STATE == "New Mexico":
    current_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/section/section/section[1]/div/section/section[2]/section/div[3]/a")
else: # otherwise click on the schedule new appointment button
    current_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/section/section/section[2]/div/section/section/section[2]/a") 
assert current_button, f"current_button is currently {current_button}, which we don't want!"
ActionChains(driver).move_to_element(current_button).click().perform()

# enter zip code, city, or state (for now we use zipcode, we could change it to instead be city)
presence_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[2]/div/span[1]/input")
zipCode = driver.find_element_by_xpath("/html/body/div[2]/div/div/section/section/section/section/section/section/section[2]/div/span[1]/input")
zipCode.clear()
zipCode.send_keys(ZIPCODE)
search_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[2]/div/span[1]/button")
ActionChains(driver).move_to_element(search_button).click().perform()

# if the zipcode outputs the appointments unavailable error, then send back the error value, otherwise continue forwards
try:
    presence_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[1]/p")
    error_msg = driver.find_element_by_xpath("/html/body/div[2]/div/div/section/section/section/section/section/section/section[1]/p")
except(TimeoutException, NoSuchElementException):
    try:
        # presence_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[1]/section/div")
        search_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[4]/a")
    except TimeoutException:
        print('Ugh the element should exist')
        driver.quit()
    else:
        # search_button = clickable_wait(driver, By.XPATH, "/html/body/div[2]/div/div/section/section/section/section/section/section/section[4]/a")
        ActionChains(driver).move_to_element(search_button).click().perform()
        print(driver.current_url)
else:
    print(error_msg.text)
    driver.quit()

time.sleep(MAXWAIT) # for debugging purposes

# driver.close() # closes the current tab
driver.quit() # closes the current window