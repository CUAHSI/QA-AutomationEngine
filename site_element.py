""" SiteElement class in theory improves organization of
site element characteristics.  Methods faciltate easy clicking
for these elements
"""
import time

class SiteElement:
    """ Defines site elements in a structured way """

    def __init__(self, the_type=None, the_id=None, the_content=None,
                 the_href=None, the_class=None):
        self.element_type = the_type
        self.element_id = the_id
        self.element_content = the_content
        self.element_href = the_href
        self.element_class = the_class

    def click_it(self, driver, element):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).  After identification
        the element is then clicked.
        """
        if self.element_id is not None:
            self.click_by_id(driver, SLEEP_TIME)
        elif self.element_href is not None:
            self.click_by_href(driver, SLEEP_TIME)
        elif self.element_content is not None:
            self.click_by_content(driver, SLEEP_TIME)
        
    def scroll_by_id(self, the_driver, sleep_time):
        """ Scrolls to a div, given its id """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.location_once_scrolled_into_view
        time.sleep(sleep_time)        
        
    def click_by_content(self, the_driver, sleep_time):
        """ Clicks on a website element, based the element text content """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[contains(text(), '" + self.element_content + "')]"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.click()
        time.sleep(sleep_time)

    def click_by_id(self, the_driver, sleep_time):
        """ Clicks on a website element, given the element type and id """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.click()
        time.sleep(sleep_time)

    def click_by_class(self, the_driver, sleep_time):
        """ Clicks on a website element, given the element class.  If
        multiple elements of the same class exist, the first one will
        be clicked
        """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@class='" + self.element_class + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.click()
        time.sleep(sleep_time)

    def click_by_href(self, the_driver, sleep_time):
        """ Clicks on a website element, given the element type and href """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[contains(@href,'" + self.element_href + "')]"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.click()
        time.sleep(sleep_time)

    def text_by_id(self, the_driver, input_text, sleep_time):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        driver = the_driver
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_pin.send_keys(input_text)
        time.sleep(sleep_time)

    def contains_text(self, the_driver, substring):
        """ Checks if an element contains contains a substring
        in it's text
        """
        driver = the_driver
        # TODO Enable non-ID element identification
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        return substring in element_pin.text

    def download_link(self, the_driver, base_url):
        """ Returns element href link, with relative links expanded
        into an absolute link
        """
        driver = the_driver
        # TODO Enable non-ID element identification
        element_spec = "//" + self.element_type + \
                       "[@id='" + self.element_id + "']"
        element_pin = driver.find_element_by_xpath(element_spec)
        element_href = element_pin.get_attribute("href")
        if (element_href[0] == '/'):
            element_href = base_url + element_href
        return element_href
