""" Runs various smoke tests for the hydroshare.org """
import os
import random
import re

from urllib.request import urlretrieve

from hs_macros import (
    Hydroshare,
    LandingPage,
    Home,
    Login,
    Apps,
    Discover,
    Resource,
    Help,
    HelpArticle,
    API,
    About,
    Profile,
    Collaborate,
    Groups,
    Group,
    MyResources,
    NewResource,
    Registration,
    SiteMap,
    WebApp,
    JupyterHub,
)

from cuahsi_base.cuahsi_base import BaseTestSuite, parse_args_run_tests
from cuahsi_base.utils import External, TestSystem
from config import BASE_URL, USERNAME, PASSWORD, GITHUB_ORG, GITHUB_REPO


# Test cases definition
class HydroshareTestSuite(BaseTestSuite):
    """ Python unittest setup for smoke tests """

    def setUp(self):
        super(HydroshareTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_B_000001(self):
        """ When creating a resource, ensure all resource types have a "Cancel"
        button available """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
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
            MyResources.create_resource(self.driver, resource_type)
            NewResource.configure(self.driver, "TEST TITLE")
            NewResource.cancel(self.driver)

    def test_B_000003(self):
        """
        Confirms Beaver Divide Air Temperature resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive and confirms the BagIt file size matches expectation
        """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            subject="iUTAH",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        self.assertEqual(Resource.get_bagit_size(self.driver, BASE_URL), 512000)

    def test_B_000005(self):
        """ Confirms password reset works for users """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.reset_password(self.driver, PASSWORD, PASSWORD + "test")
        Profile.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD + "test")
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.reset_password(self.driver, PASSWORD + "test", PASSWORD)
        Profile.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)

    def test_B_000006(self):
        """
        Confirms the sorting behavior on the Discover page (both sort
        direction and sort field) functions correctly, as evaluated by a few
        of the first rows being ordered correctly
        """
        LandingPage.to_discover(self.driver)
        orderings = ["Last Modified", "Title", "First Author", "Date Created"]
        for ordering in orderings:
            Discover.set_sort_direction(self.driver, "Ascending")
            Discover.set_sort_order(self.driver, ordering)
            self.assertTrue(
                Discover.check_sorting_multi(self.driver, ordering, "Ascending")
            )
            Discover.set_sort_direction(self.driver, "Descending")
            Discover.set_sort_order(self.driver, ordering)
            self.assertTrue(
                Discover.check_sorting_multi(self.driver, ordering, "Descending")
            )

    def test_B_000007(self):
        """
        Confirms all apps have an associated resource page which is
        correctly linked and correctly listed within the app info on the
        apps page
        """
        LandingPage.to_apps(self.driver)
        apps_count = Apps.get_count(self.driver)
        for i in range(1, apps_count + 1):  # xpath start at 1
            app_name = Apps.get_title(self.driver, i)
            Apps.show_info(self.driver, i)
            Apps.to_resource(self.driver, i)
            resource_title = Resource.get_title(self.driver)
            self.assertIn(app_name, resource_title)
            TestSystem.back(self.driver)

    def test_B_000008(self):
        """
        Checks all HydroShare Help links to confirm links are intact
        and that the topic title words come up in the associated help page
        """
        LandingPage.to_help(self.driver)
        core_count = Help.get_core_count(self.driver)
        core_topics = [
            Help.get_core_topic(self.driver, i + 1) for i in range(0, core_count)
        ]
        for ind, core_topic in enumerate(core_topics, 1):  # xpath ind start at 1
            Help.open_core(self.driver, ind)
            words_string = re.sub("[^A-Za-z]", " ", core_topic)
            matches = [
                word in HelpArticle.get_title(self.driver) for word in words_string.split(" ")
            ]
            self.assertTrue(True in matches)
            HelpArticle.to_help_breadcrumb(self.driver)

    def test_B_000009(self):
        """
        Confirms the basic get methods within hydroshare api do not return
        errors.  These basic get methods are accessible from the GUI and
        use just a resource id required parameter
        """
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
            API.execute_request(self.driver)
            response_code = API.get_response_code(self.driver)
            self.assertEqual(response_code, "200")
            API.toggle_endpoint(self.driver, endpoint["id"])

    def test_B_000010(self):
        """
        Confirms the basic get methods within hydroshare api, which require
        no parameters, can be ran through the GUI
        """
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
            API.execute_request(self.driver)
            response_code = API.get_response_code(self.driver)
            self.assertEqual(response_code, "200")
            API.toggle_endpoint(self.driver, endpoint)

    def test_B_000011(self):
        """ Check Hydroshare About policy pages to confirm links and content """
        LandingPage.to_about(self.driver)
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
            self.assertIn(policy, article_title)
            self.assertIn(policy, webpage_title)

    def test_B_000012(self):
        """
        Confirm footer links redirect to valid pages and are available
        at the bottom of a sample of pages
        """
        LandingPage.to_terms(self.driver)
        terms_title = HelpArticle.get_title(self.driver)
        self.assertIn("terms of use", terms_title.lower())
        HelpArticle.to_privacy(self.driver)
        privacy_title = HelpArticle.get_title(self.driver)
        self.assertIn("statement of privacy", privacy_title.lower())
        HelpArticle.to_sitemap(self.driver)
        self.assertNotIn(
            "Page not found", TestSystem.title(self.driver)
        )

    def test_B_000013(self):
        """
        Confirms clean removal, then readdition, of user organizations using
        the user profile interface
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.delete_organization(self.driver, 2)
        Profile.delete_organization(self.driver, 1)
        Profile.add_organization(self.driver, "Freie Universität Berlin")
        Profile.add_organization(self.driver, "Agricultural University of Warsaw")
        Profile.save_changes(self.driver)
        page_tip = Profile.page_tip.get_text(self.driver)
        self.assertEqual(
            "Your profile has been successfully updated.",
            page_tip,
        )

    def test_B_000014(self):
        """
        Confirms ability to create HydroShare groups through standard
        graphical interface and workflow
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_collaborate(self.driver)
        Collaborate.to_groups(self.driver)
        group_name = "QA Test Group {}".format(random.randint(1, 1000000))
        Groups.create_group(
            self.driver,
            name=group_name,
            purpose="1230!@#$%^&*()-=_+<{[QA TEST]}>.,/",
            about="Über Die Gruppe",
            privacy="private",
        )
        new_group_name = Group.check_title(self.driver)
        self.assertEqual(group_name, new_group_name)

    def test_B_000015(self):
        """ Confirms Resource "Open With" successfully redirects to JupyterHub """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(self.driver, author="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Resource.open_with_jupyterhub(self.driver)
        webpage_title = TestSystem.title(self.driver)
        self.assertNotIn("Page not found", webpage_title)

    def test_B_000016(self):
        """ Create basic resource without any files and confirm that the resulting
        resource landing page is OK """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Test Resource")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        resource_title = Resource.get_title(self.driver)
        self.assertEqual("Test Resource", resource_title)

    def test_B_000017(self):
        """ Confirm resource type filters can be applied in My Resources """
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
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.search_resource_type(self.driver)
        for option in options:
            MyResources.search_type(self.driver, option)
            page_title = TestSystem.title(self.driver)
            self.assertIn("My Resources", page_title)

    def test_B_000018(self):
        """
        Use My Resources search bar filters and non-ASCII characters, in
        order to verify filter usability for non-English resources
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)

        MyResources.search_resource_type(self.driver)

        self.assertNotIn("[type:", MyResources.read_searchbar(self.driver))
        MyResources.search_type(self.driver, "Web App")
        self.assertIn("[type:", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[author:", MyResources.read_searchbar(self.driver))
        MyResources.search_author(self.driver, "Über")
        self.assertIn("[author:Über", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[subject:", MyResources.read_searchbar(self.driver))
        MyResources.search_subject(self.driver, "Über")
        self.assertIn("[subject:Über", MyResources.read_searchbar(self.driver))

        self.assertIn("[type:", MyResources.read_searchbar(self.driver))
        self.assertIn("[author:Über", MyResources.read_searchbar(self.driver))
        self.assertIn("[subject:Über", MyResources.read_searchbar(self.driver))

        MyResources.clear_search(self.driver)

        self.assertNotIn("[type:", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[author:", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[subject:", MyResources.read_searchbar(self.driver))

        MyResources.search_resource_type(self.driver)
        MyResources.search_type(self.driver, "Web App")
        MyResources.search_author(self.driver, "Über")
        MyResources.search_subject(self.driver, "Über")
        MyResources.clear_author_search(self.driver)
        self.assertNotIn("[author:", MyResources.read_searchbar(self.driver))
        MyResources.clear_subject_search(self.driver)
        self.assertNotIn("[subject:", MyResources.read_searchbar(self.driver))
        MyResources.search_type(self.driver, "All")

        self.assertNotIn("[type:", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[author:", MyResources.read_searchbar(self.driver))
        self.assertNotIn("[subject:", MyResources.read_searchbar(self.driver))

    def test_B_000019(self):
        """
        Create a new resources label and verify it can be added to existing
        resources in the My Resources page
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        MyResources.create_label(self.driver, "Test")
        MyResources.toggle_label(self.driver, "Test")
        self.assertTrue(MyResources.check_label_applied(self.driver))
        MyResources.toggle_label(self.driver, "Test")
        self.assertFalse(MyResources.check_label_applied(self.driver))
        MyResources.delete_label(self.driver)

    def hold_test_B_000021(self):  # BROKEN DUE TO HYDROSHARE JS FRAMEWORK USE
        """ Confirm ability to upload CV file to users profile """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.upload_cv(
            self.driver, "http://www.bu.edu/careers/files/2012/08/Resume-Guide-2012.pdf"
        )
        Profile.save_changes(self.driver)
        num_windows_now = len(self.driver.window_handles)
        Profile.view_cv(self.driver)
        External.to_file(self.driver, num_windows_now, "cv-test")
        self.assertTrue("cv-test" in TestSystem.title(self.driver))
        External.switch_old_page(self.driver)
        External.close_new_page(self.driver)
        Profile.to_editor(self.driver)
        Profile.delete_cv(self.driver)

    def hold_test_B_000022(self):  # BROKEN DUE TO HYDROSHARE JS FRAMEWORK USE
        """ Confirm profile image upload, within the profile page """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        urlretrieve(
            "http://www.bu.edu/emd/files/2017/03/rhett_alone1.jpg", "profile.jpg"
        )
        cwd = os.getcwd()
        profile_img_path = os.path.join(cwd, "profile.jpg")
        Profile.add_photo(self.driver, profile_img_path)
        Profile.save_changes(self.driver)
        self.assertTrue(
            Profile.confirm_photo_uploaded(self.driver, "profile")
        )
        os.remove(profile_img_path)
        Profile.to_editor(self.driver)
        Profile.remove_photo(self.driver)
        self.assertFalse(
            Profile.confirm_photo_uploaded(self.driver, "profile")
        )

    def test_B_000023(self):
        """
        Ensure that the user links within a resource landing page redirect to
        the associated user landing page, and that the contribution counts in
        the resulting page are summed correctly
        """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(self.driver, owner="Castronova, Anthony")
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
        self.assertEqual(sum(contribution_counts[1:]), contributions_list_length)
        self.assertEqual(
            contribution_counts[0],  # count for "All"
            sum(contribution_counts[1:]),  # count for the rest
        )

    def test_B_000024(self):
        """ Verify the ability to extend metadata on resource landing pages """
        name_ex = "name_ex"
        value_ex = "value_ex"
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Test Metadata")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.edit(self.driver)
        Resource.add_metadata(self.driver, name_ex, value_ex)
        Resource.exists_name(self.driver, name_ex)
        Resource.exists_value(self.driver, value_ex)

    def test_B_000026(self):
        """ Confirm that the home page slider is functional """
        images = [
            'background-image: url("/static/img/home-page/carousel/bg1.jpg");',
            'background-image: url("/static/img/home-page/carousel/bg2.JPG");',
            'background-image: url("/static/img/home-page/carousel/bg3.jpg");',
        ]
        LandingPage.scroll_to_button(self.driver)
        LandingPage.scroll_to_top(self.driver)
        for i in range(0, 5):
            LandingPage.slide_hero_left(self.driver)
            self.assertTrue(LandingPage.hero_has_valid_img(self.driver, images))

    def test_B_000027(self):
        """
        Confirm that the MyResources and Discover pages have the same labels and
        resources listed in their legends
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_my_resources(self.driver)
        my_resource_legend = MyResources.legend_text(self.driver)
        MyResources.to_discover(self.driver)
        discover_legend = Discover.legend_text(self.driver)
        self.assertEqual(my_resource_legend, discover_legend)

    def test_B_000028(self):
        """
        Checks that the each social media account is accessible from
        the links in the footer
        """
        socials = ["twitter", "facebook", "youtube", "github", "linkedin"]
        expected_links = {
            "facebook": "https://www.facebook.com/pages/CUAHSI-Consortium-"
            "of-Universities-for-the-Advancement-of-Hydrologic-"
            "Science-Inc/179921902590",
            "twitter": "http://twitter.com/cuahsi",
            "youtube": "http://youtube.hydroshare.org/",
            "github": "http://github.com/hydroshare",
            "linkedin": "https://www.linkedin.com/company/2632114",
        }
        for social in socials:
            self.assertEqual(
                expected_links[social],
                LandingPage.get_social_link(self.driver, social),
            )

    def test_B_000029(self):
        """ Commenting requires a login """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(self.driver, author="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        initial_comment_count = Resource.get_comment_count(self.driver)
        Resource.add_comment(self.driver, "Test Comment")
        self.assertIn("Please log in", Login.get_notification(self.driver))
        Login.login(self.driver, USERNAME, PASSWORD)
        Resource.add_comment(self.driver, "Test Comment")
        final_comment_count = Resource.get_comment_count(self.driver)
        self.assertTrue(initial_comment_count < final_comment_count)

    def test_B_000031(self):
        """ Confirm that resources can be accessed from the sitemap links """
        LandingPage.to_sitemap(self.driver)
        SiteMap.select_resource(self.driver, "Beaver Divide Air Temperature")
        self.assertIn("Beaver Divide Air Temperature", TestSystem.title(self.driver))
        TestSystem.back(self.driver)
        SiteMap.select_resource(self.driver, "Beaver Divide Air Temperature")
        self.assertIn("Beaver Divide Air Temperature", TestSystem.title(self.driver))
        TestSystem.back(self.driver)

    def test_B_000032(self):
        """ Confirm that the hydroshare footer version number matches up with the
        latest version number in GitHub """
        displayed_release_version = LandingPage.get_version(self.driver)
        expected_release_version = LandingPage.get_latest_release(GITHUB_ORG, GITHUB_REPO)
        self.assertEqual(expected_release_version, displayed_release_version)

    def test_B_000033(self):
        """ Ensure Discover page "show all" clears all filter types """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Myers, Jessie",
            contributor="Cox, Chris",
            owner="Christopher, Adrian",
            content_type="Model Instance",
            subject="USACE Corps Water Management System (CWMS)",
            availability="public",
        )
        Discover.show_all(self.driver)
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

    def test_B_000034(self):
        """ Basic navigation to home/dashboard """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.toggle_get_started(self.driver)
        visibility = [Home.is_get_started_showing(self.driver)]
        Home.toggle_get_started(self.driver)
        visibility += [Home.is_get_started_showing(self.driver)]
        Home.to_home(self.driver)
        self.assertNotEqual(visibility[0], visibility[1])

    def test_B_000035(self):
        """ Ensure registration prompts for Organization entry """
        LandingPage.to_registration(self.driver)
        Registration.signup_user(
            self.driver,
            first_name="Jane",
            last_name="Doe",
            email="jane.doe.123@example.com",
            username="jdoe123",
            password="mypass",
        )
        error_text = Registration.check_error(self.driver)
        self.assertIn("Organization", error_text)

    def test_B_000036(self):
        """Ensure Correct Web apps show in Open With"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "ToolResource")
        NewResource.configure(self.driver, "TEST Web App")
        NewResource.create(self.driver)
        WebApp.support_resource_type(self.driver, "CompositeResource")
        WebApp.set_app_launching_url(self.driver, "https://www.hydroshare.org")
        WebApp.view(self.driver)
        WebApp.add_to_open_with(self.driver)
        WebApp.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "TEST Web App Composite")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.open_with_by_title(self.driver, "TEST Web App")

    def test_B_000038(self):
        """ Ensure invalid logins generate a helpful error message """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "Invalid", "Invalid")
        self.assertIn("username", Login.get_login_error(self.driver))
        self.assertIn("password", Login.get_login_error(self.driver))
        Login.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.toggle_get_started(self.driver)
        Home.toggle_get_started(self.driver)

    def test_B_000039(self):
        """ Ensure pre-login My Resources redirects to My Resources after login """
        LandingPage.to_my_resources(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        MyResources.enter_search(self.driver, "Search bar text")

    def test_B_000041(self):
        """ Update profile About information """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.update_about(
            self.driver, "// TODO My Profile Description", "United States", "New York"
        )
        Profile.save_changes(self.driver)

    def test_B_000046(self):
        """ Ensure clicking the Hydroshare logo links back to the home page """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_landing_page(self.driver)
        LandingPage.slide_hero_right(self.driver)

    def test_B_000047(self):
        """ Ensure DEBUG=false for production hydroshare.org """
        TestSystem.to_url(
            self.driver, "https://www.hydroshare.org/landingPageDoesNotExist/"
        )
        LandingPage.to_landing_page(self.driver)

    def test_B_000048(self):
        """ Ensure pre-login My Groups redirects to My Groups after login """
        LandingPage.to_collaborate(self.driver)
        Collaborate.to_groups(self.driver)
        Groups.to_my_groups(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        self.assertEqual("My Groups", Groups.get_title(self.driver))

    def test_B_000049(self):
        """ Ensure user can logout after logging in """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)

    def test_B_000050(self):
        """ Ensure the support email mailto is in the site footer """
        self.assertEqual("mailto:help@cuahsi.org", LandingPage.get_support_email(self.driver))

    def test_B_000051(self):
        """ Ensure all Getting Started links open correctly, and in the same tab """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        for row in [1, 2]:
            for column in [1, 2, 3]:
                Home.check_getting_started_link(self.driver, row, column)
                Hydroshare.to_landing_page(self.driver)
                TestSystem.wait()
                TestSystem.back(self.driver)
                TestSystem.wait()
                TestSystem.back(self.driver)

    def test_B_000052(self):
        """ Verify Recently Visited resources and authors link to valid pages """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        recent_activity_len = Home.get_recent_activity_length(self.driver)
        for i in range(1, recent_activity_len + 1):
            link_title, resource_title = Home.check_recent_activity_resource(
                self.driver, i
            )
            self.assertEqual(link_title, resource_title)
        for i in range(1, recent_activity_len + 1):
            link_author, profile_author = Home.check_recent_activity_author(
                self.driver, i
            )
            for word in [profile_author.split(" ")[0], profile_author.split(" ")[-1]]:
                self.assertIn(word, link_author)

    def test_B_000056(self):
        """ Verify featured apps featured on the dashboard link correctly """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        featured_apps = [
            "JupyterHub",
            "Tethys"
        ]
        for i in range(0, 2):
            Home.to_app(self.driver, "Featured", i+1)
            self.assertIn(featured_apps[i], TestSystem.title(self.driver))
            External.switch_old_page(self.driver)
            External.close_new_page(self.driver)

    def test_B_000057(self):
        """ Verify CUAHSI apps mentioned on the dashboard link correctly """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        cuahsi_apps = [
            "HydroClient",
            "HydroServerTools"
        ]
        for i in range(0, 2):
            Home.to_app(self.driver, "CUAHSI", i+1)
            self.assertIn(cuahsi_apps[i], TestSystem.title(self.driver))
            External.switch_old_page(self.driver)
            External.close_new_page(self.driver)

    def test_B_000058(self):
        """ Confirm My Resources table title and author links redirect to reasonable pages """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Linking Test Resource")
        NewResource.create(self.driver)
        Resource.to_my_resources(self.driver)
        MyResources.to_resource_from_table(self.driver, 1)
        self.assertIn("Linking Test Resource", TestSystem.title(self.driver))
        TestSystem.back(self.driver)
        MyResources.to_author_from_table(self.driver, 1)
        self.assertIn("User profile", TestSystem.title(self.driver))
        TestSystem.back(self.driver)

    def test_B_000059(self):
        """ Confirm favorite star/unstar/filter works on MyResources """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Favorite Resource Test")
        NewResource.create(self.driver)
        Resource.to_my_resources(self.driver)
        MyResources.favorite_resource(self.driver, 1)
        # "Owned by me filter", which is default checked
        MyResources.filter_table(self.driver, "owned")
        # Should still be visible, because it is favorited
        MyResources.favorite_resource(self.driver, 1)
        MyResources.filter_table(self.driver, "owned")

    def test_B_000060(self):
        """ Ensure new resources are default private """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Private Test Resource")
        NewResource.create(self.driver)
        Resource.to_my_resources(self.driver)
        resource_href = MyResources.get_resource_link(self.driver, 1)
        Resource.logout(self.driver)
        TestSystem.to_url(self.driver, resource_href)
        Login.login(self.driver, USERNAME, PASSWORD)
        self.assertIn("Private Test Resource", TestSystem.title(self.driver))


class JupyterhubTestSuite(BaseTestSuite):
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
        JupyterHub.authorize_jupyterhub(self.driver)
        JupyterHub.select_scientific_spawner(self.driver)
        JupyterHub.sort_notebooks_by_name(self.driver)


# Health cases definition
class HydroshareSpamSuite(HydroshareTestSuite):
    """ Python unittest setup for health checks """

    def setUp(self):
        super(HydroshareSpamSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_C_000001(self):
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

        Home.to_sitemap(self.driver)
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
            r"\breservation\b",
            "vacation[al]?",
            "ticket[s]?",
            r"\baccount\b",
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
            r"\bchrome\b",
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
        # verifyme_resources = check_links_against_patterns(links, verifyme_patterns)
        # print_formatted_result(verifyme_resources, classification="potentially useless")


if __name__ == "__main__":
    parse_args_run_tests(HydroshareTestSuite)
