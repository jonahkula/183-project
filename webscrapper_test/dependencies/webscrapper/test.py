from __future__ import annotations
from selenium import webdriver
from selenium_stealth import stealth
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.common.exceptions import StaleElementReferenceException
import time
from constants import *
import pprint

''' 
the path is currently hardcoded, but we need to have all drivers installed,
stored in a folder called drivers so that we can access the respective drivers
depending on what browser the user is currently using.
'''
PATH = r"/mnt/c/Users/Omelc/Downloads/chromedriver.exe" # change the path to where your chromedriver is currently located for now
ZIPCODE = "91411" # the zipcode will be provided by the the modal extracted from the database
MAXWAIT = 30 # 30 seconds is the maximum time we wait for a page to load (Note: most computers load pages in the miliseconds)
VACCINE = "None" # by default preference will be None, but in the modal the user can decide
TABS = 5 # we'll have 5 tabs open by default to be able to search through 5 possible sites

def presence_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT, ignored_exceptions=StaleElementReferenceException).until(EC.presence_of_element_located((element_type, locator)))

def clickable_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT, ignored_exceptions=StaleElementReferenceException).until(EC.element_to_be_clickable((element_type, locator)))

def vaccine_checkboxes() -> None:
    vaccine_xpaths = {
    'Moderna': presence_wait(driver, By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div[2]/div[1]/input"),
    'Johnson': presence_wait(driver, By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div[2]/div[3]/input"),
    'Pfizer': presence_wait(driver, By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div/form/div[1]/div[1]/div/div[2]/div[2]/input"),
    }

    if VACCINE == 'Moderna':
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Pfizer'])
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Johnson'])
    elif VACCINE == 'Pfizer':
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Moderna'])
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Johnson'])
    elif VACCINE == 'Johnson':
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Moderna'])
        driver.execute_script("arguments[0].click();", vaccine_xpaths['Pfizer'])

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options, executable_path=PATH)

driver.get("https://vaccinefinder.org/search/")

# time.sleep(1)

WebDriverWait(driver, MAXWAIT).until(EC.presence_of_element_located((By.ID,"searchArea")))
mile_radius = Select(driver.find_element_by_id("searchArea"))
mile_radius.select_by_visible_text("50 miles") # provide the user with the maximum allowable distance

vaccine_checkboxes()

zipCode = driver.find_element_by_id("zipCode")
zipCode.send_keys(ZIPCODE)
zipCode.send_keys(Keys.RETURN)

presence_wait(driver, By.XPATH, "//*[@id='split-screen-content']/main")

for i in range(TABS):
    url = driver.current_url
    driver.execute_script("window.open('%s', '_blank')" % url)

driver.switch_to.window(driver.window_handles[0]) # switches back to the first window

# clicks on the first available option -> VaccineFinder site
# options_page = clickable_wait(driver, By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[1]")
# ActionChains(driver).move_to_element(options_page).click().perform()

# /html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[1]
# /html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[2]
# /html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[3]

# attempting to iterate over each available location -> VaccineFinder site
# a_tags = driver.find_elements_by_tag_name('a')
a_tag_num = -1
tab_num = 0

for _ in range(TABS):
    presence_wait(driver, By.TAG_NAME, 'a')
    a_tags = driver.find_elements_by_tag_name('a')
    assert a_tags, f"no a tags present in tab {tab_num}"

    tab_num += 1

    for element in a_tags:
        # presence_wait(driver, By.XPATH, f"/html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[{a_tag_num}]")
        aria_label = element.get_attribute('aria-label')
        if aria_label is not None:
            a_tag_num += 1
            location = element.text.split("\n")
            if "In Stock" in location:
                # clicks on an available option -> VaccineFinder site
                options_page = clickable_wait(driver, By.XPATH, f"/html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[{a_tag_num}]")
                ActionChains(driver).move_to_element(options_page).click().perform()
                break
    driver.switch_to.window(driver.window_handles[tab_num])
# /html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[2]
# /html/body/div[1]/div/div[2]/div/div/div/main/div[3]/a[3]
# availablility button page -> still VaccineFinder site
# local_page = clickable_wait(driver, By.XPATH, "/html/body/div[1]/div/div[2]/div/div/div/div[1]/div[1]/a")
# ActionChains(driver).move_to_element(local_page).click().perform()

# # applies only to the Kroger website, need to add a conditional check that the user is using Kroger's website
# if driver.current_url == 'https://www.kroger.com/i/coronavirus-update/vaccine':
#     WebDriverWait(driver, MAXWAIT).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/main/div/div/div/div/div/div[3]/div/div[1]/div[2]/div/div/ul/li[1]/a"))).click()


time.sleep(MAXWAIT) # for debugging purposes

# driver.close() # closes the current tab
driver.quit() # closes the current window