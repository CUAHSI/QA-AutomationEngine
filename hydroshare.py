""" Runs various smoke tests for the hydroshare.org """
import unittest
import argparse
import sys
import os
import time
# import argparse
from selenium import webdriver
from site_element import SiteElement
from modes import setup_mode

# Test case parameters
MODE_SELECTION = 'demo'
SLEEP_TIME = setup_mode(MODE_SELECTION)
# PARSER = argparse.ArgumentParser(description='Run hydroshare test suite.')
# PARSER.add_argument('-u', '--url', required=False, help='URL for testing')
# ARGS = PARSER.parse_args()
# BASE_URL = ARGS.url
# if BASE_URL is None:
BASE_URL = "http://www.hydroshare.org" # Default

# All
DISCOVERY_TAB = SiteElement('li', el_id='dropdown-menu-search')
# Discover page
DISCOVER_START_DATE = SiteElement('input', el_id='id_start_date')
DISCOVER_END_DATE = SiteElement('input', el_id='id_end_date')
DISCOVER_VIEW_MAP_TAB = SiteElement('a', el_href='map-view')
DISCOVER_MAP_SEARCH = SiteElement('input', el_id='geocoder-address')
DISCOVER_MAP_SEARCH_SUBMIT = SiteElement('a', el_id='geocoder-submit')
DISCOVER_VIEW_LIST_TAB = SiteElement('a', el_content='List')
IUTAH_SUBJECTS_FILTER = SiteElement('input', el_id='subjects-iUTAH')
GENERIC_RESOURCE_TYPE_FILTER = SiteElement('input', el_id='resource_type-Generic')
IS_DISCOVERABLE_FILTER = SiteElement('input', el_id='discoverable-true')
IS_PUBLIC_FILTER = SiteElement('input', el_id='public-true')
BEAVER_DIVIDE_RESC = SiteElement('a', el_content='Beaver Divide Air Temperature')
# Resource landing page from Discover
DOWNLOAD_BAGIT = SiteElement('a', el_id='btn-download-all', el_content=\
                             'Download All Content as Zipped BagIt Archive')
BEAVER_DIVIDE_ZIP_SIZE = 512000

# Test cases definition
class HydroshareTestCase(unittest.TestCase):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        """ Setup driver for use in automation tests """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "CUAHSI-QA-Selenium")
        global driver
        if infrastructure == 'grid':
            driver = webdriver.Remote(command_executor='http://' + \
                                      grid_hub_ip + ':4444/wd/hub',
                                      desired_capabilities={'browserName': 'firefox'})
        else:
            driver = webdriver.Firefox(profile)
        driver.get(BASE_URL)
        driver.implicitly_wait(10)

    def tearDown(self):
        """ Tear down test environment after execution """
        driver.quit()

    def test_B_000003(self):
        """ Confirms Beaver Divide Air Temperature resource
        landing page is online via navigation and title check,
        then downloads the BagIt archive and confirms
        """
        def oracle():
            """ The Beaver Divide BagIt zip file
            matches expected file size
            """
            self.assertTrue(file_size == BEAVER_DIVIDE_ZIP_SIZE)
        # Pulls up discover search page through site header
        DISCOVERY_TAB.click(driver, SLEEP_TIME)
        # Filters by subject of iUTAH in left panel
        IUTAH_SUBJECTS_FILTER.click(driver, SLEEP_TIME)
        # Filters by resouce type of Generic in left panel
        GENERIC_RESOURCE_TYPE_FILTER.click(driver, SLEEP_TIME)
        # Filters by availability of Discoverable or Public
        IS_DISCOVERABLE_FILTER.click(driver, SLEEP_TIME)
        IS_PUBLIC_FILTER.click(driver, SLEEP_TIME)
        # Clicks specific resourse - Beaver Divide Air Temperaure
        BEAVER_DIVIDE_RESC.click(driver, SLEEP_TIME)
        # Checks download button exists with text for "Download" and "BagIt"
        self.assertTrue(('Download' in DOWNLOAD_BAGIT.get_text(driver)) and \
                        ('BagIt' in DOWNLOAD_BAGIT.get_text(driver)))
        download_href = DOWNLOAD_BAGIT.get_href(driver, BASE_URL)
        # Download the BagIt zip file
        os.system('wget ' + download_href)
        # Get the files size of the downloaded BagIt zip file
        download_file = download_href.split('/')[-1]
        file_size = os.stat(download_file).st_size
        # Confirm the downloaded file size matches expectation
        oracle()

    def todo_test_B_000004(self):
        """ Confirms date filtering functionality, as well as
        map view functionality
        """
        def oracle():
            """ Confirms valid page returned after navigation """
            self.assertTrue('HydroShare' in driver.title)
        # Pulls up discover search page through site header
        DISCOVERY_TAB.click(driver, SLEEP_TIME)
        DISCOVER_START_DATE.inject_text(driver, "01/01/2014", SLEEP_TIME)
        DISCOVER_END_DATE.inject_text(driver, "12/31/2014", SLEEP_TIME)
        # TODO fix element identification issue
        DISCOVER_VIEW_MAP_TAB.click(driver, SLEEP_TIME)
        DISCOVER_MAP_SEARCH.inject_text(driver, "Salt Lake City", SLEEP_TIME)
        DISCOVER_MAP_SEARCH_SUBMIT.click(driver, SLEEP_TIME)
        DISCOVER_VIEW_LIST_TAB.click(driver, SLEEP_TIME)
        time.sleep(5)
        oracle()

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid')
    parser.add_argument('unittest_args', nargs='*')
    
    args = parser.parse_args()
    if args.grid is None:
        infrastructure = 'standalone'
    else:
        infrastructure = 'grid'
        grid_hub_ip = args.grid
        
    # Set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args
    unittest.main(verbosity=2)
