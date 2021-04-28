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
from selenium.common.exceptions import TimeoutException, NoSuchElementException, UnexpectedTagNameException
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import Select

select_date = "Friday: April 30, 2021" # this will be selected by the user
location = "100 W LODI AVE" # location will be chosen by the user
chosen_time = "01:15 PM" # time will also be chosen by the user

second_select_date = "Friday: May 21, 2021" # this will be selected by the user
second_dose_time = "01:15 PM" # time will also be chosen by the user

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
    try:
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
    def button_auto_clicker(driver: webdriver, xpath: str, return_button=False, continue_on=False) -> Union[WebDriverWait, None]:
        try:
            driver.implicitly_wait(IMPLICIT_WAIT)
            button = clickable_wait(driver, By.XPATH, xpath)
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
        self.filter_showings()
        self.process_user_selection()
        self._get_second_times()
        self.choose_second_dose()

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
    def _get_locations(self: cvs_pages, num_locations: int) -> List[str]:
        current_location_info = []
        location_text_index = 2 # div value begins at 2 for class="clinic-info"
        print("in get_locations def")
        for _ in range(num_locations):
            print("check location_text_index:", location_text_index)
            
            self.driver.implicitly_wait(IMPLICIT_WAIT)
            time.sleep(1)
            interactive.button_auto_clicker(self.driver, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]/div[2]", False, True) # Show available times button
           
            time.sleep(3)
            # all text for the location (e.g. times, location, and distance)
            current_location = presence_wait(driver, By.XPATH, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]").text
            # current_location = self.driver.find_element_by_xpath(f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]").text
            current_location_info.append(current_location)
            location_text_index += 1
        # print("current_location info:")
        # pprint.pprint(current_location_info)
        return current_location_info

    def _see_more_locations(self: cvs_pages) -> int:
        num_locations = interactive.button_auto_clicker(self.driver, cvs_xpaths["Current Locations"], return_button=True).text
        num_locations = int(num_locations.split()[0]) # only need the number from the listing (# of pharmacy locations...)
        print("num_locations:", num_locations)

        if num_locations > 3: # there being more than 3 locations presents the + See more locations button
            times_to_click = (num_locations // 3) - 1 if num_locations % 3 == 0 else (num_locations // 3)
            see_more_div = 2 # the div value begins at 2 and increments by 3 each time
            for _ in range(times_to_click): # we need to click + See more locations n / 3 times where n is the # of locations                        
                self.driver.implicitly_wait(IMPLICIT_WAIT)
                see_more_div += 3
                print("see_more_div:", see_more_div)
                interactive.button_auto_clicker(self.driver, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{see_more_div}]/button")
                self.driver.implicitly_wait(IMPLICIT_WAIT)
        return num_locations

    # page 7
    def _get_times(self: cvs_pages) -> List[List[str]]:
        select, dates = self._select_dose_date()
        all_info = []
        for date in dates:
            print('date:', date.text)
            select.select_by_visible_text(date.text)
            if date.is_enabled():
                num_locations = self._see_more_locations()
                # num_locations = interactive.button_auto_clicker(self.driver, cvs_xpaths["Current Locations"], return_button=True).text
                # num_locations = int(num_locations.split()[0]) # only need the number from the listing (# of pharmacy locations...)
                # print("num_locations:", num_locations)

                # if num_locations > 3: # there being more than 3 locations presents the + See more locations button
                #     times_to_click = (num_locations // 3) - 1 if num_locations % 3 == 0 else (num_locations // 3)
                #     see_more_div = 2 # the div value begins at 2 and increments by 3 each time
                #     for _ in range(times_to_click): # we need to click + See more locations n / 3 times where n is the # of locations                        
                #         self.driver.implicitly_wait(IMPLICIT_WAIT)
                #         see_more_div += 3
                #         print("see_more_div:", see_more_div)
                #         interactive.button_auto_clicker(self.driver, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{see_more_div}]/button")
                #         self.driver.implicitly_wait(IMPLICIT_WAIT)

                all_locations = self._get_locations(num_locations)
                all_info.append(all_locations)
                self.driver.implicitly_wait(IMPLICIT_WAIT)
        # print("All information:")
        # pprint.pprint(all_info)
        return all_info

    # removes all the showing times with the comment "No time slots are available for this date at this location\n"
    # then will return all the showings to the user
    def filter_showings(self: cvs_pages) -> None:
        all_info = self._get_times()
        filtered_all_info = []
        no_time_slots = "No time slots are available for this date at this location"

        for dates in all_info:
            filtered_showings = []
            for showings in dates:
                if no_time_slots not in showings:
                    filtered_showings.append(showings)
            filtered_all_info.append(filtered_showings)

        # pprint.pprint(filtered_all_info)

    # page 7
    def process_user_selection(self: cvs_pages) -> None:
        broke_out = False

        # 1) Select the date that the user indicated
        select = interactive.drop_down(self.driver, cvs_xpaths["First Dose Date"], is_state=False)
        select.select_by_visible_text(select_date)

        # 2) Iterate over all locations, so make sure all places are visible first, then search each place by address
        num_locations = self._see_more_locations()
        location_text_index = 2 # div value begins at 2 for class="clinic-info"
        for _ in range(num_locations):            
            time.sleep(1)
            interactive.button_auto_clicker(self.driver, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]/div[2]", False, True) # Show available times button
            time.sleep(3)

            # all text for the location (e.g. times, location, and distance)
            current_location = presence_wait(self.driver, By.XPATH, f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]").text

            if location in current_location: # if the location is that of the user chosen location, then iterate over possible times
                for button_index in range(1, INDEX_CAP):
                    button_xpath = f"/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[{location_text_index}]/div[2]/div[2]/div[{button_index}]/div/label/button"
                    # button_xpath = f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[{location_text_index}]/div[2]/div[2]/div[{button_index}]"
                    button_text = presence_wait(self.driver, By.XPATH, button_xpath).text
                    if chosen_time == button_text:
                        print("The button_text is as follows before clicking:", button_text)
                        interactive.button_auto_clicker(self.driver, button_xpath)
                        broke_out = True
                        break
            
            if broke_out:
                break

            location_text_index += 1

            # /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[1]/div/label/button
            #/html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[2]/div/label/button
            # /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[3]/div/label/button

            # /html/body/cvs-root/div/cvs-cvd-first-dose-select/main/div[2]/cvs-store-locator/div/div/div[3]/div[2]/div[2]/div[1]/div/label/button

            # //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[1]
            # //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[2]
            # //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div[2]/div[3]

            # //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[3]/div[2]/div[2]/div[1]

        # 3) Click on the Continue Schedule button at the very bottom
        print("about to click on the continue schedule button")
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Continue Scheduling(3)"])

    # page 8 - selecting a dose date from the drop-down menu
    def _select_second_dose(self: cvs_pages) -> Tuple[Select, List[str]]:
        select = interactive.drop_down(self.driver, cvs_xpaths["Second Dose Date"], is_state=False)
        return (select, select.options)

    # page 8 - returning all the times to the user to see for the second dose
    def _get_second_times(self: cvs_pages) -> List[str]:
        select, dates = self._select_second_dose()
        all_dose_times = []
        for date in dates:
            select.select_by_visible_text(date.text)
            if date.is_enabled():
                dose_info = presence_wait(self.driver, By.XPATH, cvs_xpaths["Second Dose Location"]).text
                all_dose_times.append(dose_info)
        print("all_dose_times:")
        pprint.pprint(all_dose_times)
        return all_dose_times

     # page 8 - select the 2nd dose in which the user decided
    def choose_second_dose(self: cvs_pages)  -> None:
        
        # 1) we need to search for the specific drop-down date
        select = interactive.drop_down(self.driver, cvs_xpaths["Second Dose Date"], is_state=False)
        select.select_by_visible_text(second_select_date)

        # 2) iterate over the times and click on the one we want
        for button_index in range(1, INDEX_CAP):
            button_xpath = f"//*[@id='content']/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div/div[{button_index}]"
            button_text = presence_wait(self.driver, By.XPATH, button_xpath).text
            if second_dose_time == button_text:
                interactive.button_auto_clicker(self.driver, button_xpath)
                break

        # 3) click on the continue scheduling button
        interactive.button_auto_clicker(self.driver, cvs_xpaths["Continue Scheduling(4)"])


# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div/div[1]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div/div[2]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div/div[3]
# //*[@id="content"]/div[2]/cvs-store-locator/div/div/div[2]/div[2]/div/div[4]

cvs = cvs_pages(driver)
cvs.iterate_pages()
time.sleep(20)
driver.quit()