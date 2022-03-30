""" SiteElement class improves organization of site element
parameters.  The class methods faciltate easy manipulation
 of these elements
"""
import platform
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.select import Select

from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException


class SiteElement:
    """Defines site elements in a structured way and provides a convenient
    means for element manipulations (clicking, entering text, etc.)
    """

    def __init__(self, by, locator):
        self.by = by
        self.locator = locator

    def loc_it(self, driver):
        """
        Identifies element on page, based on an element locator.
        Waits until an element becomes available & visible in DOM, and
        then until it becomes clickable.
        """
        wait = WebDriverWait(driver, 10)
        try:
            wait.until(EC.visibility_of_element_located((self.by, self.locator)))
            target_el = wait.until(EC.element_to_be_clickable((self.by, self.locator)))
        except TimeoutException as e:
            print(
                "\nUnable to locate element by {}, "
                "locator: '{}'".format(self.by, self.locator)
            )
            raise e

        return target_el

    def loc_hidden(self, driver):
        """
        Identifies potentially hidden element on page, based on an element locator.
        """
        wait = WebDriverWait(driver, 10)
        try:
            target_el = wait.until(EC.presence_of_element_located((self.by, self.locator)))
        except TimeoutException as e:
            print(
                "\nUnable to locate element by {}, "
                "locator: '{}'".format(self.by, self.locator)
            )
            raise e

        return target_el

    def exists(self, driver):
        """
        Checks if element is visible on the page.
        """
        wait = WebDriverWait(driver, 3)
        try:
            wait.until(EC.visibility_of_element_located((self.by, self.locator)))
            target_el = wait.until(EC.element_to_be_clickable((self.by, self.locator)))
            return True
        except TimeoutException:
            return False

    def exists_in_dom(self, driver):
        """
        Checks if element exists within the DOM.
        """
        wait = WebDriverWait(driver, 3)
        try:
            wait.until(EC.presence_of_element_located((self.by, self.locator)))
            return True
        except TimeoutException:
            return False

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

    def click(self, driver):
        """Identifies an element on the page.  After identification
        the element is then clicked.
        """
        target_el = self.loc_it(driver)
        target_el.click()

    def double_click(self, driver):
        """
        Double click on element.
        """
        target_el = self.loc_it(driver)
        actionchains = ActionChains(driver)
        actionchains.double_click(target_el).perform()

    def javascript_click(self, driver):
        """
        Clicks an element using JavaScript
        """
        target_el = self.loc_it(driver)
        driver.execute_script("arguments[0].click();", target_el)

    def javascript_click_hidden(self, driver):
        """
        Simulate click on a hidden element using JavaScript
        """
        target_el = self.loc_hidden(driver)
        driver.execute_script("arguments[0].click();", target_el)

    def javascript_fill_hidden_text(self, driver, text):
        """
        Set text using JavaScript for a potentially hidden element
        """
        target_el = self.loc_hidden(driver)
        driver.execute_script(f'arguments[0].value="{text}";', target_el)

    def submit(self, driver):
        """Send ENTER to element, simulates submit"""
        target_el = self.loc_it(driver)
        target_el.send_keys(Keys.ENTER)

    def submit_hidden(self, driver):
        """Send ENTER to element that is perhaps hidden,
        simulates submit
        """
        actions = ActionChains(driver)
        actions.key_down(Keys.ENTER)
        actions.key_up(Keys.ENTER)
        actions.perform()

    def multi_click(self, driver):
        """Clicks an element while holding the control key, as to enable
        a multi-selection
        """
        target_el = self.loc_it(driver)
        actions = ActionChains(driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.LEFT_CONTROL)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_CONTROL)
        actions.perform()

    def range_click(self, driver):
        """Clicks an element while holding the control key, as to enable
        a range selection
        """
        target_el = self.loc_it(driver)
        actions = ActionChains(driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.LEFT_SHIFT)
        actions.click(target_el)
        actions.key_up(Keys.LEFT_SHIFT)
        actions.perform()

    def passive_click(self, driver):
        """Identifies an element on the page.  After identification
        the element is then clicked, regardless if it is "interactable"
        or not
        """
        target_el = self.loc_it(driver)
        ActionChains(driver).move_to_element(target_el).click(target_el).perform()

    def clear_all_text(self, driver):
        """Uses the Ctrl+A keys combination to select all text before using
        BACKSPACE key to delete it
        """
        target_el = self.loc_it(driver)
        if platform.system() == "Darwin":  # MacOs
            ctrl_key = Keys.COMMAND
        else:
            ctrl_key = Keys.CONTROL
        ActionChains(driver).move_to_element(target_el).key_down(ctrl_key).send_keys(
            "a"
        ).key_up(ctrl_key).send_keys(Keys.BACKSPACE).perform()

    def clear_text(self, driver, size):
        """Uses backspace to clear text from a field"""
        target_el = self.loc_it(driver)
        target_el.send_keys(Keys.END)
        for i in range(0, size):
            target_el.send_keys(Keys.BACK_SPACE)

    def select_option(self, driver, select_choice):
        """Selects an option from a dropdown element"""
        target_el = self.loc_it(driver)
        select_el = Select(target_el)
        select_el.select_by_value(select_choice)

    def select_option_text(self, driver, select_choice):
        """Selects an option from dropdown given visible text"""
        target_el = self.loc_it(driver)
        select_el = Select(target_el)
        select_el.select_by_visible_text(select_choice)

    def scroll_to_hidden(self, driver):
        """After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_el = self.loc_hidden(driver)
        target_el.location_once_scrolled_into_view

    def scroll_to(self, driver):
        """After element identification, the window is scrolled
        such that the element becomes visible in the window
        """
        target_el = self.loc_it(driver)
        target_el.location_once_scrolled_into_view

    def scroll_right(self, driver):
        """Scroll right using Keys.ARROW_RIGHT
        and a hold of one second
        """
        target_el = self.loc_it(driver)
        actions = ActionChains(driver)
        actions.move_to_element(target_el)
        actions.key_down(Keys.ARROW_RIGHT)
        actions.perform()
        time.sleep(1)
        actions = ActionChains(driver)
        actions.key_up(Keys.ARROW_RIGHT)
        actions.perform()

    def inject_text(self, driver, field_text):
        """Enters text into a field or other input-capable html
        element using send keys
        """
        target_el = self.loc_it(driver)
        for i in range(0, len(field_text)):
            target_el.send_keys(field_text[i])

    def hidden_inject_text(self, driver, field_text):
        """Enters text into a field or other input-capable html
        element that is hidden using send keys
        """
        target_el = self.loc_hidden(driver)
        for i in range(0, len(field_text)):
            target_el.send_keys(field_text[i])

    def send_caps(self, driver, field_text):
        """Enters capitalized text into a field or other input-capable
        html element using send_keys_to_element
        """
        actionchains = ActionChains(driver)
        target_el = self.loc_it(driver)
        actionchains.key_down(Keys.SHIFT).send_keys_to_element(
            target_el, field_text
        ).key_up(Keys.SHIFT).perform()

    def set_path(self, driver, field_text):
        """Enters text into a field or other input-capable html
        element using send keys, best for setting path to files for upload
        """
        target_el = self.loc_it(driver)
        target_el.send_keys(field_text)

    def iframe_in(self, driver):
        """Switches driver focus to an iframe within a page"""
        target_el = self.loc_it(driver)
        driver.switch_to.frame(target_el)

    def iframe_out(self, driver):
        """Switches driver focus out of iframe and back to the
        main page
        """
        driver.switch_to.parent_frame()

    def get_attribute(self, driver, attribute):
        """Returns any attribute of website element"""
        target_el = self.loc_it(driver)
        return target_el.get_attribute(attribute)

    def get_text(self, driver):
        """Returns content text of website element"""
        target_el = self.loc_it(driver)
        return target_el.text

    def get_value(self, driver):
        """Returns content text of website element"""
        target_el = self.loc_it(driver)
        return target_el.get_attribute("value")

    def get_href(self, driver, base_url=None):
        """Returns element href link, with relative links expanded
        into an absolute link
        """
        target_el = self.loc_it(driver)
        target_href = target_el.get_attribute("href")
        if target_href[0] == "/":
            target_href = base_url + target_href
        return target_href

    def get_bag_url(self, driver, base_url=None):
        """Returns element href link, with relative links expanded
        into an absolute link
        """
        target_el = self.loc_it(driver)
        target_href = target_el.get_attribute("data-bag-url")
        if target_href[0] == "/":
            target_href = base_url + target_href
        return target_href

    def get_child_count(self, driver):
        """Returns the number of child elements, given a parent
        element specification
        """
        target_el = self.loc_it(driver)
        return len(target_el.find_elements_by_xpath(".//*"))

    def get_relatives_by_xpath(self, driver, xpath):
        """Returns the relatives by xpath, given a parent
        element specification
        """
        target_el = self.loc_it(driver)
        return target_el.find_elements_by_xpath(xpath)

    def get_texts_from_xpath(self, driver, xpath):
        """Returns the text in relatives matching xpath, given a parent
        element specification
        """
        web_elements = self.get_relatives_by_xpath(driver, xpath)
        keywords = []
        for el in web_elements:
            keywords.append(el.text)
        return keywords

    def get_parent(self, driver):
        """Returns the parent element
        """
        target_el = self.loc_hidden(driver)
        return target_el.find_element_by_xpath("..")

    def get_immediate_child_count(self, driver):
        """Returns the number of immediate child elements, given a parent
        element specification
        """
        target_el = self.loc_it(driver)
        return len(target_el.find_elements_by_xpath("*"))

    def get_class(self, driver):
        target_el = self.loc_it(driver)
        target_class = target_el.get_attribute("class")
        return target_class

    def get_style(self, driver):
        target_el = self.loc_it(driver)
        target_style = target_el.get_attribute("style")
        return target_style

    def wait_on_visibility(self, driver, max_time):
        locator = self.by, self.locator
        WebDriverWait(driver, max_time).until(EC.visibility_of_element_located(locator))

    def right_click(self, driver):
        target_el = self.loc_it(driver)
        actions = ActionChains(driver)
        actions.context_click(target_el)
        actions.perform()


class SiteElementsCollection:
    """
    Provides a way to locate all page elements which are identified by a
    common locator.
    """

    def __init__(self, by, locator):
        self.by = by
        self.locator = locator

    def loc_them(self, driver):
        """
        Finds all elements on a page that match a given locator.
        Waits until all elements become visible in a DOM.
        """
        wait = WebDriverWait(driver, 30)
        try:
            elements = wait.until(
                EC.visibility_of_all_elements_located((self.by, self.locator))
            )
        except TimeoutException as e:
            print(
                "\nUnable to locate elements by {}, "
                "locator: '{}'".format(self.by, self.locator)
            )
            raise e

        return elements

    def items(self, driver):
        return self.loc_them(driver)
