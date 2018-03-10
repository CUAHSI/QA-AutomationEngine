""" SiteElement class improves organization of site element
parameters.  The class methods faciltate easy manipulation
 of these elements
"""
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select


class SiteElement:
    """ Defines site elements in a structured way and provides a convenient
    means for element manipulations (clicking, entering text, etc.)
    """
    def __init__(self, el_type=None, el_id=None, el_content=None,
                 el_href=None, el_class=None, el_dom=None, el_name=None,
                 el_placeholder=None, el_title=None, el_recursive=None):
        self.el_type = el_type
        self.el_id = el_id
        self.el_content = el_content
        self.el_href = el_href
        self.el_class = el_class
        self.el_dom = el_dom
        self.el_name = el_name
        self.el_placeholder = el_placeholder
        self.el_title = el_title
        self.el_recursive = el_recursive

    def loc_it(self, el_driver):
        """ Identifies element on page, based on a hierarchy
        of preferred identification methods (eg. by html element
        id is preferrable to html element class).
        """
        def loc_next(loc_base, loc_child=None):
            """ Locates the "next" element through absolute (loc_child==None)
            or relative (loc_child!=None) means
            """
            def loc_by_id(loc_base, loc_child):
                """ Locates a website element, given the element type and id
                """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[@id='" + self.el_id + "']"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[@id='" + loc_child.el_id + "']"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_name(loc_base, loc_child):
                """ Locates a website element, given the name attribute """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[@name='" + self.el_name + "']"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[@name='" + loc_child.el_name + "']"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_title(loc_base, loc_child):
                """ Locates a website element, given the title
                attribute
                """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[@title='" + self.el_title + "']"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[@title='" + loc_child.el_title + "']"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_placeholder(loc_base, loc_child):
                """ Locates a website element, given the placeholder
                attribute
                """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[@placeholder='" + self.el_placeholder + "']"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[@placeholder='" + \
                               loc_child.el_placeholder + "']"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_href(loc_base, loc_child):
                """ Locates a website element, given the element type
                and href
                """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[contains(@href,'" + self.el_href + "')]"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[contains(@href,'" + \
                               loc_child.el_href + "')]"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_class(loc_base, loc_child):
                """ Locates a website element, given the element class """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[@class='" + self.el_class + "']"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[@class='" + loc_child.el_class + "']"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_content(loc_base, loc_child):
                """ Locates a website element, based the element
                text content
                """
                if loc_child is None:
                    el_xpath = "//" + self.el_type + \
                               "[contains(text(), '" + \
                               self.el_content + "')]"
                else:
                    el_xpath = ".//" + loc_child.el_type + \
                               "[contains(text(), '" + \
                               loc_child.el_content + "')]"
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_dom(loc_base, loc_child):
                """ Locates a website element given DOM path to element """
                if loc_child is None:
                    el_xpath = self.el_dom
                else:
                    el_xpath = loc_child.el_dom
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            def loc_by_nothing(loc_base, loc_child):
                """ Locates a website element based only on the tag/type """
                if loc_child is None:
                    el_xpath = "//" + self.el_type
                else:
                    el_xpath = ".//" + loc_child.el_type
                target_el = loc_base.find_element_by_xpath(el_xpath)
                return target_el

            if loc_child is None:
                defining_el = self  # For absolute identification
            else:
                defining_el = loc_child  # For relative identification

            # Hierarchy for identification using element attributes is
            # id->name->title->href->class->content->DOM->type(no attributes)
            if defining_el.el_id is not None:
                target_el = loc_by_id(loc_base, loc_child)
            elif defining_el.el_name is not None:
                target_el = loc_by_name(loc_base, loc_child)
            elif defining_el.el_title is not None:
                target_el = loc_by_title(loc_base, loc_child)
            elif defining_el.el_placeholder is not None:
                target_el = loc_by_placeholder(loc_base, loc_child)
            elif defining_el.el_href is not None:
                target_el = loc_by_href(loc_base, loc_child)
            elif defining_el.el_class is not None:
                target_el = loc_by_class(loc_base, loc_child)
            elif defining_el.el_content is not None:
                target_el = loc_by_content(loc_base, loc_child)
            elif defining_el.el_dom is not None:
                target_el = loc_by_dom(loc_base, loc_child)
            else:
                target_el = loc_by_nothing(loc_base, loc_child)
            return target_el

        if self.el_recursive is None:  # Use basic/single identification
            target_el = loc_next(el_driver)
        else:  # Use recursive identification
            target_el = loc_next(el_driver)
            for i in range(0, len(self.el_recursive)):
                target_el = loc_next(target_el, self.el_recursive[i])
        return target_el

    def click(self, el_driver, sleep_time):
        """ Identifies an element on the page.  After identification
        the element is then clicked.
        """
        target_el = self.loc_it(el_driver)
        target_el.click()
        time.sleep(sleep_time)

    def multi_click(self, el_driver, sleep_time):
        """ Clicks an element while holding the control key, as to enable
        a multi-selection
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.key_down(Keys.LEFT_CONTROL)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_CONTROL)
        actions.perform()
        time.sleep(sleep_time)

    def range_click(self, el_driver, sleep_time):
        """ Clicks an element while holding the control key, as to enable
        a range selection
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.key_down(Keys.LEFT_SHIFT)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_SHIFT)
        actions.perform()
        time.sleep(sleep_time)

    def passive_click(self, el_driver, sleep_time):
        """ Identifies an element on the page.  After identification
        the element is then clicked, regardless if it is "interactable"
        or not
        """
        target_el = self.loc_it(el_driver)
        actions = ActionChains(el_driver)
        actions.move_to_element(target_el)
        actions.click(target_el)
        actions.perform()
        time.sleep(sleep_time)

    def clear_all_text(self, el_driver, sleep_time):
        """ Uses the END and HOME to select all text before using
        BACKSPACE key to delete it
        """
        actions = ActionChains(el_driver)
        actions.key_down(Keys.HOME)
        actions.key_up(Keys.HOME)
        actions.perform()
        time.sleep(sleep_time/3)
        actions.key_down(Keys.LEFT_SHIFT)
        actions.key_down(Keys.END)
        actions.key_up(Keys.END)
        actions.key_up(Keys.LEFT_SHIFT)
        actions.perform()
        time.sleep(sleep_time/3)
        actions.key_down(Keys.BACK_SPACE)
        actions.key_up(Keys.BACK_SPACE)
        actions.perform()
        time.sleep(sleep_time/3)

    def clear_text(self, el_driver, size, sleep_time):
        """ Uses backspace to clear text from a field """
        target_el = self.loc_it(el_driver)
        target_el.send_keys(Keys.END)
        for i in range(0, size):
            target_el.send_keys(Keys.BACK_SPACE)
            time.sleep(sleep_time/size)
        time.sleep(sleep_time)

    def select_option(self, el_driver, select_choice, sleep_time):
        """ Selects an option from a dropdown element """
        target_el = self.loc_it(el_driver)
        select_el = Select(target_el)
        select_el.select_by_value(select_choice)
        time.sleep(sleep_time)

    def select_option_text(self, el_driver, select_choice, sleep_time):
        """ Selects an option from dropdown given visible text """
        target_el = self.loc_it(el_driver)
        select_el = Select(target_el)
        select_el.select_by_visible_text(select_choice)
        time.sleep(sleep_time)

    def scroll_to(self, el_driver, sleep_time):
        """ After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_el = self.loc_it(el_driver)
        target_el.location_once_scrolled_into_view
        time.sleep(sleep_time)

    def scroll_right(self, el_driver, sleep_time):
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
        time.sleep(sleep_time/2)

    def inject_text(self, el_driver, field_text, sleep_time):
        """ Enters text into a field or other input-capable html
        element using send keys
        """
        target_el = self.loc_it(el_driver)
        for i in range(0, len(field_text)):
            target_el.send_keys(field_text[i])
            time.sleep(sleep_time/len(field_text))
        time.sleep(sleep_time)

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
