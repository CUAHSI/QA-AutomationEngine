""" Runs various smoke tests for the hydroshare.org """
import argparse
import re
import sys
import unittest

from selenium import webdriver
from hs_macros import Home, Apps, Discover, Resource, Help, API
from utils import External, TestSystem

# Test case parameters
BASE_URL = "http://www.hydroshare.org"


# Test cases definition
class HydroshareTestSuite(unittest.TestCase):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        """ Setup driver for use in automation tests """
        profile = webdriver.FirefoxProfile()
        profile.set_preference("general.useragent.override", "CUAHSI-QA-Selenium")
        # TODO use self.driver instead of making it global
        global driver
        if infrastructure == 'grid':
            driver = webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(grid_hub_ip),
                desired_capabilities={'browserName': 'firefox'})
        else:
            driver = webdriver.Firefox(profile)
        driver.get(BASE_URL)
        driver.implicitly_wait(20)

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
            self.assertEqual(Resource.size_download(driver, BASE_URL), 512000)
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
            self.assertTrue(Discover.check_sorting_multi(driver, column_name,
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

    def test_B_000007(self):
        """ Confirms all apps have an associated resource page which is
        correctly linked and correctly listed within the app info on the
        apps page
        """
        def oracle(app_name, resource_page):
            self.assertIn(app_name, resource_page)
        Home.to_apps(driver)
        External.switch_new_page(driver)
        apps_count = Apps.count(driver)
        for i in range(0, apps_count):  # +1 used below - xpath start at 1
            app_name = Apps.get_title(driver, i+1)
            Apps.show_info(driver, i+1)
            Apps.to_resource(driver, i+1)
            oracle(app_name, External.source_new_page(driver))
            TestSystem.back(driver)

    def test_B_000008(self):
        """ Checks all HydroShare Help links to confirm links are intact
        and that the topic title words come up in the associated help page
        """
        def oracle(core_topic):
            words_string = re.sub('[^A-Za-z]', ' ', core_topic)
            for word in words_string.split(' '):
                self.assertIn(word, TestSystem.page_source(driver))
        Home.to_help(driver)
        core_count = Help.count_core(driver)
        core_topics = [Help.get_core_topic(driver, i+1)
                       for i in range(0, core_count)]
        for ind, core_topic in enumerate(core_topics, 1):  # xpath ind start at 1
            Help.open_core(driver, ind)
            oracle(core_topic)
            Help.to_core_breadcrumb(driver)

    def test_B_000009(self):
        """ Confirms absense of errors for the basic get methods within hydroshare
        api that use just a resource id required parameter
        """
        def oracle(response_code):
            self.assertEqual(response_code, '200')
        resource_id = '927094481da54af38ffb6f0c39ad8787'
        endpoints = ['/hsapi/resource/{id}/',
                     '/hsapi/resource/{id}/file_list/',
                     '/hsapi/resource/{id}/files/',
                     '/hsapi/resource/{id}/map/',
                     '/hsapi/resource/{id}/scimeta/']
        TestSystem.to_url(driver, '{}/hsapi/'.format(BASE_URL))
        API.expand_hsapi(driver)
        for endpoint in endpoints:
            API.toggle_endpoint(driver, endpoint, 'GET')
            API.set_resource_id(driver, endpoint, 'GET', resource_id)
            API.submit(driver, endpoint, 'GET')
            response_code = API.response_code(driver, endpoint, 'GET')
            oracle(response_code)
            API.toggle_endpoint(driver, endpoint, 'GET')

    def test_B_000010(self):
        """ Confirms absense of errors for the basic get methods within hydroshare
        api that require no parameters
        """
        def oracle(response_code):
            """ Response code from api endpoint call is 200 """
            self.assertEqual(response_code, '200')
        endpoints = ['/hsapi/dictionary/universities/',
                     '/hsapi/resource/',
                     '/hsapi/resource/types/',
                     '/hsapi/resourceList/',
                     '/hsapi/resourceTypes/',
                     '/hsapi/user/',
                     '/hsapi/userInfo/']
        TestSystem.to_url(driver, '{}/hsapi/'.format(BASE_URL))
        API.expand_hsapi(driver)
        for endpoint in endpoints:
            API.toggle_endpoint(driver, endpoint, 'GET')
            API.submit(driver, endpoint, 'GET')
            API.response_code(driver, endpoint, 'GET')
            TestSystem.wait(3)  # wait 3 seconds for empty field population
            response_code = API.response_code(driver, endpoint, 'GET')
            oracle(response_code)
            API.toggle_endpoint(driver, endpoint, 'GET')


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
