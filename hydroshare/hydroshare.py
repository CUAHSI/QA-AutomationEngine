""" Runs various smoke tests for the hydroshare.org """
import os
import random
import re
import urllib.request

from hs_macros import Home, Apps, Discover, Resource, Help, API, About, Profile, \
    Groups, Group, MyResources
from hs_elements import AppsPage

from cuahsi_base.cuahsi_base import BaseTest, parse_args_run_tests
from cuahsi_base.utils import External, TestSystem
from config import BASE_URL, USERNAME, PASSWORD


# Test cases definition
class HydroshareTestSuite(BaseTest):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        super(HydroshareTestSuite, self).setUp()
        self.driver.get(BASE_URL)

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

        Home.to_discover(self.driver)
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
        num_windows_now = len(driver.window_handles)
        Home.to_apps(driver)
        External.switch_new_page(driver, num_windows_now,
                                 AppsPage.apps_container_locator)
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
        TestSystem.wait(1)
        About.toggle_tree(self.driver)
        TestSystem.wait(1)
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

    def test_B_000012(self):
        """ Confirm footer links redirect to valid pages and are available
        at the bottom of a sample of pages """
        def oracle_helppage(webpage_title, expected_title):
            """ Expected title is actual page title """
            self.assertIn(expected_title.lower(), webpage_title.lower())

        def oracle_sitemap(webpage_title):
            """ Resulting page exists """
            self.assertNotIn('Page not found', webpage_title)

        Home.to_help(self.driver)
        Help.to_footer_terms(self.driver)
        oracle_helppage(Help.get_title(self.driver), 'Terms of Use')
        Help.to_footer_privacy(self.driver)
        oracle_helppage(Help.get_title(self.driver), 'Statement of Privacy')
        Help.to_footer_sitemap(self.driver)
        oracle_sitemap(TestSystem.title(self.driver))

    def test_B_000013(self):
        """ Confirms clean removal, then readdition, of user organizations using
        the user profile interface """
        def oracle():
            self.assertIn('Your profile has been successfully updated.',
                          TestSystem.page_source(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.delete_org(self.driver, 2)
        Profile.delete_org(self.driver, 1)
        Profile.add_org(self.driver, 'Freie Universität Berlin')
        Profile.add_org(self.driver, 'Agricultural University of Warsaw')
        Profile.save(self.driver)
        TestSystem.wait(3)  # TODO setup config file for delays
        oracle()

    def test_B_000014(self):
        """ Confirms ability to create HydroShare groups through standard
        graphical interface and workflow """
        def oracle(group_name):
            self.assertEqual(Group.check_title(self.driver), group_name)
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_collaborate(self.driver)
        group_name = 'QA Test Group {}'.format(random.randint(1, 1000000))
        Groups.create_group(self.driver,
                            name=group_name,
                            purpose='1230!@#$%^&*()-=_+<{[QA TEST]}>.,/',
                            about='Über Die Gruppe',
                            privacy='private')
        oracle(group_name)

    def test_B_000015(self):
        """ Confirms Resource "Open With" successfully redirects to JupyterHub """
        def oracle(webpage_title):
            """ Resulting page exists """
            self.assertNotIn('Page not found', webpage_title)

        Home.to_discover(self.driver)
        Discover.filters(self.driver, author='Castronova, Anthony')
        Discover.to_resource(self.driver, 'Terrain Processing - TauDem Example')
        Resource.open_with_jupyterhub(self.driver)
        oracle(TestSystem.title(self.driver))

    def test_B_000016(self):
        """ Create basic resource without any files """
        def oracle(resource_title):
            """ Check title to make sure it matches initial input """
            self.assertEqual('Test Resource', resource_title)

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.create_resource(self.driver, 'Test Resource')
        TestSystem.wait()
        resource_title = Resource.get_title(self.driver)
        oracle(resource_title)

    def test_B_000017(self):
        """ Confirm applying resource type filters in My Resources does not break system """
        def oracle(page_title):
            """ My Resources page is still clean/active """
            self.assertIn('My Resources', page_title)
        options = ['Collection',
                   'Composite Resource',
                   'Generic',
                   'Geographic Feature',
                   'Geographic Raster',
                   'HIS Referenced',
                   'Model Instance',
                   'Model Program',
                   'MODFLOW',
                   'Multidimensional',
                   'Script Resource',
                   'Swat Model Instance',
                   'Time Series',
                   'Web App']
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.search_resource_type(self.driver)
        for option in options:
            MyResources.search_type(self.driver, option)
            oracle(TestSystem.title(self.driver))

    def test_B_000018(self):
        """ Use My Resources search bar filters and non-ASCII characters """
        def oracle_type(is_applied):
            """ Search bar shows the resource type filter """
            if is_applied:
                self.assertIn('[type:', MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn('[type:', MyResources.read_searchbar(self.driver))

        def oracle_author(is_applied):
            """ Search bar shows the author filter """
            if is_applied:
                self.assertIn('[author:Über', MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn('[author:', MyResources.read_searchbar(self.driver))

        def oracle_subject(is_applied):
            """ Search bar shows the subject filter """
            if is_applied:
                self.assertIn('[subject:Über', MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn('[subject:', MyResources.read_searchbar(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)

        MyResources.search_resource_type(self.driver)

        oracle_type(False)
        MyResources.search_type(self.driver, 'Web App')
        oracle_type(True)
        oracle_author(False)
        MyResources.search_author(self.driver, 'Über')
        oracle_author(True)
        oracle_subject(False)
        MyResources.search_subject(self.driver, 'Über')
        oracle_subject(True)

        oracle_type(True)
        oracle_author(True)
        oracle_subject(True)

        MyResources.clear_search(self.driver)

        oracle_type(False)
        oracle_author(False)
        oracle_subject(False)

        MyResources.search_resource_type(self.driver)
        MyResources.search_type(self.driver, 'Web App')
        MyResources.search_author(self.driver, 'Über')
        MyResources.search_subject(self.driver, 'Über')
        MyResources.clear_author_search(self.driver)
        oracle_author(False)
        MyResources.clear_subject_search(self.driver)
        oracle_subject(False)
        MyResources.search_type(self.driver, 'All')

        oracle_type(False)
        oracle_author(False)
        oracle_subject(False)

    def test_B_000019(self):
        """ Create a new resources label """
        def oracle_selected():
            """ The label class is showing as selected """
            self.assertTrue(MyResources.check_label_applied(self.driver))

        def oracle_deselected():
            """ The label class is showing as deselected """
            self.assertFalse(MyResources.check_label_applied(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.create_label(self.driver, 'Test')
        MyResources.toggle_label(self.driver, 'Test')
        oracle_selected()
        MyResources.toggle_label(self.driver, 'Test')
        oracle_deselected()
        MyResources.delete_label(self.driver)

    def test_B_000021(self):
        """ Confirm ability to upload CV file to users profile """
        def oracle(cv_filename):
            """ Checks "View CV" window page title contains the file name """
            self.assertTrue(cv_filename in TestSystem.title(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        urllib.request.urlretrieve ('https://www.bu.edu/com-csc/resume/resume_samples.pdf', 'cv-test.pdf')
        cwd = os.getcwd()
        cv_path = os.path.join(cwd, 'cv-test.pdf')
        Profile.add_cv(self.driver, cv_path)
        TestSystem.scroll_to_top(self.driver)
        Profile.save(self.driver)
        num_windows_now = len(self.driver.window_handles)
        Profile.view_cv(self.driver)
        External.to_file(self.driver, num_windows_now, 'cv-test')
        oracle('cv-test')
        os.remove(cv_path)
        External.switch_old_page(self.driver)
        External.close_new_page(self.driver)
        Profile.to_editor(self.driver)
        Profile.delete_cv(self.driver)

    def test_B_000023(self):
        """ Ensure resource links to profile work """
        def oracle(contribution_counts):
            """ Confirm the "All" contibutions count is the sum of all the other
            resource type contributions """
            self.assertEqual(
                contribution_counts[0],  # count for "All"
                sum(contribution_counts[1:])  # count for the rest
            )
        Home.to_discover(self.driver)
        Discover.filters(self.driver, author='Castronova, Anthony')
        Discover.to_resource(self.driver, 'Lowering the barriers to Computational Modeling of the Earth Surface')
        Discover.to_last_updated_profile(self.driver)
        Profile.view_contributions(self.driver)
        resource_types_count = Profile.get_resource_type_count(self.driver)
        contribution_counts = []
        for i in range(0, resource_types_count):
            Profile.view_contribution_type(self.driver, i)
            contribution_counts.append(
                Profile.get_contribution_type_count(self.driver, i)
            )
        oracle(contribution_counts)


if __name__ == '__main__':
    parse_args_run_tests(HydroshareTestSuite)
