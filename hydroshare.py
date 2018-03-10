""" Runs various smoke tests for the hydroshare.org """
import argparse
import sys
import unittest

from selenium import webdriver
from hs_macros import Home, Discover, Resource

# Test case parameters
BASE_URL = "http://www.hydroshare.org"


# Test cases definition
class HydroshareTestSuite(unittest.TestCase):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        """ Setup driver for use in automation tests """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override",
                               "CUAHSI-QA-Selenium")
        # TODO use self.driver instead of making it global
        global driver
        if infrastructure == 'grid':
            driver = \
                webdriver.Remote(command_executor='http://' +
                                 grid_hub_ip + ':4444/wd/hub',
                                 desired_capabilities=(
                                     {'browserName': 'firefox'}))
        else:
            driver = webdriver.Firefox(profile)
        driver.get(BASE_URL)
        driver.implicitly_wait(10)

    def tearDown(self):
        """ Tear down test environment after execution """
        driver.quit()

    def test_B_000003(self):
        """ Confirms Beaver Divide Air Temperature resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive and confirms the BagIt file size matches expectation
        """
        def oracle():
            """ The Beaver Divide BagIt zip file matches expected file
            size (in Bytes)
            """
            self.assertEqual(Resource.size_download(driver, BASE_URL),
                             512000)
        Discover.filters(driver, subject='iUTAH', resource_type='Generic',
                         availability=['discoverable', 'public'])
        Discover.to_resource(driver, 'Beaver Divide Air Temperature')
        oracle()

    def test_B_000006(self):
        """ Confirms the sorting behavior on the Discover page (both sort
        direction and sort field) functions correctly, as evaluated by a few
        of the first rows being ordered correctly
        """
        def oracle(driver, column_name, ascend_or_descend):
            """ Sorting is correctly implemented, as measured by a sample
            of row comparisons (not exhaustive)
            """
            self.assertTrue(Discover.check_sorting_multi(driver,
                                                         column_name,
                                                         ascend_or_descend))
        Home.to_discover(driver)
        Discover.sort_direction(driver, 'Ascending')
        Discover.sort_order(driver, 'Last Modified')
        oracle(driver, 'Last Modified', 'Ascending')
        Discover.sort_order(driver, 'Title')
        oracle(driver, 'Title', 'Ascending')
        Discover.sort_order(driver, 'First Author')
        oracle(driver, 'First Author', 'Ascending')
        Discover.sort_order(driver, 'Date Created')
        oracle(driver, 'Date Created', 'Ascending')
        Discover.sort_direction(driver, 'Descending')
        Discover.sort_order(driver, 'Title')
        oracle(driver, 'Title', 'Descending')
        Discover.sort_order(driver, 'Date Created')
        oracle(driver, 'Date Created', 'Descending')
        Discover.sort_order(driver, 'Last Modified')
        oracle(driver, 'Last Modified', 'Descending')
        Discover.sort_order(driver, 'First Author')
        oracle(driver, 'First Author', 'Descending')
        Discover.sort_direction(driver, 'Ascending')
        Discover.sort_order(driver, 'Date Created')
        oracle(driver, 'Date Created', 'Ascending')
        Discover.sort_order(driver, 'Last Modified')
        oracle(driver, 'Last Modified', 'Ascending')
        Discover.sort_order(driver, 'First Author')
        oracle(driver, 'First Author', 'Ascending')
        Discover.sort_order(driver, 'Title')
        oracle(driver, 'Title', 'Ascending')


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
