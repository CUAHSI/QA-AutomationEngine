""" Contains the general, non-page specific utilities for test case
 execution.  Unlike hc_macros or hs_macros, these methods interact
directly with the Selenium driver
"""
import re
import time

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

from .delays import NEW_PAGE_LOAD


class External:
    """ Utilities for handling new tabs/windows """

    def switch_new_page(self, driver, num_windows_before, new_window_load_locator):
        WebDriverWait(driver, NEW_PAGE_LOAD).until(
            EC.number_of_windows_to_be(num_windows_before + 1)
        )
        win_handle = driver.window_handles[-1]
        driver.switch_to.window(win_handle)
        WebDriverWait(driver, NEW_PAGE_LOAD).until(
            EC.visibility_of_element_located(new_window_load_locator)
        )
        TestSystem.check_language(driver)

    def switch_old_page(self, driver):
        win_handle = driver.window_handles[-2]
        driver.switch_to.window(win_handle)

    def close_new_page(self, driver):
        orig_handle = driver.current_window_handle
        new_handle = driver.window_handles[-1]
        driver.switch_to.window(new_handle)
        driver.close()
        driver.switch_to.window(orig_handle)

    def source_new_page(self, driver):
        orig_handle = driver.current_window_handle
        new_handle = driver.window_handles[-1]
        driver.switch_to.window(new_handle)
        time.sleep(NEW_PAGE_LOAD)
        source = driver.page_source
        TestSystem.check_language(driver)
        driver.switch_to.window(orig_handle)
        time.sleep(NEW_PAGE_LOAD)
        return source

    def to_file(self, driver, num_windows_before, title):
        WebDriverWait(driver, NEW_PAGE_LOAD).until(
            EC.number_of_windows_to_be(num_windows_before + 1)
        )
        win_handle = driver.window_handles[-1]
        driver.switch_to.window(win_handle)
        WebDriverWait(driver, NEW_PAGE_LOAD).until(EC.title_contains(title))


class TestSystem:
    """ General utilities for Hydroclient test case creation """

    def scroll_to_top(self, driver):
        driver.execute_script("window.scrollTo(0, 0)")

    def to_url(self, driver, url):
        driver.get(url)
        time.sleep(NEW_PAGE_LOAD)

    def title(self, driver):
        return driver.title

    def wait(self, seconds=3):
        time.sleep(seconds)

    def page_source(self, driver):
        return driver.page_source

    def back(self, driver, count=1):
        driver.execute_script("window.history.go(-{})".format(count))

    def pull_words(self, driver):
        elements = driver.find_elements_by_xpath("*")
        texts = [element.text for element in elements]
        contents = [text for text in texts if text is not None]
        alpha_contents = [re.sub("[^A-Za-z]", " ", content) for content in contents]
        words = [word for content in alpha_contents for word in content.split(" ")]
        return words

    def check_language(self, driver):
        """ Confirms that language is consistent with CUAHSI standards for
        terminology, capitalization, etc.
        """
        lang_dict = {}
        with open("cuahsi_base/language.yaml", "r") as stream:
            lines = stream.readlines()
        config_lines = [line for line in lines if "###" not in line]
        for config_line in config_lines:
            lang_key, lang_value = config_line.split(":")
            lang_dict[lang_key] = lang_value
        words = self.pull_words(driver)
        bad_words = [word for word in words if word in lang_dict.keys()]
        print(driver.current_url)
        for bad_word in bad_words:
            print("{} -> {}".format(bad_word, lang_dict[bad_word]))

    def execute_javascript(self, driver, script):
        driver.execute_script(script)


External = External()
TestSystem = TestSystem()
