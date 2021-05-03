from __future__ import annotations
from typing import Union, Tuple, List
from selenium import webdriver
from selenium_stealth import stealth
from constants import *
import sys
import time
import pprint
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedTagNameException, ElementNotInteractableException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

PATH = r"/mnt/c/Users/Omelc/Downloads/chromedriver.exe" # change the path to where your chromedriver is currently located for now
RITEAID_DOB = "02/11/1999"

options = webdriver.ChromeOptions()
options.add_argument('start-maximized')
options.add_argument('disable-infobars')
options.add_argument('--disable-extensions')

options.add_experimental_option('excludeSwitches', ['enable-automation'])
options.add_experimental_option('useAutomationExtension', False)

driver = webdriver.Chrome(options=options, executable_path=PATH)

stealth(driver,
    languages=["en-US", "en"],
    vendor="Google Inc.",
    platform="Win64",
)

def presence_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    try:
        WebDriverWait(driver, MAXWAIT).until(EC.visibility_of_element_located((element_type, locator)))
        element = WebDriverWait(driver, MAXWAIT).until(EC.presence_of_element_located((element_type, locator)))
    except TimeoutException:
        print("An error occurred waiting for the presence of an element")
        driver.quit()
        sys.exit()
    return element

def clickable_wait(driver: webdriver, element_type: str, locator: str) -> WebDriverWait:
    return WebDriverWait(driver, MAXWAIT).until(EC.element_to_be_clickable((element_type, locator)))



class interactive():

    @staticmethod
    def button_auto_clicker(driver: webdriver, dom_value: str, return_button : bool = False, continue_on : bool = False, elem_type : str = By.XPATH) -> Union[WebDriverWait, None]:
        try:
            button = clickable_wait(driver, elem_type, dom_value)
        except(TimeoutException, NoSuchElementException):
            if not continue_on:
                print("some button wasn't present")
                driver.quit()
                sys.exit()
            else:
                return
        else:    
            ActionChains(driver).move_to_element(button).click().perform()
            return button if return_button else None

    @staticmethod
    def drop_down(driver: webdriver, select: str, is_state=True) -> Union[None, Select]:
        try:
            presence_wait(driver, By.XPATH, select)
        except(TimeoutException, UnexpectedTagNameException, NoSuchElementException):
            print("the drop-down menu wasn't found")
            driver.quit()
            sys.exit()
        else:
            select = Select(driver.find_element_by_xpath(select))
            if is_state:
                select.select_by_visible_text(STATE)
            return select

    @staticmethod
    def termination(driver: webdriver) -> None:
        time.sleep(20) # for testing purposes, remove after
        driver.quit()

    @staticmethod
    def fill_in(driver: webdriver, dom_value: str, input_value: str, elem_type : str = By.XPATH) -> None:
        try:

            field = presence_wait(driver, elem_type, dom_value)
        except (TimeoutException, ElementNotInteractableException):
            print("the input field wasn't available")
            driver.quit()
            sys.exit()
        else:
            try:
                field.send_keys(input_value)
            except ElementNotInteractableException:
                print("Element was non-interactable")
                driver.quit()
                sys.exit()

class riteaid():

    def __init__(self: riteaid, driver: webdriver) -> None:
        self.driver = driver
        driver.get("https://www.riteaid.com/pharmacy/covid-qualifier")
        driver.implicitly_wait(IMPLICIT_WAIT)
    
    # page 1
    def user_info(self: riteaid) -> None:
        interactive.fill_in(self.driver, riteaid_paths["DOB"], RITEAID_DOB)
        interactive.fill_in(self.driver, riteaid_paths["City"], CITY)
        interactive.fill_in(self.driver, riteaid_paths["State"], STATE)
        interactive.fill_in(self.driver, riteaid_paths["Zipcode"], ZIPCODE)
        
        interactive.button_auto_clicker(self.driver, riteaid_paths["Occupation"])
        interactive.button_auto_clicker(self.driver, riteaid_paths["None of the Above(1)"])
        
        interactive.button_auto_clicker(self.driver, riteaid_paths["Medical Conditions"])
        interactive.button_auto_clicker(self.driver, riteaid_paths["None of the Above(2)"])

        interactive.button_auto_clicker(self.driver, riteaid_paths["Next"])
        interactive.button_auto_clicker(self.driver, riteaid_paths["Continue"])

r = riteaid(driver)
r.user_info()
time.sleep(10)
driver.quit()