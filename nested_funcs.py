""" This module contains function to support the identification and
manipulation of elements which cannot be identified independently, but
rather through descending the DOM from a more identifiable parent element
"""

import time

def nest_loc_it(the_parent, the_child):
    """ Idenfies nested element based on hierarchy of
    preferred identification methods
    """
    def nest_loc_by_id(parent, child):
        """ Clicks on a website element, given the element type and id """
        element_spec = "//" + child.element_type + \
                       "[@id='" + child.element_id + "']"
        element_pin = parent.find_element_by_xpath(element_spec)
        return element_pin

    def nest_loc_by_href(parent, child):
        """ Clicks on a website element, given the element type and href """
        element_spec = "//" + child.element_type + \
                       "[contains(@href,'" + child.element_href + "')]"
        element_pin = parent.find_element_by_xpath(element_spec)
        return element_pin
    
    def nest_loc_by_class(parent, child):
        """ Clicks on a website element, given the element class.  If
        multiple elements of the same class exist, the first one will
        be clicked
        """
        element_spec = "//" + child.element_type + \
                       "[@class='" + child.element_class + "']"
        element_pin = parent.find_element_by_xpath(element_spec)
        return element_pin
    
    def nest_loc_by_content(parent, child):
        """ Clicks on a website element, based the element text content """
        element_spec = "//" + child.element_type + \
                       "[contains(text(), '" + child.element_content + "')]"
        element_pin = parent.find_element_by_xpath(element_spec)
        return element_pin
    
    def nest_loc_by_nothing(parent, child):
        """ Selects a website element based only on the tag/type """
        element_spec = "//" + child.element_type
        element_pin = parent.find_element_by_xpath(element_spec)
        return element_pin

    if the_child.element_id is not None:
        the_element = nest_loc_by_id(the_parent, the_child)
    elif the_child.element_href is not None:
        the_element = nest_loc_by_href(the_parent, the_child)
    elif the_child.element_class is not None:
        the_element = nest_loc_by_class(the_parent, the_child)
    elif the_child.element_content is not None:
        the_element = nest_loc_by_content(the_parent, the_child)
    else:
        the_element = nest_loc_by_nothing(the_parent, the_child)
    return the_element

