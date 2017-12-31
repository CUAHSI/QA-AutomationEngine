import sys
import os
from hs_elements import *
from modes import setup_mode

# Testing parameters
MODE_SELECTION = 'demo'
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)

class ResourceLanding:
    """ Individual resource info/download page macros """
    def download_size(self, driver, BASE_URL):
        download_href = ResourceLandingPage.download_bagit.get_href(driver, BASE_URL)
        os.system('wget ' + download_href)
        download_file = download_href.split('/')[-1]
        file_size = os.stat(download_file).st_size
        return file_size

class Discover:
    """ Discover tool macros """
    def open_resource(self, driver, resource_title):
        DiscoverPage.open_resource(resource_title).click(driver, SLEEP_TIME)

    def discover_resources(self, driver, author=None, subject=None,
                           resource_type=None, owner=None, variable=None,
                           sample_medium=None, unit=None, availability=None):
        HomePage.goto_discover(driver, SLEEP_TIME)
        if type(author) is list:
            for author_item in author:
                DiscoverPage.filter_author(author_item).click(driver, SLEEP_TIME)
        elif author is not None:
            DiscoverPage.filter_author(author).click(driver, SLEEP_TIME)
        if type(subject) is list:
            for subject_item in subject:
                DiscoverPage.filter_subject(subject_item).click(driver, SLEEP_TIME)
        elif subject is not None:
            DiscoverPage.filter_subject(subject).click(driver, SLEEP_TIME)
        if type(resource_type) is list:
            for resource_type_item in resource_type:
                DiscoverPage.filter_resource_type(resource_type_item).click(driver, SLEEP_TIME)
        elif resource_type is not None:
            DiscoverPage.filter_resource_type(resource_type).click(driver, SLEEP_TIME)
        if type(owner) is list:
            for owner_item in owner:
                DiscoverPage.filter_owner(owner_item).click(driver, SLEEP_TIME)
        elif owner is not None:
            DiscoverPage.filter_owner(owner).click(driver, SLEEP_TIME)
        if type(variable) is list:
            for variable_item in variable:
                DiscoverPage.filter_variable(variable_item).click(driver, SLEEP_TIME)
        elif variable is not None:
            DiscoverPage.filter_variable(variable).click(driver, SLEEP_TIME)
        if type(sample_medium) is list:
            for sample_medium_item in sample_medium:
                DiscoverPage.filter_sample_medium(sample_medium_item).click(driver, SLEEP_TIME)
        elif sample_medium is not None:
            DiscoverPage.filter_sample_medium(sample_medium).click(driver, SLEEP_TIME)
        if type(unit) is list:
            for unit_item in unit:
                DiscoverPage.filter_unit(unit_item).click(driver, SLEEP_TIME)
        elif unit is not None:
            DiscoverPage.filter_unit(unit).click(driver, SLEEP_TIME)
        if type(availability) is list:
            for availability_item in availability:
                DiscoverPage.filter_availability(availability_item).click(driver, SLEEP_TIME)
        elif availability is not None:
            DiscoverPage.filter_availability(availability).click(driver, SLEEP_TIME)
    
ResourceLanding = ResourceLanding()
Discover = Discover()
