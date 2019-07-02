""" Runs various smoke tests for the hydroshare.org """
import os
import random
import re

from urllib.request import urlretrieve, urlopen

from hs_macros import Home, Apps, Discover, Resource, Help, API, About, Profile, \
    Groups, Group, MyResources, Dashboard, NewResource
from hs_elements import AppsPage, MyResourcesPage, HomePage, DiscoverPage

from cuahsi_base.cuahsi_base import BaseTest, parse_args_run_tests
from cuahsi_base.utils import External, TestSystem
from config import BASE_URL, USERNAME, PASSWORD, GITHUB_ORG, GITHUB_REPO


# Test cases definition
class HydroshareTestSuite(BaseTest):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        super(HydroshareTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_B_000001(self):
        """ When creating a resource, ensure all resource types have a "Cancel"
        button available """
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        resource_types = [
            'CompositeResource',
            'CollectionResource',
            'ToolResource',
            'ModelProgramResource',
            'ModelInstanceResource',
            'SWATModelInstanceResource',
            'MODFLOWModelInstanceResource'
        ]
        for resource_type in resource_types:
            Home.create_resource(self.driver, resource_type)
            NewResource.configure(self.driver, 'TEST TITLE')
            NewResource.cancel(self.driver)

    def test_B_000003(self):
        """
        Confirms Beaver Divide Air Temperature resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive and confirms the BagIt file size matches expectation
        """
        def oracle():
            """
            The Beaver Divide BagIt zip file matches expected file
            size (in Bytes)
            """
            self.assertEqual(
                Resource.size_download(self.driver, BASE_URL),
                512000
            )

        Home.to_discover(self.driver)
        Discover.filters(
            self.driver,
            subject='iUTAH',
            resource_type='Generic',
            availability=['discoverable', 'public']
        )
        Discover.to_resource(self.driver, 'Beaver Divide Air Temperature')
        oracle()

    def test_B_000006(self):
        """
        Confirms the sorting behavior on the Discover page (both sort
        direction and sort field) functions correctly, as evaluated by a few
        of the first rows being ordered correctly
        """
        def oracle(driver, column_name, ascend_or_descend):
            """
            Sorting is correctly implemented, as measured by a sample
            of row comparisons (not exhaustive)
            """
            self.assertTrue(
                Discover.check_sorting_multi(
                    driver, column_name, ascend_or_descend
                )
            )

        driver = self.driver
        Home.to_discover(driver)
        orderings = [
            'Last Modified',
            'Title',
            'First Author',
            'Date Created',
        ]
        for ordering in orderings:
            Discover.sort_direction(driver, 'Ascending')
            Discover.sort_order(driver, ordering)
            oracle(driver, ordering, 'Ascending')
            Discover.sort_direction(driver, 'Descending')
            Discover.sort_order(driver, ordering)
            oracle(driver, ordering, 'Descending')

    def test_B_000007(self):
        """
        Confirms all apps have an associated resource page which is
        correctly linked and correctly listed within the app info on the
        apps page
        """
        def oracle(app_name, resource_page):
            """ The resource page contains the associated app name """
            self.assertIn(app_name, resource_page)

        driver = self.driver
        num_windows_now = len(driver.window_handles)
        Home.to_apps(driver)
        External.switch_new_page(driver, num_windows_now,
                                 AppsPage.apps_container_locator)
        apps_count = Apps.count(driver)
        for i in range(1, apps_count+1):  # xpath start at 1
            app_name = Apps.get_title(driver, i)
            Apps.show_info(driver, i)
            Apps.to_resource(driver, i)
            oracle(app_name, External.source_new_page(driver))
            TestSystem.back(driver)

    def test_B_000008(self):
        """
        Checks all HydroShare Help links to confirm links are intact
        and that the topic title words come up in the associated help page
        """
        def oracle(core_topic):
            """ The help link text is contained in the help page """
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
        """
        Confirms the basic get methods within hydroshare api do not return
        errors.  These basic get methods are accessible from the GUI and
        use just a resource id required parameter
        """
        def oracle(response_code):
            """ Response code is 200 - an "OK" response """
            self.assertEqual(response_code, '200')

        resource_id = '927094481da54af38ffb6f0c39ad8787'
        endpoints = [
            {'id':'operations-hsapi-hsapi_resource_read', 'resource_param_ind': 1},
            {'id':'operations-hsapi-hsapi_resource_file_list_list', 'resource_param_ind': 3},
            {'id':'operations-hsapi-hsapi_resource_files_list', 'resource_param_ind': 3},
            {'id':'operations-hsapi-hsapi_resource_map_list', 'resource_param_ind': 1},
            {'id':'operations-hsapi-hsapi_resource_scimeta_list', 'resource_param_ind': 1},
            {'id': 'operations-hsapi-hsapi_resource_scimeta_elements_read', 'resource_param_ind': 1},
            {'id': 'operations-hsapi-hsapi_resource_sysmeta_list', 'resource_param_ind': 1}
        ]

        TestSystem.to_url(self.driver, '{}/hsapi/'.format(BASE_URL))
        for endpoint in endpoints:
            API.toggle_endpoint(self.driver, endpoint['id'])
            API.try_endpoint(self.driver)
            API.set_parameter(self.driver, endpoint['resource_param_ind'], resource_id)
            API.submit(self.driver)
            response_code = API.get_response_code(self.driver)
            oracle(response_code)
            API.toggle_endpoint(self.driver, endpoint['id'])

    def test_B_000010(self):
        """
        Confirms the basic get methods within hydroshare api, which require
        no parameters, can be ran through the GUI
        """
        def oracle(response_code):
            """ Response code is 200 - response "OK" """
            self.assertEqual(response_code, '200')

        endpoints = [
            'operations-hsapi-hsapi_resource_content_types_list',
            'operations-hsapi-hsapi_resource_types_list',
            'operations-hsapi-hsapi_user_list',
            'operations-hsapi-hsapi_userInfo_list'
        ]
        TestSystem.to_url(self.driver, '{}/hsapi/'.format(BASE_URL))
        for endpoint in endpoints:
            API.toggle_endpoint(self.driver, endpoint)
            API.try_endpoint(self.driver)
            API.submit(self.driver)
            response_code = API.get_response_code(self.driver)
            oracle(response_code)
            API.toggle_endpoint(self.driver, endpoint)

    def test_B_000011(self):
        """ Check Hydroshare About policy pages to confirm links and content """
        def oracle(policy, article_title, webpage_title):
            """
            The policy link text matches up with the opened policy
            page title and webpage title
            """
            self.assertIn(policy, article_title)
            self.assertIn(policy, webpage_title)

        Home.to_about(self.driver)
        About.toggle_tree(self.driver)
        About.toggle_tree(self.driver)
        About.expand_tree_top(self.driver, 'Policies')
        policies = [
            'HydroShare Publication Agreement',
            'Quota',
            'Statement of Privacy',
            'Terms of Use'
        ]
        for policy in policies:
            About.open_policy(self.driver, policy)
            article_title = About.get_title(self.driver)
            webpage_title = TestSystem.title(self.driver)
            oracle(policy, article_title, webpage_title)

    def test_B_000012(self):
        """
        Confirm footer links redirect to valid pages and are available
        at the bottom of a sample of pages
        """
        def oracle_helppage(webpage_title, expected_title):
            """ Help page title from the link matches the actual page title """
            self.assertIn(expected_title.lower(), webpage_title.lower())

        def oracle_sitemap(webpage_title):
            """ Page is found - no 404 page returned """
            self.assertNotIn('Page not found', webpage_title)

        Home.to_help(self.driver)
        Help.to_footer_terms(self.driver)
        oracle_helppage(Help.get_title(self.driver), 'Terms of Use')
        Help.to_footer_privacy(self.driver)
        oracle_helppage(Help.get_title(self.driver), 'Statement of Privacy')
        Help.to_footer_sitemap(self.driver)
        oracle_sitemap(TestSystem.title(self.driver))

    def test_B_000013(self):
        """
        Confirms clean removal, then readdition, of user organizations using
        the user profile interface
        """
        def oracle():
            """ Profile is updated successfully with the organizations change """
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
        oracle()

    def test_B_000014(self):
        """
        Confirms ability to create HydroShare groups through standard
        graphical interface and workflow
        """
        def oracle(group_name):
            """ Group name is visible in the new group page """
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
            """ JupyterHub page opens without a 404 or missing page error """
            self.assertNotIn('Page not found', webpage_title)

        Home.to_discover(self.driver)
        Discover.filters(self.driver, author='Castronova, Anthony')
        Discover.to_resource(self.driver, 'Terrain Processing - TauDem Example')
        Resource.open_with_jupyterhub(self.driver)
        oracle(TestSystem.title(self.driver))

    def test_B_000016(self):
        """
        Create basic resource without any files and confirm that the resulting
        resource landing page is OK
        """
        def oracle(resource_title):
            """ Test resource landing page shows the right resource name """
            self.assertEqual('Test Resource', resource_title)

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, 'CompositeResource')
        NewResource.configure(self.driver, 'Test Resource')
        NewResource.create(self.driver)
        Resource.view(self.driver)
        resource_title = Resource.get_title(self.driver)
        oracle(resource_title)

    def test_B_000017(self):
        """
        Confirm resource type filters can be applied in My Resources """
        def oracle(page_title):
            """ My Resources page is still clean/active """
            self.assertIn('My Resources', page_title)
        options = [
            'Collection',
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
            'Web App'
        ]
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.search_resource_type(self.driver)
        for option in options:
            MyResources.search_type(self.driver, option)
            oracle(TestSystem.title(self.driver))

    def test_B_000018(self):
        """
        Use My Resources search bar filters and non-ASCII characters, in
        order to verify filter usability for non-English resources
        """
        def oracle_type(is_applied):
            """ Search bar shows the correct resource type filter """
            if is_applied:
                self.assertIn(
                    '[type:',
                    MyResources.read_searchbar(self.driver)
                )
            else:
                self.assertNotIn(
                    '[type:',
                    MyResources.read_searchbar(self.driver)
                )

        def oracle_author(is_applied):
            """ Search bar shows the correct author filter """
            if is_applied:
                self.assertIn(
                    '[author:Über',
                    MyResources.read_searchbar(self.driver)
                )
            else:
                self.assertNotIn(
                    '[author:',
                    MyResources.read_searchbar(self.driver)
                )

        def oracle_subject(is_applied):
            """ Search bar shows the correct subject filter """
            if is_applied:
                self.assertIn(
                    '[subject:Über',
                    MyResources.read_searchbar(self.driver)
                )
            else:
                self.assertNotIn(
                    '[subject:',
                    MyResources.read_searchbar(self.driver)
                )

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
        """
        Create a new resources label and verify it can be added to existing
        resources in the My Resources page
        """
        def oracle_selected():
            """ The label is showing as selected """
            self.assertTrue(MyResources.check_label_applied(self.driver))

        def oracle_deselected():
            """ The label is showing as deselected """
            self.assertFalse(MyResources.check_label_applied(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.create_label(self.driver, 'Test')
        MyResources.toggle_label(self.driver, 'Test')
        oracle_selected()
        MyResources.toggle_label(self.driver, 'Test')
        oracle_deselected()
        MyResources.delete_label(self.driver)

    def hold_test_B_000021(self):  # BROKEN DUE TO HYDROSHARE JS FRAMEWORK USE
        """ Confirm ability to upload CV file to users profile """
        def oracle(cv_filename):
            """ "View CV" window page title contains the file name """
            self.assertTrue(cv_filename in TestSystem.title(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.upload_cv(self.driver, 'http://www.bu.edu/careers/files/2012/08/Resume-Guide-2012.pdf')
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

    def hold_test_B_000022(self):  # BROKEN DUE TO HYDROSHARE JS FRAMEWORK USE
        """ Confirm profile image upload, within the profile page """
        def oracle(img_filename, is_uploaded):
            """
            Profile pic div contains the image filename in it's style
            attribute (the system uses style background image approach)
            """
            if is_uploaded:
                self.assertTrue(
                    Profile.confirm_photo_uploaded(self.driver, img_filename)
                )
            else:
                self.assertFalse(
                    Profile.confirm_photo_uploaded(self.driver, img_filename)
                )
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        urlretrieve(
            'http://www.bu.edu/emd/files/2017/03/rhett_alone1.jpg',
            'profile.jpg'
        )
        cwd = os.getcwd()
        profile_img_path = os.path.join(cwd, 'profile.jpg')
        Profile.add_photo(self.driver, profile_img_path)
        Profile.save(self.driver)
        oracle('profile', True)
        os.remove(profile_img_path)
        Profile.to_editor(self.driver)
        Profile.remove_photo(self.driver)
        oracle('profile', False)

    def test_B_000023(self):
        """
        Ensure that the user links within a resource landing page redirect to
        the associated user landing page, and that the contribution counts in
        the resulting page are summed correctly
        """
        def oracle(contribution_counts):
            """
            The "All" contibutions count is the sum of all the other
            resource type contributions
            """
            self.assertEqual(
                contribution_counts[0],  # count for "All"
                sum(contribution_counts[1:])  # count for the rest
            )
        Home.to_discover(self.driver)
        Discover.filters(self.driver, author='Brazil, Liza')
        Discover.to_resource(
            self.driver,
            'University of Arizona CUAHSI Data Services Workshop'
        )
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

    def test_B_000024(self):
        """ Verify the ability to extend metadata on resource landing pages """
        name_ex = 'name_ex'
        value_ex = 'value_ex'

        def oracle(name, value):
            """ The metadata was created with the right name and value """
            Resource.exists_name(self.driver, name)
            Resource.exists_value(self.driver, value)

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, 'CompositeResource')
        NewResource.configure(self.driver, 'Test Metadata')
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.edit(self.driver)
        Resource.add_metadata(self.driver, name_ex, value_ex)
        oracle(name_ex, value_ex)

    def test_B_000026(self):
        """
        Confirm that the home page slider is functional
        """
        def oracle_active():
            """ At least one slider is active """
            self.assertTrue(Home.a_slider_is_active(self.driver))

        def oracle_image(images):
            """ The slider background image is in the list of images """
            self.assertTrue(Home.slider_has_valid_img(self.driver, images))

        images = ['background-image: url("/static/img/home-page/carousel/bg1.jpg");',
                  'background-image: url("/static/img/home-page/carousel/bg2.JPG");',
                  'background-image: url("/static/img/home-page/carousel/bg3.jpg");']
        Home.scroll_to_button(self.driver)
        Home.scroll_to_top(self.driver)
        for i in range(0, 5):
            Home.slider_left(self.driver)
            oracle_active()
            oracle_image(images)

    def test_B_000027(self):
        """
        Confirm that the MyResources and Discover pages have the same labels and
        resources listed in their legends
        """
        def oracle(legend_one, legend_two):
            """ Text from the legends on MyResources and Discover match """
            self.assertEqual(legend_one, legend_two)
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        my_resource_legend = MyResources.legend_text(self.driver)
        Home.to_discover(self.driver)
        discover_legend = Discover.legend_text(self.driver)
        oracle(my_resource_legend, discover_legend)

    def test_B_000028(self):
        """
        Checks that the each social media account is accessible from
        the links in the footer
        """

        def get_link_href(link_element):
            return link_element.get_attribute(self.driver, 'href')

        def oracle(expected_href, target_link):
            """ Href matches the expected social media account url """
            actual_href = get_link_href(target_link)
            self.assertEqual(expected_href, actual_href)

        oracle('http://twitter.com/cuahsi', HomePage.twitter_link)
        exp_fb_href = 'https://www.facebook.com/pages/CUAHSI-Consortium-' \
                      'of-Universities-for-the-Advancement-of-Hydrologic-' \
                      'Science-Inc/179921902590'
        oracle(exp_fb_href, HomePage.facebook_link)
        oracle('http://youtube.hydroshare.org/', HomePage.youtube_link)
        oracle('http://github.com/hydroshare', HomePage.git_link)
        oracle('https://www.linkedin.com/company/2632114', HomePage.linkedin_link)

    def test_B_000031(self):
        """ Confirm that resources can be accessed from the sitemap links """
        def oracle(text):
            """ Page title matches with the resource title """
            self.assertTrue(text in TestSystem.title(self.driver))
            TestSystem.back(self.driver)

        Home.to_site_map(self.driver)
        Home.select_resource(self.driver, 'GIS in Water Resources Term Project 2015')
        oracle('GIS in Water Resources Term Project 2015')
        Home.select_resource(self.driver,
                             'Flow measurements at Manabao, Dominican Republic')
        oracle('Flow measurements at Manabao, Dominican Republic')

    def test_B_000032(self):
        """
        Confirm that the hydroshare footer version number matches up with the
        latest version number in GitHub
        """
        def oracle(expected, actual):
            """ Versions in the hydroshare footer and github match """
            self.assertEqual(expected, actual)

        displayed_release_version = Home.version(self.driver)
        expected_release_version = Home.get_hs_latest_release(GITHUB_ORG, GITHUB_REPO)
        oracle(expected_release_version, displayed_release_version)

    def test_B_000033(self):
        """ Ensure Discover page "show all" clears all filter types """

        def oracle():
            """ All previous filters are inactive due to "Show All" """
            self.assertFalse(DiscoverPage.filter_author(
                'Myers, Jessie').is_selected(self.driver))
            self.assertFalse(DiscoverPage.filter_contributor(
                'Cox, Chris').is_selected(self.driver))
            self.assertFalse(DiscoverPage.filter_owner(
                'Christopher, Adrian').is_selected(self.driver))
            self.assertFalse(DiscoverPage.filter_content_type(
                'Model Instance').is_selected(self.driver))
            self.assertFalse(
              DiscoverPage
                .filter_subject('USACE Corps Water Management System (CWMS)')
                .is_selected(self.driver)
            )
            self.assertFalse(DiscoverPage.filter_availability(
                'public').is_selected(self.driver))

        Home.to_discover(self.driver)
        Discover.filters(self.driver,
                         author='Myers, Jessie',
                         contributor='Cox, Chris',
                         owner='Christopher, Adrian',
                         content_type='Model Instance',
                         subject='USACE Corps Water Management System (CWMS)',
                         availability='public'
                         )
        Discover.show_all(self.driver)
        oracle()

    def test_B_000034(self):
        """ Basic navigation to dashboard """

        def oracle():
            """ Expect get started to be showing """
            self.assertTrue(Dashboard.is_get_started_showing(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Dashboard.toggle_get_started(self.driver)
        Dashboard.toggle_get_started(self.driver)
        Home.to_home(self.driver)
        oracle()
        


if __name__ == '__main__':
    parse_args_run_tests(HydroshareTestSuite)
