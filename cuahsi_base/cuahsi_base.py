import argparse
import datetime
import json
import sys
import time
import unittest
import warnings

from botocore.config import Config
from google.cloud import pubsub_v1
from selenium import webdriver

from .browser import USER_AGENT
from .utils import kinesis_record

SPAM_DATA_STREAM_NAME = "cuahsi-quality-spam-data-stream"
SPAM_DATA_STREAM_CONFIG = Config(
    region_name="us-east-2",
)
TEST_DURATION_DATA_STREAM_NAME = "cuahsi-quality-test-duration-data-stream"
TEST_DURATION_DATA_STREAM_CONFIG = Config(
    region_name="us-east-2",
)

GCP_PROJECT_ID = "cuahsiqa"
GCP_TOPIC_ID = "test-runs"

USER_COUNT = 1


class BaseTestSuite(unittest.TestCase):
    grid_hub_ip = None
    resource = None
    browser = "firefox"
    records = None
    base_url_arg = None
    headless = False
    data = {}
    past_errors = 0
    past_failures = 0
    publisher = None
    topic_path = None

    def setUp(self):
        """Setup driver for use in automation tests"""

        if self.records is not None:
            self.data["test"] = self._testMethodName
        if self.records == "aws":
            self.data["start_time"] = time.time()
        elif self.records == "gcp":
            self.data["start_time"] = datetime.datetime.now().isoformat()

        if self.grid_hub_ip is not None:
            warnings.simplefilter("ignore", ResourceWarning)
            remote_args = {
                "command_executor": "http://{}:4444/wd/hub".format(self.grid_hub_ip),
                "desired_capabilities": {"browserName": self.browser},
            }
            if self.browser == "firefox":
                remote_args["browser_profile"] = self._firefox_profile()
            elif self.browser == "chrome":
                remote_args["options"] = self._chrome_options()
            driver = webdriver.Remote(**remote_args)
        else:
            if self.browser == "firefox":
                options = webdriver.FirefoxOptions()
                if self.headless:
                    options.add_argument("--headless")
                    options.set_preference(
                        "dom.webnotifications.serviceworker.enabled", False
                    )
                    options.set_preference("dom.webnotifications.enabled", False)
                driver = webdriver.Firefox(self._firefox_profile(), options=options)
            elif self.browser == "chrome":
                options = self._chrome_options()
                if self.headless:
                    options.add_argument("--headless")
                driver = webdriver.Chrome(options=options)
            elif self.browser == "safari":
                # Fails with 'AttributeError' at time of writing this comment
                # (selenium==3.11.0) because of a bug in selenium code.
                # See https://github.com/SeleniumHQ/selenium/issues/5578
                driver = webdriver.Safari()
            else:
                raise RuntimeError(
                    "Unknown browser type. Supported browser types "
                    'are: "firefox", "chrome", "safari".'
                )

        self.driver = driver

    def getResourceId(self):
        return self.resource

    @staticmethod
    def _firefox_profile():
        profile = webdriver.FirefoxProfile()
        profile.accept_untrusted_certs = True
        profile.set_preference("general.useragent.override", USER_AGENT)
        return profile

    @staticmethod
    def _chrome_options():
        options = webdriver.ChromeOptions()
        options.add_argument("ignore-certificate-errors")
        options.add_argument("--user-agent={}".format(USER_AGENT))
        return options

    def list2reason(self, exc_list):
        if exc_list and exc_list[-1][0] is self:
            return exc_list[-1][1]

    def tearDown(self):
        self.driver.quit()

        # https://gist.github.com/hynekcer/1b0a260ef72dae05fe9611904d7b9675
        if hasattr(self, "_outcome"):  # Python 3.4+
            result = self.defaultTestResult()  # these 2 methods have no side effects
            self._feedErrorsToResult(result, self._outcome.errors)
        else:  # Python 3.2 - 3.3 or 2.7
            result = getattr(self, "_outcomeForDoCleanups", self._resultForDoCleanups)
        ok = self.past_errors == len(result.errors) and self.past_failures == len(
            result.failures
        )
        self.past_errors = len(result.errors)
        self.past_failures = len(result.failures)

        if self.records == "aws":
            self.data["end_time"] = time.time()
            self.data["passed"] = ok
            self.data["parallel_users"] = USER_COUNT
            kinesis_record(
                TEST_DURATION_DATA_STREAM_CONFIG,
                TEST_DURATION_DATA_STREAM_NAME,
                "test-duration",
                self.data,
            )
        elif self.records == "gcp":
            self.data["end_time"] = datetime.datetime.now().isoformat()
            self.data["passed"] = ok
            self.data["parallel_users"] = USER_COUNT
            future = self.publisher.publish(
                self.topic_path,
                json.dumps(self.data, ensure_ascii=False).encode("utf8"),
            )
            future.result()


def basecli():
    parser = argparse.ArgumentParser()
    parser.add_argument("--grid")
    parser.add_argument("--browser")
    parser.add_argument("--resource")
    parser.add_argument("--records")
    parser.add_argument("--base")
    parser.add_argument("--headless", action=argparse.BooleanOptionalAction)
    parser.add_argument("unittest_args", nargs="*")

    return parser


def parse_args_run_tests(test_class):
    args = basecli().parse_args()
    test_class.grid_hub_ip = args.grid
    test_class.resource = args.resource
    if args.browser is not None:
        test_class.browser = args.browser
    if args.records is not None:
        test_class.records = args.records
    if args.base is not None:
        test_class.base_url_arg = args.base
    if args.headless is not None:
        test_class.headless = args.headless
    if args.records == "gcp":
        test_class.publisher = pubsub_v1.PublisherClient()
        test_class.topic_path = test_class.publisher.topic_path(
            GCP_PROJECT_ID, GCP_TOPIC_ID
        )

    sys.argv[1:] = args.unittest_args
    unittest.main(verbosity=2)
