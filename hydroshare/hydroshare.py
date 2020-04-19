""" Runs various smoke tests for the hydroshare.org """
import os
import random
import re

from urllib.request import urlretrieve

from hs_macros import (
    Home,
    Login,
    Apps,
    Discover,
    Resource,
    Help,
    API,
    About,
    Profile,
    Groups,
    Group,
    MyResources,
    Dashboard,
    NewResource,
    Registration,
    SiteMap,
    WebApp,
    JupyterHub,
)

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
            "CompositeResource",
            "CollectionResource",
            "ToolResource",
            "ModelProgramResource",
            "ModelInstanceResource",
            "SWATModelInstanceResource",
            "MODFLOWModelInstanceResource",
        ]
        for resource_type in resource_types:
            Home.create_resource(self.driver, resource_type)
            NewResource.configure(self.driver, "TEST TITLE")
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
            self.assertEqual(Resource.size_download(self.driver, BASE_URL), 512000)

        Home.to_discover(self.driver)
        Discover.filters(
            self.driver,
            subject="iUTAH",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        oracle()

    def test_B_000005(self):
        """ Confirms password reset works for users """
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.reset_password(self.driver, PASSWORD, PASSWORD + "test")
        Home.login(self.driver, USERNAME, PASSWORD + "test")
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.reset_password(self.driver, PASSWORD + "test", PASSWORD)
        Home.login(self.driver, USERNAME, PASSWORD)

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
                Discover.check_sorting_multi(driver, column_name, ascend_or_descend)
            )

        driver = self.driver
        Home.to_discover(driver)
        orderings = ["Last Modified", "Title", "First Author", "Date Created"]
        for ordering in orderings:
            Discover.sort_direction(driver, "Ascending")
            Discover.sort_order(driver, ordering)
            oracle(driver, ordering, "Ascending")
            Discover.sort_direction(driver, "Descending")
            Discover.sort_order(driver, ordering)
            oracle(driver, ordering, "Descending")

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
        Home.to_apps(driver)
        apps_count = Apps.count(driver)
        for i in range(1, apps_count + 1):  # xpath start at 1
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
            words_string = re.sub("[^A-Za-z]", " ", core_topic)
            matches = [
                word in Help.get_title(self.driver) for word in words_string.split(" ")
            ]
            self.assertTrue(True in matches)

        Home.to_help(self.driver)
        core_count = Help.count_core(self.driver)
        core_topics = [
            Help.get_core_topic(self.driver, i + 1) for i in range(0, core_count)
        ]
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
            self.assertEqual(response_code, "200")

        resource_id = "927094481da54af38ffb6f0c39ad8787"
        endpoints = [
            {"id": "operations-hsapi-hsapi_resource_read", "resource_param_ind": 1},
            {
                "id": "operations-hsapi-hsapi_resource_file_list_list",
                "resource_param_ind": 3,
            },
            {
                "id": "operations-hsapi-hsapi_resource_files_list",
                "resource_param_ind": 3,
            },
            {"id": "operations-hsapi-hsapi_resource_map_list", "resource_param_ind": 1},
            {
                "id": "operations-hsapi-hsapi_resource_scimeta_list",
                "resource_param_ind": 1,
            },
            {
                "id": "operations-hsapi-hsapi_resource_scimeta_elements_read",
                "resource_param_ind": 1,
            },
            {
                "id": "operations-hsapi-hsapi_resource_sysmeta_list",
                "resource_param_ind": 1,
            },
        ]

        TestSystem.to_url(self.driver, "{}/hsapi/".format(BASE_URL))
        for endpoint in endpoints:
            API.toggle_endpoint(self.driver, endpoint["id"])
            API.try_endpoint(self.driver)
            API.set_parameter(self.driver, endpoint["resource_param_ind"], resource_id)
            API.submit(self.driver)
            response_code = API.get_response_code(self.driver)
            oracle(response_code)
            API.toggle_endpoint(self.driver, endpoint["id"])

    def test_B_000010(self):
        """
        Confirms the basic get methods within hydroshare api, which require
        no parameters, can be ran through the GUI
        """

        def oracle(response_code):
            """ Response code is 200 - response "OK" """
            self.assertEqual(response_code, "200")

        endpoints = [
            "operations-hsapi-hsapi_resource_content_types_list",
            "operations-hsapi-hsapi_resource_types_list",
            "operations-hsapi-hsapi_user_list",
            "operations-hsapi-hsapi_userInfo_list",
        ]
        TestSystem.to_url(self.driver, "{}/hsapi/".format(BASE_URL))
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
        About.expand_tree_top(self.driver, "Policies")
        policies = [
            "HydroShare Publication Agreement",
            "Quota",
            "Statement of Privacy",
            "Terms of Use",
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
            self.assertNotIn("Page not found", webpage_title)

        Home.to_help(self.driver)
        Help.to_footer_terms(self.driver)
        oracle_helppage(Help.get_title(self.driver), "Terms of Use")
        Help.to_footer_privacy(self.driver)
        oracle_helppage(Help.get_title(self.driver), "Statement of Privacy")
        Help.to_footer_sitemap(self.driver)
        oracle_sitemap(TestSystem.title(self.driver))

    def test_B_000013(self):
        """
        Confirms clean removal, then readdition, of user organizations using
        the user profile interface
        """

        def oracle():
            """ Profile is updated successfully with the organizations change """
            self.assertIn(
                "Your profile has been successfully updated.",
                TestSystem.page_source(self.driver),
            )

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.delete_org(self.driver, 2)
        Profile.delete_org(self.driver, 1)
        Profile.add_org(self.driver, "Freie Universität Berlin")
        Profile.add_org(self.driver, "Agricultural University of Warsaw")
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
        Home.to_groups(self.driver)
        group_name = "QA Test Group {}".format(random.randint(1, 1000000))
        Groups.create_group(
            self.driver,
            name=group_name,
            purpose="1230!@#$%^&*()-=_+<{[QA TEST]}>.,/",
            about="Über Die Gruppe",
            privacy="private",
        )
        oracle(group_name)

    def test_B_000015(self):
        """ Confirms Resource "Open With" successfully redirects to JupyterHub """

        def oracle(webpage_title):
            """ JupyterHub page opens without a 404 or missing page error """
            self.assertNotIn("Page not found", webpage_title)

        Home.to_discover(self.driver)
        Discover.filters(self.driver, author="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Resource.open_with_jupyterhub(self.driver)
        oracle(TestSystem.title(self.driver))

    def test_B_000016(self):
        """
        Create basic resource without any files and confirm that the resulting
        resource landing page is OK
        """

        def oracle(resource_title):
            """ Test resource landing page shows the right resource name """
            self.assertEqual("Test Resource", resource_title)

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Test Resource")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        resource_title = Resource.get_title(self.driver)
        oracle(resource_title)

    def test_B_000017(self):
        """
        Confirm resource type filters can be applied in My Resources """

        def oracle(page_title):
            """ My Resources page is still clean/active """
            self.assertIn("My Resources", page_title)

        options = [
            "Collection",
            "Composite Resource",
            "Generic",
            "Geographic Feature",
            "Geographic Raster",
            "HIS Referenced",
            "Model Instance",
            "Model Program",
            "MODFLOW",
            "Multidimensional",
            "Script Resource",
            "Swat Model Instance",
            "Time Series",
            "Web App",
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
                self.assertIn("[type:", MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn("[type:", MyResources.read_searchbar(self.driver))

        def oracle_author(is_applied):
            """ Search bar shows the correct author filter """
            if is_applied:
                self.assertIn("[author:Über", MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn("[author:", MyResources.read_searchbar(self.driver))

        def oracle_subject(is_applied):
            """ Search bar shows the correct subject filter """
            if is_applied:
                self.assertIn("[subject:Über", MyResources.read_searchbar(self.driver))
            else:
                self.assertNotIn("[subject:", MyResources.read_searchbar(self.driver))

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)

        MyResources.search_resource_type(self.driver)

        oracle_type(False)
        MyResources.search_type(self.driver, "Web App")
        oracle_type(True)
        oracle_author(False)
        MyResources.search_author(self.driver, "Über")
        oracle_author(True)
        oracle_subject(False)
        MyResources.search_subject(self.driver, "Über")
        oracle_subject(True)

        oracle_type(True)
        oracle_author(True)
        oracle_subject(True)

        MyResources.clear_search(self.driver)

        oracle_type(False)
        oracle_author(False)
        oracle_subject(False)

        MyResources.search_resource_type(self.driver)
        MyResources.search_type(self.driver, "Web App")
        MyResources.search_author(self.driver, "Über")
        MyResources.search_subject(self.driver, "Über")
        MyResources.clear_author_search(self.driver)
        oracle_author(False)
        MyResources.clear_subject_search(self.driver)
        oracle_subject(False)
        MyResources.search_type(self.driver, "All")

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
        MyResources.create_label(self.driver, "Test")
        MyResources.toggle_label(self.driver, "Test")
        oracle_selected()
        MyResources.toggle_label(self.driver, "Test")
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
        Profile.upload_cv(
            self.driver, "http://www.bu.edu/careers/files/2012/08/Resume-Guide-2012.pdf"
        )
        Profile.save(self.driver)
        num_windows_now = len(self.driver.window_handles)
        Profile.view_cv(self.driver)
        External.to_file(self.driver, num_windows_now, "cv-test")
        oracle("cv-test")
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
            "http://www.bu.edu/emd/files/2017/03/rhett_alone1.jpg", "profile.jpg"
        )
        cwd = os.getcwd()
        profile_img_path = os.path.join(cwd, "profile.jpg")
        Profile.add_photo(self.driver, profile_img_path)
        Profile.save(self.driver)
        oracle("profile", True)
        os.remove(profile_img_path)
        Profile.to_editor(self.driver)
        Profile.remove_photo(self.driver)
        oracle("profile", False)

    def test_B_000023(self):
        """
        Ensure that the user links within a resource landing page redirect to
        the associated user landing page, and that the contribution counts in
        the resulting page are summed correctly
        """

        def oracle_total(contribution_counts):
            """
            The "All" contibutions count is the sum of all the other
            resource type contributions
            """
            self.assertEqual(
                contribution_counts[0],  # count for "All"
                sum(contribution_counts[1:]),  # count for the rest
            )

        def oracle_type(contributions_count, contributions_list_length):
            self.assertEqual(contributions_count, contributions_list_length)

        Home.to_discover(self.driver)
        Discover.filters(self.driver, owner="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Discover.to_last_updated_profile(self.driver)
        Profile.view_contributions(self.driver)
        resource_types_count = Profile.get_resource_type_count(self.driver)
        contribution_counts = []
        contributions_list_length = Profile.get_contributions_list_length(self.driver)
        for i in range(0, resource_types_count):
            Profile.view_contribution_type(self.driver, i)
            contribution_counts.append(
                Profile.get_contribution_type_count(self.driver, i)
            )
        oracle_type(sum(contribution_counts[1:]), contributions_list_length)
        oracle_total(contribution_counts)

    def test_B_000024(self):
        """ Verify the ability to extend metadata on resource landing pages """
        name_ex = "name_ex"
        value_ex = "value_ex"

        def oracle(name, value):
            """ The metadata was created with the right name and value """
            Resource.exists_name(self.driver, name)
            Resource.exists_value(self.driver, value)

        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Test Metadata")
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

        images = [
            'background-image: url("/static/img/home-page/carousel/bg1.jpg");',
            'background-image: url("/static/img/home-page/carousel/bg2.JPG");',
            'background-image: url("/static/img/home-page/carousel/bg3.jpg");',
        ]
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

        def oracle(expected, actual):
            """ Href matches the expected social media account url """
            self.assertEqual(expected, actual)

        socials = ["twitter", "facebook", "youtube", "github", "linkedin"]

        for social in socials:
            oracle(
                Home.get_social_link_expected(social),
                Home.get_social_link_actual(self.driver, social),
            )

    def test_B_000029(self):
        """ Commenting requires a login """

        def oracle_login_prompt():
            self.assertIn("Please log in", Login.get_notification(self.driver))

        def oracle_commented(initial, final):
            self.assertTrue(initial < final)

        Home.to_discover(self.driver)
        Discover.filters(self.driver, author="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        initial_comment_count = Resource.get_comment_count(self.driver)
        Resource.add_comment(self.driver, "Test Comment")
        oracle_login_prompt()
        Login.login(self.driver, USERNAME, PASSWORD)
        Resource.add_comment(self.driver, "Test Comment")
        final_comment_count = Resource.get_comment_count(self.driver)
        oracle_commented(initial_comment_count, final_comment_count)

    def test_B_000031(self):
        """ Confirm that resources can be accessed from the sitemap links """

        def oracle(text):
            """ Page title matches with the resource title """
            self.assertIn(text, TestSystem.title(self.driver))
            TestSystem.back(self.driver)

        Home.to_site_map(self.driver)
        Home.select_resource(self.driver, "Beaver Divide Air Temperature")
        oracle("Beaver Divide Air Temperature")
        Home.select_resource(self.driver, "Beaver Divide Air Temperature")
        oracle("Beaver Divide Air Temperature")

    def hold_test_B_000032(self):
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
            self.assertFalse(Discover.is_selected(self.driver, author="Myers, Jessie"))
            self.assertFalse(
                Discover.is_selected(self.driver, contributor="Cox, Chris")
            )
            self.assertFalse(
                Discover.is_selected(self.driver, owner="Christopher, Adrian")
            )
            self.assertFalse(
                Discover.is_selected(self.driver, content_type="Model Instance")
            )
            self.assertFalse(
                Discover.is_selected(
                    self.driver, subject="USACE Corps Water Management System (CWMS)"
                )
            )
            self.assertFalse(Discover.is_selected(self.driver, availability="public"))

        Home.to_discover(self.driver)
        Discover.filters(
            self.driver,
            author="Myers, Jessie",
            contributor="Cox, Chris",
            owner="Christopher, Adrian",
            content_type="Model Instance",
            subject="USACE Corps Water Management System (CWMS)",
            availability="public",
        )
        Discover.show_all(self.driver)
        oracle()

    def test_B_000034(self):
        """ Basic navigation to dashboard """

        def oracle(visibility):
            """ Expect get started to be showing """
            self.assertNotEqual(visibility[0], visibility[1])

        Home.login(self.driver, USERNAME, PASSWORD)
        Dashboard.toggle_get_started(self.driver)
        visibility = [Dashboard.is_get_started_showing(self.driver)]
        Dashboard.toggle_get_started(self.driver)
        visibility += [Dashboard.is_get_started_showing(self.driver)]
        Home.to_home(self.driver)
        oracle(visibility)

    def test_B_000035(self):
        """ Ensure registration prompts for Organization entry """

        def oracle(error_text):
            """ Error message suggests Organization data is missing """
            self.assertIn("Organization", error_text)

        Home.signup(
            self.driver,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe.123@example.com",
            username="jdoe123",
            password="mypass",
        )
        error_text = Registration.check_error(self.driver)
        oracle(error_text)

    def test_B_000036(self):
        """Ensure Correct Web apps show in Open With"""

        # login
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "ToolResource")

        # create web app resource
        NewResource.configure(self.driver, "TEST Web App")
        NewResource.create(self.driver)

        # configure web app resource
        WebApp.support_resource_type(self.driver, "CompositeResource")
        WebApp.set_app_launching_url(self.driver, "https://www.hydroshare.org")
        WebApp.view(self.driver)
        WebApp.add_to_open_with(self.driver)

        # create composite resource
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "TEST Web App Composite")
        NewResource.create(self.driver)

        # Validate new web app is a available on the composite resource page
        Resource.view(self.driver)
        Resource.open_with_by_title(self.driver, "TEST Web App")

    def test_B_000038(self):
        """ Ensure invalid logins generate a helpful error message """

        def oracle(error_message):
            self.assertIn("username", error_message)
            self.assertIn("password", error_message)

        Home.login(self.driver, "Invalid", "Invalid")
        oracle(Login.get_login_error(self.driver))
        Home.login(self.driver, USERNAME, PASSWORD)
        Dashboard.toggle_get_started(self.driver)
        Dashboard.toggle_get_started(self.driver)

    def test_B_000039(self):
        """ Ensure pre-login My Resources redirects to My Resources after login """
        Home.to_my_resources(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        MyResources.search(self.driver, "Search bar text")

    def test_B_000041(self):
        """ Update profile About information """
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.update_about(
            self.driver, "// TODO My Profile Description", "United States", "New York"
        )
        Profile.save(self.driver)

    def test_B_000046(self):
        """ Ensure clicking the Hydroshare logo links back to the home page """
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Home.click_logo(self.driver)
        Home.slider_left(self.driver)

    def test_B_000047(self):
        """ Ensure DEBUG=false for production hydroshare.org """
        TestSystem.to_url(
            self.driver, "https://www.hydroshare.org/landingPageDoesNotExist/"
        )
        Home.click_logo(self.driver)

    def test_B_000048(self):
        """ Ensure pre-login My Groups redirects to My Groups after login """

        def oracle():
            self.assertEqual("My Groups", Groups.get_title(self.driver))

        Home.to_groups(self.driver)
        Groups.to_my_groups(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        oracle()

    def test_B_000049(self):
        """ Ensure user can logout after logging in """
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)

    def test_B_000050(self):
        """ Ensure the support email mailto is in the site footer """
        self.assertIn("Support", Home.email_support(self.driver))

    def test_B_000051(self):
        """ Ensure all Getting Started links open correctly, and in the same tab """
        Home.login(self.driver, USERNAME, PASSWORD)
        for row in [1, 2]:
            for column in [1, 2, 3]:
                Dashboard.check_getting_started_link(self.driver, row, column)

    def test_B_000052(self):
        """ Verify Recently Visited resources and authors link to valid pages """

        def oracle_resource(link_title, resource_title):
            self.assertEqual(link_title, resource_title)

        def oracle_author(link_author, profile_author):
            """ Confirm first and last name from the profile are in the recent activity author cell """
            for word in [profile_author.split(" ")[0], profile_author.split(" ")[-1]]:
                self.assertIn(word, link_author)

        Home.login(self.driver, USERNAME, PASSWORD)
        recent_activity_len = Dashboard.get_recent_activity_length(self.driver)
        for i in range(
            1, recent_activity_len + 1
        ):  # css selector nth-of-type starts at 1
            link_title, resource_title = Dashboard.check_recent_activity_resource(
                self.driver, i
            )
            oracle_resource(link_title, resource_title)
        for i in range(
            1, recent_activity_len + 1
        ):  # css selector nth-of-type starts at 1
            link_author, profile_author = Dashboard.check_recent_activity_author(
                self.driver, i
            )
            oracle_author(link_author, profile_author)


class JupyterhubTestSuite(BaseTest):
    """ Python unittest setup for jupyterhub testing """

    def setUp(self):
        super(JupyterhubTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_000001(self):
        """ Spawn and interact with a server """
        TestSystem.to_url(self.driver, "https://whw.cuahsi.org/hub/login")
        JupyterHub.to_hs_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.wait(3)
        JupyterHub.authorize(self.driver)
        JupyterHub.select_scientific_spawner(self.driver)
        JupyterHub.sort_notebooks_by_name(self.driver)


# Health cases definition
class HydroshareHealthSuite(BaseTest):
    """ Python unittest setup for health checks """

    def setUp(self):
        super(HydroshareHealthSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_sitemap_does_not_contain_spam_resources(self):
        """
        Tries to identify potential spam resources (e.g., advertisements) on the
        SiteMap page.
        To do this, it collects all links to resources from the SiteMap page,
        and tests if a link text matches specific patterns (e.g., contains
        specific keywords, or parts of words, or simply general patterns, such
        as phone numbers).
        The test will simply print all suspicious resources to stdout, there are
        no assertions in it.
        """

        def check_links_against_patterns(links, patterns):
            resources = []
            # Compile a single regular expression that will match any individual
            # pattern from a given list of patterns, case-insensitive.
            # ( '|' is a special character in regular expressions. An expression
            # 'A|B' will match either 'A' or 'B' ).
            full_pattern = re.compile("|".join(patterns), re.IGNORECASE)
            for link in links:
                match = re.search(full_pattern, link.text)
                # Link text matches one of the patterns.
                if match is not None:
                    link_url = link.get_attribute("href")
                    match_text = match.group()
                    resources.append([link.text, match_text, link_url])

            return resources

        def print_formatted_result(detected_resources, classification):
            print(f"Found {len(detected_resources)} {classification} resources:\n")
            detected_resources = [
                f'"{item[0]}" (has word(s) "{item[1]}" '
                f"in text). Resource URL: {item[2]}"
                for item in detected_resources
            ]
            print("  * " + "\n  * ".join(detected_resources) + "\n\n")

        Home.to_site_map(self.driver)
        links = SiteMap.get_resource_list(self.driver)
        print(
            f"\nThere are {len(links)} resources at HydroShare " f'"Site Map" page.\n'
        )

        spam_patterns = [
            "amazing",
            "business",
            "cheap[est]?",
            "credit[s]?",
            "customer[s]?",
            "deal[s]?",
            "phone number",
            "price",
            "4free",
            # US phone number format (1-[3 digits]-[3 digits]-[4 digits]
            # r'' is a 'raw' string (backslash symbol is treated as a literal
            # backslash).
            r"\d-[\d]{3}-[\d]{3}-[\d]{4}",
            "airline[s]?",
            "baggage",
            "booking",
            "flight[s]?",
            "reservation",
            "vacation[al]?",
            "ticket[s]?",
            "account",
            "antivirus",
            "cleaner",
            "cookies",
            "[e]?mail",
            "laptop",
            "password",
            "sign up",
            "sign in",
            "wi[-]?fi",
            # r'' is a 'raw' string (backslash symbol is treated as a literal
            # backslash).
            # '\b' stands for 'word boundary'.
            r"\bgoogle\b",
            "android",
            "chrome",
            "apple",
            "icloud",
            r"\bios\b",
            "iphone",
            r"\bmac\b",
            "macbook",
            "macos",
            "facebook",
            "microsoft",
            "windows",
            "internet explorer",
            "adult",
            "escort",
            "porn",
            "xxx",
        ]
        spam_resources = check_links_against_patterns(links, spam_patterns)
        print_formatted_result(spam_resources, classification="potential spam")

        # Not related to spam, but these are potentially useless resources.
        verifyme_patterns = [
            "hello",
            "hello world",
            "my first",
            "test resource",
            "untitled",
            r"\b123\b",
        ]
        verifyme_resources = check_links_against_patterns(links, verifyme_patterns)
        print_formatted_result(verifyme_resources, classification="potentially useless")


if __name__ == "__main__":
    parse_args_run_tests(HydroshareTestSuite)
