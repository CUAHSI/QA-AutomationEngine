""" Runs various smoke tests for the data submission portal """
import time
import unittest
import functools
from bs4 import BeautifulSoup
import datetime

from botocore.config import Config

from pathlib import Path
import contextlib

# from percy import percySnapshot

from dsp_macros import (
    Dsp,
    SubmitLandingPage,
    MySubmissions,
    OrcidWindow,
    HydroshareAuthWindow,
    GeneralSubmitToRepo,
    GeneralEditSubmission,
    SubmitHydroshare,
    EditHSSubmission,
    SubmitExternal,
    EditExternalSubmission,
    SubmitZenodo,
    EditZenodoSubmission,
    ZenodoAuthWindow,
    SubmitEarthchem,
    EditEarthchemSubmission,
    EarthchemAuthWindow,
    ZenodoResourcePage,
    HSResourcePage,
    EarthchemResourcePage,
    RepoAuthWindow,
)

from cuahsi_base.cuahsi_base import BaseTestSuite, parse_args_run_tests
from cuahsi_base.utils import TestSystem
from config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
    HS_PASSWORD,
    HS_USERNAME,
    EARTHCHEM_USERNAME,
    EARTHCHEM_PASSWORD,
)

SPAM_DATA_STREAM_NAME = "cuahsi-quality-spam-data-stream"
SPAM_DATA_STREAM_CONFIG = Config(
    region_name="us-east-2",
)


