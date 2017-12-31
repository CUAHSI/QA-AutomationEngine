""" Runs various smoke tests for the data.cuahsi.org """
import unittest
import argparse
import sys
import time
from hc_macros import *
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

# Test case parameters
BASE_URL = 'http://data.cuahsi.org'

# Test cases definition
class HydroclientTestCase(unittest.TestCase):
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
        time.sleep(5)
        driver.implicitly_wait(10)

    def tearDown(self):
        """ Tear down test environment after execution """
        driver.quit()

    def test_A_000002(self):
        """ Confirms metadata available through
        HydroClient and that a sample of the data
        downloads successfully
        """
        def oracle():
            """ The Lake Annie FL data can be successfully
            sent to the workspace, and then is processed
            successfully in the workspace
            """
            self.assertTrue(Workspace.completed_count(driver) == 1)

        Search.location_search(driver, 'Lake Annie Highlands County')
        ServiceSearch.filter_services(driver, organizations='Archbold Biological Station')
        FilterResults.any_to_workspace(driver)
        oracle()

    def test_A_000003(self):
        """ Confirms repeated search for Lake Annie data does not result
        in problematic behavior
        """
        def oracle():
            """ 51 results show up for the Lake Annie FL data search,
            with the "Archbold Biological Center" set as the only
            service visible via search filtering
            """
            self.assertTrue('51' in Search.results_count(driver))
        Search.location_search(driver, 'Lake Annie Highlands County')
        ServiceSearch.filter_services(driver, organizations='Archbold Biological Station')
        for i in range(0, 60):
            SearchPage.search_now.click(driver, SLEEP_TIME)
            time.sleep(1)
        oracle()

    def test_A_000004(self):
        """ Confirms date filtering of NWIS UV data service is maintained
        throughout search and workspace export workflow
        """
        def oracle():
            """ Start date and end date in workspace match the initial
            date filtering values established in the Search interface
            """
            self.assertTrue(Workspace.in_results(driver,['2015-12-01','2015-12-30']))
        Search.location_search(driver, 'Tampa ')
        ServiceSearch.filter_services(driver, titles='NWIS Unit Values')
        Search.date_filter(driver, '12/01/2015', '12/30/2015')
        FilterResults.derived_value_to_workspace(driver)
        oracle()

    def test_A_000005(self):
        """ Confirms New Haven CT Site X416-Y130 metadata and data are
        available for NASA Goddard Earth Sciences services
        """
        def oracle():
            """ Export to workspace is successfull
            """
            self.assertTrue(Workspace.completed_count(driver) == 2)
        Search.location_search(driver, 'New Haven ')
        ServiceSearch.filter_services(driver, titles=['NLDAS Hourly NOAH Data','NLDAS Hourly Primary Forcing Data'])
        FilterResults.search_filter_table(driver, 'X416-Y130')
        FilterResults.model_sim_and_derived_value_to_workspace(driver)
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
