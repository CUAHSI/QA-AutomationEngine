""" Runs various smoke tests for the data.cuahsi.org """
import unittest
import argparse
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from hydroclient_elements import *
from modes import setup_mode

# Test case parameters
MODE_SELECTION = 'demo'
SLEEP_TIME = setup_mode(MODE_SELECTION)
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
            workspace_load = True
            try:
                SiteElement('span', el_class='glyphicon-thumbs-up')
            except NoSuchElementException:
                workspace_load = False
            self.assertTrue(workspace_load)
        SearchPage.location_search.inject_text(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SearchPage.service_filter.click(driver, SLEEP_TIME)
        ServiceSearch.sort_organization.click(driver, SLEEP_TIME)
        ServiceSearch.archbold.click(driver, SLEEP_TIME)
        ServiceSearch.save.click(driver, SLEEP_TIME)
        SearchPage.search_now.click(driver, SLEEP_TIME)
        time.sleep(10)
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_TIME)
        FilterResults.nav_close.scroll_to(driver, SLEEP_TIME)
        FilterResults.select_any.click(driver, SLEEP_TIME)
        FilterResults.choose_action.click(driver, SLEEP_TIME)
        FilterResults.export_workspace.click(driver, SLEEP_TIME)
        FilterResults.nav_workspace.click(driver, SLEEP_TIME)
        time.sleep(60)
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
            self.assertTrue('51' in SearchPage.results_found.get_text(driver))
        SearchPage.location_search.inject_text(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SearchPage.service_filter.click(driver, SLEEP_TIME)
        ServiceSearch.sort_organization.click(driver, SLEEP_TIME)
        ServiceSearch.archbold.click(driver, SLEEP_TIME)
        ServiceSearch.save.click(driver, SLEEP_TIME)
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
            self.assertIn('2015-12-01', driver.page_source)
            self.assertIn('2015-12-30', driver.page_source)
        SearchPage.location_search.inject_text(driver, 'Tampa ', 2*SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SearchPage.service_filter.click(driver, SLEEP_TIME)
        ServiceSearch.table_count.select_option(driver, '100', SLEEP_TIME)
        ServiceSearch.nwis_uv.click(driver, SLEEP_TIME)
        ServiceSearch.save.click(driver, SLEEP_TIME)
        SearchPage.date_filter.click(driver, SLEEP_TIME)
        SearchPage.date_start.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_start.inject_text(driver, '12/01/2015', SLEEP_TIME)
        SearchPage.date_clickout.passive_click(driver, SLEEP_TIME)
        SearchPage.date_end.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_end.inject_text(driver, '12/30/2015', SLEEP_TIME)
        SearchPage.date_save.click(driver, SLEEP_TIME)
        SearchPage.search_now.click(driver, SLEEP_TIME)
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResults.select_derived_value.click(driver, SLEEP_TIME)
        FilterResults.choose_action.click(driver, SLEEP_TIME)
        FilterResults.export_workspace.click(driver, SLEEP_TIME)
        time.sleep(10*SLEEP_TIME)
        FilterResults.nav_workspace.click(driver, SLEEP_TIME)
        oracle()

    def test_A_000005(self):
        """ Confirms New Haven CT Site X416-Y130 metadata and data are
        available for NASA Goddard Earth Sciences services
        """
        def oracle():
            """ Export to workspace is successfull
            """
            self.assertTrue(driver.page_source.count('<em> Completed</em>') == 2)
        SearchPage.location_search.inject_text(driver, 'New Haven ', SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SearchPage.service_filter.click(driver, SLEEP_TIME)
        ServiceSearch.table_count.select_option(driver, '100', SLEEP_TIME)
        ServiceSearch.nasa_noah.click(driver, SLEEP_TIME)
        ServiceSearch.nasa_forcing.scroll_to(driver, SLEEP_TIME)
        ServiceSearch.nasa_forcing.multi_click(driver, SLEEP_TIME)
        ServiceSearch.search.click(driver, SLEEP_TIME)
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResults.search.inject_text(driver, 'X416-Y130', SLEEP_TIME)
        FilterResults.sort_service.click(driver, SLEEP_TIME)
        FilterResults.table_count.select_option(driver, '100', SLEEP_TIME)
        FilterResults.select_model_sim.click(driver, SLEEP_TIME)
        FilterResults.sort_service.click(driver, SLEEP_TIME)
        FilterResults.select_derived_value.scroll_to(driver, SLEEP_TIME)
        FilterResults.select_derived_value.multi_click(driver, SLEEP_TIME)
        FilterResults.choose_action.click(driver, SLEEP_TIME)
        FilterResults.export_workspace.click(driver, SLEEP_TIME)
        FilterResults.nav_workspace.click(driver, SLEEP_TIME)
        time.sleep(60*SLEEP_TIME)
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