def catch_exception(f):
    @functools.wraps(f)
    def func(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except Exception as error:
            print(f"\nCaught an exception in: {f.__name__}")
            print(f"{error=}, {type(error)=}")
            # attempt to figure out what page we are on
            test = args[0]
            Path("debug").mkdir(parents=True, exist_ok=True)
            file_name = (
                "debug/"
                + f.__name__
                + " "
                + datetime.datetime.now().strftime("%I%M_%p_%B_%d_%Y")
            )
            test.driver.save_screenshot(file_name + ".png")
            soup = BeautifulSoup(test.driver.page_source, "html.parser")
            app = soup.find("div", id="main-container")
            with open(file_name + ".txt", "w") as o:
                with contextlib.redirect_stdout(o):
                    print(f"Page source for {f.__name__}\n" + "*" * 100)
                    for node in app.find_all("div"):
                        print(node.text)
                    print("*" * 100 + f"\nEnd page source for {f.__name__}")
            raise

    return func


class ErrorCatcher(type):
    def __new__(cls, name, bases, dct):
        for m in dct:
            if hasattr(dct[m], "__call__"):
                dct[m] = catch_exception(dct[m])
        return type.__new__(cls, name, bases, dct)


# Test cases definition
class DspTestSuite(BaseTestSuite, metaclass=ErrorCatcher):
    """Python unittest setup for functional tests"""

    def setUp(self):
        super(DspTestSuite, self).setUp()
        self.driver.set_window_size(1200, 1080)
        if not self.base_url_arg:
            self.driver.get(BASE_URL)
        else:
            self.driver.get(self.base_url_arg)

    def login_orcid(self):
        """Authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_nav_login.click(self.driver)
        Dsp.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self, repo):
        self.login_orcid()
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, repo)

    def fill_ids_submit_and_check(self, sort_text, section, nth, dict, array=False):
        """Fill additional fields of submit page based on 'data-id'
        Then submit the form, search in 'My Submissions',
        and check that all of the fields match what was entered
        """
        success_filling = GeneralSubmitToRepo.fill_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(success_filling)
        self.submit_and_check(sort_text, section, nth, dict, array)

    def submit_and_check(self, sort_text, section, nth, dict, array=False):
        self.submit(sort_text)
        self.check(section, nth, dict, array)

    def submit(self, sort_text):
        GeneralSubmitToRepo.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, sort_text)
        MySubmissions.edit_top_submission(self.driver)

    def check(self, section, nth, dict, array=False):
        match = GeneralEditSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth, array
        )
        self.assertTrue(match)

    def check_array_fieldset_unknown_order(self, section, ns, dicts, array):
        reversed = False
        for nth in ns:
            if not reversed:
                try:
                    self.check(section, nth, dicts[nth], array)
                except AssertionError:
                    reversed = True
                    ns.insert(0, nth)
                    print("\n Array items were reversed during this test")
            else:
                self.check(section, nth, dicts.pop(), array)

    def test_base_000001_home_page(self):
        """
        Check home page load
        """

        self.assertTrue(Dsp.app_contains_text("Critical Zone Collaborative Network"))


class DspHydroshareTestSuite(DspTestSuite):
    """DSP tests for the Hydroshare repository"""

    repo_name = "HydroShare"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Title": auto_text + " Title",
            "Abstract": auto_text + " Abstract",
            "Subjectkeywords": [auto_text + " SubjectKeywords"],
        }
        funding_agency = {
            "Agencyname": auto_text + " Agencyname",
        }

        # created separately so that we can check individually if needed
        required_elements = {
            "BasicInformation": basic_info,
            "Fundingagencyinformation": funding_agency,
        }
        return required_elements

    def login_orcid_and_hs(self):
        """Authenticate with orcid and then HS credentials"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.wait_until_element_exist(
            self.driver, SubmitLandingPage.repositories_header
        )
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new HS auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        HydroshareAuthWindow.authorize_repo(self.driver, HS_USERNAME, HS_PASSWORD)
        HydroshareAuthWindow.to_origin_window(self.driver)

    def login_and_autofill_hs_required(self, auto_text):
        """A shortcut to fill required fields of HS submit page
        So that additional non-required fields can easily be checked
        """
        self.login_orcid_and_hs()
        template = self.required_elements_template(auto_text)
        SubmitHydroshare.autofill_required_elements(self.driver, template)

    def test_hs_000001_anon_nav_my_sumissions_shows_orcid(self):
        """Ensure anonymous navigation to my submissions shows orcid login modal"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_my_submissions(self.driver)
        login_visible = MySubmissions.is_visible_orcid_modal(self.driver)
        self.assertTrue(login_visible)

    def test_hs_000002_auth_then_nav_to_submit(self):
        """
        Check authentication to submit page

        Logs in with Orcid, then navigates to the HS repository for submission
        """
        self.login_orcid_and_hs()
        header = SubmitHydroshare.get_header_text(self.driver)
        self.assertIn("Submit", header)

    def test_hs_000003_find_submit_instructions(self):
        """Check that instructions are shown on the Submit page"""
        self.login_orcid_and_hs()
        # SubmitLandingPage.to_repo_form(self.driver, self.repo_name)
        alert = SubmitHydroshare.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_hs_000004_submit_required_fields(self):
        """Confirm successful submit of basic required fields to HS"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_orcid_and_hs()
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        self.assertEqual(
            "Edit Submission", EditHSSubmission.get_header_title(self.driver)
        )
        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_hs_000005_cant_submit_without_each_required(self):
        """Confirm that one can't submit to HS without each required field"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

        template = self.required_elements_template(auto_text)
        for section, dict in template.items():
            for data_id, value in dict.items():
                SubmitHydroshare.unfill_text_by_data_id(
                    self.driver, data_id, section=section, nth=0, array=False
                )
                self.assertRaises(
                    BaseException, SubmitHydroshare.is_finishable(self.driver)
                )
                SubmitHydroshare.expand_section_by_did(self.driver, section)
                SubmitHydroshare.fill_input_by_data_id(
                    self.driver, data_id, value, section, nth=0
                )
                self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

    def test_hs_000006_creator_populates_from_hs(self):
        """
        Confirm that CREATOR is populated from HS profile

        Completing a submission to HS should cause the 'creator' field to be populated
        with info from HS profile
        """
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        section = "Creators"
        nth = 0
        dict = {
            "Name": "test, czhub",
            # "Phone": "4444444444", phone is no longer showing up on beta HS
            "Organization": ("test"),
            "Email": "czhub.test@gmail.com",
        }
        match = EditHSSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    def test_hs_000007_required_fields_persist(self):
        """Check that required fields persist after submit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_hs_required(auto_text)
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_hs_000008_temporal_coverage_persists(self):
        """Confirm that Temporal coverage persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Periodcoverage"
        nth = 0
        dict = {
            "Start": "2022-03-25T01:00",
            "End": "2022-04-25T02:00",
            "Name": auto_text + "Meister, Jim",
        }
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        match = EditHSSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    def test_hs_000009_funding_agency_persists(self):
        """Confirm that Funding Agency info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Fundingagencyinformation"
        nth = 0
        dict = {
            "Awardtitle": auto_text + "Funding Agency title2-input",
            "Awardnumber": "5",
            "FundingAgencyUrl": "http://funding-agency.com/" + auto_text,
        }
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_hs_000010_contributors_info_persists(self):
        """Confirm that Contributors info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Contributors"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "Phone": "1234567890",
            "Address": "contributor address " + auto_text,
            "Organization": "contributor org " + auto_text,
            "Email": auto_text + "@gmail.com",
            "Homepage": "http://contibutor-homepage.com/" + auto_text,
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_hs_000011_spatial_coverage_persists(self):
        """Confirm that Spatial Point Coverage info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Spatialcoverage"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "East": "20",
            "North": "-20",
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_hs_000012_additional_metadata_persists(self):
        """Confirm that additional metadata info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Additionalmetadata"
        nth = 0
        dict = {"Key": auto_text + " key", "Value": auto_text + " value"}
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_hs_000013_related_resources_persists(self):
        """Confirm that Related Resources info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        dict = {"RelationType": "This resource includes", "Value": auto_text + " value"}
        nth = 0
        section = "Relatedresources"
        SubmitHydroshare.fill_related_resources(
            self.driver, dict["RelationType"], dict["Value"], nth
        )
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        relation = EditHSSubmission.get_nth_relation_type(self.driver, nth)
        self.assertEqual(relation.pop(), dict.pop("RelationType"))
        match = EditHSSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    def test_hs_000014_spatial_box_coverate_persists(self):
        """Confirm that Spatial Box Coverage info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Spatialcoverage"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "Northlimit": "20",
            "Eastlimit": "120",
            "Southlimit": "-20",
            "Westlimit": "-120",
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        SubmitHydroshare.open_tab(self.driver, section, tab_number=2)
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        EditHSSubmission.open_tab(self.driver, section, tab_number=2)
        match = EditHSSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    @unittest.expectedFailure
    def test_hs_000015_invalid_spatial_coverage_rejects(self):
        """
        Confirm that invalid Spatial Box Coverage info doesn't submit

        Attempts to submit Box Coverage that doesn't make geographic sense and ensures
        that the invalid info is not accepted
        """
        # TODO: this test fails pending issue
        # https://github.com/cznethub/dspfront/issues/55
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Spatialcoverage"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "Northlimit": "-20",
            "Southlimit": "20",
            "Eastlimit": "120",
            "Westlimit": "-120",
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        SubmitHydroshare.open_tab(self.driver, section, tab_number=2)
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(success_filling)
        self.assertFalse(SubmitHydroshare.is_finishable(self.driver))

    def test_hs_000016_submissions_sorted(self):
        """
        Confirm that submissions are sorted after submission

        The most recent submission should be at the top of the page initially
        """
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_orcid_and_hs()
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_hs_000017_multiple_creators_persist(self):
        """Confirm that multiple Creators info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Creators"
        ns = [0, 1]
        dicts = [None] * len(ns)
        array = True
        for nth in ns:
            dicts[nth] = {
                "Name": f"{auto_text} name {nth}",
                "Phone": "1234567890",
                "Address": f"creator address {auto_text} {nth}",
                "Organization": f"creator org {auto_text} {nth}",
                "Email": f"{auto_text}{nth}@gmail.com",
                "Homepage": f"http://contibutor-homepage.com/{auto_text}{nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            self.check(section, nth, dicts[nth], array)

    def test_hs_000018_multiple_contributors_persist(self):
        """Confirm that multiple Contributors info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Contributors"
        ns = [0, 1]
        array = True
        dicts = [None] * len(ns)
        for nth in ns:
            dicts[nth] = {
                "Name": f"{auto_text} name {nth}",
                "Phone": "1234567890",
                "Address": f"contributor address {auto_text} {nth}",
                "Organization": f"contributor org {auto_text} {nth}",
                "Email": f"{auto_text}{nth}@gmail.com",
                "Homepage": f"http://contibutor-homepage.com/{auto_text}{nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)

        self.submit(auto_text)
        self.check_array_fieldset_unknown_order(section, ns, dicts, array)

    def test_hs_000019_multiple_metadata_persists(self):
        """
        Confirm that multiple Additional Metadata info persists from submit to edit
        """
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Additionalmetadata"
        ns = [0, 1]
        dicts = [None] * len(ns)
        array = True
        for nth in ns:
            dicts[nth] = {
                "Key": f"{auto_text} key {nth}",
                "Value": f"{auto_text} value {nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)

        self.submit(auto_text)
        self.check_array_fieldset_unknown_order(section, ns, dicts, array)

    def test_hs_000020_multiple_related_resources_persist(self):
        """Confirm that multiple Related Resources info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Relatedresources"
        ns = [0, 1]
        array = True
        dicts = [None] * len(ns)
        for nth in ns:
            dicts[nth] = {
                "RelationType": "This resource includes",
                "Value": f"{auto_text} value {nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)

        self.submit(auto_text)

        for nth in ns:
            relation = EditHSSubmission.get_nth_relation_type(self.driver, nth)
            self.assertEqual(relation.pop(), dicts[nth].pop("RelationType"))

        self.check_array_fieldset_unknown_order(section, ns, dicts, array)

    def test_hs_000021_multiple_funding_agencies_persist(self):
        """Confirm that multiple Funding Agencies info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_orcid_and_hs()
        template = {
            "BasicInformation": {
                "Title": auto_text + " Title",
                "Abstract": auto_text + " Abstract",
                "Subjectkeywords": [auto_text + " SubjectKeywords"],
            }
        }
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        section = "Fundingagencyinformation"
        ns = [0, 1]
        dicts = [None] * len(ns)
        array = True
        for nth in ns:
            dicts[nth] = {
                "Agencyname": f"{auto_text} Funding Agency Name {nth}",
                "Awardtitle": f"{auto_text} Funding Agency title2-input {nth}",
                "Awardnumber": f"5{nth}",
                "FundingAgencyUrl": f"http://funding-agency.com/{auto_text}/{nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)

        self.submit(auto_text)

        self.check_array_fieldset_unknown_order(section, ns, dicts, array)

    def test_hs_000022_able_to_view_in_repository(self):
        """
        From My Submissions, confirm that we can "view in repository" HS submission
        """
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_orcid_and_hs()
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.view_top_submission(self.driver)

        MySubmissions.to_hs_repo(self.driver)
        self.assertEqual(
            HSResourcePage.get_title(self.driver), template["BasicInformation"]["Title"]
        )


class DspExternalTestSuite(DspTestSuite):
    """DSP tests for External (No Repo)"""

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Nameortitle": auto_text + " Nameortitle",
            "Url": "http://basicinfourl.com/" + auto_text,
            "Datepublished": "2022-04-05T00:04",
            "Descriptionorabstract": auto_text + " Descriptionorabstract",
            "SubjectKeywords": [auto_text + " SubjectKeywords"],
        }
        creator = {
            "Name": "Meister, Jim",
            "Organization": (
                "Freie Universität Berlin;Agricultural University of Warsaw"
            ),
            "Email": "concretejackbill@gmail.com",
            "ORCID": "0000-0003-0813-0443",
        }
        funding_agency = {
            "Fundingagencyname": auto_text + " Fundingagencyname",
            "Awardnumberoridentifier*": auto_text + " Awardnumberoridentifier",
            "Awardname": auto_text + " Awardname",
        }
        provider = {
            "ProviderName": auto_text + " ProviderName",
            "Url": "http://providerurl.com/" + auto_text,
        }

        # created separately so that we can check individually if needed
        required_elements = {
            "BasicInformation": basic_info,
            "Creators": creator,
            "Fundingagencyinformation": funding_agency,
            "Provider": provider,
        }
        return required_elements

    def login_orcid_and_external(self):
        """Authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, "RegisterDataset")

        SubmitLandingPage.select_external_dataset(self.driver)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

    def login_and_autofill_external_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        self.login_orcid_and_external()
        SubmitExternal.autofill_required_elements(
            self.driver, self.required_elements_template(auto_text)
        )

    def test_ex_000001_authenticate_then_submit_page(self):
        """
        Check authentication to submit page

        First, authenticate with Orcid, then navigate to the submit page
        """
        self.login_orcid_and_external()
        header = SubmitExternal.get_header_text(self.driver)
        self.assertIn("External", header)

    def test_ex_000002_submit_instructions_shown(self):
        """Check that instructions are shown on the Submit page"""
        self.login_orcid_and_external()
        alert = SubmitExternal.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_ex_000003_submit_required_fields(self):
        """Confirm successful submit of required fields for External Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        # self.login_and_autofill_external_required(auto_text)
        self.login_orcid_and_external()
        template = self.required_elements_template(auto_text)
        SubmitExternal.autofill_required_elements(self.driver, template)

        self.assertTrue(SubmitExternal.is_finishable(self.driver))
        SubmitExternal.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)

        top_name = MySubmissions.get_top_submission_name(self.driver)

        self.assertEqual(template["BasicInformation"]["Nameortitle"], top_name)

        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual(
            "Register Dataset from External Repository",
            EditExternalSubmission.get_header_title(self.driver),
        )
        self.assertTrue(
            EditExternalSubmission.check_required_elements(self.driver, template)
        )

    def test_ex_000004_contributors_info_persists(self):
        """Confirm that Contributors info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)
        section = "Contributors"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            # "Phone": "1234567890",
            # "Address": "contributor address " + auto_text,
            "Organization": "contributor org " + auto_text,
            "Email": auto_text + "@gmail.com",
            # "Homepage": "http://contibutor-homepage.com/" + auto_text,
        }
        SubmitExternal.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_ex_000005_temporal_coverage_persists(self):
        """Confirm that Temporal coverage persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)
        section = "Temporalcoverage"
        nth = 0
        dict = {
            "Start": "2022-03-25T01:00",
            "End": "2022-04-25T02:00",
            "Name": auto_text + "Meister, Jim",
        }
        success_filling = SubmitExternal.fill_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(success_filling)
        SubmitExternal.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        match = EditExternalSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    def test_ex_000006_spatial_coverage_persists(self):
        """Confirm that Spatial Point Coverage info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)
        section = "Spatialcoverage"
        nth = 0
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "East": "20",
            "North": "-20",
        }
        SubmitExternal.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    @unittest.skip("Test needs to be fixed")
    def test_ex_000007_related_resources_persists(self):
        """Confirm that Related Resources info persists from submit to edit"""
        # TODO: fix this test
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)
        dict = {"RelationType": "This resource requires", "Value": auto_text + " value"}
        nth = 0
        section = "Relatedresources"
        SubmitExternal.fill_related_resources(
            self.driver, dict["RelationType"], dict["Value"], nth
        )
        SubmitExternal.finish_submission(self.driver)

        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        relation = EditExternalSubmission.get_nth_relation_type(self.driver, nth)

        self.assertEqual(relation.pop(), dict.pop("RelationType"))
        match = EditExternalSubmission.check_inputs_by_data_ids(
            self.driver, dict, section, nth
        )
        self.assertTrue(match)

    @unittest.skip("Test needs to be fixed")
    def test_ex_000008_multiple_related_resources_persist(self):
        """Confirm that multiple Related Resources info persists from submit to edit"""
        # TODO: fix this test
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)
        section = "Relatedresources"
        ns = [0, 1]
        array = True
        dicts = [None] * len(ns)
        for nth in ns:
            dicts[nth] = {
                "RelationType": "This resource requires",
                "Value": f"{auto_text} value {nth}",
            }
            SubmitExternal.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitExternal.fill_inputs_by_data_ids(
                self.driver, dicts[nth], section, nth, array
            )
            self.assertTrue(success_filling)
        self.submit(auto_text)

        for nth in ns:
            relation = EditExternalSubmission.get_nth_relation_type(self.driver, nth)
            self.assertEqual(relation.pop(), dicts[nth].pop("RelationType"))

        self.check_array_fieldset_unknown_order(section, ns, dicts, array)


