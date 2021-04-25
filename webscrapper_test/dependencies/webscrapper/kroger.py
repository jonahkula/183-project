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

no_conditions = True
received_vaccine = False

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
        presence_wait(driver, By.XPATH, eligibility_xpath["Select State"])
    except(TimeoutException, UnexpectedTagNameException):
        print("the drop-down menu wasn't found")
        driver.quit()
        sys.exit()
    else:
        select_state = Select(driver.find_element_by_xpath(eligibility_xpath["Select State"]))
        select_state.select_by_value(states[STATE])

def fill_in(driver: webdriver, enter_value: str, xpath_values: tuple) -> None:
    try:
        field = presence_wait(driver, By.XPATH, xpath_values[0]) # DOB Field / Find Location
    except TimeoutException:
        print("the input field for entering the dob wasn't available")
        driver.quit()
        sys.exit()
    else:
        field.send_keys(enter_value)
        submit = clickable_wait(driver, By.XPATH, xpath_values[1]) # DOB Submit
        ActionChains(driver).move_to_element(submit).click().perform()

def page_one(driver: webdriver) -> None:
    copied_xpaths = eligibility_xpath.copy()
    copied_xpaths.pop("DOB Submit")
    copied_xpaths.pop("Threatening Yes") if no_conditions else copied_xpaths.pop("Threatening No")
    if received_vaccine:
        copied_xpaths.pop("First Dose No")
        copied_xpaths.pop("Received Vaccine No")
    else:
        copied_xpaths.pop("First Dose Yes")
        copied_xpaths.pop("Received Vaccine Yes")
    print(copied_xpaths.keys())

    copied_xpaths_keys = list(copied_xpaths.keys())

    for field in range(KROGER_FIELDS):
        if field == 2: # drop-down menu for state
            drop_down(driver)
        elif field == 3: # dob input field
            fill_in(driver, DOB, (eligibility_path["DOB Field"], eligibility_path["DOB Submit"]))
        else:
            print(copied_xpaths_keys[field])
            button_auto_clicker(driver, copied_xpaths[copied_xpaths_keys[field]])
        time.sleep(5)

def page_two() -> None:
    # part 1
    fill_in(driver, ZIPCODE, (scheduling_xpath["Find Location"], scheduling_xpath["Location Submit"]))
    time.sleep(2)
    # part 2 <- can redirect the user to the scheduling page

    time.sleep(2)

driver.get("https://www.kroger.com/rx/covid-eligibility")
page_one(driver)
driver.quit()

# try:
#     # page that indicates the possible state to get vaccinated
#     state_vaccine_choice = WebDriverWait(driver, MAXWAIT).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/div[3]/div[1]/main/div/div/div/div/div/div[3]/div/div[1]/div[2]/div/div/ul/li[1]/a")))
# except TimeoutException:
#     print("Either an error occurred or you live in one of 14 states (we're not going to list them), which Kroger isn't in")
#     driver.quit()
# else:
#     state_vaccine_choice.click()