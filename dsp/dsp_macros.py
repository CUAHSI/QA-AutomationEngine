import json
import os
import re
import requests
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dateutil import parser
from urllib.request import urlretrieve, urlopen
from datetime import datetime

from cuahsi_base.site_element import SiteElement, SiteElementsCollection
from cuahsi_base.utils import External, TestSystem

from config import BASE_URL

from timing import (
    EXTERNAL_PAGE_LOAD,
    KEYS_RESPONSE,
    MY_SUBMISSIONS_LOAD,
    RETURN_PREVIOUS,
    AUTH_WINDOW
)


class WebPage:
    body_locator = By.CSS_SELECTOR, "body"

    @classmethod
    def to_previous_window(self, driver, wait=False):
        if wait:
            TestSystem.wait(RETURN_PREVIOUS)
        External.switch_old_page(driver)
    
    @classmethod
    def to_origin_window(self, driver, wait=False):
        if wait:
            TestSystem.wait(RETURN_PREVIOUS)
        External.switch_first_page(driver)


class Dsp(WebPage):
    navigation_logo = SiteElement(By.CSS_SELECTOR, "#app-bar .logo")
    navigation_home = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/"]')
    navigation_my_submissions = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/submissions"]')
    navigation_resources = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/resources"]')
    navigation_submit = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/submit"]')
    navigation_about = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/about"]')
    navigation_contact = SiteElement(By.CSS_SELECTOR, '.nav-items a[href="/contact"]')
    
    # responsive
    navigation_hamburger = SiteElement(By.CSS_SELECTOR, "#app-bar .v-app-bar__nav-icon")
    navigation_drawer = SiteElement(By.CSS_SELECTOR, ".v-navigation-drawer")
    drawer_nav_home = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/"]')
    drawer_nav_my_submissions = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/submissions"]')
    drawer_nav_resources = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/resources"]')
    drawer_nav_submit = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/submit"]')
    drawer_nav_about = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/about"]')
    drawer_nav_contact = SiteElement(By.CSS_SELECTOR, '.v-navigation-drawer__content a[href="/contact"]')

    # login
    orcid_login_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login")
    orcid_login_continue = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login button.primary")

    @classmethod
    def logo_to_home(self, driver):
        self.navigation_logo.click(driver)

    @classmethod
    def to_home(self, driver):
        self.navigation_home.click(driver)
    
    @classmethod
    def show_mobile_nav(self, driver):
        self.navigation_hamburger.click(driver)

    @classmethod
    def to_my_submissions(self, driver):
        self.navigation_my_submissions.click(driver)
        TestSystem.wait(MY_SUBMISSIONS_LOAD)
    
    @classmethod
    def drawer_to_my_submissions(self, driver):
        self.drawer_nav_my_submissions.click(driver)
        TestSystem.wait(MY_SUBMISSIONS_LOAD)
    
    @classmethod
    def drawer_to_submit(self, driver):
        self.drawer_nav_submit.click(driver)

    @classmethod
    def to_resources(self, driver):
        self.navigation_resources.click(driver)

    @classmethod
    def to_submit(self, driver):
        self.navigation_submit.click(driver)

    @classmethod
    def to_about(self, driver):
        self.navigation_about.click(driver)

    @classmethod
    def to_contact(self, driver):
        self.navigation_contact.click(driver)

    @classmethod
    def is_visible_orcid_modal(self, driver):
        return self.orcid_login_modal.is_visible(driver)
    
    @classmethod
    def to_orcid_window(self, driver):
        num_windows_now = len(driver.window_handles)
        self.orcid_login_continue.click(driver)
        External.switch_new_page(driver, num_windows_now, self.body_locator)

class OrcidWindow(WebPage):
    """ Orcid window"""
    username = SiteElement(By.ID, "username")
    password = SiteElement(By.ID, "password")
    submit = SiteElement(By.ID, "signin-button")

    @classmethod
    def fill_credentials(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)

class HydroshareWindow(WebPage):
    """ Authentication window to use Hydroshare as Backend """
    username = SiteElement(By.ID, "id_username")
    password = SiteElement(By.ID, "id_password")
    submit = SiteElement(By.CSS_SELECTOR, ".account-form .btn-primary")
    authorize =  SiteElement(By.CSS_SELECTOR, '#authorizationForm input[name="allow"]')

    @classmethod
    def authorize_hs_backend(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)
        self.authorize.click(driver)

class MySubmissions(Dsp):
    """ Page displaying users submissions """
    # TODO: tests for my_submissions
    pass


class SubmitLandingPage(Dsp):
    """ Page containing options for submitting data """
    hydroshare_repo = SiteElement(By.CSS_SELECTOR, 'div.repositories img[alt="HydroShare"]')
    submit_to_hs_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog div.cz-authorize")
    submit_to_hs_authorize = SiteElement(By.CSS_SELECTOR, ".cz-authorize button.primary")

    @classmethod
    def hydroshare_repo_select(self, driver):
        self.hydroshare_repo.click(driver)

    @classmethod
    def authorize_hs_submit(self, driver):
        self.submit_to_hs_authorize.click(driver)

    @classmethod
    def to_hs_window(self, driver):
        TestSystem.wait(AUTH_WINDOW)
        num_windows_now = len(driver.window_handles)
        self.submit_to_hs_authorize.click(driver)
        External.switch_new_page(driver, num_windows_now, self.body_locator)
    
    @classmethod
    def to_hs_submit(self, driver):
        Dsp.show_mobile_nav(driver)
        Dsp.drawer_to_submit(driver)
        self.hydroshare_repo_select(driver)

class SubmitHydroshare(Dsp):
    """ Page containing forms for submitting data with HS backend"""

    header = SiteElement(By.CSS_SELECTOR, ".cz-new-submission h1")
    alert = SiteElement(By.CSS_SELECTOR,  ".v-alert .v-alert__content")
    top_save = SiteElement(By.CSS_SELECTOR, "div.cz-new-submission-actions:nth-of-type(1) button:nth-of-type(1)")
    title =  SiteElement(By.ID, "#/properties/title-input")
    abstract = SiteElement(By.ID, "#/properties/abstract-input")
    subjects_input = SiteElement(By.ID, "#/properties/subjects-input")
    bottom_save = SiteElement(By.CSS_SELECTOR, ".cz-new-submission-actions:nth-of-type(2) button:nth-of-type(1)")

    @classmethod
    def get_header_text(self, driver):
        return self.header.get_text(driver)
    
    @classmethod
    def get_alert_text(self, driver):
        return self.alert.get_text(driver)

    @classmethod
    def is_form_saveable(self, driver):
        return self.top_save.get_attribute(driver, "disabled") != "disabled"




class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
