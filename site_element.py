""" SiteElement class improves organization of site element 
parameters.  The class methods faciltate easy manipulation
 of these elements
"""
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select
from nested_funcs import *

class SiteElement:
    """ Defines site elements in a structured way and provides a convenient means
    for element manipulations (clicking, entering text, etc.)
    """

    def __init__(self, el_type=None, el_id=None, el_content=None,
                 el_href=None, el_class=None, el_dom=None, el_name=None):
        self.el_type = el_type
        self.el_id = el_id
        self.el_content = el_content
        self.el_href = el_href
        self.el_class = el_class
        self.el_dom = el_dom
        self.el_name = el_name

    def loc_it(self, the_driver):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).
        """
        def loc_by_id(the_driver):
            """ Locates a website element, given the element type and id """
            driver = the_driver
            element_xpath = "//" + self.el_type + \
                           "[@id='" + self.el_id + "']"
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element
        
        def loc_by_name(the_driver):
            """ Locates a website element, given the name attribute """
            driver = the_driver
            element_xpath = "//" + self.el_type + \
                            "[@name='" + self.el_name + "']"
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element
        
        def loc_by_href(the_driver):
            """ Locates a website element, given the element type and href """
            driver = the_driver
            element_xpath = "//" + self.el_type + \
                           "[contains(@href,'" + self.el_href + "')]"
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element

        def loc_by_class(the_driver):
            """ Locates a website element, given the element class """
            driver = the_driver
            element_xpath = "//" + self.el_type + \
                           "[@class='" + self.el_class + "']"
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element
        
        def loc_by_content(the_driver):
            """ Locates a website element, based the element text content """
            driver = the_driver
            element_xpath = "//" + self.el_type + \
                           "[contains(text(), '" + self.el_content + "')]"
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element

        def loc_by_dom(the_driver):
            """ Locates a website element given DOM path to element """
            driver = the_driver
            element_xpath = self.el_dom
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element
        
        def loc_by_nothing(the_driver):
            """ Locates a website element based only on the tag/type """
            driver = the_driver
            element_xpath = "//" + self.el_type
            target_element = driver.find_element_by_xpath(element_xpath)
            return target_element
        
        if self.el_id is not None:
            target_element = loc_by_id(the_driver)
        elif self.el_name is not None:
            target_element = loc_by_name(the_driver)
        elif self.el_href is not None:
            target_element = loc_by_href(the_driver)
        elif self.el_class is not None:
            target_element = loc_by_class(the_driver)
        elif self.el_content is not None:
            target_element = loc_by_content(the_driver)
        elif self.el_dom is not None:
            target_element = loc_by_dom(the_driver)
        else:
            target_element = loc_by_nothing(the_driver)
        return target_element

    def click_it(self, the_driver, sleep_time):
        """ Identifies an element on the page.  After identification
        the element is then clicked.
        """
        target_element = self.loc_it(the_driver)
        target_element.click()
        time.sleep(sleep_time)

    def multi_click_it(self, the_driver, sleep_time):
        """ Clicks an element while holding the control key, as to enable
        a multi-selection
        """
        target_element = self.loc_it(the_driver)
        actions = ActionChains(the_driver)
        actions.key_down(Keys.LEFT_CONTROL)
        actions.click(target_element)
        actions.key_up(Keys.LEFT_CONTROL)
        actions.perform()
        time.sleep(sleep_time)
        
    def passive_click_it(self, the_driver, sleep_time):
        """ Identifies an element on the page.  After identification
        the element is then clicked, regardless if it is "interactable"
        or not
        """
        target_element = self.loc_it(the_driver)
        actions = ActionChains(the_driver)
        actions.move_to_element(target_element)
        actions.click(target_element)
        actions.perform()
        time.sleep(sleep_time)
        
    def clear_it(self, the_driver, size, sleep_time):
        """ Uses backspace to clear text from a field """
        target_element = self.loc_it(the_driver)
        target_element.send_keys(Keys.END)
        for i in range(0, size):
            target_element.send_keys(Keys.BACK_SPACE)
            time.sleep(sleep_time/size)
        time.sleep(sleep_time)

    def select_from_it(self, the_driver, select_option, sleep_time):
        """ Selects an option from a dropdown element """
        target_element = self.loc_it(the_driver)
        select_element = Select(target_element)
        select_element.select_by_value(select_option)
        time.sleep(sleep_time)
        
    def scroll_to_it(self, the_driver, sleep_time):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_element = self.loc_it(the_driver)
        target_element.location_once_scrolled_into_view
        time.sleep(sleep_time)

    def text_into_it(self, the_driver, input_text, sleep_time):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        target_element = self.loc_it(the_driver)
        for i in range(0, len(input_text)):
            target_element.send_keys(input_text[i])
            time.sleep(sleep_time/len(input_text))
        time.sleep(sleep_time)

    def get_text(self, the_driver):
        """ Returns content text of website element """
        target_element = self.loc_it(the_driver)
        return target_element.text

    def get_href(self, the_driver, base_url):
        """ Returns element href link, with relative links expanded
        into an absolute link
        """
        target_element = self.loc_it(the_driver)
        element_href = target_element.get_attribute("href")
        if element_href[0] == '/':
            element_href = base_url + element_href
        return element_href

    def nested_click(self, the_driver, children, sleep_time):
        """ Enables nesting specs for element identification.
        The approach below injects the parent element as the
        driver argument during location (consider maintainability
        improvements as future todo)
        """
        target_element = self.loc_it(the_driver)
        for i in range(0, len(children)):
            target_element = nest_loc_it(target_element, children[i])
        target_element.click()
        time.sleep(sleep_time)

    def nested_multi_click(self, the_driver, children, sleep_time):
        """ Enables nesting specs for element identification.
        The approach below injects the parent element as the
        driver argument during location (consider maintainability
        improvements as future todo)
        """
        target_element = self.loc_it(the_driver)
        for i in range(0, len(children)):
            target_element = nest_loc_it(target_element, children[i])
        actions = ActionChains(the_driver)
        actions.key_down(Keys.LEFT_CONTROL)
        actions.click(target_element)
        actions.key_up(Keys.LEFT_CONTROL)
        actions.perform()
        time.sleep(sleep_time)

    def nested_scroll(self, the_driver, children, sleep_time):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_element = self.loc_it(the_driver)
        for i in range(0, len(children)):
            target_element = nest_loc_it(target_element, children[i])
        target_element.location_once_scrolled_into_view
        time.sleep(sleep_time)
        
    def nested_text_into(self, the_driver, children, input_text, sleep_time):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        target_element = self.loc_it(the_driver)
        for i in range(0, len(children)):
            target_element = nest_loc_it(target_element, children[i])
        for i in range(0, len(input_text)):
            target_element.send_keys(input_text[i])
            time.sleep(sleep_time/len(input_text))
        time.sleep(sleep_time)