class DspZenodoTestSuite(DspTestSuite):
    """DSP tests for Zenodo backend"""

    repo_name = "Zenodo"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Title": auto_text + " Title",
            "Description/Abstract": auto_text + " Description/Abstract",
            "Keywords": [auto_text + " Keywords"],
        }
        # as of the following commit
        # https://github.com/cznethub/dspfront/commit/2ef4408e40dfb74d837c9699adaeb7879c843d74
        # funding agency is required but it is pre-filled now...
        # funding_agency = {
        #     "Agencyname": auto_text + " Fundingagencyname",
        #     "Awardtitle": auto_text + " Awardtitle",
        #     "Awardnumber": auto_text + " Awardnumberoridentifier",
        #     "AgencyURL": "http://funding-agency.com/" + auto_text,
        # }

        required_elements = {
            "BasicInformation": basic_info,
            # "FundingAgencyMetadata": funding_agency,
        }
        return required_elements

    def zenodo_then_login_orcid(self):
        """Select Zenodo repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Zenodo auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)

        ZenodoAuthWindow.authorize_via_orcid(self.driver)
        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

    def zenodo_then_login_username_password(self):
        """Select Zenodo repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Zenodo auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        ZenodoAuthWindow.authorize_email_password(
            self.driver, email=USERNAME, password=PASSWORD
        )
        ZenodoAuthWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self):
        """Authenticate with orcid the select repo"""
        super().login_orcid_to_submit(self.repo_name)
        if RepoAuthWindow.submit_to_repo_authorize.exists(self.driver):
            SubmitLandingPage.to_repo_auth_window(self.driver)
            ZenodoAuthWindow.authorize_email_password(
                self.driver, email=USERNAME, password=PASSWORD
            )
            ZenodoAuthWindow.to_origin_window(self.driver, wait=True)

    def login_and_autofill_zenodo_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        self.zenodo_then_login_username_password()
        SubmitZenodo.autofill_required_elements(
            self.driver, self.required_elements_template(auto_text)
        )

    def test_ze_000001_orcid_then_submit(self):
        """Check authentication with Orcid, then navigate to submit page"""
        self.login_orcid_to_submit()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)
        alert = SubmitZenodo.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    @unittest.skip("Fails pending https://github.com/cznethub/dspfront/issues/57")
    def test_ze_000002_repo_then_auth_w_orcid(self):
        """Navigate to Zenodo submit first, then auth with orcid"""
        self.zenodo_then_login_orcid()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_ze_000003_nav_to_repo_then_auth_user_pw(self):
        """Navigate to Zenodo submit, then auth with uname/pw"""
        self.zenodo_then_login_username_password()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_ze_000004_submit_required_fields(self):
        """Confirm successful submit of required fields for Zenodo Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_zenodo_required(auto_text)
        self.assertTrue(SubmitZenodo.is_finishable(self.driver))
        SubmitZenodo.finish_submission(self.driver, USERNAME, PASSWORD)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))
        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")

    def test_ze_000005_required_fields_persist(self):
        """Check that required fields persist after submit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_zenodo_required(auto_text)
        SubmitZenodo.finish_submission(self.driver, USERNAME, PASSWORD)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual(
            "Edit Submission", EditZenodoSubmission.get_header_title(self.driver)
        )
        check = EditZenodoSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_ze_000006_able_to_view_in_repository(self):
        """
        From My Submissions, confirm that we can "view in repository" zenodo submission
        """
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_zenodo_required(auto_text)
        SubmitZenodo.finish_submission(self.driver, USERNAME, PASSWORD)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.view_top_submission(self.driver)
        MySubmissions.to_zenodo_repo(self.driver)
        self.assertEqual(
            ZenodoResourcePage.get_title(self.driver),
            template["BasicInformation"]["Title"],
        )


