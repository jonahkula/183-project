from __future__ import annotations
from typing import Union, Tuple, List
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

class interactive():

    @staticmethod
    def button_auto_clicker(driver: webdriver, xpath: str, return_button=False) -> Union[WebDriverWait, None]:
        try:
            button = clickable_wait(driver, By.XPATH, xpath)
        except TimeoutException:
            print("some button wasn't present")
            driver.quit()
            sys.exit()
        else:    
            ActionChains(driver).move_to_element(button).click().perform()
            return button if return_button else None

    @staticmethod
    def drop_down(driver: webdriver, select: str, is_state=True) -> Union[None, Select]:
        try:
            presence_wait(driver, By.XPATH, select)
        except(TimeoutException, UnexpectedTagNameException):
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
    def fill_in(driver: webdriver, xpath_value: str, input_value: str) -> None:
        try:
            field = presence_wait(driver, By.XPATH, xpath_value)
        except TimeoutException:
            print("the input field wasn't available")
            driver.quit()
            sys.exit()
        else:
            field.send_keys(input_value)

class cvs_pages():

    def __init__(self: cvs_pages, driver: webdriver) -> None:
        self.driver = driver
        self.driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")

    def iterate_pages(self: cvs_pages) -> None:
        self.choose_state()
        self.questions()
        self.current_dose()
        self.choosing_state()
        self.current_age()
        self.begin_scheduling()
        self.get_times()

    # page 1
    def choose_state(self: cvs_pages) -> None:
        interactive.drop_down(self.driver, cvs_xpaths["State"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Get Started"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Schedule"])

    # page 2
    def questions(self: cvs_pages) -> None:
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Tested Positive"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Close Contact"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Current Conditions"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Continue"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    # page 3
    def current_dose(self: cvs_pages) -> None:
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Need Vaccination"]) if not schedule_second_dose else interactive.button_auto_clicker(self.driver, cvs_xpaths["Second Dose"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Continue Scheduling(1)"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    # page 4
    def choosing_state(self: cvs_pages) -> None:
        interactive.drop_down(self.driver, cvs_xpaths["Select State"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Continue Scheduling(2)"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)
    
    # page 5
    def current_age(self: cvs_pages) -> None:
        interactive.fill_in(self.driver, cvs_xpaths["Age"], AGE)
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Acknowledgment"])
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Confirm Eligiblity"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    # page 6
    def begin_scheduling(self: cvs_pages) -> None:
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Start Scheduling"])
        self.driver.implicitly_wait(IMPLICIT_WAIT)

    # page 7 - part 1 (private method)
    def _select_dose_date(self: cvs_pages) -> Tuple[Select, List[str]]:
        interactive.fill_in(self.driver, cvs_xpaths["Search Input"], ZIPCODE)
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Search Button"])
        select = interactive.drop_down(self.driver, cvs_xpaths["First Dose Date"], is_state=False)
        return (select, select.options)

    # page 7 - part 2 (private method)
    def _get_locations(self: cvs_pages, num_locations: str) -> List[str]:
        current_location_info = []
        location_text_index = 2 # div value begins at 2 for class="clinic-info"
        for index in range(int(num_locations)):
            interactive.button_auto_clicker(self.driver, f"//*[@id='availableTimes{index}']", False) # Show available times button
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            # all text for the location (e.g. times, location, and distance)
            current_location = self.driver.find_element_by_xpath(f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]").text
            current_location_info.append(current_location)
        return current_location

    # page 7
    def get_times(self: cvs_pages) -> None:
        select, dates = self._select_dose_date()
        all_info = []
        for date in dates:
            print('date:', date.text)
            select.select_by_visible_text(date.text)
            if date.is_enabled():
                num_locations = interactive.button_auto_clicker(self.driver, cvs_xpaths["Current Locations"], return_button=True).text
                num_locations = int(num_locations.split()[0]) # only need the number from the listing (# of pharmacy locations...)
                print("num_locations:", num_locations)
                if num_locations > 3: # there being more than 3 locations presents the + See more locations button
                    for _ in range(num_locations // 3): # we need to click + See more locations n / 3 times where n is the # of locations
                        interactive.button_auto_clicker(self.driver, cvs_xpaths["See More Locations"])
                        self.driver.implicitly_wait(IMPLICIT_WAIT)
        
# //*[@id="availableTimes0"]
# //*[@id="availableTimes1"]
# //*[@id="availableTimes11"]

# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[4]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[5]

# driver.get("https://www.cvs.com/immunizations/covid-19-vaccine")
# button_auto_clicker(driver, state_xpaths["Alabama"])
# driver.implicitly_wait(5)
# button_auto_clicker(driver, cvs_xpaths["Schedule"])
# driver.implicitly_wait(5)
# button_auto_clicker(driver, cvs_xpaths["Tested Positive"])
# button_auto_clicker(driver, cvs_xpaths["Close Contact"])
# button_auto_clicker(driver, cvs_xpaths["Current Conditions"])
# button_auto_clicker(driver, cvs_xpaths["Continue"])
# driver.implicitly_wait(5)
# button_auto_clicker(driver, cvs_xpaths["Need Vaccination"]) if not schedule_second_dose else button_auto_clicker(driver, cvs_xpaths["Second Dose"])
# button_auto_clicker(driver, cvs_xpaths["Continue Scheduling(1)"])
# driver.implicitly_wait(5)
# drop_down(driver)
# button_auto_clicker(driver, cvs_xpaths["Continue Scheduling(2)"])
# driver.implicitly_wait(5)
# fill_in(driver, cvs_xpaths["Age"], AGE)
# button_auto_clicker(driver, cvs_xpaths["Acknowledgment"])
# button_auto_clicker(driver, cvs_xpaths["Confirm Eligiblity"])
# driver.implicitly_wait(5)
# button_auto_clicker(driver, cvs_xpaths["Start Scheduling"])
# driver.implicitly_wait(5)
# fill_in(driver, cvs_xpaths["Search Input"], ZIPCODE)
# button_auto_clicker(driver, cvs_xpaths["Search Button"])
cvs = cvs_pages(driver)
cvs.iterate_pages()
time.sleep(20)
driver.quit()