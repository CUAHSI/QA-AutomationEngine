""" Runs various smoke tests for the hydroshare.org """
import unittest
import os
import time
from selenium import webdriver
from site_element import SiteElement
from modes import setup_mode

# Test case parameters
MODE_SELECTION = 'demo'
setup_mode(MODE_SELECTION)
BASE_URL = 'http://www.hydroshare.org'

# All
DISCOVERY_TAB = SiteElement('li', the_id='dropdown-menu-search')
# Discover page
DISCOVER_START_DATE = SiteElement('input', the_id='id_start_date')
DISCOVER_END_DATE = SiteElement('input', the_id='id_end_date')
DISCOVER_VIEW_MAP_TAB = SiteElement('a', the_href='map-view')
DISCOVER_MAP_SEARCH = SiteElement('input', the_id='geocoder-address')
DISCOVER_MAP_SEARCH_SUBMIT = SiteElement('a', the_id='geocoder-submit')
DISCOVER_VIEW_LIST_TAB = SiteElement('a', the_content='List')
IUTAH_SUBJECTS_FILTER = SiteElement('input', the_id='subjects-iUTAH')
GENERIC_RESOURCE_TYPE_FILTER = SiteElement('input', the_id='resource_type-Generic')
IS_DISCOVERABLE_FILTER = SiteElement('input', the_id='discoverable-true')
IS_PUBLIC_FILTER = SiteElement('input', the_id='public-true')
BEAVER_DIVIDE_RESC = SiteElement('a', the_content='Beaver Divide Air Temperature')
# Resource landing page from Discover
DOWNLOAD_BAGIT = SiteElement('a', the_id='btn-download-all', the_content=\
                             'Download All Content as Zipped BagIt Archive')
BEAVER_DIVIDE_ZIP_SIZE = 512000

def setup_driver():
    """ Setup driver for use in automation tests """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "CUAHSI-QA-Selenium")
    driver = webdriver.Firefox(profile)
    return driver

# Test cases definition
class HydroshareTestCase(unittest.TestCase):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        """ Sets up browser for future tests """
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def todo_test_B_000001(self):
        """ Confirms homepage online via page title """
        def oracle():
            """ The Hydroshare homepage is online """
            self.assertIn('HydroShare', driver.title)

        driver = setup_driver()
        driver.get(BASE_URL)
        time.sleep(SLEEP_TIME)
        oracle()
        driver.quit()

    def todo_test_B_000002(self):
        """ Confirms discovery page is online via navigation
        and title check
        """
        def oracle():
            """ The discovery page can be navigated to
            from the HydroShare homepage, using the top
            menu tabs
            """
            self.assertIn('Discover', driver.title)

        driver = setup_driver()
        driver.get(BASE_URL)
        DISCOVERY_TAB.click_it(driver, SLEEP_TIME)
        oracle()
        driver.quit()

    def todo_test_B_000003(self):
        """ Confirms Beaver Divide Air Temperature resource
        landing page is online via navigation and title check,
        then downloads the BagIt archive and confirms
        """
        def oracle():
            """ The Beaver Divide BagIt zip file
            matches expected file size
            """
            self.assertTrue(file_size == BEAVER_DIVIDE_ZIP_SIZE)

        driver = setup_driver()
        driver.get(BASE_URL)
        # Pulls up discover search page through site header
        DISCOVERY_TAB.click_it(driver, SLEEP_TIME)
        # Filters by subject of iUTAH in left panel
        IUTAH_SUBJECTS_FILTER.click_it(driver, SLEEP_TIME)
        # Filters by resouce type of Generic in left panel
        GENERIC_RESOURCE_TYPE_FILTER.click_it(driver, SLEEP_TIME)
        # Filters by availability of Discoverable or Public
        IS_DISCOVERABLE_FILTER.click_it(driver, SLEEP_TIME)
        IS_PUBLIC_FILTER.click_it(driver, SLEEP_TIME)
        # Clicks specific resourse - Beaver Divide Air Temperaure
        BEAVER_DIVIDE_RESC.click_it(driver, SLEEP_TIME)
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
        driver.quit()

    def test_B_000004(self):
        """ Confirms date filtering functionality, as well as
        map view functionality
        """
        driver = setup_driver()
        driver.get(BASE_URL)
        # Pulls up discover search page through site header
        DISCOVERY_TAB.click_it(driver, SLEEP_TIME)
        DISCOVER_START_DATE.text_into_it(driver, "01/01/2014", SLEEP_TIME)
        DISCOVER_END_DATE.text_into_it(driver, "12/31/2014", SLEEP_TIME)
        # TODO fix element identification issue
        DISCOVER_VIEW_MAP_TAB.click_it(driver, SLEEP_TIME)
        DISCOVER_MAP_SEARCH.text_into_it(driver, "Salt Lake City", SLEEP_TIME)
        DISCOVER_MAP_SEARCH_SUBMIT.click_it(driver, SLEEP_TIME)
        DISCOVER_VIEW_LIST_TAB.click_it(driver, SLEEP_TIME)
        time.sleep(5)
        driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
