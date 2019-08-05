""" Runs various smoke tests for the hydroshare.org """
import os
import random
import re
import time

from urllib.request import urlretrieve

from hs_macros import (
    Home,
    Resource,
    NewResource,
    WebApp,
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

    def test_webapp(self):
        """Ensure Correct Web apps show in Open With"""

        # login
        Home.login(self.driver, USERNAME, PASSWORD)
        Home.create_resource(self.driver, "ToolResource")

        # create web app resource
        NewResource.configure(self.driver, "TEST Web App")
        NewResource.create(self.driver)

        # configure web app resource
        WebApp.support_composite(self.driver)
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

if __name__ == "__main__":
    parse_args_run_tests(HydroshareTestSuite)
