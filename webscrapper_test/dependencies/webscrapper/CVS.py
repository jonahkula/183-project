from selenium import webdriver
from selenium_stealth import stealth
from constants import *
import sys
import time
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedTagNameException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

PATH = r"/mnt/c/Users/Omelc/Downloads/chromedriver.exe" # change the path to where your chromedriver is currently located for now
schedule_second_dose = False

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

def presence_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT).until(EC.presence_of_element_located((element_type, locator)))

def clickable_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT).until(EC.element_to_be_clickable((element_type, locator)))

def button_auto_clicker(driver: webdriver, xpath: str) -> None:
    try:
        button = clickable_wait(driver, By.XPATH, xpath)
    except TimeoutException:
        print("some button wasn't present")
        driver.quit()
        sys.exit()
    else:    
        ActionChains(driver).move_to_element(button).click().perform()

def drop_down(driver: webdriver) -> None:
    try:
        presence_wait(driver, By.XPATH, cvs_xpaths["Select State"])
    except(TimeoutException, UnexpectedTagNameException):
        print("the drop-down menu wasn't found")
        driver.quit()
        sys.exit()
    else:
        select_state = Select(driver.find_element_by_xpath(cvs_xpaths["Select State"]))
        select_state.select_by_visible_text(STATE)

def fill_in(driver: webdriver, xpath_value: str, input_value: str) -> None:
    try:
        field = presence_wait(driver, By.XPATH, xpath_value)
    except TimeoutException:
        print("the input field wasn't available")
        driver.quit()
        sys.exit()
    else:
        field.send_keys(input_value)

# def get_select_values() -> :

driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")
button_auto_clicker(driver, state_xpaths["Alabama"])
driver.implicitly_wait(5)
button_auto_clicker(driver, cvs_xpaths["Schedule"])
driver.implicitly_wait(5)
button_auto_clicker(driver, cvs_xpaths["Tested Positive"])
button_auto_clicker(driver, cvs_xpaths["Close Contact"])
button_auto_clicker(driver, cvs_xpaths["Current Conditions"])
button_auto_clicker(driver, cvs_xpaths["Continue"])
driver.implicitly_wait(5)
button_auto_clicker(driver, cvs_xpaths["Need Vaccination"]) if not schedule_second_dose else button_auto_clicker(driver, cvs_xpaths["Second Dose"])
button_auto_clicker(driver, cvs_xpaths["Continue Scheduling(1)"])
driver.implicitly_wait(5)
drop_down(driver)
button_auto_clicker(driver, cvs_xpaths["Continue Scheduling(2)"])
driver.implicitly_wait(5)
fill_in(driver, cvs_xpaths["Age"], AGE)
button_auto_clicker(driver, cvs_xpaths["Acknowledgment"])
button_auto_clicker(driver, cvs_xpaths["Confirm Eligiblity"])
driver.implicitly_wait(5)
button_auto_clicker(driver, cvs_xpaths["Start Scheduling"])
driver.implicitly_wait(5)
fill_in(driver, cvs_xpaths["Search Input"], ZIPCODE)
button_auto_clicker(driver, cvs_xpaths["Search Button"])
time.sleep(20)
driver.quit()