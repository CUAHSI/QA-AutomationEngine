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

from dsp_macros import (
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
class DspTestSuite(BaseTestSuite):
    """Python unittest setup for functional tests"""

    def setUp(self):
        super(DspTestSuite, self).setUp()
        self.driver.get(BASE_URL)

    def test_A_000001(self):
        """
        TODO: This will be the first DSP test...
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


if __name__ == "__main__":
    parse_args_run_tests(DspTestSuite)
