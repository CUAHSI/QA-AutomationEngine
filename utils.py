""" Contains the general, non-page specific utilities for test case
 execution.  Unlike hc_macros or hs_macros, these methods interact
directly with the Selenium driver
"""
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
    def title(self, driver):
        return driver.title

    def wait(self, seconds=3):
        time.sleep(seconds)

    def page_source(self, driver):
        return driver.page_source

    def back(self, driver):
        self.check_language(driver)
        driver.execute_script("window.history.go(-1)")

    def pull_texts(self, driver):
        elements = driver.find_elements_by_xpath('*')
        texts = []
        for element in elements:
            if element.text is not None:
                texts += element.text.split(' ')
        return texts

    def check_language(self, driver):
        """ Confirms that language is consistent with CUAHSI standards for
        terminology, capitalization, etc.
        """
        lang_dict = {}
        with open("config/language.yaml", 'r') as stream:
            lines = stream.readlines()
        for line in lines:
            if line[0:3] != '###':
                lang_dict[line.split(':')[0].strip()] = (
                    line.split(':')[1].strip())
        pulled_words = self.pull_texts(driver)
        words = []
        for pulled_word in pulled_words:
            words += pulled_word.split('\n')
        words = list(filter(None, words))
        words = [word.replace('.', '') for word in words]
        words = [word.replace(',', '') for word in words]
        words = [word.replace('(', '') for word in words]
        words = [word.replace(')', '') for word in words]
        for word in words:
            if word in lang_dict.keys():
                print('\n', driver.current_url, '\n',
                      word + ' should be changed to ' + lang_dict[word])


External = External()
TestSystem = TestSystem()
