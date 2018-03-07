""" Runs various smoke tests for the data.cuahsi.org """
import argparse
import sys
import time
import unittest

from selenium import webdriver

from hc_macros import Search, Marker, Services, Keywords, Advanced, \
    Filter, About, QuickStart, Zendesk, Workspace
from utils import External, TestSystem

# Test case parameters
BASE_URL = 'http://data.cuahsi.org'


# Test cases definition
class HydroclientTestSuite(unittest.TestCase):
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
        driver.maximize_window()
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
            self.assertEqual(Workspace.count_complete(driver, 50), 1)

        Search.search_location(driver, 'Lake Annie Highlands County')
        Services.filters(driver, orgs='Archbold Biological Station')
        Filter.to_workspace_cell(driver, 1, 1)
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
            self.assertIn('51', Search.count_results(driver))

        Search.search_location(driver, 'Lake Annie Highlands County')
        Services.filters(driver, orgs='Archbold Biological Station')
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
            self.assertTrue(Workspace.is_in_results(driver,
                                                    ['2015-12-01',
                                                     '2015-12-30'],
                                                    10))

        Search.search_location(driver, 'Tampa ')
        Services.filters(driver, titles='NWIS Unit Values')
        Search.filter_dates(driver, '12/01/2015', '12/30/2015')
        Filter.to_workspace_text(driver, 'Derived Value')
        oracle()

    def test_A_000005(self):
        """ Confirms New Haven CT Site X416-Y130 metadata and data are
        available for NASA Goddard Earth Sciences services
        """
        def oracle():
            """ Export to workspace is successful """
            self.assertEqual(Workspace.count_complete(driver, 50), 2)
        Search.search_location(driver, 'New Haven ')
        Services.filters(driver, titles=['NLDAS Hourly NOAH Data',
                                         'NLDAS Hourly ' +
                                         'Primary Forcing Data'])

        Filter.search_field(driver, 'X416-Y130')
        Filter.to_workspace_texts_range(driver, ['Model Simulation Result',
                                                 'Derived Value'])
        oracle()

    def test_A_000006(self):
        """ Confirms Prague data is online for a site near Köln
        Germany
        """
        def oracle():
            """ Export to workspace is successful """
            self.assertEqual(Workspace.count_complete(driver), 4)

        Search.search_location(driver, 'Köln ')
        Search.search(driver)
        Search.to_map_marker(driver, '4')
        Marker.to_workspace_all(driver)
        oracle()

    def test_A_000007(self):
        """ Confirms visibility of the legend when the USGS Landcover
        layer is turned on within the search interface
        """
        def oracle():
            """ Legend is visible when Landcover layer on
            and not visible when the layer is off
            """
            self.assertTrue(Search.is_legend_visible(driver))
            Search.toggle_layer(driver, 'USGS LandCover 2011')
            self.assertFalse(Search.is_legend_visible(driver))

        Search.search_location(driver, 'Anchorage ')
        Search.toggle_layer(driver, 'USGS LandCover 2011')
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
                self.assertIn('<li>' + layer + '</li>',
                              TestSystem.page_source(driver))

        def oracle_2():
            """ Layer naming in the help documentation page matches the
            naming within the HydroClient search interface
            """
            for layer in layers:
                self.assertIn(layer, TestSystem.page_source(driver))

        layers = ['USGS Stream Gages', 'Nationalmap Hydrology',
                  'EPA Watersheds', 'USGS LandCover 2011']
        for layer in layers:  # Turn all on
            Search.toggle_layer(driver, layer)
        for layer in layers:  # Turn all off
            Search.toggle_layer(driver, layer)
        Search.to_quickstart(driver)
        QuickStart.section(driver, 'Using the Layer Control')
        oracle_1()
        QuickStart.more(driver, 'Click for more information ' +
                        'on the Layer Control')
        External.switch_new_page(driver)
        oracle_2()

    def test_A_000009(self):
        """ Layers help documentation available through ZenDesk help
        overlay button/widget
        """
        def oracle():
            """ Test center results load without error """
            self.assertIn('Help Center', TestSystem.title(driver))

        Search.search_location(driver, 'San Diego')
        Search.search_location(driver, 'Amsterdam')
        Zendesk.to_help(driver, 'Layers', 'Using the Layer Control')
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
            self.assertTrue(all(x == rio_counts[0]
                                for x in rio_counts))
            self.assertTrue(all(x == dallas_counts[0]
                                for x in dallas_counts))

        rio_counts = []
        dallas_counts = []
        Search.search_location(driver, 'Rio De Janeiro')
        rio_counts.append(Search.count_results(driver))
        Keywords.filter_root(driver, ['Biological', 'Chemical', 'Physical'])
        rio_counts.append(Search.count_results(driver))
        Advanced.filter_all_value_types(driver)
        rio_counts.append(Search.count_results(driver))
        Search.reset(driver)
        Search.search_location(driver, 'Dallas')
        dallas_counts.append(Search.count_results(driver))
        Keywords.filter_root(driver, ['Biological', 'Chemical', 'Physical'])
        dallas_counts.append(Search.count_results(driver))
        TestSystem.wait(3)  # sec
        Advanced.filter_all_value_types(driver)
        TestSystem.wait(3)  # sec
        dallas_counts.append(Search.count_results(driver))
        oracle()

    def test_A_000011(self):
        """ Confirms About dropdown links successfully open up the
        associated resource in new tab and do not show a 404 Error
        """
        def oracle():
            """ No 404 Errors exist in external page sources """
            self.assertNotIn('404 Error', external_sources)

        external_sources = ''
        About.to_helpcenter(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        About.to_license_repo_top(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        About.to_contact(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        About.to_license_repo_inline(driver)
        external_sources += External.source_new_page(driver)
        External.close_new_page(driver)
        oracle()

    def test_A_000012(self):
        """ Confirms repeated map scrolls do not cause issues in
        subsequent map searches
        """
        def oracle():
            """ Results count is nonzero after map navigations """
            self.assertNotEqual(Search.count_results(driver), '0')

        Search.scroll_map(driver, 25)
        Search.search_location(driver, 'Raleigh')
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

        Search.to_workspace(driver)
        Workspace.select_all(driver)
        Workspace.clear_select(driver)
        Workspace.remove_select(driver)
        Workspace.clear_select(driver)
        Workspace.select_all(driver)
        Workspace.remove_select(driver)
        Workspace.to_csv(driver)
        Workspace.to_viewer(driver)
        Workspace.to_none(driver)
        Workspace.to_viewer(driver)
        Workspace.to_csv(driver)
        oracle()

    def test_A_000014(self):
        """ Check NLDAS service over ocean to ensure sites don't exist """
        def oracle():
            """ The results count over Cape Cod Bay (no land in view)
            is 0 after filtering for only NLDAS services
            """
            self.assertEqual(Search.count_results(driver), '0')

        Search.search_location(driver, 'Cape Cod Bay')
        Search.zoom_in(driver, 3)
        Services.filters(driver,
                         titles=['NLDAS Hourly NOAH Data',
                                 'NLDAS Hourly ' +
                                 'Primary Forcing Data'])
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
