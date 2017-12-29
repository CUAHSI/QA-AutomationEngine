""" Runs various smoke tests for the data.cuahsi.org """
import unittest
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
SERVICE_TABLE_COUNT = SiteElement('select', el_name='tblDataServices_length')
SERVICE_ARCHBOLD_SEARCH = SiteElement('td',
                                      el_content='Archbold Biological Station')
SERVICE_NWIS_UV_SEARCH = SiteElement('a', el_content='NWIS Unit Values')
SERVICE_NWIS_UV_SEARCH_DIVE = [SiteElement(el_dom='./../..'),
                               SiteElement(el_dom='./td[1]')]
# Filter interface
SELECT_ACTION = SiteElement('div', el_id='ddActionsDSR')
WORKSPACE_SELECTION = SiteElement('a', el_id='anchorAddSelectionsToWorkspaceDSR')
VIEW_EXPORTS = SiteElement('button', el_id='tableModal-DownloadMgrSearchSummary')
VIEW_WORKSPACE = SiteElement('button', el_id='tableModal-DataMgrSearchSummary')
CLOSE_FILTER = SiteElement('button', el_id='closeSearchSummary')
FILTER_TABLE = SiteElement('table', el_id='tblDetailedSearchResults')
FILTER_TABLE_DIVE = [SiteElement(el_dom='./tbody'),
                     SiteElement(el_dom='./tr'),
                     SiteElement(el_dom='./td'),
                     SiteElement(el_dom='./div')]
FILTER_DERIVED_VALUE_ROW = SiteElement('td', el_content='Derived Value')

def setup_driver():
    """ Setup driver, including profile config, for test executions """
    profile = webdriver.FirefoxProfile()
    profile.set_preference("general.useragent.override", "CUAHSI-QA-Selenium")
    driver = webdriver.Firefox(profile)
    return driver

# Test cases definition
class HydroclientTestCase(unittest.TestCase):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        """ Sets up browser for future tests """
        self.browser = webdriver.Firefox()
        self.addCleanup(self.browser.quit)

    def test_A_000001(self):
        """ Confirms homepage online via page title """
        def oracle():
            """ The HydroClient homepage is online """
            self.assertIn('HydroClient', driver.title)

        driver = setup_driver()
        driver.get(BASE_URL)
        driver.implicitly_wait(10)
        oracle()
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

        driver = setup_driver()
        driver.get(BASE_URL)
        driver.implicitly_wait(10)
        LOCATION_SEARCH_BOX.text_into_it(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_ORGANIZATION_SORT.click_it(driver, SLEEP_TIME)
        SERVICE_ARCHBOLD_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click_it(driver, SLEEP_TIME)
        SEARCH_NOW.click_it(driver, SLEEP_TIME)
        time.sleep(10)
        FILTER_RESULTS.click_it(driver, SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(SLEEP_TIME)
        CLOSE_FILTER.scroll_to_it(driver, SLEEP_TIME)
        FILTER_TABLE.nested_click(driver, FILTER_TABLE_DIVE, SLEEP_TIME)
        SELECT_ACTION.click_it(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click_it(driver, SLEEP_TIME)
        VIEW_WORKSPACE.click_it(driver, SLEEP_TIME)
        time.sleep(60)
        oracle()
        driver.quit()

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

        driver = setup_driver()
        driver.get(BASE_URL)
        driver.implicitly_wait(10)
        LOCATION_SEARCH_BOX.text_into_it(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_ORGANIZATION_SORT.click_it(driver, SLEEP_TIME)
        SERVICE_ARCHBOLD_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click_it(driver, SLEEP_TIME)
        for i in range(0, 60):
            SEARCH_NOW.click_it(driver, SLEEP_TIME)
            time.sleep(1)
        oracle()
        driver.quit()

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

        driver = setup_driver()
        driver.get(BASE_URL)
        driver.implicitly_wait(10)
        LOCATION_SEARCH_BOX.text_into_it(driver, 'Tampa ', 2*SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_TABLE_COUNT.select_from_it(driver, '100', SLEEP_TIME)
        SERVICE_NWIS_UV_SEARCH.nested_click(driver, SERVICE_NWIS_UV_SEARCH_DIVE, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click_it(driver, SLEEP_TIME)
        DATE_FILTER_ON.click_it(driver, SLEEP_TIME)
        DATE_FILTER_START.clear_it(driver, 12, SLEEP_TIME)
        DATE_FILTER_START.text_into_it(driver, '12/01/2015', SLEEP_TIME)
        DATE_FILTER_CLICKOUT.passive_click_it(driver, SLEEP_TIME)
        DATE_FILTER_END.clear_it(driver, 12, SLEEP_TIME)
        DATE_FILTER_END.text_into_it(driver, '12/30/2015', SLEEP_TIME)
        DATE_FILTER_SAVE.click_it(driver, SLEEP_TIME)
        SEARCH_NOW.click_it(driver, SLEEP_TIME)
        FILTER_RESULTS.click_it(driver, SLEEP_TIME)
        FILTER_DERIVED_VALUE_ROW.click_it(driver, SLEEP_TIME)
        SELECT_ACTION.click_it(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click_it(driver, SLEEP_TIME)
        VIEW_WORKSPACE.click_it(driver, SLEEP_TIME)
        oracle()
        driver.quit()

if __name__ == '__main__':
    unittest.main(verbosity=2)
