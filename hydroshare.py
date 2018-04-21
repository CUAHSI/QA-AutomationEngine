""" Runs various smoke tests for the hydroshare.org """
import re
import sys
import unittest

from cuahsi_base import BaseTest, basecli
from hs_macros import Home, Apps, Discover, Resource, Help, API, About
from utils import External, TestSystem

# Test case parameters
BASE_URL = "http://www.hydroshare.org"


# Test cases definition
class HydroshareTestSuite(BaseTest):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        super(HydroshareTestSuite, self).setUp()
        self.driver.get(BASE_URL)
        self.driver.implicitly_wait(10)

    def test_B_000003(self):
        """ Confirms Beaver Divide Air Temperature resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive and confirms the BagIt file size matches expectation
        """
        def oracle():
            """ The Beaver Divide BagIt zip file matches expected file
            size (in Bytes)
            """
            self.assertEqual(Resource.size_download(self.driver, BASE_URL), 512000)
        Discover.filters(self.driver, subject='iUTAH', resource_type='Generic',
                         availability=['discoverable', 'public'])
        Discover.to_resource(self.driver, 'Beaver Divide Air Temperature')
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

        driver = self.driver
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

        driver = self.driver
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
                self.assertIn(word, TestSystem.page_source(self.driver))
        Home.to_help(self.driver)
        core_count = Help.count_core(self.driver)
        core_topics = [Help.get_core_topic(self.driver, i+1)
                       for i in range(0, core_count)]
        for ind, core_topic in enumerate(core_topics, 1):  # xpath ind start at 1
            Help.open_core(self.driver, ind)
            oracle(core_topic)
            Help.to_core_breadcrumb(self.driver)

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
        TestSystem.to_url(self.driver, '{}/hsapi/'.format(BASE_URL))
        API.expand_hsapi(self.driver)
        for endpoint in endpoints:
            API.toggle_endpoint(self.driver, endpoint, 'GET')
            API.set_resource_id(self.driver, endpoint, 'GET', resource_id)
            API.submit(self.driver, endpoint, 'GET')
            response_code = API.response_code(self.driver, endpoint, 'GET')
            oracle(response_code)
            API.toggle_endpoint(self.driver, endpoint, 'GET')

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
        TestSystem.to_url(self.driver, '{}/hsapi/'.format(BASE_URL))
        API.expand_hsapi(self.driver)
        for endpoint in endpoints:
            API.toggle_endpoint(self.driver, endpoint, 'GET')
            API.submit(self.driver, endpoint, 'GET')
            API.response_code(self.driver, endpoint, 'GET')
            TestSystem.wait(3)  # wait 3 seconds for empty field population
            response_code = API.response_code(self.driver, endpoint, 'GET')
            oracle(response_code)
            API.toggle_endpoint(self.driver, endpoint, 'GET')

    def test_B_000011(self):
        """ Check Hydroshare About policy pages to confirm links and content """
        def oracle(policy, article_title, webpage_title):
            """ Confirms the policy link text matches up with the opened policy
            page title and webpage title
            """
            self.assertIn(policy, article_title)
            self.assertIn(policy, webpage_title)
        Home.to_about(self.driver)
        About.toggle_tree(self.driver)
        About.toggle_tree(self.driver)
        About.expand_tree_top(self.driver, 'Policies')
        policies = ['HydroShare Publication Agreement',
                    'Quota',
                    'Statement of Privacy',
                    'Terms of Use']
        for policy in policies:
            About.open_policy(self.driver, policy)
            article_title = About.get_title(self.driver)
            webpage_title = TestSystem.title(self.driver)
            oracle(policy, article_title, webpage_title)


if __name__ == '__main__':
    args = basecli().parse_args()
    HydroshareTestSuite.GRID_HUB_IP = vars(args).get('grid')

    # Set the sys.argv to the unittest_args (leaving sys.argv[0] alone)
    sys.argv[1:] = args.unittest_args
    unittest.main(verbosity=2)
