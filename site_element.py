""" SiteElement class in theory improves organization of
site element characteristics.  Methods faciltate easy clicking
for these elements
"""
import time
from nested_funcs import *

class SiteElement:
    """ Defines site elements in a structured way """

    def __init__(self, the_type=None, the_id=None, the_content=None,
                 the_href=None, the_class=None):
        self.element_type = the_type
        self.element_id = the_id
        self.element_content = the_content
        self.element_href = the_href
        self.element_class = the_class

    def loc_it(self, the_driver):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).
        """
        if self.element_id is not None:
            the_element = self.loc_by_id(the_driver)
        elif self.element_href is not None:
            the_element = self.loc_by_href(the_driver)
        elif self.element_class is not None:
            the_element = self.loc_by_class(the_driver)
        elif self.element_content is not None:
            the_element = self.loc_by_content(the_driver)
        else:
            the_element = self.loc_by_nothing(the_driver)
        return the_element

    def click_it(self, the_driver, sleep_time):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).  After identification
        the element is then clicked.
        """
        the_element = self.loc_it(the_driver)
        the_element.click()
        time.sleep(sleep_time)

    def scroll_to_it(self, the_driver, sleep_time):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        the_element = self.loc_it(the_driver)
        the_element.location_once_scrolled_into_view
        time.sleep(sleep_time)

    def text_into_it(self, the_driver, input_text, sleep_time):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        the_element = self.loc_it(the_driver)
        the_element.send_keys(input_text)
        time.sleep(sleep_time)

    def loc_by_id(self, the_driver): #Dont call in scripts directly
        """ Clicks on a website element, given the element type and id """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        return element_pin

    def loc_by_href(self, the_driver): #Dont call in scripts directly
        """ Clicks on a website element, given the element type and href """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[contains(@href,'" + self.element_href + "')]"
        element_pin = driver.find_element_by_xpath(element_spec)
        return element_pin

    def loc_by_class(self, the_driver): #Dont call in scripts directly
        """ Clicks on a website element, given the element class.  If
        multiple elements of the same class exist, the first one will
        be clicked
        """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@class='" + self.element_class + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        return element_pin

    def loc_by_content(self, the_driver): #Dont call in scripts directly
        """ Clicks on a website element, based the element text content """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[contains(text(), '" + self.element_content + "')]"
        element_pin = driver.find_element_by_xpath(element_spec)
        return element_pin

    def loc_by_nothing(self, the_driver): #Dont call in scripts directly
        """ Selects a website element based only on the tag/type """
        driver = the_driver
        element_spec = "//" + self.element_type
        element_pin = driver.find_element_by_xpath(element_spec)
        return element_pin

    def get_text(self, the_driver):
        """ Returns content text of website element """
        the_element = self.loc_it(the_driver)
        return the_element.text

    def get_href(self, the_driver, base_url):
        """ Returns element href link, with relative links expanded
        into an absolute link
        """
        the_element = self.loc_it(the_driver)
        element_href = the_element.get_attribute("href")
        if element_href[0] == '/':
            element_href = base_url + element_href
        return element_href

    def nested_click(self, the_driver, children, sleep_time):
        """ Enables nesting specs for element identification.
        The approach below injects the parent element as the
        driver argument during location (consider maintainability
        improvements as future todo)
        """
        the_element = self.loc_it(the_driver)
        for i in range(0, len(children)):
            the_element = nest_loc_it(the_element, children[i])
        the_element.click()
        time.sleep(sleep_time)
