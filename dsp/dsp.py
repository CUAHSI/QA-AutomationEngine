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
    MySubmissions,
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
class DspTestSuite(BaseTestSuite):
    """Python unittest setup for functional tests"""

    def setUp(self):
        super(DspTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_A_000001(self):
        """Ensure anonymous navigation to my submissions shows orcid login modal"""
        Dsp.show_mobile_nav(self.driver)
        Dsp.drawer_to_my_submissions(self.driver)
        login_visible = MySubmissions.is_visible_orcid_login(self.driver)
        self.assertTrue(login_visible)


if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
