""" Runs various smoke tests for the data submission portal """
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

from dsp_macros import (
    Dsp,
    SubmitLandingPage,
    MySubmissions,
    OrcidWindow,
    HydroshareAuthWindow,
    SubmitHydroshare,
    EditHSSubmission,
    SubmitExternal,
    EditExternalSubmission,
    SubmitZenodo,
    EditZenodoSubmission,
    ZenodoAuthWindow,
    SubmitEarthchem,
    EditEarthchemSubmission,
    EarthchemAuthWindow
)

from cuahsi_base.cuahsi_base import BaseTestSuite, parse_args_run_tests
from cuahsi_base.utils import kinesis_record, External, TestSystem
from config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
    HS_PASSWORD,
    HS_USERNAME,
    EARTHCHEM_USERNAME,
    EARTHCHEM_PASSWORD
)

SPAM_DATA_STREAM_NAME = "cuahsi-quality-spam-data-stream"
SPAM_DATA_STREAM_CONFIG = Config(
    region_name="us-east-2",
)


# Test cases definition
class DspTestSuite(BaseTestSuite):
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
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self, repo):
        self.login_orcid()
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, repo)


class DspHydroshareTestSuite(DspTestSuite):
    """DSP tests for Hydroshare repository"""

    repo_name = "HydroShare"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Title": auto_text + " Title",
            "Abstract": auto_text + " Abstract",
            "Subjectkeywords": [auto_text + " SubjectKeywords"]
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
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new HS auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        self.assertIn(self.repo_name, TestSystem.title(self.driver))
        HydroshareAuthWindow.authorize_repo(self.driver, HS_USERNAME, HS_PASSWORD)
        HydroshareAuthWindow.to_origin_window(self.driver)

    def login_and_autofill_hs_required(self, auto_text):
        """A shortcut to fill required fields of HS submit page
        So that additional non-required fields can easily be checked
        """
        self.login_orcid_and_hs()
        template = self.required_elements_template(auto_text)
        SubmitHydroshare.autofill_required_elements(self.driver, template)

    def fill_ids_submit_and_check(self, sort_text, section, nth, dict, array=False):
        """Fill additional fields of HS submit page based on 'data-id'
        Then submit the form, search in 'My Submissions',
        and check that all of the fields match what was entered
        """
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        self.submit_and_check(sort_text, section, nth, dict, array)

    def submit_and_check(self, sort_text, section, nth, dict, array=False):
        self.submit(sort_text)
        self.check(section, nth, dict, array)

    def submit(self, sort_text):
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, sort_text)
        MySubmissions.edit_top_submission(self.driver)

    def check(self, section, nth, dict, array=False):
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth, array)
        self.assertTrue(match)

    def test_A_000001(self):
        """Ensure anonymous navigation to my submissions shows orcid login modal"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_my_submissions(self.driver)
        login_visible = MySubmissions.is_visible_orcid_modal(self.driver)
        self.assertTrue(login_visible)

    def test_A_000002(self):
        """Check authentication to submit page"""
        self.login_orcid_and_hs()
        header = SubmitHydroshare.get_header_text(self.driver)
        self.assertIn("Submit", header)

    def test_A_000003(self):
        """Check that submit instructions are shown"""
        self.login_orcid_and_hs()
        SubmitLandingPage.to_repo_form(self.driver, self.repo_name)
        alert = SubmitHydroshare.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_A_000004(self):
        """Confirm successful submit of basic required fields to HS"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_orcid_and_hs()
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)

        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditHSSubmission.get_header_title(self.driver))
        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_A_000005(self):
        """Confirm that one can't submit to HS without each required field"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

        required_text_items = ["agency_name", "abstract", "title"]
        for text_elem in required_text_items:
            SubmitHydroshare.unfill_text_by_page_property(self.driver, text_elem)
            self.assertRaises(BaseException, SubmitHydroshare.is_finishable(self.driver))
            if "url" in text_elem:
                SubmitHydroshare.fill_text_by_page_property(self.driver, text_elem, "http://" + auto_text)
            else:
                SubmitHydroshare.fill_text_by_page_property(self.driver, text_elem, auto_text)
            self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

    def test_A_000006(self):
        """Confirm that CREATOR is populated from HS profile"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        section = "Creators"
        nth = 0
        dict = {
            "Name": "Meister, Jim",
            # "Phone": "4444444444", phone is no longer showing up on beta HS
            "Organization": "Freie Universität Berlin;Agricultural University of Warsaw",
            "Email": "concretejackbill@gmail.com"
        }
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

    def test_A_000007(self):
        """Check that required fields persist after submit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_hs_required(auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditHSSubmission.get_header_title(self.driver))
        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_A_000008(self):
        """Confirm that Temporal coverage persists from submit to edit"""
        # TODO: this test fills the date/times but they fail to submit
        # so this test will fail until this issue is fixed in DSP
        # https://github.com/cznethub/dspfront/issues/52
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Temporalcoverage"
        nth = 0
        dict = {
            "Start": "2022-03-25T01:00",
            "End": "2022-04-25T02:00",
            "Name": auto_text + "Meister, Jim",
        }
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

    def test_A_000009(self):
        """Confirm that Funding Agency info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Fundingagencyinformation"
        nth = 0
        dict = {
            "Awardtitle": auto_text + "Funding Agency title2-input",
            "Awardnumber": "5",
            "AgencyURL": "http://funding-agency.com/" + auto_text,
        }
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000010(self):
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
            "Homepage": "http://contibutor_homepage.com/" + auto_text,
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000011(self):
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

    def test_A_000012(self):
        """Confirm that additional metadata info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Additionalmetadata"
        nth = 0
        dict = {
            "Key": auto_text + " key",
            "Value": auto_text + " value"
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000013(self):
        """Confirm that Related Resources info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        dict = {
            "RelationType": "This resource includes",
            "Value": auto_text + " value"
        }
        nth = 0
        section = "Relatedresources"
        SubmitHydroshare.fill_related_resources(self.driver, dict["RelationType"], dict["Value"], nth)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        relation = EditHSSubmission.get_nth_relation_type(self.driver, nth)
        self.assertEqual(relation.pop(), dict.pop("RelationType"))
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

    def test_A_000014(self):
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
            "Westlimit": "-120"
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        SubmitHydroshare.open_tab(self.driver, section, tab_number=2)
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        EditHSSubmission.open_tab(self.driver, section, tab_number=2)
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

    def test_A_000015(self):
        """Confirm that invalid Spatial Box Coverage info doesn't submit"""
        # TODO: this test fails pending issue:
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
            "Westlimit": "-120"
        }
        SubmitHydroshare.expand_section_by_did(self.driver, data_id=section)
        SubmitHydroshare.open_tab(self.driver, section, tab_number=2)
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        self.assertFalse(SubmitHydroshare.is_finishable(self.driver))

    def test_A_000016(self):
        """Confirm that submissions are sorted after submission"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_orcid_and_hs()
        SubmitHydroshare.autofill_required_elements(self.driver, template)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

        # TODO: this test fails pending this issue
        # https://github.com/cznethub/dspfront/issues/53
        # The page isn't sorted upon load, so top submission will not be the most recent
        MySubmissions.edit_top_submission(self.driver)

        self.assertEqual("Edit Submission", EditHSSubmission.get_header_title(self.driver))
        check = EditHSSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)

    def test_A_000017(self):
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
                "Homepage": f"http://contibutor_homepage.com/{auto_text}{nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dicts[nth], section, nth, array)
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            self.check(section, nth, dicts[nth], array)

    def test_A_000018(self):
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
                "Homepage": f"http://contibutor_homepage.com/{auto_text}{nth}"
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dicts[nth], section, nth, array)
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            self.check(section, (nth), dicts[nth], array)

    def test_A_000019(self):
        """Confirm that multiple Additional Metadata info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Additionalmetadata"
        ns = [0, 1]
        dicts = [None] * len(ns)
        array = True
        for nth in ns:
            dicts[nth] = {
                "Key": f"{auto_text} key {nth}",
                "Value": f"{auto_text} value {nth}"
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dicts[nth], section, nth, array)
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            self.check(section, nth, dicts.pop(), array)

    def test_A_000020(self):
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
                "Value": f"{auto_text} value {nth}"
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dicts[nth], section, nth, array)
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            relation = EditHSSubmission.get_nth_relation_type(self.driver, nth)
            self.assertEqual(relation.pop(), dicts[nth].pop("RelationType"))
            self.check(section, nth, dicts[nth], array)

    def test_A_000021(self):
        """Confirm that multiple Funding Agencies info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_orcid_and_hs()
        template = {"BasicInformation": {
            "Title": auto_text + " Title",
            "Abstract": auto_text + " Abstract",
            "Subjectkeywords": [auto_text + " SubjectKeywords"]
        }}
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
                "AgencyURL": f"http://funding-agency.com/{auto_text}/{nth}",
            }
            SubmitHydroshare.add_form_array_item_by_did(self.driver, data_id=section)
            success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dicts[nth], section, nth, array)
            self.assertTrue(success_filling)

        self.submit(auto_text)
        for nth in ns:
            self.check(section, nth, dicts[nth], array)


class DspExternalTestSuite(DspTestSuite):
    """DSP tests for External (No Repo)"""

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Nameortitle": auto_text + " Nameortitle",
            "URL": "http://basic_info_url.com/" + auto_text,
            "Datepublished": "2022-04-05T00:04",
            "Descriptionorabstract": auto_text + " Descriptionorabstract",
            "SubjectKeywords": [auto_text + " SubjectKeywords"]
        }
        creator = {
            "Name": "Meister, Jim",
            "Organization": "Freie Universität Berlin;Agricultural University of Warsaw",
            "Email": "concretejackbill@gmail.com",
            "ORCID": "0000-0003-0813-0443"
        }
        funding_agency = {
            "Fundingagencyname": auto_text + " Fundingagencyname",
            "Awardnumberoridentifier*": auto_text + " Awardnumberoridentifier",
            "Awardname": auto_text + " Awardname"
        }
        provider = {
            "ProviderName": auto_text + " ProviderName",
            "ProviderURL": "http://provider_url.com/" + auto_text
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

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

    def login_and_autofill_external_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        self.login_orcid_and_external()
        SubmitExternal.autofill_required_elements(self.driver, self.required_elements_template(auto_text))

    def test_A_000001(self):
        """Check authentication to submit page"""
        self.login_orcid_and_external()
        header = SubmitExternal.get_header_text(self.driver)
        self.assertIn("External", header)

    def test_A_000002(self):
        """Check that submit instructions are shown"""
        self.login_orcid_and_external()
        alert = SubmitExternal.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_A_000003(self):
        """Confirm successful submit of basic required fields for External Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_external_required(auto_text)

        # TODO: this test fails due to date-time issue:
        # https://github.com/cznethub/dspfront/issues/52
        self.assertTrue(SubmitExternal.is_finishable(self.driver))
        SubmitExternal.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        top_name = MySubmissions.get_top_submission_name(self.driver)
        self.assertEqual(auto_text, top_name)

        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditExternalSubmission.get_header_title(self.driver))

        self.assertTrue(EditExternalSubmission.check_required_elements(self.driver, auto_text))


