""" Contains the general, non-page specific utilities for test case
 execution.  Unlike hc_macros or hs_macros, these methods interact
directly with the Selenium driver
"""
import re
import time

from modes import setup_mode

# General testing parameters
MODE_SELECTION = 'safe-demo'  # quick, watch, demo, or safe-demo
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)


class External:
    """ Utilities for handling new tabs/windows """
    def switch_new_page(self, driver):
        win_handle = driver.window_handles[-1]
        driver.switch_to.window(win_handle)
        time.sleep(SLEEP_TIME)
        TestSystem.check_language(driver)

    def switch_old_page(self, driver):
        win_handle = driver.window_handles[-2]
        driver.switch_to.window(win_handle)
        time.sleep(SLEEP_TIME)

    def close_new_page(self, driver):
        orig_handle = driver.current_window_handle
        new_handle = driver.window_handles[-1]
        driver.switch_to.window(new_handle)
        time.sleep(SLEEP_TIME/2)
        driver.close()
        driver.switch_to.window(orig_handle)
        time.sleep(SLEEP_TIME/2)

    def source_new_page(self, driver):
        orig_handle = driver.current_window_handle
        new_handle = driver.window_handles[-1]
        driver.switch_to.window(new_handle)
        time.sleep(SLEEP_TIME/2)
        source = driver.page_source
        TestSystem.check_language(driver)
        driver.switch_to.window(orig_handle)
        time.sleep(SLEEP_TIME/2)
        return source


class TestSystem:
    """ General utilities for Hydroclient test case creation """
    def to_url(self, driver, url):
        driver.get(url)
        time.sleep(3*SLEEP_TIME)

    def title(self, driver):
        return driver.title

    def wait(self, seconds=3):
        time.sleep(seconds)

    def page_source(self, driver):
        return driver.page_source

    def back(self, driver, count=1):
        driver.execute_script("window.history.go(-{})".format(count))
        time.sleep(SLEEP_TIME)

    def pull_words(self, driver):
        elements = driver.find_elements_by_xpath('*')
        texts = [element.text for element in elements]
        contents = [text for text in texts if text is not None]
        alpha_contents = [re.sub('[^A-Za-z]', ' ', content) for content in contents]
        words = [word for content in alpha_contents for word in content.split(' ')]
        return words

    def check_language(self, driver):
        """ Confirms that language is consistent with CUAHSI standards for
        terminology, capitalization, etc.
        """
        lang_dict = {}
        with open("config/language.yaml", 'r') as stream:
            lines = stream.readlines()
        config_lines = [line for line in lines if '###' not in line]
        for config_line in config_lines:
            lang_key, lang_value = config_line.split(':')
            lang_dict[lang_key] = lang_value
        words = self.pull_words(driver)
        bad_words = [word for word in words if word in lang_dict.keys()]
        print(driver.current_url)
        for bad_word in bad_words:
            print('{} -> {}'.format(bad_word, lang_dict[bad_word]))


External = External()
TestSystem = TestSystem()
