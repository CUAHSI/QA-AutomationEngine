""" Contains the general, non-page specific utilities for test case
 execution.  Unlike hc_macros or hs_macros, these methods interact 
directly with the Selenium driver
"""
import time

class External:
    """ Utilities for handling new tabs/windows """
    def switch_new_page(self, driver):
        win_handle = driver.window_handles[-1]
        driver.switch_to.window(win_handle)
        time.sleep(SLEEP_TIME)

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

External = External()
Hydroclient = Hydroclient()
