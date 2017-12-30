""" Runs various smoke tests for the data.cuahsi.org """
import unittest
import argparse
import sys
import time
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.keys import Keys
from site_element import SiteElement
from modes import setup_mode

# Test case parameters
MODE_SELECTION = 'demo'
SLEEP_TIME = setup_mode(MODE_SELECTION)
BASE_URL = 'http://data.cuahsi.org'

# Search interface
SEARCH_NOW = SiteElement('button', el_id='btnSearchNow')
FILTER_RESULTS = SiteElement('button', el_id='btnSearchSummary')
LOCATION_SEARCH_BOX = SiteElement('input', el_id='pac-input')
SERVICE_SEARCH = SiteElement('button', el_id='btnSelectDataServices',
                             el_content='Data Service(s)...')
NUM_SEARCH_RESULTS = SiteElement('span', el_id='timeseriesFoundOrFilteredCount')
DATE_FILTER_ON = SiteElement('*', el_id='optionsDatesRange')
DATE_FILTER_START = SiteElement('*', el_id='startDateModal')
DATE_FILTER_END = SiteElement('*', el_id='endDateModal')
DATE_FILTER_CLICKOUT = SiteElement('h3',
                                   el_content='Please select your date range:')
DATE_FILTER_SAVE = SiteElement('*', el_id='btnDateRangeModalSave')
# Service search
SERVICE_ORGANIZATION_SORT = SiteElement('th', el_content='Organization')
SERVICE_SEARCH_SAVE = SiteElement('button', el_id='btnServicesModalSave')
SERVICE_SEARCH_SEARCH = SiteElement('button', el_id='btnServicesModalSearch')
SERVICE_TABLE_COUNT = SiteElement('select', el_name='tblDataServices_length')
SERVICE_ARCHBOLD_SEARCH = SiteElement('td',
                                      el_content='Archbold Biological Station')
SERVICE_NWIS_UV_SEARCH = SiteElement('a',
                                     el_content='NWIS Unit Values',
                                     recursive_loc=[SiteElement(el_dom='./../..'),
                                                    SiteElement(el_dom='./td[1]')])
SERVICE_NASA_NOAH = SiteElement('a',
                                el_content='NLDAS Hourly NOAH Data',
                                recursive_loc=[SiteElement(el_dom='./../..'),
                                               SiteElement(el_dom='./td[1]')])
SERVICE_NASA_PRIMARY_FORCING = SiteElement('a',
                                           el_content='NLDAS Hourly Primary Forcing Data',
                                           recursive_loc=[SiteElement(el_dom='./../..'),
                                                          SiteElement(el_dom='./td[1]')])

# Filter interface
SELECT_ACTION = SiteElement('div', el_id='ddActionsDSR')
FILTER_TABLE_COUNT = SiteElement('select', el_name='tblDetailedSearchResults_length')
WORKSPACE_SELECTION = SiteElement('a', el_id='anchorAddSelectionsToWorkspaceDSR')
VIEW_EXPORTS = SiteElement('button', el_id='tableModal-DownloadMgrSearchSummary')
VIEW_WORKSPACE = SiteElement('button', el_id='tableModal-DataMgrSearchSummary')
CLOSE_FILTER = SiteElement('button', el_id='closeSearchSummary')
FILTER_TABLE_SEARCH = SiteElement('div',
                                  el_id='tblDetailedSearchResults_filter',
                                  recursive_loc=[SiteElement(el_dom='./label'),
                                                 SiteElement(el_dom='./input')])
FILTER_TABLE = SiteElement('table',
                           el_id='tblDetailedSearchResults',
                           recursive_loc=[SiteElement(el_dom='./tbody'),
                                          SiteElement(el_dom='./tr'),
                                          SiteElement(el_dom='./td'),
                                          SiteElement(el_dom='./div')])
