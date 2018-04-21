import argparse
import unittest

from selenium import webdriver


class BaseTest(unittest.TestCase):
    GRID_HUB_IP = None

    def setUp(self):
        """ Setup driver for use in automation tests """

        if self.GRID_HUB_IP is not None:
            driver = webdriver.Remote(
                command_executor='http://{}:4444/wd/hub'.format(self.GRID_HUB_IP),
                desired_capabilities={'browserName': 'firefox'})
        else:
            profile = webdriver.FirefoxProfile()
            profile.set_preference('general.useragent.override',
                                   'CUAHSI-QA-Selenium')
            driver = webdriver.Firefox(profile)

        self.driver = driver

    def tearDown(self):
        self.driver.quit()


def basecli():
    parser = argparse.ArgumentParser()
    parser.add_argument('--grid')
    parser.add_argument('unittest_args', nargs='*')

    return parser
