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
    GITHUB_ORG,
    GITHUB_REPO,
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
        self.driver.get(BASE_URL)
    
    def login_orcid_and_hs(self):
        """Authenticate with orcid and then HS credentials"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_submit(self.driver)
        SubmitLandingPage.hydroshare_repo_select(self.driver)

        #new ORCID window
        SubmitLandingPage.to_orcid_window(self.driver)
        self.assertIn("ORCID", TestSystem.title(self.driver))

        OrcidWindow.fill_credentials(self.driver, USERNAME, PASSWORD)
        OrcidWindow.to_origin_window(self.driver)

        #new HS auth window
        SubmitLandingPage.to_hs_window(self.driver)
        self.assertIn("HydroShare", TestSystem.title(self.driver))
        HydroshareWindow.authorize_hs_backend(self.driver, HS_USERNAME, HS_PASSWORD)
        HydroshareWindow.to_origin_window(self.driver)

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
        self.login_orcid_and_hs()
        SubmitLandingPage.to_hs_submit(self.driver)
        auto_text = time.strftime("%d %b %Y %H:%M:%S", time.gmtime())
        SubmitHydroshare.autofill_required_elements(self.driver, auto_text)
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

        # TODO: this test fails because of a bad css selector for checking keywords
        TestSystem.wait()

    def test_A_000005(self):
        """Confirm that one can't submit to HS without required fields"""
        self.login_orcid_and_hs()
        SubmitLandingPage.to_hs_submit(self.driver)
        auto_text = time.strftime("%d %b %Y %H:%M:%S", time.gmtime())
        SubmitHydroshare.autofill_required_elements(self.driver, auto_text)
        self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

        # TODO: this works for abstract, but not for agency or title...
        # required_text_items = ["abstract", "title", "agency_name"]

        required_text_items = ["abstract"]
        for text_elem in required_text_items:
            SubmitHydroshare.unfill_text_element_by_name(self.driver, text_elem)
            self.assertRaises(BaseException, SubmitHydroshare.is_finishable(self.driver))
            SubmitHydroshare.fill_text_element_by_name(self.driver, text_elem, auto_text)
            self.assertTrue(SubmitHydroshare.is_finishable(self.driver))

if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
