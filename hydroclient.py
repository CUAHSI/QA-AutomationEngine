""" Runs various smoke tests for the data.cuahsi.org """
import unittest
import time
from selenium import webdriver
from site_element import SiteElement
from selenium.webdriver.common.keys import Keys
from modes import setup_mode

# Test case parameters
MODE_SELECTION = 'demo'
setup_mode(MODE_SELECTION)
BASE_URL = 'http://data.cuahsi.org'
# Search interface
SEARCH_NOW = SiteElement('button', the_id='btnSearchNow')
FILTER_RESULTS = SiteElement('button', the_id='btnSearchSummary')
LOCATION_SEARCH_BOX = SiteElement('input', the_id='pac-input')
SERVICE_SEARCH = SiteElement('button', the_id='btnSelectDataServices',
                             the_content='Data Service(s)...')
SERVICE_ORGANIZATION_SORT = SiteElement('th', the_content='Organization')
SERVICE_ARCHBOLD_SEARCH = SiteElement('td',
                                      the_content='Archbold Biological Station')
SERVICE_SEARCH_SAVE = SiteElement('button', the_id='btnServicesModalSave')
NUM_SEARCH_RESULTS = SiteElement('span', the_id='timeseriesFoundOrFilteredCount')
# Filter interface
FILTER_COL_DATA_TYPE = SiteElement('th', the_content='Data Type')
SELECT_ACTION = SiteElement('div', the_id='ddActionsDSR')
WORKSPACE_SELECTION = SiteElement('a', the_id='anchorAddSelectionsToWorkspaceDSR')
VIEW_EXPORTS = SiteElement('button', the_id='tableModal-DownloadMgrSearchSummary')
VIEW_WORKSPACE = SiteElement('button', the_id='tableModal-DataMgrSearchSummary')
CLOSE_FILTER = SiteElement('button', the_id='closeSearchSummary')
FILTER_TABLE = SiteElement('table', the_id='tblDetailedSearchResults')
FILTER_TABLE_DIVE = [SiteElement('tbody'),
                     SiteElement('tr', the_class='disable-selection even'),
                     SiteElement('td'),
                     SiteElement('div')]

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
        time.sleep(SLEEP_TIME)
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
                SiteElement('span', the_class='glyphicon-thumbs-up')
            except NoSuchElementException:
                workspace_load = False
            self.assertTrue(workspace_load)

        driver = setup_driver()
        driver.get(BASE_URL)
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
        # click_it(driver, FILTER_COL_DATA_TYPE)
        # Below clicks first row only
        CLOSE_FILTER.scroll_to_it(driver, SLEEP_TIME)
        FILTER_TABLE.nested_click(driver, FILTER_TABLE_DIVE, SLEEP_TIME)
        SELECT_ACTION.click_it(driver, SLEEP_TIME)
        WORKSPACE_SELECTION.click_it(driver, SLEEP_TIME)
        VIEW_WORKSPACE.click_it(driver, SLEEP_TIME)
        time.sleep(60)
        oracle()
        driver.quit()

    def test_A_000003(self):
        """ Confirms repeated search for Lake Annie does not result
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
        LOCATION_SEARCH_BOX.text_into_it(driver, "Lake Annie Highlands County", SLEEP_TIME)
        time.sleep(SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        LOCATION_SEARCH_BOX.text_into_it(driver, Keys.RETURN, SLEEP_TIME)
        SERVICE_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_ORGANIZATION_SORT.click_it(driver, SLEEP_TIME)
        SERVICE_ARCHBOLD_SEARCH.click_it(driver, SLEEP_TIME)
        SERVICE_SEARCH_SAVE.click_it(driver, SLEEP_TIME)
        for i in range(0, 500):
            SEARCH_NOW.click_it(driver, SLEEP_TIME)
            time.sleep(1)
        oracle()
        driver.quit()

    def todo_test_A_000004(self):
        """ Confirms simultaneous searches for Lake Annie does not result
        in problematic behavior
        """
        def oracle():
            self.assertTrue('51' in NUM_SEARCH_RESULTS.get_text(driver))

        # DOESNT WORK - NEED TO FIX TABS ISSUE
        driver = setup_driver()
        for i in range(0, 20):
            driver.execute_script('''window.open("http://google.com","_blank");''')
            time.sleep(3)
            driver.get(BASE_URL)
            time.sleep(3)
            LOCATION_SEARCH_BOX.text_into_it(driver, "Lake Annie Highlands County", SLEEP_TIME)
            time.sleep(SLEEP_TIME)
            LOCATION_SEARCH_BOX.text_into_it(driver, Keys.ARROW_DOWN, SLEEP_TIME)
            LOCATION_SEARCH_BOX.text_into_it(driver, Keys.RETURN, SLEEP_TIME)
            SERVICE_SEARCH.click_it(driver, SLEEP_TIME)
            SERVICE_ORGANIZATION_SORT.click_it(driver, SLEEP_TIME)
            SERVICE_ARCHBOLD_SEARCH.click_it(driver, SLEEP_TIME)
            SERVICE_SEARCH_SAVE.click_it(driver, SLEEP_TIME)
            SEARCH_NOW.click_it(driver, SLEEP_TIME)
            time.sleep(1)
            self.assertTrue('51' in NUM_SEARCH_RESULTS.get_text(driver))
        for i in range(0, 20):
            SEARCH_NOW.click_it(driver, SLEEP_TIME)
            time.sleep(1)
            oracle()
        driver.quit()


if __name__ == '__main__':
    unittest.main(verbosity=2)
