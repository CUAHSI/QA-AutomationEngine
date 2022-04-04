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
    HydroshareWindow,
    SubmitHydroshare,
    EditHSSubmission
)

from cuahsi_base.cuahsi_base import BaseTestSuite, parse_args_run_tests
from cuahsi_base.utils import kinesis_record, External, TestSystem
from config import (
    BASE_URL,
    USERNAME,
    PASSWORD,
    HS_PASSWORD,
    HS_USERNAME,
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
        if not self.base_url_arg:
            self.driver.get(BASE_URL)
        else:
            self.driver.get(self.base_url_arg)

    def login_orcid_and_hs(self):
        """Authenticate with orcid and then HS credentials"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.hydroshare_repo_select(self.driver)

        # new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        # new HS auth window
        SubmitLandingPage.to_hs_window(self.driver)
        self.assertIn("HydroShare", TestSystem.title(self.driver))
        HydroshareWindow.authorize_hs_backend(self.driver, HS_USERNAME, HS_PASSWORD)
        HydroshareWindow.to_origin_window(self.driver)

    def login_and_autofill_hs_required(self, auto_text):
        """A shortcut to fill required fields of HS submit page
        So that additional non-required fields can easily be checked
        """
        self.login_orcid_and_hs()
        SubmitLandingPage.to_hs_submit(self.driver)
        SubmitHydroshare.autofill_required_elements(self.driver, auto_text)

    def fill_ids_submit_and_check(self, sort_text, section, nth, dict):
        """Fill additional fields of HS submit page based on 'data-id'
        Then submit the form, search in 'My Submissions',
        and check that all of the fields match what was entered
        """
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, sort_text)
        MySubmissions.edit_top_submission(self.driver)

        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
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
        SubmitLandingPage.to_hs_submit(self.driver)
        alert = SubmitHydroshare.get_alert_text(self.driver)
        self.assertIn("Instructions:", alert)

    def test_A_000004(self):
        """Confirm successful submit of basic required fields to HS"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))
        SubmitHydroshare.finish_submission(self.driver)
        self.assertEqual("My Submissions", MySubmissions.get_title(self.driver))

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        top_name = MySubmissions.get_top_submission_name(self.driver)
        self.assertEqual(auto_text, top_name)

        MySubmissions.edit_top_submission(self.driver)
        self.assertEqual("Edit Submission", EditHSSubmission.get_header_title(self.driver))

        self.assertTrue(EditHSSubmission.check_required_elements(self.driver, auto_text))

    def test_A_000005(self):
        """Confirm that one can't submit to HS without each required field"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

        required_text_items = ["agency_name", "abstract", "title", "rights_statement", "rights_url"]
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
        nth = 1
        dict = {
            "Name": "Meister, Jim",
            # "Phone": "4444444444", phone is no longer showing up on beta HS
            "Organization": "Freie Universität Berlin;Agricultural University of Warsaw",
            "Email": "concretejackbill@gmail.com"
        }
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

    def test_A_000007(self):
        """Confirm that Basic Info persists from submit to edit"""
        self.login_orcid_and_hs()
        SubmitLandingPage.to_hs_submit(self.driver)
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        dict = {
            "title-input": auto_text + "title-input",
            "abstract-input": auto_text + "abstract-input",
            "subjects-input": ["keyword1", "keyword2"],
            "funding_agency_name-input": auto_text + "funding_agency_name-input"
        }
        SubmitHydroshare.autofill_required_elements(self.driver, dict)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text + "title-input")
        MySubmissions.edit_top_submission(self.driver)

        # check keywords separately
        keywords = dict.pop("subjects-input")
        self.assertTrue(EditHSSubmission.check_keywords(self.driver, keywords))

        match = EditHSSubmission.check_fields_by_dict(self.driver, dict)
        self.assertTrue(match)

    def test_A_000008(self):
        """Confirm that Temporal coverage persists from submit to edit"""
        # TODO: this test fills the date/times but they fail to submit
        # so this test will fail until this issue is fixed in DSP
        # https://github.com/cznethub/dspfront/issues/52
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Temporalcoverage"
        nth = 1
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
        nth = 1
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
        nth = 1
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "Phone": "1234567890",
            "Address": "contributor address " + auto_text,
            "Organization": "contributor org " + auto_text,
            "Email": auto_text + "@gmail.com",
            "Homepage": "http://contibutor_homepage.com/" + auto_text,
        }
        SubmitHydroshare.click_expand_contributors(self.driver)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000011(self):
        """Confirm that Spatial Point Coverage info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Spatialcoverage"
        nth = 1
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "East": "20",
            "North": "-20",
        }
        SubmitHydroshare.click_expand_spatial(self.driver)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000012(self):
        """Confirm that additional metadata info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        section = "Additionalmetadata"
        nth = 1
        dict = {
            "Key": auto_text + " key",
            "Value": auto_text + " value"
        }
        SubmitHydroshare.click_expand_metadata(self.driver)
        self.fill_ids_submit_and_check(auto_text, section, nth, dict)

    def test_A_000013(self):
        """Confirm that Related Resources info persists from submit to edit"""
        auto_text = time.strftime("%d_%b_%Y_%H-%M-%S", time.gmtime())
        self.login_and_autofill_hs_required(auto_text)
        dict = {
            "RelationType": "This resource includes",
            "Value": auto_text + " value"
        }
        nth = 1
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
        nth = 1
        dict = {
            "Name": auto_text + "Contributor name2-input",
            "Northlimit": "-20",
            "Eastlimit": "120",
            "Southlimit": "20",
            "Westlimit": "-120"
        }
        SubmitHydroshare.click_expand_spatial(self.driver)
        SubmitHydroshare.open_tab(self.driver, section, tab_number=2)
        success_filling = SubmitHydroshare.fill_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(success_filling)
        SubmitHydroshare.finish_submission(self.driver)

        # The page isn't sorted upon load
        MySubmissions.enter_text_in_search(self.driver, auto_text)
        MySubmissions.edit_top_submission(self.driver)

        EditHSSubmission.click_expand_spatial(self.driver)
        EditHSSubmission.open_tab(self.driver, section, tab_number=2)
        match = EditHSSubmission.check_inputs_by_data_ids(self.driver, dict, section, nth)
        self.assertTrue(match)

if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
