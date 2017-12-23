""" This module contains function to support the identification and
manipulation of elements which cannot be identified independently, but
instead are identified by descending the DOM from a more identifiable
parent element
"""

import time

def nest_loc_it(parent_element, child_element):
    """ Idenfies nested element based on hierarchy of
    preferred identification methods
    """
    def nest_loc_by_id(parent_element, child_element):
        """ Locates a website element, given the element type and id """
        child_xpath = "//" + child_element.el_type + \
                       "[@id='" + child_element.el_id + "']"
        result_element = parent_element.find_element_by_xpath(child_xpath)
        return result_element

    def nest_loc_by_href(parent_element, child_element):
        """ Locates a website element, given the element type and href """
        child_xpath = "//" + child_element.el_type + \
                       "[contains(@href,'" + child_element.el_href + "')]"
        result_element = parent_element.find_element_by_xpath(child_xpath)
        return result_element
    
    def nest_loc_by_class(parent_element, child_element):
        """ Locates a website element, given the element class """
        child_xpath = "//" + child_element.el_type + \
                       "[@class='" + child_element.el_class + "']"
        result_element = parent_element.find_element_by_xpath(child_xpath)
        return result_element
    
    def nest_loc_by_content(parent_element, child_element):
        """ Locates a website element, based the element text content """
        child_xpath = "//" + child_element.el_type + \
                       "[contains(text(), '" + child_element.el_content + "')]"
        result_element = parent_element.find_element_by_xpath(child_xpath)
        return result_element

    def nest_loc_by_dom(parent_element, child_element):
        """ Locates a website element, based on DOM path to element """
        child_xpath = child_element.el_dom
        result_element = parent_element.find_element_by_xpath(child_xpath)
    
    def nest_loc_by_nothing(parent_element, child_element):
        """ Locates a website element based only on the tag/type """
        child_xpath = "//" + child_element.el_type
        result_element = parent_element.find_element_by_xpath(child_xpath)
        return result_element

    if child_element.el_id is not None:
        target_element = nest_loc_by_id(parent_element, child_element)
    elif child_element.el_href is not None:
        target_element = nest_loc_by_href(parent_element, child_element)
    elif child_element.el_class is not None:
        target_element = nest_loc_by_class(parent_element, child_element)
    elif child_element.el_content is not None:
        target_element = nest_loc_by_content(parent_element, child_element)
    elif child_element.el_dom is not None:
        target_element = nest_loc_by_dom(parent_element, child_element)
    else:
        target_element = nest_loc_by_nothing(parent_element, child_element)
    return target_element

