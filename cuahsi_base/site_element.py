""" SiteElement class improves organization of site element
parameters.  The class methods faciltate easy manipulation
 of these elements
"""
import platform
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class SiteElement:
    """ Defines site elements in a structured way and provides a convenient
    means for element manipulations (clicking, entering text, etc.)
    """
    def __init__(self, by, locator):
        self.by = by
        self.locator = locator

    def loc_it(self, el_driver):
        """
        Identifies element on page, based on an element locator.
        Waits until an element becomes available & visible in DOM, and
        then until it becomes clickable.
        """
        wait = WebDriverWait(el_driver, 10)
        try:
            wait.until(EC.visibility_of_element_located((self.by, self.locator)))
            target_el = wait.until(EC.element_to_be_clickable(
                (self.by, self.locator)))
        except TimeoutException as e:
            print("\nUnable to locate element by {}, "
                  "locator: '{}'".format(self.by, self.locator))
            raise e

        return target_el

    def is_visible(self, driver):
        """
        Checks if element is visible on the page.
        """
        target_el = driver.find_element(self.by, self.locator)
        return target_el.is_displayed()

    def is_selected(self, driver):
        """
        Checks if element is visible on the page.
        """
        target_el = driver.find_element(self.by, self.locator)
        return target_el.is_selected()

    def click(self, el_driver):
        """ Identifies an element on the page.  After identification
        the element is then clicked.
        """
        target_el = self.loc_it(el_driver)
        target_el.click()

    def double_click(self, el_driver):
        """
        Double click on element.
        """
        target_el = self.loc_it(el_driver)
        actionchains = ActionChains(el_driver)
        actionchains.double_click(target_el).perform()

    def javascript_click(self, driver):
        """
        Clicks an element using JavaScript
        """
        target_el = self.loc_it(driver)
        driver.execute_script('arguments[0].click();', target_el)

    def submit(self, el_driver):
        """ Send ENTER to element, simulates submit """
        target_el = self.loc_it(el_driver)
        target_el.send_keys(Keys.ENTER)

    def multi_click(self, el_driver):
        """ Clicks an element while holding the control key, as to enable
        a multi-selection
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.LEFT_CONTROL)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_CONTROL)
        actions.perform()

    def range_click(self, el_driver):
        """ Clicks an element while holding the control key, as to enable
        a range selection
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.LEFT_SHIFT)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_SHIFT)
        actions.perform()

    def passive_click(self, el_driver):
        """ Identifies an element on the page.  After identification
        the element is then clicked, regardless if it is "interactable"
        or not
        """
        target_el = self.loc_it(el_driver)
        ActionChains(el_driver).move_to_element(target_el).click(target_el).perform()

    def clear_all_text(self, el_driver):
        """ Uses the Ctrl+A keys combination to select all text before using
        BACKSPACE key to delete it
        """
        target_el = self.loc_it(el_driver)
        if platform.system() == 'Darwin':   # MacOs
            ctrl_key = Keys.COMMAND
        else:
            ctrl_key = Keys.CONTROL
        ActionChains(el_driver).move_to_element(target_el).key_down(ctrl_key).\
            send_keys('a').key_up(ctrl_key).send_keys(Keys.BACKSPACE).perform()

    def clear_text(self, el_driver, size):
        """ Uses backspace to clear text from a field """
        target_el = self.loc_it(el_driver)
        target_el.send_keys(Keys.END)
        for i in range(0, size):
            target_el.send_keys(Keys.BACK_SPACE)

    def select_option(self, el_driver, select_choice):
        """ Selects an option from a dropdown element """
        target_el = self.loc_it(el_driver)
        select_el = Select(target_el)
        select_el.select_by_value(select_choice)

    def select_option_text(self, el_driver, select_choice):
        """ Selects an option from dropdown given visible text """
        target_el = self.loc_it(el_driver)
        select_el = Select(target_el)
        select_el.select_by_visible_text(select_choice)

    def scroll_to(self, el_driver):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_el = self.loc_it(el_driver)
        target_el.location_once_scrolled_into_view

    def scroll_right(self, el_driver):
        """ Scroll right using Keys.ARROW_RIGHT
        and a hold of one second
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.ARROW_RIGHT)
        actions.perform()
        time.sleep(1)
        actions = ActionChains(el_driver)
        actions.key_up(Keys.ARROW_RIGHT)
        actions.perform()

    def inject_text(self, el_driver, field_text):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        target_el = self.loc_it(el_driver)
        for i in range(0, len(field_text)):
            target_el.send_keys(field_text[i])

    def set_path(self, el_driver, field_text):
        """ Enters text into a field or other input-capable html
        element using send keys, best for setting path to files for upload
        """
        target_el = self.loc_it(el_driver)
        target_el.send_keys(field_text)

    def iframe_in(self, el_driver):
        """ Switches driver focus to an iframe within a page """
        target_el = self.loc_it(el_driver)
        el_driver.switch_to.frame(target_el)

    def iframe_out(self, el_driver):
        """ Switches driver focus out of iframe and back to the
        main page
        """
        el_driver.switch_to.parent_frame()

    def get_attribute(self, el_driver, attribute):
        """ Returns any attribute of website element """
        target_el = self.loc_it(el_driver)
        return target_el.get_attribute(attribute)

    def get_text(self, el_driver):
        """ Returns content text of website element """
        target_el = self.loc_it(el_driver)
        return target_el.text

    def get_value(self, el_driver):
        """ Returns content text of website element """
        target_el = self.loc_it(el_driver)
        return target_el.get_attribute('value')

    def get_href(self, el_driver, base_url):
        """ Returns element href link, with relative links expanded
        into an absolute link
        """
        target_el = self.loc_it(el_driver)
        target_href = target_el.get_attribute("href")
        if target_href[0] == '/':
            target_href = base_url + target_href
        return target_href

    def get_child_count(self, el_driver):
        """ Returns the number of child elements, given a parent
        element specification
        """
        target_el = self.loc_it(el_driver)
        return len(target_el.find_elements_by_xpath(".//*"))

    def get_immediate_child_count(self, el_driver):
        """ Returns the number of immediate child elements, given a parent
        element specification
        """
        target_el = self.loc_it(el_driver)
        return len(target_el.find_elements_by_xpath("*"))

    def get_class(self, el_driver):
        target_el = self.loc_it(el_driver)
        target_class = target_el.get_attribute('class')
        return target_class

    def get_style(self, el_driver):
        target_el = self.loc_it(el_driver)
        target_style = target_el.get_attribute('style')
        return target_style