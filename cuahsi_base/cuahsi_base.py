import argparse
import sys
import unittest

from selenium import webdriver

from .browser import USER_AGENT


class BaseTest(unittest.TestCase):
    grid_hub_ip = None
    browser = 'firefox'

    def setUp(self):
        """ Setup driver for use in automation tests """

        if self.grid_hub_ip is not None:
            remote_args = {'command_executor':
                           'http://{}:4444/wd/hub'.format(self.grid_hub_ip),
                           'desired_capabilities': {'browserName': self.browser}}
            if self.browser == 'firefox':
                remote_args['browser_profile'] = self._firefox_profile()
            elif self.browser == 'chrome':
                remote_args['options'] = self._chrome_options()
            unittest.main(warnings="ignore")
            driver = webdriver.Remote(**remote_args)
        else:
            if self.browser == 'firefox':
                driver = webdriver.Firefox(self._firefox_profile())
            elif self.browser == 'chrome':
                driver = webdriver.Chrome(options=self._chrome_options())
            elif self.browser == 'safari':
                # Fails with 'AttributeError' at time of writing this comment
                # (selenium==3.11.0) because of a bug in selenium code.
                # See https://github.com/SeleniumHQ/selenium/issues/5578
                driver = webdriver.Safari()
            else:
                raise RuntimeError('Unknown browser type. Supported browser types '
                                   'are: "firefox", "chrome", "safari".')

        self.driver = driver

    @staticmethod
    def _firefox_profile():
        profile = webdriver.FirefoxProfile()
        profile.set_preference('general.useragent.override', USER_AGENT)
        return profile

    @staticmethod
    def _chrome_options():
        options = webdriver.ChromeOptions()
        options.add_argument('--user-agent={}'.format(USER_AGENT))
        return options

    def tearDown(self):
        self.driver.quit()


def basecli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid')
    parser.add_argument('--browser')
    parser.add_argument('unittest_args', nargs='*')

    return parser


def parse_args_run_tests(test_class):
    args = basecli().parse_args()
    test_class.grid_hub_ip = args.grid
    if args.browser is not None:
        test_class.browser = args.browser

    sys.argv[1:] = args.unittest_args
    unittest.main(verbosity=2)
