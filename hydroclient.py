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

    def no_test_A_000002(self):
        """ Confirms metadata available through
        HydroClient and that a sample of the data
        downloads successfully
        """
        def oracle():
            """ The Lake Annie FL data can be successfully
            sent to the workspace, and then is processed
            successfully in the workspace
            """
            self.assertEqual(Workspace.completed_count(driver), 1)

        Search.location_search(driver, 'Lake Annie Highlands County')
        ServiceSearch.filter_services(driver, organizations='Archbold Biological Station')
        FilterResults.any_to_workspace(driver)
        oracle()

    def no_test_A_000003(self):
        """ Confirms repeated search for Lake Annie data does not result
        in problematic behavior
        """
        def oracle():
            """ 51 results show up for the Lake Annie FL data search,
            with the "Archbold Biological Center" set as the only
            service visible via search filtering
            """
            self.assertIn('51', Search.results_count(driver))
        Search.location_search(driver, 'Lake Annie Highlands County')
        ServiceSearch.filter_services(driver, organizations='Archbold Biological Station')
        Search.search(driver, 60)
        oracle()

    def no_test_A_000004(self):
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

    def no_test_A_000005(self):
        """ Confirms New Haven CT Site X416-Y130 metadata and data are
        available for NASA Goddard Earth Sciences services
        """
        def oracle():
            """ Export to workspace is successful
            """
            self.assertEqual(Workspace.completed_count(driver), 2)
        Search.location_search(driver, 'New Haven ')
        ServiceSearch.filter_services(driver, titles=['NLDAS Hourly NOAH Data','NLDAS Hourly Primary Forcing Data'])
        FilterResults.search_filter_table(driver, 'X416-Y130')
        FilterResults.model_sim_and_derived_value_to_workspace(driver)
        oracle()

    def no_test_A_000006(self):
        """ Confirms Prague data is online for a site near Köln
        Germany
        """
        def oracle():
            """ Export to workspace is successful """
            self.assertEqual(Workspace.completed_count(driver), 4)
        Search.location_search(driver, 'Köln ')
        Search.search(driver)
        Search.map_icon_open(driver, '4')
        MapMarker.all_to_workspace(driver)
        oracle()

    def no_test_A_000007(self):
        """ Confirms visibility of the legend when the USGS Landcover
        layer is turned on within the search interface
        """
        def oracle():
            """ Legend is visible when Landcover layer on
            and not visible when the layer is off
            """
            self.assertTrue(Search.legend_visible(driver))
            Search.layer_toggle_landcover(driver)
            self.assertFalse(Search.legend_visible(driver))
        Search.location_search(driver, 'Anchorage ')
        Search.layer_toggle_landcover(driver)
        oracle()
        
    def test_A_000008(self):
        """ Confirms consistency of layer naming among the HydroClient
        and the associated documentation
        """
        def oracle_1():
            """ Layer naming in the Quick Start matches the 
            naming within the HydroClient search interface
            """
            for layer in layers:
                self.assertIn('<li>' + layer + '</li>', QuickStart.full_page(driver))
        def oracle_2():
            """ Layer naming in the help documentation page matches the 
            naming within the HydroClient search interface
            """
            for layer in layers:
                self.assertIn('<h2>' + layer + '</h2>', External.full_page(driver))
                
        layers = ['USGS Stream Gages', 'Nationalmap Hydrology',
                  'EPA Watersheds', 'USGS LandCover 2011']
        for layer in layers: # Turn all on
            Search.layer_toggle(driver, layer)
        for layer in layers: # Turn all off
            Search.layer_toggle(driver, layer)
        Search.quick_start(driver)
        QuickStart.help_expand(driver, 'Using the Layer Control')
        oracle_1()
        QuickStart.help_more(driver, 'Click for more information on the Layer Control')
        External.switch_new_page(driver)
        oracle_2()
        
        
                
        

        
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
