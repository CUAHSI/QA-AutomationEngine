""" Runs various smoke tests for the hydroshare.org """
import boto3
import inspect
import json
import os
import random
import re
import requests
import time

from botocore.config import Config
from google.cloud import vision
from urllib.request import urlretrieve

# from percy import percySnapshot

from hs_macros import (
    Downloads,
    MatlabOnline,
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
    JupyterHubNotebooks,
    JupyterHubNotebook,
    Utilities,
)

from cuahsi_base.cuahsi_base import BaseTestSuite, parse_args_run_tests
from cuahsi_base.utils import kinesis_record, External, TestSystem
from config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
    GITHUB_ORG,
    GITHUB_REPO,
)

SPAM_DATA_STREAM_NAME = "cuahsi-quality-spam-data-stream"
SPAM_DATA_STREAM_CONFIG = Config(
    region_name="us-east-2",
)

# Test cases definition
class HydroshareTestSuite(BaseTestSuite):
    """Python unittest setup for functional tests"""

    def setUp(self):
        super(HydroshareTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_B_000001(self):
        """
        When creating a resource, ensure all resource types have a "Cancel"
        button available, so that they are not forced to finish creating a resource
        if they don't actually want one or if they made a mistake
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        resource_types = [
            "CompositeResource",
            "CollectionResource",
            "ToolResource",
        ]
        for resource_type in resource_types:
            Home.create_resource(self.driver, resource_type)
            NewResource.configure(self.driver, "TEST TITLE")
            NewResource.cancel(self.driver)

    def test_B_000003(self):
        """
        Confirms the Beaver Divide Air Temperature example resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive to make sure it downloads successfully
        """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Castronova, Anthony",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Resource.download_bagit(self.driver)
        self.assertTrue(Downloads.check_successful_download_new_tab(self.driver))

    def test_B_000005(self):
        """
        Confirms user passwords can be changed, and then changed back
        to the original value, using the Profile interface
        """
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
        Discover.add_filters(
            self.driver,
            availability=["published"],
        )  # remove once long delay issue is fixed
        orderings = [
            {
                "name": "First Author",
                "column": 3,
            },
            {
                "name": "Date Created",
                "column": 4,
            },
            {
                "name": "Last Modified",
                "column": 5,
            },
        ]
        for ordering in orderings:
            Discover.set_sort(self.driver, ordering["column"])
            TestSystem.wait()  # remove once long delay issue is fixed
            self.assertTrue(
                Discover.check_sorting_multi(self.driver, ordering["name"], "Ascending")
            )
            Discover.set_sort(self.driver, ordering["column"])
            TestSystem.wait()  # remove once long delay issue is fixed
            self.assertTrue(
                Discover.check_sorting_multi(
                    self.driver, ordering["name"], "Descending"
                )
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
        Checks all HydroShare Help links lead to valid pages
        and that the topic title words come up in the associated help page
        """
        LandingPage.to_help(self.driver)
        core_count = Help.get_core_count(self.driver)
        core_topics = [
            Help.get_core_topic(self.driver, i + 1) for i in range(0, core_count)
        ][
            :-3
        ]  # Last three topics include mailto: contact emails
        for ind, core_topic in enumerate(core_topics, 1):  # xpath ind start at 1
            Help.open_core(self.driver, ind)
            words_string = re.sub("[^A-Za-z]", " ", core_topic)
            matches = [
                word in HelpArticle.get_title(self.driver)
                for word in words_string.split(" ")
            ]
            self.assertTrue(True in matches)
            HelpArticle.to_help_breadcrumb(self.driver)

    def test_B_000009(self):
        """
        Confirms the basic get methods within hydroshare api do not return
        errors.  These basic get methods are accessible from the Swagger UI and
        use just a resource id required parameter
        """
        resource_id = "54ae2ade31f646d097d78ef0695bb36c"
        endpoints = [
            {"id": "operations-resource-resource_read", "resource_param_ind": 1},
            {
                "id": "operations-resource-resource_file_list_list",
                "resource_param_ind": 3,
            },
            {
                "id": "operations-resource-resource_files_list",
                "resource_param_ind": 3,
            },
            {"id": "operations-resource-resource_map_list", "resource_param_ind": 1},
            {
                "id": "operations-resource-resource_scimeta_list",
                "resource_param_ind": 1,
            },
            {
                "id": "operations-resource-resource_scimeta_elements_read",
                "resource_param_ind": 1,
            },
            {
                "id": "operations-resource-resource_sysmeta_list",
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
        no parameters, can be ran through the Swagger UI
        """
        endpoints = [
            "operations-resource-resource_content_types_list",
            "operations-resource-resource_types_list",
            "operations-user-user_list",
            "operations-userInfo-userInfo_list",
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
        """
        Check Hydroshare About policy pages to confirm link titles, content titles, and page titles all align
        """
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
        self.assertNotIn("Page not found", TestSystem.title(self.driver))

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
        Confirms ability to create HydroShare groups through the standard
        GUI workflow
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
        """
        Confirms the resource landing page "Open With" works, in the case of JupyterHub
        """
        LandingPage.to_discover(self.driver)
        Discover.add_filters(self.driver, owner="Castronova, Anthony")
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Resource.open_with_jupyterhub(self.driver)
        webpage_title = TestSystem.title(self.driver)
        self.assertNotIn("Page not found", webpage_title)

    def test_B_000016(self):
        """
        Create a basic resource without any files and confirm that the resulting
        resource landing page is OK
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Test Resource")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        resource_title = Resource.get_title(self.driver)
        self.assertEqual("Test Resource", resource_title)

    def test_B_000017(self):
        """
        Confirm resource type filters can be applied in My Resources
        """
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
        resources on the My Resources page
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
        """
        Confirm the ability to upload a CV file within the profile interface
        """
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.upload_cv(
            self.driver,
            "https://www.bu.edu/careers/files/2012/08/Resume-Guide-2012.pdf",
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
        """
        Confirm profile image upload and removal works, within the profile page
        """
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
        self.assertTrue(Profile.confirm_photo_uploaded(self.driver, "profile"))
        os.remove(profile_img_path)
        Profile.to_editor(self.driver)
        Profile.remove_photo(self.driver)
        self.assertFalse(Profile.confirm_photo_uploaded(self.driver, "profile"))

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
        """Verify the ability to extend metadata on resource landing pages"""
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
        """Confirm that the home page slider is functional"""
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
        """Commenting requires a login, and redirect works as expected"""
        LandingPage.to_discover(self.driver)
        Discover.search(self.driver, "DeBuhr")
        Discover.add_filters(self.driver, owner="DeBuhr, Neal")
        Discover.to_resource(
            self.driver, "Beaver Divide Air Temperature - Further Development"
        )
        initial_comment_count = Resource.get_comment_count(self.driver)
        Resource.add_comment(self.driver, "Test Comment")
        self.assertIn("Please log in", Login.get_notification(self.driver))
        Login.login(self.driver, USERNAME, PASSWORD)
        Resource.add_comment(self.driver, "Test Comment")
        final_comment_count = Resource.get_comment_count(self.driver)
        self.assertTrue(initial_comment_count < final_comment_count)

    def test_B_000031(self):
        """Confirm that resources can be accessed from the sitemap links"""
        LandingPage.to_sitemap(self.driver)
        SiteMap.select_resource(self.driver, "Beaver Divide Air Temperature - Demo")
        self.assertIn(
            "Beaver Divide Air Temperature - Demo", TestSystem.title(self.driver)
        )
        TestSystem.back(self.driver)
        SiteMap.select_resource(self.driver, "Beaver Divide Air Temperature - Demo")
        self.assertIn(
            "Beaver Divide Air Temperature - Demo", TestSystem.title(self.driver)
        )
        TestSystem.back(self.driver)

    def test_B_000032(self):
        """Confirm that the hydroshare footer version number matches up with the
        latest version number in GitHub"""
        displayed_release_version = LandingPage.get_version(self.driver)
        expected_release_version = LandingPage.get_latest_release(
            GITHUB_ORG, GITHUB_REPO
        )
        self.assertEqual(expected_release_version, displayed_release_version)

    def test_B_000033(self):
        """Ensure Discover page refresh clears all filters"""
        LandingPage.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Myers, Jessie",
            contributor="Cox, Chris",
            owner="Christopher, Adrian",
            subject="USACE Corps Water Management System (CWMS)",
            availability="public",
        )
        TestSystem.refresh(self.driver)
        TestSystem.wait(3)
        self.assertFalse(Discover.is_selected(self.driver, author="Myers, Jessie"))
        self.assertFalse(Discover.is_selected(self.driver, contributor="Cox, Chris"))
        self.assertFalse(Discover.is_selected(self.driver, owner="Christopher, Adrian"))
        self.assertFalse(
            Discover.is_selected(
                self.driver, subject="USACE Corps Water Management System (CWMS)"
            )
        )
        self.assertFalse(Discover.is_selected(self.driver, availability="public"))

    def test_B_000034(self):
        """Basic navigation to home/dashboard"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.toggle_get_started(self.driver)
        visibility = [Home.is_get_started_showing(self.driver)]
        Home.toggle_get_started(self.driver)
        visibility += [Home.is_get_started_showing(self.driver)]
        Home.to_home(self.driver)
        self.assertNotEqual(visibility[0], visibility[1])

    def test_B_000035(self):
        """Ensure registration prompts for Organization entry"""
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
        """Ensure invalid logins generate a helpful error message"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "Invalid", "Invalid")
        self.assertIn("username", Login.get_login_error(self.driver))
        self.assertIn("password", Login.get_login_error(self.driver))
        Login.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.toggle_get_started(self.driver)
        Home.toggle_get_started(self.driver)

    def test_B_000039(self):
        """Ensure pre-login My Resources redirects to My Resources after login"""
        LandingPage.to_my_resources(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        MyResources.enter_search(self.driver, "Search bar text")

    def test_B_000040(self):
        """Ensure invalid login messages are identical"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, "Invalid")
        self.assertIn(
            "Invalid username/email and password", Login.get_login_error(self.driver)
        )
        Login.to_login(self.driver)
        Login.login(self.driver, "Invalid", PASSWORD)
        self.assertIn(
            "Invalid username/email and password", Login.get_login_error(self.driver)
        )
        Login.to_login(self.driver)
        Login.login(self.driver, "Invalid", "Invalid")
        self.assertIn(
            "Invalid username/email and password", Login.get_login_error(self.driver)
        )
        Login.to_login(self.driver)

    def test_B_000041(self):
        """Update profile About information"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.update_about(
            self.driver, "// TODO My Profile Description", "United States", "New York"
        )
        Profile.save_changes(self.driver)

    def test_B_000046(self):
        """Ensure clicking the Hydroshare logo links back to the home page"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_landing_page(self.driver)
        LandingPage.slide_hero_right(self.driver)

    def test_B_000047(self):
        """Ensure DEBUG=false for production hydroshare.org"""
        TestSystem.to_url(
            self.driver, "https://www.hydroshare.org/landingPageDoesNotExist/"
        )
        LandingPage.to_landing_page(self.driver)

    def test_B_000048(self):
        """Ensure pre-login My Groups redirects to My Groups after login"""
        LandingPage.to_collaborate(self.driver)
        Collaborate.to_groups(self.driver)
        Groups.to_my_groups(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        self.assertEqual("My Groups", Groups.get_title(self.driver))

    def test_B_000049(self):
        """Ensure user can logout after logging in"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.logout(self.driver)

    def test_B_000050(self):
        """Ensure the support email mailto is in the site footer"""
        self.assertEqual(
            "mailto:help@cuahsi.org", LandingPage.get_support_email(self.driver)
        )

    def test_B_000051(self):
        """Ensure all Getting Started links open correctly, and in the same tab"""
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
        """Verify Recently Visited resources and authors link to valid pages"""
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

    def test_B_000053(self):
        """Ensure private resources are not shown for anonymous viewers on the contributions profile page"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.view_contributions(self.driver)
        initial_count = Profile.get_contribution_type_count(self.driver, 0)
        Profile.to_home(self.driver)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Private Contributions Test Resource")
        NewResource.create(self.driver)
        NewResource.to_profile(self.driver)
        Profile.view_contributions(self.driver)
        incremented_count = Profile.get_contribution_type_count(self.driver, 0)
        self.assertTrue(initial_count + 1 == incremented_count)
        Resource.logout(self.driver)
        TestSystem.to_url(self.driver, BASE_URL + "/user/3887/")
        Profile.view_contributions(self.driver)
        public_count = Profile.get_contribution_type_count(self.driver, 0)
        self.assertTrue(public_count < initial_count)

    def test_B_000055(self):
        """Verify featured apps featured on the dashboard link correctly"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        # JupyterHub
        Home.to_app(self.driver, "Featured", 1)
        self.assertIn("JupyterHub", TestSystem.title(self.driver))
        External.switch_old_page(self.driver)
        External.close_new_page(self.driver)
        # MATLAB Online
        TestSystem.to_url(self.driver, "http://matlab-launcher.cuahsi.org")
        # Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.wait(30)
        MatlabOnline.authorize(self.driver)
        TestSystem.wait(120)
        self.assertIn("MATLAB Online", TestSystem.title(self.driver))
        # External.switch_old_page(self.driver)
        # External.close_new_page(self.driver)

    def hold_test_B_000056(self):
        """Verify featured apps featured on the dashboard link correctly"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        # JupyterHub
        Home.to_app(self.driver, "Featured", 1)
        self.assertIn("JupyterHub", TestSystem.title(self.driver))
        External.switch_old_page(self.driver)
        External.close_new_page(self.driver)
        # MATLAB Online
        Home.to_app(self.driver, "Featured", 2)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.wait(30)
        MatlabOnline.authorize(self.driver)
        TestSystem.wait(30)
        self.assertIn("MATLAB Online", TestSystem.title(self.driver))
        External.switch_old_page(self.driver)
        External.close_new_page(self.driver)

    def test_B_000057(self):
        """Verify CUAHSI apps mentioned on the dashboard link correctly"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        cuahsi_apps = ["HydroClient", "HydroServerTools"]
        for i in range(0, 2):
            Home.to_app(self.driver, "CUAHSI", i + 1)
            self.assertIn(cuahsi_apps[i], TestSystem.title(self.driver))
            External.switch_old_page(self.driver)
            External.close_new_page(self.driver)

    def test_B_000058(self):
        """Confirm My Resources table title and author links redirect to reasonable pages"""
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
        """Confirm favorite star/unstar/filter works on MyResources"""
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
        """Ensure new resources are default private"""
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

    def test_B_000064(self):
        """Ensure title renders properly for a sample of resources"""
        Home.to_sitemap(self.driver)
        links = SiteMap.get_resource_list(self.driver)
        print(len(links))
        for i in range(0, len(links), 761):
            SiteMap.select_resource_by_index(self.driver, i)
            self.assertTrue(len(Resource.get_title(self.driver)) > 0)
            print(Resource.get_title(self.driver))
            TestSystem.back(self.driver)

    def test_B_000073(self):
        """Adding and removing a resource reference works properly"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Resource Reference Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.edit(self.driver)
        Resource.add_reference(self.driver, "First Principles")
        Resource.delete_reference(self.driver)
        Resource.add_reference(self.driver, "First Principles")
        Resource.delete_reference(self.driver)

    def test_B_000075(self):
        """Confirm making a resource public requires the prerequisite metadata to be filled out
        and that the notice about this stays visible in view and edit modes"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Making Resource Public Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.edit(self.driver)
        Resource.populate_abstract(self.driver, "// TODO Abstract")
        Resource.view(self.driver)
        Resource.edit(self.driver)
        Resource.is_visible_public_resource_notice(self.driver)
        Resource.add_subject_keyword(self.driver, "keyphrase multiple words")
        Resource.view(self.driver)
        Resource.is_visible_public_resource_notice(self.driver)

    def test_B_000085(self):
        """Copy a resource"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Castronova, Anthony",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Discover.clear_notifications(self.driver)
        Resource.copy_resource(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        self.assertTrue(
            "Beaver Divide Air Temperature" in Resource.get_title(self.driver)
        )

    def test_B_000086(self):
        """Confirm basic resource versioning"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Castronova, Anthony",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Discover.clear_notifications(self.driver)
        Resource.copy_resource(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.create_version(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        TestSystem.back(self.driver)
        try:
            Resource.edit(self.driver)
            # Old resource should no longer be editable
            self.assertTrue(False)
        except:
            TestSystem.wait(1)

    def test_B_000087(self):
        """Validate version rollback, through resource deletion"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Castronova, Anthony",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Discover.clear_notifications(self.driver)
        Resource.copy_resource(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        resource_copy = TestSystem.current_url(self.driver)
        Resource.create_version(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.delete_resource(self.driver)
        TestSystem.wait(20)
        TestSystem.refresh(self.driver)
        self.assertIn("My Resources", TestSystem.title(self.driver))
        TestSystem.back(self.driver)
        # Deleted new version
        self.assertIn("Page not found", TestSystem.title(self.driver))
        # Now editable old version
        TestSystem.to_url(self.driver, resource_copy)
        try:
            Resource.edit(self.driver)
        except:
            self.assertTrue(False)

    def test_B_000088(self):
        """Confirm My Resources lists the latest resource version"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            author="Castronova, Anthony",
            resource_type="Composite",
            availability=["discoverable", "public"],
        )
        Discover.to_resource(self.driver, "Beaver Divide Air Temperature")
        Discover.clear_notifications(self.driver)
        Resource.copy_resource(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.edit(self.driver)
        Resource.set_title(self.driver, "Old Version - Test")
        Resource.view(self.driver)
        Resource.create_version(self.driver)
        TestSystem.wait(20)
        Resource.use_notification_link(self.driver, 1)
        Resource.edit(self.driver)
        Resource.set_title(self.driver, "New Version - Test")
        Resource.view(self.driver)
        Resource.to_my_resources(self.driver)
        MyResources.to_resource_from_table(self.driver, 1)
        TestSystem.wait()
        self.assertEqual(Resource.get_title(self.driver), "New Version - Test")
        Resource.delete_resource(self.driver)
        TestSystem.wait(20)
        Resource.to_my_resources(self.driver)
        MyResources.to_resource_from_table(self.driver, 1)
        TestSystem.wait()
        self.assertEqual(Resource.get_title(self.driver), "Old Version - Test")
        try:
            Resource.edit(self.driver)
        except:
            # Old resource version should be editable, after the newer one is deleted
            self.assertTrue(False)

    def test_B_000089(self):
        """Confirm core resource sharing (viewer) functionality"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Sharing Resource Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.grant_viewer(self.driver, "selenium-user2")
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 2)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user2", "abc123")
        self.driver.get(resource_url)
        self.assertEqual(Resource.get_title(self.driver), "Sharing Resource Test")

    def test_B_000091(self):
        """Confirm editor sharing"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Editor Resource Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.grant_editor(self.driver, "selenium-user3")
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 2)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user3", "abc123")
        self.driver.get(resource_url)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        self.assertEqual(Resource.get_title(self.driver), "Editor Resource Test")

    def test_B_000092(self):
        """Confirm owner sharing"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Owner Resource Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.grant_owner(self.driver, "selenium-user4")
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 2)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user4", "abc123")
        self.driver.get(resource_url)
        Resource.delete_resource(self.driver)
        TestSystem.wait(20)
        TestSystem.back(self.driver)
        TestSystem.refresh(self.driver)
        self.assertIn("Page not found", TestSystem.title(self.driver))

    def test_B_000094(self):
        """Confirm sharable functionality with a share chain"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Sharable Chain Resource Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.grant_editor(self.driver, "selenium-user5")
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 2)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user5", "abc123")
        self.driver.get(resource_url)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        Resource.grant_editor(self.driver, "selenium-user6")
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 3)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user6", "abc123")
        self.driver.get(resource_url)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        self.assertEqual(
            Resource.get_title(self.driver), "Sharable Chain Resource Test"
        )

    def test_B_000095(self):
        """Confirm the ability to block sharable functionality with the sharable setting"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Sharable Chain Resource Test")
        NewResource.create(self.driver)
        Resource.view(self.driver)
        Resource.grant_editor(self.driver, "selenium-user5")
        Resource.toggle_sharable(self.driver)
        users_with_access = Resource.get_user_access_count(self.driver)
        resource_url = TestSystem.current_url(self.driver)
        self.assertEqual(users_with_access, 2)
        Resource.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, "selenium-user5", "abc123")
        self.driver.get(resource_url)
        Resource.edit(self.driver)
        Resource.view(self.driver)
        try:
            Resource.grant_editor(self.driver, "selenium-user6")
            self.assertTrue(False)  # Selenium-User5 should not be able to share
        except:
            TestSystem.wait(1)

    def test_B_000096(self):
        """Update profile contact information"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.update_contact(
            self.driver,
            phone1="555-555-5555",
            phone2="555-555-5555",
            email="jim@example.com",
            website="example.com",
        )
        Profile.save_changes(self.driver)

    def test_B_000097(self):
        """Update profile name matches logout interface name"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        self.assertEqual(
            Profile.get_logged_in_name(self.driver), Profile.get_name(self.driver)
        )

    def test_B_000098(self):
        """Update profile email matches logout interface name"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        self.assertEqual(
            Profile.get_logged_in_name(self.driver), Profile.get_name(self.driver)
        )
        Profile.to_editor(self.driver)
        self.assertEqual(
            Profile.get_logged_in_email(self.driver), Profile.get_email(self.driver)
        )

    def test_B_000099(self):
        """Ensure the total for each author matches the total when the author filter is applied in Discover"""
        LandingPage.to_discover(self.driver)
        for i in range(1, 20, 4):
            Discover.toggle_author_filter_by_index(self.driver, i)
            filter_count = Discover.get_author_resource_count_by_index(self.driver, i)
            table_count = Discover.count_results_in_table(self.driver)
            Discover.toggle_author_filter_by_index(self.driver, i)
            self.assertEqual(filter_count, table_count)

    def test_B_000100(self):
        """Ensure the total for each contributor matches the total when the contributor filter is applied in Discover"""
        LandingPage.to_discover(self.driver)
        for i in range(2, 20, 4):
            Discover.toggle_contributor_filter_by_index(self.driver, i)
            filter_count = Discover.get_contributor_resource_count_by_index(
                self.driver, i
            )
            table_count = Discover.count_results_in_table(self.driver)
            Discover.toggle_contributor_filter_by_index(self.driver, i)
            self.assertEqual(filter_count, table_count)

    def test_B_000101(self):
        """Ensure the total for each owner matches the total when the owner filter is applied in Discover"""
        LandingPage.to_discover(self.driver)
        for i in range(3, 20, 4):
            Discover.toggle_owner_filter_by_index(self.driver, i)
            filter_count = Discover.get_owner_resource_count_by_index(self.driver, i)
            table_count = Discover.count_results_in_table(self.driver)
            Discover.toggle_owner_filter_by_index(self.driver, i)
            self.assertEqual(filter_count, table_count)

    def test_B_000102(self):
        """Confirm dates are formatted consistently across resources in the results table"""
        LandingPage.to_discover(self.driver)
        Discover.uses_consistent_date_formatting(self.driver)

    def test_B_000103(self):
        """Ensure resource logos are consistent within each resource type"""
        LandingPage.to_discover(self.driver)
        for i in range(3, Discover.get_count_of_types(self.driver), 7):
            Discover.toggle_type_filter_by_index(self.driver, i)
            self.assertTrue(Discover.uses_consistent_icon(self.driver))
            Discover.toggle_type_filter_by_index(self.driver, i)

    def test_B_000105(self):
        """Ensure the total for each resource type matches the total when the resource type filter is applied in Discover"""
        LandingPage.to_discover(self.driver)
        for i in range(4, Discover.get_count_of_types(self.driver), 3):
            Discover.toggle_type_filter_by_index(self.driver, i)
            filter_count = Discover.get_type_resource_count_by_index(self.driver, i)
            table_count = Discover.count_results_in_table(self.driver)
            Discover.toggle_type_filter_by_index(self.driver, i)
            self.assertEqual(filter_count, table_count)

    def test_B_000106(self):
        """Ensure the listed first author in the Discover page is listed as an author on the resource page"""
        LandingPage.to_discover(self.driver)
        # Get a pseudo-random sample by taking the first result of a few random string searches
        search_strings = [
            "Berlin",
            "CUAHSI",
            "99",
            "Estuary",
            "New York",
            "Precipitation",
            "Ice",
            "Antarctica",
            "Phosphorus",
            "Leak",
            "Database",
        ]
        for search_string in search_strings:
            Discover.search(self.driver, search_string)
            first_author = Discover.get_first_author_by_resource_index(self.driver, 1)
            Discover.to_resource_by_index(self.driver, 1)  # first row, second column
            authors_csv = ", ".join(Resource.get_authors(self.driver))
            for name_part in first_author.replace(",", "").split(" "):
                self.assertIn(name_part, authors_csv)
            External.switch_old_page(self.driver)
            External.close_new_page(self.driver)

    def test_B_000109(self):
        """
        Confirms Beaver Divide Air Temperature resource landing page is
        online via navigation and title check, then downloads the BagIt
        archive and confirms the BagIt file size matches expectation
        """
        LandingPage.to_discover(self.driver)
        Discover.search(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Discover.to_resource(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Resource.download_bagit(self.driver)
        TestSystem.wait()
        TestSystem.to_url(self.driver, "chrome://downloads")
        Downloads.check_successful_download(self.driver)

    def test_B_000110(self):
        """
        Confirms file downloads within a resource are successful
        """
        LandingPage.to_discover(self.driver)
        Discover.search(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Discover.to_resource(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Resource.download_file_by_index(self.driver, 2)
        TestSystem.wait(10)
        TestSystem.to_url(self.driver, "chrome://downloads")
        Downloads.check_successful_download(self.driver)

    def test_B_000111(self):
        """
        Confirms file zip downloads within a resource are successful
        """
        LandingPage.to_discover(self.driver)
        Discover.search(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Discover.to_resource(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Resource.download_file_zip_by_index(self.driver, 3)
        TestSystem.wait(10)
        TestSystem.to_url(self.driver, "chrome://downloads")
        Downloads.check_successful_download(self.driver)

    def test_B_000112(self):
        """
        Confirms the resource file download links are valid
        """
        LandingPage.to_discover(self.driver)
        Discover.search(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        Discover.to_resource(
            self.driver,
            "Waterhackweek 2019 Cyberseminar: Jupyter notebooks and workflows on Hydroshare",
        )
        file_download_link = Resource.get_file_download_link_by_index(self.driver, 1)
        TestSystem.to_url(self.driver, file_download_link)
        TestSystem.wait(10)
        TestSystem.to_url(self.driver, "chrome://downloads")
        Downloads.check_successful_download(self.driver)

    def test_B_000113(self):
        """
        Download and upload a 541 MB file from the API, then download it from the GUI
        """
        urlretrieve(
            BASE_URL
            + "/resource/a7b99c31adfe4f56899bef1a6700f9cf/data/contents/1m_snowOff_filter_SHD.zip",
            "1m_snowOff_filter_SHD.zip",
        )
        r = requests.post(
            BASE_URL + "/hsapi/resource/",
            auth=(USERNAME, PASSWORD),
            data={
                "title": "Automated Test Resource CUAHSI QA",
                "abstract": "This is a test resource for QA purposes.",
                "keywords": ["test", "QA", "CUAHSI"],
            },
        )
        resource_id = r.json()["resource_id"]
        files = {"file": open("1m_snowOff_filter_SHD.zip", "rb")}
        r = requests.post(
            BASE_URL + "/hsapi/resource/{}/files/".format(resource_id),
            auth=(USERNAME, PASSWORD),
            files=files,
        )
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.to_url(self.driver, BASE_URL + "/resource/{}/".format(resource_id))
        Resource.download_bagit(self.driver)
        TestSystem.wait(10)
        self.assertTrue(Downloads.check_successful_download_new_tab(self.driver))

    def test_B_000115(self):
        """Confirms password reset is not confirmed unless submit is clicked"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.to_profile(self.driver)
        Profile.to_editor(self.driver)
        Profile.queue_password_change(self.driver, PASSWORD, PASSWORD + "test")
        Home.logout(self.driver)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD + "test")
        self.assertIn(
            "Invalid username/email and password", Login.get_login_error(self.driver)
        )

    def test_B_000117(self):
        """Create a discoverable resource"""
        urlretrieve(
            BASE_URL
            + "/resource/a7b99c31adfe4f56899bef1a6700f9cf/data/contents/1m_snowOff_filter_SHD.zip",
            "1m_snowOff_filter_SHD.zip",
        )
        r = requests.post(
            BASE_URL + "/hsapi/resource/",
            auth=(USERNAME, PASSWORD),
            data={
                "title": "Discoverable Resource CUAHSI QA",
                "abstract": "This is a test resource for QA purposes.",
                "keywords": ["test", "QA", "CUAHSI"],
            },
        )
        resource_id = r.json()["resource_id"]
        files = {"file": open("1m_snowOff_filter_SHD.zip", "rb")}
        r = requests.post(
            BASE_URL + "/hsapi/resource/{}/files/".format(resource_id),
            auth=(USERNAME, PASSWORD),
            files=files,
        )
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.to_url(self.driver, BASE_URL + "/resource/{}/".format(resource_id))
        Resource.edit(self.driver)
        Resource.make_discoverable(self.driver)
        Resource.logout(self.driver)
        LandingPage.to_discover(self.driver)
        Discover.add_filters(
            self.driver,
            availability=["discoverable"],
        )
        Discover.to_resource(self.driver, "Discoverable Resource CUAHSI QA")

    def test_B_000118(self):
        """Confirm the addition and deletion of metadata works for both point and box coverage"""
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "CompositeResource")
        NewResource.configure(self.driver, "Spatial Coverage Test")
        NewResource.create(self.driver)
        Resource.set_spatial_coverage_box(self.driver, 44, 43, 42, 41)
        Resource.delete_spatial_coverage(self.driver)
        TestSystem.wait()
        Resource.set_spatial_coverage_point(self.driver, 42, 42)
        Resource.delete_spatial_coverage(self.driver)

    def test_B_000119(self):
        """Comfirm a warning message when making a resource no longer public-compatible"""
        urlretrieve(
            BASE_URL
            + "/resource/a7b99c31adfe4f56899bef1a6700f9cf/data/contents/1m_snowOff_filter_SHD.zip",
            "1m_snowOff_filter_SHD.zip",
        )
        r = requests.post(
            BASE_URL + "/hsapi/resource/",
            auth=(USERNAME, PASSWORD),
            data={
                "title": "Discoverable Resource CUAHSI QA",
                "abstract": "This is a test resource for QA purposes.",
                "keywords": ["test", "QA", "CUAHSI"],
            },
        )
        resource_id = r.json()["resource_id"]
        files = {"file": open("1m_snowOff_filter_SHD.zip", "rb")}
        r = requests.post(
            BASE_URL + "/hsapi/resource/{}/files/".format(resource_id),
            auth=(USERNAME, PASSWORD),
            files=files,
        )
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.to_url(self.driver, BASE_URL + "/resource/{}/".format(resource_id))
        Resource.edit(self.driver)
        Resource.populate_abstract(self.driver, "// TODO Abstract")
        Resource.add_subject_keyword(self.driver, "keyphrase multiple words")
        Resource.make_public(self.driver)
        Resource.view(self.driver)
        self.assertEqual(Resource.get_sharing_status(self.driver), "Public")
        Resource.edit(self.driver)
        Resource.delete_file_by_index(self.driver, 1)
        Resource.view(self.driver)
        self.assertEqual(Resource.get_sharing_status(self.driver), "Private")
    
    def test_B_000120(self):
        """
        Confirm profile image upload for .svg files
        """
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

        Profile.to_editor(self.driver)
        urlretrieve(
            "https://upload.wikimedia.org/wikipedia/commons/0/02/SVG_logo.svg", "profile.svg"
        )
        cwd = os.getcwd()
        img_path = os.path.join(cwd, "profile.svg")
        Profile.add_photo(self.driver, profile_img_path)
        Profile.save_changes(self.driver)
        self.assertTrue(Profile.confirm_photo_uploaded(self.driver, "profile"))
        os.remove(profile_img_path)
        Profile.to_editor(self.driver)
        Profile.remove_photo(self.driver)
        self.assertFalse(Profile.confirm_photo_uploaded(self.driver, "profile"))

class PerformanceTestSuite(BaseTestSuite):
    """Python unittest setup for smoke tests"""

    def setUp(self):
        super(PerformanceTestSuite, self).setUp()

    def test_D_000000(self):
        """
        Anonymously download a BagIt, straight from the resource landing page
        """
        resource = super(PerformanceTestSuite, self).getResourceId()
        TestSystem.to_url(self.driver, BASE_URL + "/resource/{}/".format(resource))
        Resource.download_bagit(self.driver)
        TestSystem.wait()
        Resource.wait_on_task_completion(self.driver, 1, 300)
        Resource.use_notification_link(self.driver, 1)
        TestSystem.to_url(self.driver, "chrome://downloads")
        self.assertTrue(Downloads.check_successful_download(self.driver))

    def test_D_000001(self):
        """
        Login, then download a BagIt, straight from the resource landing page
        """
        resource = super(PerformanceTestSuite, self).getResourceId()
        TestSystem.to_url(self.driver, BASE_URL)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        TestSystem.to_url(self.driver, BASE_URL + "/resource/{}/".format(resource))
        Resource.download_bagit(self.driver)
        TestSystem.wait()
        Resource.wait_on_task_completion(self.driver, 1, 300)
        Resource.use_notification_link(self.driver, 1)
        TestSystem.to_url(self.driver, "chrome://downloads")
        self.assertTrue(Downloads.check_successful_download_new_tab(self.driver))

    def test_D_000002(self):
        """
        Make a set of test resources public
        """
        TestSystem.to_url(self.driver, BASE_URL)
        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)
        resource_ids = [
            # Copy resource IDs here
        ]
        for resource_id in resource_ids:
            TestSystem.to_url(
                self.driver, BASE_URL + "/resource/{}/".format(resource_id)
            )
            Resource.edit(self.driver)
            Resource.make_public(self.driver)


class JupyterhubTestSuite(HydroshareTestSuite):
    """Python unittest setup for jupyterhub testing"""

    def setUp(self):
        super(JupyterhubTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_000001(self):
        """Spawn and interact with a server"""
        TestSystem.to_url(self.driver, "https://jupyter-edu.cuahsi.org/hub/login")
        # JupyterHub.agree_to_terms_of_use(self.driver)
        JupyterHub.to_hs_login(self.driver)
        Login.login(self.driver, "selenium-user1", "abc123")
        TestSystem.wait(3)
        JupyterHub.authorize_jupyterhub(self.driver)
        # JupyterHub.select_minimal_spawner(self.driver)
        # JupyterHub.select_scientific_spawner(self.driver)
        # JupyterHub.select_r_scientific_spawner(self.driver)
        JupyterHubNotebooks.wait_on_server_creation(self.driver)
        if not JupyterHubNotebooks.is_spawner_set(self.driver):
            JupyterHubNotebooks.select_notebook_spawner(self.driver)
        JupyterHubNotebook.save_notebook(self.driver)
        TestSystem.wait(5)


# Health cases definition
class HydroshareSpamSuite(BaseTestSuite):
    """Python unittest setup for health checks"""

    vision_client = None

    def setUp(self):
        super(HydroshareSpamSuite, self).setUp()
        self.driver.get(BASE_URL)
        self.vision_client = vision.ImageAnnotatorClient()

    def send_record(self, data):
        if self.records == "aws":
            kinesis_record(
                SPAM_DATA_STREAM_CONFIG,
                SPAM_DATA_STREAM_NAME,
                "spam-user",
                data,
            )
        if self.records == "gcp":
            future = self.publisher.publish(
                self.publisher.topic_path("cuahsiqa", "spam-users"),
                json.dumps(data, ensure_ascii=False).encode("utf8"),
            )
            future.result()

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
            r"\bdeal[s]?\b",
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
            r"\bapple\b",
            "icloud",
            r"\bios\b",
            "iphone",
            r"\bmac\b",
            "macbook",
            "macos",
            "facebook",
            "microsoft",
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

    def test_C_000002(self):
        """
        Tries to identify potential spam users, via user ID sweep.
        The test will simply print all suspicious resources to stdout, there are
        no assertions in it.
        """

        patterns = [
            "amazing",
            "business",
            "cheap[est]?",
            "credit[s]?",
            "customer[s]?",
            "deal[s]?",
            "phone number",
            "price",
            "4free",
            "airline[s]?",
            "baggage",
            "booking",
            "flight[s]?",
            r"\breservation\b",
            "vacation[al]?",
            "ticket[s]?",
            # r"\baccount\b",
            "antivirus",
            "cleaner",
            "cookies",
            # r"\b[e]?mail\b",
            "laptop",
            "password",
            "mail7d.com",
            "inbox-me.top",
            "smart-email.me",
            "best service",
            "SEO services",
            "sign up",
            "sign in",
            "wi[-]?fi",
            # r'' is a 'raw' string (backslash symbol is treated as a literal
            # backslash).
            # '\b' stands for 'word boundary'.
            # r"\bgoogle\b",
            "android",
            r"\bchrome\b",
            r"\bapple\b",
            " icloud ",
            r"\bios\b",
            "iphone",
            r" mac ",
            "macbook",
            "macos",
            # "facebook",
            "microsoft",
            "internet explorer",
            "adult",
            "escort",
            "porn",
            "xxx",
        ]
        profile_picture_flags = [
            "Lingerie top",
            "Brassiere",
            "Lingerie",
            "Undergarment",
            "Gun barrel",
            "Gun",
            "Food",
            "Trigger",
            "Drugs",
            "Drug",
            "Prescription",
            "Pills",
            "Pill bottle",
            "Pill",
        ]
        full_pattern = re.compile("|".join(patterns), re.IGNORECASE)

        LandingPage.to_login(self.driver)
        Login.login(self.driver, USERNAME, PASSWORD)

        for i in range(1708, 7746):
            TestSystem.to_url(self.driver, BASE_URL + "/user/{}/".format(i))
            if "User profile" in TestSystem.title(self.driver):
                data = Profile.get_data(self.driver)
                match = re.search(
                    full_pattern, json.dumps(Profile.get_data(self.driver))
                )
                profile_picture_match = False
                if data["profile_picture"] not in [None, ""]:
                    response = self.vision_client.label_detection(
                        image={
                            "source": {"image_uri": BASE_URL + data["profile_picture"]}
                        }
                    )
                    print(
                        i, [label.description for label in response.label_annotations]
                    )
                    if any(
                        [
                            label.description in profile_picture_flags
                            for label in response.label_annotations
                        ]
                    ):
                        profile_picture_match = True
                # Link text matches one of the patterns.
                if match is not None or profile_picture_match:
                    data["id"] = i
                    data["matches"] = str(match)
                    if data["profile_picture"] not in [None, ""]:
                        data["profile_picture_labels"] = ",".join(
                            [label.description for label in response.label_annotations]
                        )
                    else:
                        data["profile_picture_labels"] = ""
                    self.send_record(data)


if __name__ == "__main__":
    parse_args_run_tests(HydroshareTestSuite)
