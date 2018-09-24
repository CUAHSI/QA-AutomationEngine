""" Runs various smoke tests for the data.cuahsi.org """
from hc_macros import Search, Marker, Services, Keywords, Advanced, \
    Filter, About, QuickStart, Zendesk, Workspace
from hc_elements import ZendeskArticlePage

from cuahsi_base.utils import External, TestSystem
from cuahsi_base.cuahsi_base import BaseTest, parse_args_run_tests

# Test case parameters
BASE_URL = 'https://data.cuahsi.org'  # production


# Test cases definition
class HydroclientTestSuite(BaseTest):
    """ Test suite for the HydroClient software system """

    def setUp(self):
        super(HydroclientTestSuite, self).setUp()
        self.driver.maximize_window()
        self.driver.get(BASE_URL)

    def test_A_000002(self):
        """ Confirms Archbold service metadata is available through
        HydroClient and that a sample of the data downloads successfully
        """
        def oracle():
            """ The Lake Annie Florida data can be successfully sent to the
            workspace, and then is processed successfully in the
            workspace ("completed" status)
            """
            self.assertEqual(Workspace.count_complete(self.driver), 1)

        Search.search_location(self.driver, 'Lake Annie Highlands County')
        Services.filters(self.driver, orgs='Archbold Biological Station')
        Filter.open(self.driver)
        Filter.to_workspace_cell(self.driver, 1, 1)
        oracle()

    def test_A_000003(self):
        """ Confirms repeated search for Lake Annie data does not result
        in problematic behavior
        """
        def oracle():
            """ 51 results are returned for a Lake Annie Florida data search,
            when the search is filtered to only include "Archbold Biological
            Center" service
            """
            self.assertEqual(51, Search.count_results(self.driver))

        Search.search_location(self.driver, 'Lake Annie Highlands County')
        Services.filters(self.driver, orgs='Archbold Biological Station')
        Search.search(self.driver, 60)
        oracle()

    def test_A_000004(self):
        """ Confirms the start and end date in a NWIS Unit Values
        data search are applied throughout search and workspace export
        workflow
        """
        def oracle():
            """ Start date and end date in workspace match the initial
            date filtering values established in the Search interface
            """
            self.assertTrue(Workspace.is_in_results(self.driver,
                                                    ['2015-12-01', '2015-12-30'],
                                                    10))

        Search.search_location(self.driver, 'Tampa ')
        Services.filters(self.driver, titles='NWIS Unit Values')
        Search.filter_dates(self.driver, '12/01/2015', '12/30/2015')
        Filter.open(self.driver)
        Filter.to_workspace_text(self.driver, 'Derived Value')
        oracle()

    def test_A_000005(self):
        """ Confirms metadata and data availability for the NASA Goddard
        Earth Sciences services, using the New Haven CT Site X416-Y130.
        The two associated services are NLDAS Hourly NOAH Data and NLDAS
        Hourly Primary Forcing Data
        """
        def oracle():
            """ The time series are sent to the workspace and processed,
            resulting in a "completed" status for all time series
            """
            self.assertEqual(Workspace.count_complete(self.driver, 6), 3)

        Search.search_location(self.driver, 'New Haven ')
        Services.filters(self.driver, titles=['NLDAS Hourly NOAH Data',
                                              'NLDAS Hourly Primary Forcing Data'])

        Filter.open(self.driver)
        Filter.search_field(self.driver, 'X416-Y130')
        Filter.to_workspace_cell_multi(self.driver, [1, 5, 9])  # rows 1, 5, 9
        oracle()

    def test_A_000006(self):
        """ Confirms metadata availability and the capability to download data
        near Köln Germany
        """
        def oracle():
            """ Results are exported to workspace and number of successfully
            processed time series is above 0
            """
            self.assertNotEqual(Workspace.count_complete(self.driver), 0)

        Search.search_location(self.driver, 'Köln ')
        Search.search(self.driver)
        Search.to_random_map_marker(self.driver, 24)
        Marker.to_workspace_one(self.driver)
        oracle()

    def test_A_000008(self):
        """ Confirms that map layer naming, as defined in the HydroClient
        user interface, is consistent with the Quick Start and help pages
        documentation
        """
        def oracle_1():
            """ Map layer naming in the Quick Start modal matches the
            naming within the HydroClient map search interface
            """
            for layer in layers:
                self.assertIn('<li>{}</li>'.format(layer),
                              TestSystem.page_source(driver))

        def oracle_2():
            """ Map layer naming in the help documentation page matches the
            naming within the HydroClient search interface
            """
            for layer in layers:
                self.assertIn(layer, TestSystem.page_source(driver))

        driver = self.driver
        layers = ['USGS Stream Gages', 'Nationalmap Hydrology', 'EPA Watersheds']
        for layer in layers:  # Turn all layer on
            Search.toggle_layer(driver, layer)
        for layer in layers:  # Turn all layers off
            Search.toggle_layer(driver, layer)
        Search.to_quickstart(driver)
        QuickStart.section(driver, 'Using the Layer Control')
        oracle_1()
        num_windows_opened = len(driver.window_handles)
        QuickStart.more(driver, 'Click for more information on the Layer Control')
        External.switch_new_page(driver, num_windows_opened,
                                 ZendeskArticlePage.article_header_locator)
        oracle_2()

    def test_A_000009(self):
        """ Confirms that additional help on layer control can be
        accessed using the Zendesk widget
        """
        def oracle():
            """ A valid help center page is opened from the Zendesk
            widget, and the page contains the word "Layers"
            """
            self.assertIn('Help Center', TestSystem.title(driver))
            self.assertIn('Layer', TestSystem.title(driver))

        driver = self.driver
        Search.search_location(driver, 'San Diego')
        Search.search_location(driver, 'Amsterdam')
        num_windows_opened = len(driver.window_handles)
        Zendesk.to_help(driver, 'Layers', 'Using the Layer Control')
        External.switch_new_page(driver, num_windows_opened,
                                 ZendeskArticlePage.article_header_locator)
        oracle()

    def test_A_000010(self):
        """ Confirms that filtering by all keywords and all data types
        returns the same number of results as if no search parameters
        were applied.  This test is applied near both the Dallas Texas
        and Rio De Janeiro Brazil areas
        """
        def oracle():
            """ A search which filters for all keywords and all data types
            returns the same number of results as a search without any
            filters
            """
            for rio_count in rio_counts:
                self.assertEqual(rio_count, rio_counts[0])
            for dallas_count in dallas_counts:
                self.assertEqual(dallas_count, dallas_counts[0])

        driver = self.driver
        rio_counts = []
        dallas_counts = []
        Search.search_location(driver, 'Rio De Janeiro')
        Keywords.filter_root(driver, ['Biological', 'Chemical', 'Physical'])
        rio_counts.append(Search.count_results(driver))
        Advanced.filter_all_value_types(driver)
        rio_counts.append(Search.count_results(driver))
        Search.reset(driver)
        Search.search(self.driver)
        rio_counts.append(Search.count_results(driver))
        Search.search_location(driver, 'Dallas')
        Keywords.filter_root(driver, ['Biological', 'Chemical', 'Physical'])
        dallas_counts.append(Search.count_results(driver))
        Advanced.filter_all_value_types(driver)
        dallas_counts.append(Search.count_results(driver))
        Search.reset(driver)
        Search.search(self.driver)
        dallas_counts.append(Search.count_results(driver))
        oracle()

    def test_A_000011(self):
        """ Confirms "About" modal dropdown links successfully open up
        the associated resource in a new tab and do not show a 404 Error
        """
        def oracle():
            """ None of the resource pages contain the text "404 Error" """
            self.assertNotIn('404 Error', external_sources,
                             msg='"{}" page was not found.'.format(page))

        driver = self.driver

        page = 'Help Center'
        for to_helpcenter_link in [About.to_helpcenter, About.to_contact]:
            to_helpcenter_link(driver)
            external_sources = External.source_new_page(driver)
            External.close_new_page(driver)
            oracle()
        About.contact_close(driver)

        page = 'CUAHSI GitHub repository'
        # opens in new window
        About.to_license_repo_top(driver)
        external_sources = External.source_new_page(driver)
        External.close_new_page(driver)
        oracle()
        About.licensing_close(driver)
        # opens in the same window
        About.to_license_repo_inline(driver)
        external_sources = External.source_new_page(driver)
        # TODO Brian fix of _blank target inconsistency in the works
        # External.close_new_page(driver)
        oracle()

    def test_A_000012(self):
        """ Confirms repeated map scrolls, followed by a location search,
        returns nonzero results for an area which normally has nonzero
        search results.  Effectively, this test confirms that viewing
        duplicate map instances to the left and right of the main (starting)
        map instance does not cause problems during location searching.
        """
        def oracle():
            """ Results count is nonzero after map navigations and a map
            location search (in that order)
            """
            self.assertNotEqual(Search.count_results(self.driver), 0)

        Search.scroll_map(self.driver, 25)
        Search.search_location(self.driver, 'Raleigh')
        Search.search(self.driver)
        oracle()

    def test_A_000013(self):
        """ Confirms operations within the Workspace user interface
        do not result in errors when the workspace is empty
        """
        def oracle():
            """ The browser is still on using the HydroClient system
            after Workspace operations are used on an empty Workspace
            """
            self.assertIn('HydroClient', TestSystem.title(driver))

        driver = self.driver
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
        """ Confirms NLDAS data is not available over the ocean (from
        either of the two services) """
        def oracle():
            """ The results count over Cape Cod Bay (no land in view)
            is 0 after filtering for only NLDAS services
            """
            self.assertEqual(Search.count_results(self.driver), 0)

        Search.search_location(self.driver, 'Cape Cod Bay')
        Search.zoom_in(self.driver, 3)
        Services.filters(self.driver, titles=['NLDAS Hourly NOAH Data',
                                              'NLDAS Hourly Primary Forcing Data'])
        oracle()

    def test_A_000015(self):
        """ Confirms no date filters returns the same number of results as
        applying a date filter from 01/01/0100 to 01/01/9000 """
        def oracle(init_count, final_count):
            self.assertEqual(init_count, final_count)
        Search.search_location(self.driver, 'United States')
        Search.search(self.driver)
        Search.filter_dates(self.driver, '01/01/0100', '01/01/9000')
        init_count = Search.count_results(self.driver)
        Search.clear_date_filter(self.driver)
        Search.search(self.driver)
        final_count = Search.count_results(self.driver)
        oracle(init_count, final_count)

    def test_A_000016(self):
        """ Austin, TX search successfully pulls metadata, which is then viewable
        within the Filter Results dialog.
        """
        def oracle(result_nums):
            """ Results count is between 1k and 10k, as seen from Filter Results
            dialog reporting
            """
            self.assertEqual(result_nums[0], 1)  # first results page is active
            self.assertEqual(result_nums[1], 10)  # 10 results on first page
            self.assertTrue(1000 < result_nums[2] and result_nums[2] < 10000)

        Search.search_location(self.driver, 'Austin, TX')
        Search.search(self.driver)
        Filter.open(self.driver)
        TestSystem.wait(10)
        result_nums = Filter.count_results(self.driver)
        result_nums = [int(result_num) for result_num in result_nums]
        oracle(result_nums)

    def test_A_000017(self):
        """ Confirm Reset button clears Filter Results text and categorical filters """
        def oracle_results_count(expected_results, should_match):
            if should_match:
                self.assertEqual(Search.count_results(self.driver), expected_results)
            else:
                self.assertNotEqual(Search.count_results(self.driver), expected_results)
        def oracle_data_prop_selection(data_props, should_be_selected):
            """ Checks that filter options not selected """
            for data_prop in data_props:
                if should_be_selected:
                    self.assertTrue(Filter.data_prop_is_selected(self.driver, data_prop))
                else:
                    self.assertFalse(Filter.data_prop_is_selected(self.driver, data_prop))

        def oracle_data_service_selection(data_services, should_be_selected):
            """ Checks that filter options not selected """
            for data_service in data_services:
                if should_be_selected:
                    self.assertTrue(Filter.data_service_is_selected(self.driver, data_service))
                else:
                    self.assertFalse(Filter.data_service_is_selected(self.driver, data_service))

        data_props = ['Data Type', 'Sample Medium']
        data_services = ['National Oceanic and Atmospheric Administration (NOAA)',
                         'Community Collaborative Rain, Hail and Snow Network']
        Search.search_location(self.driver, 'Montreal ')
        Search.search(self.driver)
        expected_results = Search.count_results(self.driver)
        Filter.open(self.driver)
        Filter.selection(self.driver)
        Filter.close(self.driver)
        TestSystem.wait(5)
        Search.reset(self.driver)
        Search.search(self.driver)
        oracle_results_count(expected_results, should_match=True)
        Filter.open(self.driver)
        Filter.find_in_table(self.driver, 'DOLLARD')
        oracle_results_count(expected_results, should_match=False)
        Search.reset(self.driver)
        Search.search(self.driver)
        oracle_results_count(expected_results, should_match=True)
        Filter.open(self.driver)
        Filter.set_data_props(self.driver, data_props)
        Filter.open(self.driver)
        Filter.set_data_services(self.driver, data_services)
        oracle_results_count(expected_results, should_match=False)
        Filter.open(self.driver)
        oracle_data_prop_selection(data_props, should_be_selected=True)
        oracle_data_service_selection(data_services, should_be_selected=True)
        Filter.close(self.driver)
        Search.reset(self.driver)
        Search.search(self.driver)
        oracle_results_count(expected_results, should_match=True)
        Filter.open(self.driver)
        oracle_data_prop_selection(data_props, should_be_selected=False)
        oracle_data_service_selection(data_services, should_be_selected=False)

    def test_A_000019(self):
        """ Confirm empty operations on the filter modals don't affect the
        results set or the persistance of the searchbox entry """
        def oracle_search_text_is_same(text):
            """ Check if the text is the same in the search field """
            self.assertEqual(Search.get_searchbox_text(self.driver), text)
        def oracle_result(init_result):
            """ Compare search results count to the initial level """
            self.assertEqual(init_result, Search.count_results(self.driver))

        location = 'NUIO üł. 54343nt, 342sf 234sdf, 12...'  # deliberately random
        Search.search_location(self.driver, location)
        Search.search(self.driver)
        init_result_count = Search.count_results(self.driver)
        Services.filters(self.driver)  # apply no services filters
        Keywords.empty_keywords(self.driver)  # no keyword filters
        Advanced.empty_advanced(self.driver)  # no advanced filters
        Search.search(self.driver)
        oracle_result(init_result_count)
        oracle_search_text_is_same(location)
        Search.reset(self.driver)
        Search.search(self.driver)
        oracle_result(init_result_count)
        oracle_search_text_is_same(location)


if __name__ == '__main__':
    parse_args_run_tests(HydroclientTestSuite)
