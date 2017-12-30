""" SiteElement class improves organization of site element 
parameters.  The class methods faciltate easy manipulation
 of these elements
"""
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

class SiteElement:
    """ Defines site elements in a structured way and provides a convenient means
    for element manipulations (clicking, entering text, etc.)
    """
    def __init__(self, el_type=None, el_id=None, el_content=None,
                 el_href=None, el_class=None, el_dom=None, el_name=None,
                 recursive_loc=None):
        self.el_type = el_type
        self.el_id = el_id
        self.el_content = el_content
        self.el_href = el_href
        self.el_class = el_class
        self.el_dom = el_dom
        self.el_name = el_name
        self.recursive_loc = recursive_loc

    def loc_it(self, the_driver):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).
        """
        def next_el_loc(loc_base, loc_child=None):
            """ Locates the "next" element through absolute (loc_child==None)
            or relative (loc_child!=None) means
            """
            def loc_by_id(loc_base, loc_child):
                """ Locates a website element, given the element type and id """
                if loc_child is None:
                    element_xpath = "//" + self.el_type + \
                                    "[@id='" + self.el_id + "']"
                else:
                    element_xpath = ".//" + loc_child.el_type + \
                                    "[@id='" + loc_child.el_id + "']"
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element
                
            def loc_by_name(loc_base, loc_child):
                """ Locates a website element, given the name attribute """
                if loc_child is None:
                    element_xpath = "//" + self.el_type + \
                                    "[@name='" + self.el_name + "']"
                else:
                    element_xpath = ".//" + loc_child.el_type + \
                                    "[@name='" + loc_child.el_name + "']"
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element
        
            def loc_by_href(loc_base, loc_child):
                """ Locates a website element, given the element type
                and href 
                """
                if loc_child is None:
                    element_xpath = "//" + self.el_type + \
                                    "[contains(@href,'" + self.el_href + "')]"
                else:
                    element_xpath = ".//" + loc_child.el_type + \
                                    "[contains(@href,'" + loc_child.el_href + "')]"
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element

            def loc_by_class(loc_base, loc_child):
                """ Locates a website element, given the element class """
                if loc_child is None:
                    element_xpath = "//" + self.el_type + \
                                    "[@class='" + self.el_class + "']"
                else:
                    element_xpath = ".//" + loc_child.el_type + \
                                    "[@class='" + loc_child.el_class + "']"
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element
        
            def loc_by_content(loc_base, loc_child):
                """ Locates a website element, based the element text content """
                if loc_child is None:
                    element_xpath = "//" + self.el_type + \
                                    "[contains(text(), '" + \
                                    self.el_content + "')]"
                else:
                    element_xpath = ".//" + loc_child.el_type + \
                                    "[contains(text(), '" + \
                                    loc_child.el_content + "')]"
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element

            def loc_by_dom(loc_base, loc_child):
                """ Locates a website element given DOM path to element """
                if loc_child is None:
                    element_xpath = self.el_dom
                else:
                    element_xpath = loc_child.el_dom
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element
        
            def loc_by_nothing(loc_base, loc_child):
                """ Locates a website element based only on the tag/type """
                if loc_child is None:
                    element_xpath = "//" + self.el_type
                else:
                    element_xpath = ".//" + loc_child.el_type
                target_element = loc_base.find_element_by_xpath(element_xpath)
                return target_element

            if loc_child is None:
                defining_el = self # For absolute identification
            else:
                defining_el = loc_child # For relative identification

            # Hierarcy for identification using element attributes is
            # id->name->href->class->content->DOM->type(no attributes)
            if defining_el.el_id is not None:
                target_element = loc_by_id(loc_base, loc_child)
            elif defining_el.el_name is not None:
                target_element = loc_by_name(loc_base, loc_child)
            elif defining_el.el_href is not None:
                target_element = loc_by_href(loc_base, loc_child)
            elif defining_el.el_class is not None:
                target_element = loc_by_class(loc_base, loc_child)
            elif defining_el.el_content is not None:
                target_element = loc_by_content(loc_base, loc_child)
            elif defining_el.el_dom is not None:
                target_element = loc_by_dom(loc_base, loc_child)
            else:
                target_element = loc_by_nothing(loc_base, loc_child)
            return target_element

        
        if self.recursive_loc is None: # Use basic/single identification
            target_element = next_el_loc(the_driver)
        else: # Use recursive identification
            target_element = next_el_loc(the_driver)
            for i in range(0, len(self.recursive_loc)):
                target_element = next_el_loc(target_element,
                                             self.recursive_loc[i])
        return target_element
        

    def click(self, the_driver, sleep_time):
        """ Identifies an element on the page.  After identification
        the element is then clicked.
        """
        target_element = self.loc_it(the_driver)
        target_element.click()
        time.sleep(sleep_time)

    def multi_click(self, the_driver, sleep_time):
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
        
    def passive_click(self, the_driver, sleep_time):
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
        
    def clear_text(self, the_driver, size, sleep_time):
        """ Uses backspace to clear text from a field """
        target_element = self.loc_it(the_driver)
        target_element.send_keys(Keys.END)
        for i in range(0, size):
            target_element.send_keys(Keys.BACK_SPACE)
            time.sleep(sleep_time/size)
        time.sleep(sleep_time)

    def select_option(self, the_driver, select_option, sleep_time):
        """ Selects an option from a dropdown element """
        target_element = self.loc_it(the_driver)
        select_element = Select(target_element)
        select_element.select_by_value(select_option)
        time.sleep(sleep_time)
        
    def scroll_to(self, the_driver, sleep_time):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_element = self.loc_it(the_driver)
        target_element.location_once_scrolled_into_view
        time.sleep(sleep_time)

    def inject_text(self, the_driver, input_text, sleep_time):
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