class DspZenodoTestSuite(DspTestSuite):
    """DSP tests for Zenodo backend"""

    repo_name = "Zenodo"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Title": auto_text + " Title",
            "Description/Abstract": auto_text + " Description/Abstract",
            "Keywords": [auto_text + " Keywords"]
        }

        required_elements = {
            "BasicInformation": basic_info
        }
        return required_elements

    def zenodo_then_login_orcid(self):
        """Select Zenodo repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Zenodo auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)

        ZenodoAuthWindow.authorize_via_orcid(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))
        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

    def zenodo_then_login_username_password(self):
        """Select Zenodo repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Zenodo auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        ZenodoAuthWindow.authorize_email_password(self.driver, email=USERNAME, password=PASSWORD)
        ZenodoAuthWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self):
        """Authenticate with orcid the select repo"""
        super().login_orcid_to_submit(self.repo_name)

    def login_and_autofill_zenodo_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        self.zenodo_then_login_username_password()
        SubmitZenodo.autofill_required_elements(self.driver, self.required_elements_template(auto_text))

    def test_A_000001(self):
        """Orcid auth first, then to submit page"""
        self.login_orcid_to_submit()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)
        alert = SubmitZenodo.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_A_000002(self):
        """Navigate to repo then auth with orcid"""
        # TODO: this test fails pending issue
        # https://github.com/cznethub/dspfront/issues/57
        self.zenodo_then_login_orcid()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_A_000003(self):
        """Navigate to repo then auth with orcid"""
        self.zenodo_then_login_username_password()
        header = SubmitZenodo.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_A_000004(self):
        """Confirm successful submit of required fields for Zenodo Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_zenodo_required(auto_text)
        self.assertTrue(SubmitZenodo.is_finishable(self.driver))
        SubmitZenodo.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

    def test_A_000005(self):
        """Check that required fields persist after submit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_zenodo_required(auto_text)
        self.assertTrue(SubmitZenodo.is_finishable(self.driver))
        SubmitZenodo.finish_submission(self.driver)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditZenodoSubmission.get_header_title(self.driver))
        check = EditZenodoSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)