class DspEarthchemTestSuite(DspTestSuite):
    """DSP tests for Earthchem backend"""

    repo_name = "EarthChem"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "DatasetTitle": auto_text + " Title",
            "AbstractorDescription": auto_text + " Description/Abstract",
            "DataTypes": ["Chemistry"],
            "Keywords": [auto_text + " Keywords"],
        }
        lead_author = {
            "FirstName": auto_text + "FirstName",
            "LastName": auto_text + "LastName",
            "Email": f"{auto_text}@gmail.com",
        }
        spatial = {"SpatialCoverage": ["Global"]}

        required_elements = {
            "group-BasicInformation": basic_info,
            "SpatialCoverageInformation": spatial,
            "LeadAuthor": lead_author,
        }
        return required_elements

    def earthchem_then_login_orcid(self):
        """Select Earthchem repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(
            self.driver, EARTHCHEM_USERNAME, EARTHCHEM_PASSWORD
        )
        OrcidWindow.to_origin_window(self.driver)

        # new Earthchem auth window
        if RepoAuthWindow.submit_to_repo_authorize.exists(self.driver):
            SubmitLandingPage.to_repo_auth_window(self.driver)
            EarthchemAuthWindow.authorize_via_orcid(self.driver)
            EarthchemAuthWindow.to_origin_window(self.driver, wait=True)

    def earthchem_then_login_username_password(self):
        """Select Earthchem repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)

        OrcidWindow.fill_credentials(
            self.driver, EARTHCHEM_USERNAME, EARTHCHEM_PASSWORD
        )
        OrcidWindow.to_origin_window(self.driver)

        # new Earthchem auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        EarthchemAuthWindow.authorize_email_password(
            self.driver, email=EARTHCHEM_USERNAME, password=EARTHCHEM_PASSWORD
        )
        EarthchemAuthWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self):
        """Authenticate with orcid then select repo"""
        super().login_orcid_to_submit(self.repo_name)

        # first time that a user auths to ECL, there is an extra window
        if RepoAuthWindow.submit_to_repo_authorize.exists(self.driver):
            SubmitLandingPage.to_repo_auth_window(self.driver)
            EarthchemAuthWindow.authorize_via_orcid(self.driver)
            OrcidWindow.fill_credentials(
                self.driver, EARTHCHEM_USERNAME, EARTHCHEM_PASSWORD
            )
            OrcidWindow.to_origin_window(self.driver, wait=True)

    def login_and_autofill_earthchem_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        # self.earthchem_then_login_username_password()
        self.login_orcid_to_submit()
        SubmitEarthchem.autofill_required_elements(
            self.driver, self.required_elements_template(auto_text)
        )

    def submit(self, sort_text):
        """
        Save an EarthChem record

        ECL is unique in that it has multiple options for submit vs finish_later. This funtions name is confusing...here we are overriding the default TestSuite submit()
        This would be more aptly named 'finish_later()'
        """
        SubmitEarthchem.finish_submission_later(self.driver)

        MySubmissions.enter_text_in_search(self.driver, sort_text)
        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")

        MySubmissions.edit_top_submission(self.driver)

    def test_ec_000001_orcid_auth_then_submit(self):
        """Authenticate with Orcid, then navigate to Earthchem submit page"""
        self.login_orcid_to_submit()
        header = SubmitEarthchem.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)
        alert = SubmitEarthchem.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_ec_000002_repo_then_orcid_auth(self):
        """Navigate to Earthchem submit, then authenticate with orcid"""
        self.earthchem_then_login_orcid()
        header = SubmitEarthchem.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_ec_000003_save_required_fields(self):
        """Confirm successful save of required fields for Earthchem Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        self.assertTrue(SubmitEarthchem.is_finishable(self.driver))
        SubmitEarthchem.finish_submission_later(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))
        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")

    def test_ec_000004_required_fields_persist(self):
        """Check that required fields persist after save"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_earthchem_required(auto_text)
        SubmitEarthchem.finish_submission_later(self.driver)
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        check = EditEarthchemSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    @unittest.skip("Lead Author became a required field so is tested elsewhere")
    def test_ec_000005_lead_author_persists(self):
        """Confirm that Lead Author info persists from save to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        section = "LeadAuthor"
        nth = 0
        dict = {
            "FirstName": auto_text + "FirstName",
            "LastName": auto_text + "LastName",
            "Email": f"{auto_text}@gmail.com",
        }
        SubmitEarthchem.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_ec_000006_co_author_persist(self):
        """Confirm that Co-Author info persists from save to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        section = "Co-Authors"
        nth = 0
        dict = {
            "FirstName": auto_text + "FirstName",
            "LastName": auto_text + "LastName",
            "Email": f"{auto_text}@gmail.com",
        }
        SubmitEarthchem.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_ec_000007_related_resource_persists(self):
        """Confirm that Related Resource Info persists from save to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        section = "RelatedInformation"
        nth = 0
        dict = {
            "PublicationDOI": auto_text + "PublicationDOI",
            # "RelatedInformation": "(R2R) - Cruise DOI"
        }

        # This section is nested...
        SubmitEarthchem.expand_section_by_did(self.driver, data_id="RelatedResources")
        SubmitEarthchem.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_ec_000008_funding_source_persists(self):
        """Confirm that Funding Source Info persists from save to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        section = "FundingSource"
        nth = 0
        dict = {
            # "Selectone": "U.S. Department of Energy",
            "AwardNumber": auto_text
            + "AwardNumber"
        }
        SubmitEarthchem.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_ec_000009_license_persists(self):
        """Confirm that License Info persists from save to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        section = "License"
        nth = 0
        dict = {"License": "(CC0-1.0) - Creative Commons No Rights Reserved"}
        SubmitEarthchem.expand_section_by_did(self.driver, data_id=section)
        try:
            self.fill_ids_submit_and_check(auto_text, section, nth, dict)
        except AssertionError:
            license = SubmitEarthchem.get_license(self.driver)
            self.assertEqual(license, dict["License"])

    def test_ec_000010_able_to_view_in_repository(self):
        """
        From My Submissions, confirm that we can "view in repository" ECL submission, after saving
        """
        # TODO: set production ECL env via GH workflow
        # https://github.com/cznethub/dspback/issues/118
        if "localhost" in self.base_url_arg or "test" in self.base_url_arg:
            self.skipTest("Viewing ECL submissions not supported in test environment")
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_earthchem_required(auto_text)
        SubmitEarthchem.finish_submission_later(self.driver)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.view_top_submission(self.driver)
        MySubmissions.to_earthchem_repo(self.driver)
        EarthchemResourcePage.authenticate_if_needed(self.driver)

        self.assertEqual(
            EarthchemResourcePage.get_title(self.driver),
            template["group-BasicInformation"]["DatasetTitle"],
        )

    def test_ec_000011_submit_for_review_required_fields(self):
        """
        From My Submissions, confirm that we can "view in repository" ECL submission, after SUBMITTING FOR REVIEW
        """
        # TODO: set production ECL env via GH workflow
        # https://github.com/cznethub/dspback/issues/118
        if "localhost" in self.base_url_arg or "test" in self.base_url_arg:
            self.skipTest("Viewing ECL submissions not supported in test environment")
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        SubmitEarthchem.submit_for_review(self.driver)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.wait_until_app_contains_text(self.driver, "My Submissions")

        MySubmissions.view_top_submission(self.driver)
        MySubmissions.to_earthchem_repo(self.driver)

        EarthchemResourcePage.authenticate_if_needed(self.driver)
        self.assertIn(auto_text, EarthchemResourcePage.get_title(self.driver))


if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