FILTER_DERIVED_VALUE_ROW = SiteElement('td', el_content='Derived Value')
FILTER_MODEL_SIM_RESULT_ROW = SiteElement('td', el_content='Model Simulation Result')
FILTER_BY_SERVICE = SiteElement('div',
                                el_id='tblDetailedSearchResults_wrapper',
                                recursive_loc=[SiteElement('th', el_content='Service Title')])

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
        LOCATION_SEARCH_BOX.inject_text(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_ORGANIZATION_SORT.click(driver, SLEEP_TIME)
        SERVICE_ARCHBOLD_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click(driver, SLEEP_TIME)
        SEARCH_NOW.click(driver, SLEEP_TIME)
        time.sleep(10)
        FILTER_RESULTS.click(driver, SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_TIME)
        CLOSE_FILTER.scroll_to(driver, SLEEP_TIME)
        FILTER_TABLE.click(driver, SLEEP_TIME)
        SELECT_ACTION.click(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click(driver, SLEEP_TIME)
        VIEW_WORKSPACE.click(driver, SLEEP_TIME)
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
            self.assertTrue('51' in NUM_SEARCH_RESULTS.get_text(driver))
        LOCATION_SEARCH_BOX.inject_text(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_ORGANIZATION_SORT.click(driver, SLEEP_TIME)
        SERVICE_ARCHBOLD_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click(driver, SLEEP_TIME)
        for i in range(0, 60):
            SEARCH_NOW.click(driver, SLEEP_TIME)
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
        LOCATION_SEARCH_BOX.inject_text(driver, 'Tampa ', 2*SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_TABLE_COUNT.select_option(driver, '100', SLEEP_TIME)
        SERVICE_NWIS_UV_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click(driver, SLEEP_TIME)
        DATE_FILTER_ON.click(driver, SLEEP_TIME)
        DATE_FILTER_START.clear_text(driver, 12, SLEEP_TIME)
        DATE_FILTER_START.inject_text(driver, '12/01/2015', SLEEP_TIME)
        DATE_FILTER_CLICKOUT.passive_click(driver, SLEEP_TIME)
        DATE_FILTER_END.clear_text(driver, 12, SLEEP_TIME)
        DATE_FILTER_END.inject_text(driver, '12/30/2015', SLEEP_TIME)
        DATE_FILTER_SAVE.click(driver, SLEEP_TIME)
        SEARCH_NOW.click(driver, SLEEP_TIME)
        FILTER_RESULTS.click(driver, SLEEP_TIME)
        FILTER_DERIVED_VALUE_ROW.click(driver, SLEEP_TIME)
        SELECT_ACTION.click(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click(driver, SLEEP_TIME)
        time.sleep(10*SLEEP_TIME)
        VIEW_WORKSPACE.click(driver, SLEEP_TIME)
        oracle()

    def test_A_000005(self):
        """ Confirms New Haven CT Site X416-Y130 metadata and data are
        available for NASA Goddard Earth Sciences services
        """
        def oracle():
            """ Export to workspace is successfull
            """
            self.assertTrue(driver.page_source.count('<em> Completed</em>') == 2)
        LOCATION_SEARCH_BOX.inject_text(driver, 'New Haven ', SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click(driver, SLEEP_TIME)
        SERVICE_TABLE_COUNT.select_option(driver, '100', SLEEP_TIME)
        SERVICE_NASA_NOAH.click(driver, SLEEP_TIME)
        SERVICE_NASA_PRIMARY_FORCING.scroll_to(driver, SLEEP_TIME)
        SERVICE_NASA_PRIMARY_FORCING.multi_click(driver, SLEEP_TIME)
        SERVICE_SEARCH_SEARCH.click(driver, SLEEP_TIME)
        FILTER_RESULTS.click(driver, SLEEP_TIME)
        FILTER_TABLE_SEARCH.inject_text(driver, 'X416-Y130', SLEEP_TIME)
        FILTER_BY_SERVICE.click(driver, SLEEP_TIME)
        FILTER_TABLE_COUNT.select_option(driver, '100', SLEEP_TIME)
        FILTER_MODEL_SIM_RESULT_ROW.click(driver, SLEEP_TIME)
        FILTER_BY_SERVICE.click(driver, SLEEP_TIME)
        FILTER_DERIVED_VALUE_ROW.scroll_to(driver, SLEEP_TIME)
        FILTER_DERIVED_VALUE_ROW.multi_click(driver, SLEEP_TIME)
        SELECT_ACTION.click(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click(driver, SLEEP_TIME)
        VIEW_WORKSPACE.click(driver, SLEEP_TIME)
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