class DspEarthchemTestSuite(DspTestSuite):
    """DSP tests for Earthchem backend"""

    repo_name = "EarthChem"

    @classmethod
    def required_elements_template(self, auto_text):
        basic_info = {
            "Title": auto_text + " Title",
            "Description/Abstract": auto_text + " Description/Abstract",
            "Keywords": [auto_text + " Keywords"]
        }

        required_elements = {
            "BasicInformation": basic_info
        }
        return required_elements

    def earthchem_then_login_orcid(self):
        """Select Earthchem repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Earthchem auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)

        EarthchemAuthWindow.authorize_via_orcid(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))
        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

    def earthchem_then_login_username_password(self):
        """Select Earthchem repo then authenticate with orcid"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.select_repo_by_id(self.driver, self.repo_name)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new Earthchem auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        EarthchemAuthWindow.authorize_email_password(self.driver, email=USERNAME, password=PASSWORD)
        EarthchemAuthWindow.to_origin_window(self.driver, wait=True)

    def login_orcid_to_submit(self):
        """Authenticate with orcid then select repo"""
        super().login_orcid_to_submit(self.repo_name)

        # new EC auth window
        SubmitLandingPage.to_repo_auth_window(self.driver)
        self.assertIn("ecl-realm", TestSystem.title(self.driver))
        # TODO: not sure that u/p actually works?
        # EarthchemAuthWindow.authorize_username_password(self.driver, EARTHCHEM_USERNAME, EARTHCHEM_PASSWORD)
        EarthchemAuthWindow.authorize_via_orcid(self.driver)
        # TODO: looks like even if you already logged into ORCID, it asks for those creds again...
        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        EarthchemAuthWindow.login_button.click(self.driver)
        OrcidWindow.to_origin_window(self.driver, wait=True)
        # EarthchemAuthWindow.to_origin_window(self.driver)

    def login_and_autofill_earthchem_required(self, auto_text):
        """A shortcut to fill required fields of submit page
        So that additional non-required fields can easily be checked
        """
        self.earthchem_then_login_username_password()
        SubmitEarthchem.autofill_required_elements(self.driver, self.required_elements_template(auto_text))

    def test_A_000001(self):
        """Orcid auth first, then to submit page"""
        self.login_orcid_to_submit()
        header = SubmitEarthchem.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)
        alert = SubmitEarthchem.get_alert_text(self.driver)
        self.assertIn("Instructions", alert)

    def test_A_000002(self):
        """Navigate to repo then auth with orcid"""
        # TODO: this test fails pending issue
        # https://github.com/cznethub/dspfront/issues/57
        self.earthchem_then_login_orcid()
        header = SubmitEarthchem.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_A_000003(self):
        """Navigate to repo then auth with orcid"""
        self.earthchem_then_login_username_password()
        header = SubmitEarthchem.get_header_text(self.driver)
        self.assertIn(self.repo_name, header)

    def test_A_000004(self):
        """Confirm successful submit of required fields for Earthchem Repo"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_earthchem_required(auto_text)
        self.assertTrue(SubmitEarthchem.is_finishable(self.driver))
        SubmitEarthchem.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

    def test_A_000005(self):
        """Check that required fields persist after submit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        template = self.required_elements_template(auto_text)
        self.login_and_autofill_earthchem_required(auto_text)
        self.assertTrue(SubmitEarthchem.is_finishable(self.driver))
        SubmitEarthchem.finish_submission(self.driver)

        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditEarthchemSubmission.get_header_title(self.driver))
        check = EditEarthchemSubmission.check_required_elements(self.driver, template)
        self.assertTrue(check)


if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
