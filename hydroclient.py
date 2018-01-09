""" Runs various smoke tests for the data.cuahsi.org """
import unittest
import argparse
import sys
import time
from hc_macros import *
from utils import *
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
            self.assertEqual(Workspace.completed_count(driver), 1)

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
            self.assertIn('51', Search.results_count(driver))
        Search.location_search(driver, 'Lake Annie Highlands County')
        ServiceSearch.filter_services(driver, organizations='Archbold Biological Station')
        Search.search(driver, 60)
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
            """ Export to workspace is successful
            """
            self.assertEqual(Workspace.completed_count(driver), 2)
        Search.location_search(driver, 'New Haven ')
        ServiceSearch.filter_services(driver, titles=['NLDAS Hourly NOAH Data','NLDAS Hourly Primary Forcing Data'])
        FilterResults.search_filter_table(driver, 'X416-Y130')
        FilterResults.model_sim_and_derived_value_to_workspace(driver)
        oracle()

    def test_A_000006(self):
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

    def test_A_000007(self):
        """ Confirms visibility of the legend when the USGS Landcover
        layer is turned on within the search interface
        """
        def oracle():
            """ Legend is visible when Landcover layer on
            and not visible when the layer is off
            """
            self.assertTrue(Search.legend_visible(driver))
            Search.layer_toggle(driver, 'USGS LandCover 2011')
            self.assertFalse(Search.legend_visible(driver))
        Search.location_search(driver, 'Anchorage ')
        Search.layer_toggle(driver, 'USGS LandCover 2011')
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
                self.assertIn('<li>' + layer + '</li>', TestSystem.page_source(driver))
        def oracle_2():
            """ Layer naming in the help documentation page matches the 
            naming within the HydroClient search interface
            """
            for layer in layers:
                self.assertIn('<h2>' + layer + '</h2>', TestSystem.page_source(driver))
                
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
        
    def test_A_000009(self):
        """ Layers help documentation available through ZenDesk help
        overlay button/widget
        """
        def oracle():
            """ Test center results load without error """
            self.assertIn('Help Center', TestSystem.title(driver))

        Search.location_search(driver, 'San Diego')
        Search.location_search(driver, 'Amsterdam')
        Search.zendesk_help(driver, 'Layers', 'Using the Layer Control')
        External.switch_new_page(driver)
        oracle()

    def test_A_000010(self):
        """ Confirms that filtering by all keywords and all data types
        returns the same number of results as if no search parameters
        were applied
        """
        def oracle():
            """ Searches return same number of results as initial search
            without parameters
            """
            self.assertTrue(all(x == rio_counts[0] for x in rio_counts))
            self.assertTrue(all(x == dallas_counts[0] for x in dallas_counts))
        rio_counts = []
        dallas_counts = []
        Search.location_search(driver, 'Rio De Janeiro')
        rio_counts.append(Search.results_count(driver))
        KeywordSearch.root_keywords(driver, ['Biological', 'Chemical', 'Physical'])
        rio_counts.append(Search.results_count(driver))
        AdvancedSearch.all_value_type(driver)
        rio_counts.append(Search.results_count(driver))
        Search.reset_params(driver)
        
        Search.location_search(driver, 'Dallas')
        dallas_counts.append(Search.results_count(driver))
        KeywordSearch.root_keywords(driver, ['Biological', 'Chemical', 'Physical'])
        dallas_counts.append(Search.results_count(driver))
        TestSystem.wait(3) #sec
        AdvancedSearch.all_value_type(driver)
        TestSystem.wait(3) #sec
        dallas_counts.append(Search.results_count(driver))

    def test_A_000011(self):
        """ Confirms About dropdown links successfully open up the
        associated resource in new tab and do not show a 404 Error
        """
        def oracle():
            """ No 404 Errors exist in external page sources """
            self.assertNotIn('404 Error', external_sources)
        external_sources = ''
        Search.about_helpcenter(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        Search.about_license_repo_top(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        Search.about_contact(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        Search.about_license_repo_inline(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        oracle()

    def test_A_000012(self):
        """ Confirms repeated map scrolls do not cause issues in
        subsequent map searches
        """
        def oracle():
            """ Results count is nonzero after map navigations """
            self.assertNotEqual(Search.results_count(driver), '0')
        Search.map_scroll(driver, 25)
        Search.location_search(driver, 'Raleigh')
        Search.search(driver)
        oracle()

    def test_A_000013(self):
        """ Confirms operations and button clicks on an empty workspace
        do not result in errors
        """
        def oracle():
            """ Page has not been redirected and no fatal errors have
            been raised
            """
            self.assertIn('HydroClient', TestSystem.title(driver))
        Workspace.goto_from_search(driver)
        Workspace.select_all(driver)
        Workspace.clear_selected(driver)
        Workspace.remove_selected(driver)
        Workspace.clear_selected(driver)
        Workspace.select_all(driver)
        Workspace.remove_selected(driver)
        Workspace.export_csv(driver)
        Workspace.export_data_viewer(driver)
        Workspace.export_none(driver)
        Workspace.export_data_viewer(driver)
        Workspace.export_csv(driver)
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
