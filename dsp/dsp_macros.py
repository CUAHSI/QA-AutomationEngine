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
    AUTH_WINDOW,
    HS_SUBMIT
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
    navigation_home = SiteElement(By.ID, "navbar-nav-home")
    navigation_my_submissions = SiteElement(By.ID, "navbar-nav-MySubmissions")
    navigation_resources = SiteElement(By.ID, "navbar-nav-Resources")
    navigation_submit = SiteElement(By.ID, "navbar-nav-SubmitData")
    navigation_about = SiteElement(By.ID, "navbar-nav-About")
    navigation_contact = SiteElement(By.ID,"navbar-nav-Contact")
    
    # responsive
    navigation_hamburger = SiteElement(By.CSS_SELECTOR, "#app-bar .v-app-bar__nav-icon")
    navigation_drawer = SiteElement(By.CSS_SELECTOR, ".v-navigation-drawer")
    drawer_nav_home = SiteElement(By.ID, "drawer-nav-home")
    drawer_nav_my_submissions = SiteElement(By.ID, "drawer-nav-MySubmissions")
    drawer_nav_resources = SiteElement(By.ID, "drawer-nav-Resources")
    drawer_nav_submit = SiteElement(By.ID, "drawer-nav-SubmitData")
    drawer_nav_about = SiteElement(By.ID, "drawer-nav-About")
    drawer_nav_contact = SiteElement(By.ID, "drawer-nav-Contact")

    # login
    orcid_login_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login")
    orcid_login_continue = SiteElement(By.ID, "orcid_login_continue")

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
    title = SiteElement(By.CSS_SELECTOR, ".text-h4")
    total_submissions = SiteElement(By.ID, "total_submissions")
    top_submission = SiteElement(By.ID, "submission-0")
    top_submission_name = SiteElement(By.ID, "sub-0-title")
    top_submission_date = SiteElement(By.ID, "sub-0-date")
    sort_order_select = SiteElement(By.ID, "sort-order")
    my_submissions_search = SiteElement(By.ID, "my_submissions_search")
    top_submission_edit = SiteElement(By.ID, "sub-0-edit")

    @classmethod
    def get_title(self, driver):
        return self.title.get_text(driver)

    @classmethod
    def get_total_submissions(self, driver):
        text = self.total_submissions.get_text(driver)
        return int(text.split(" ", 1)[0])
    
    # TODO: get sort order working with Vuetify dropdowns
    # @classmethod
    # def sort_order(self, driver, index=1):
    #     self.sort_order_select.javascript_click_invisible(driver)
    #     select_string = f"#sort-order v-list-item__content:nth-of-type({index})"
    #     to_select = SiteElement(By.CSS_SELECTOR, select_string)
    #     to_select.click(driver)

    @classmethod
    def get_top_submission_name(self, driver):
        return self.top_submission_name.get_text(driver)
    
    @classmethod
    def get_top_submission_date(self, driver):
        return self.top_submission_date.get_text(driver)

    @classmethod
    def enter_text_in_search(self, driver, field_text):
        self.my_submissions_search.inject_text(driver, field_text)
    
    @classmethod
    def edit_top_submission(self, driver):
        self.top_submission_edit.click(driver)


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
    top_save = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-top button.submission-save")
    title =  SiteElement(By.ID, "#/properties/title-input")
    abstract = SiteElement(By.ID, "#/properties/abstract-input")
    subject_keyword_input = SiteElement(By.CSS_SELECTOR, 'input[id="#/properties/subjects-input"]:nth-of-type(1)')
    subject_keywords = SiteElementsCollection(By.CSS_SELECTOR, 'span.v-chip__content')
    bottom_save = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-save")
    bottom_finish = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-finish")

    # required_elements = SiteElementsCollection(By.CSS_SELECTOR, "input[required='required']")
    expand_funding_agency = SiteElement(By.CSS_SELECTOR, 'button[aria-label*="Funding agency"]')
    agency_name = SiteElement(By.ID, "#/properties/funding_agency_name-input")

    @classmethod
    def get_header_text(self, driver):
        return self.header.get_text(driver)
    
    @classmethod
    def get_alert_text(self, driver):
        return self.alert.get_text(driver)

    @classmethod
    def is_form_saveable(self, driver):
        return self.top_save.get_attribute(driver, "disabled") != "disabled"
    
    @classmethod
    def autofill_required_elements(self, driver, auto):
        self.fill_basic_info(driver, auto, auto, auto)
        self.fill_funding_agency(driver, auto)
    
    @classmethod
    def unfill_text_element_by_name(self, driver, element):
        self.header.scroll_to(driver)
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.click(driver)".format(element))
        eval("self.{}.clear_all_text(driver)".format(element))
        self.header.scroll_to(driver)
    
    @classmethod
    def fill_text_element_by_name(self, driver, element, text_to_fill):
        self.header.scroll_to(driver)
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.click(driver)".format(element))
        eval("self.{}.inject_text(driver, '{}')".format(element, text_to_fill))
        self.header.scroll_to(driver)

    @classmethod
    def fill_basic_info(self, driver, title, abstract, subject_keyword_input):
        self.title.scroll_to(driver)
        self.title.inject_text(driver, title)
        self.abstract.inject_text(driver, abstract)
        self.subject_keyword_input.javascript_click_invisible(driver)
        if isinstance(subject_keyword_input, str):
            self.subject_keyword_input.inject_invisible_text(driver, subject_keyword_input)
            self.subject_keyword_input.submit_invisible(driver)
        else:
            for keyword in subject_keyword_input:
                self.subject_keyword_input.inject_invisible_text(driver, keyword)
                self.subject_keyword_input.submit_invisible(driver)
    
    @classmethod
    def fill_funding_agency(self, driver, agency):
        self.expand_funding_agency.scroll_to(driver)
        self.expand_funding_agency.javascript_click(driver)
        self.agency_name.inject_text(driver, agency)
        self.agency_name.submit(driver)
    
    @classmethod
    def save_bottom(self, driver):
        self.bottom_save.scroll_to(driver)
        self.bottom_save.click(driver)
        TestSystem.wait(HS_SUBMIT)

    @classmethod
    def is_finishable(self, driver):
        self.bottom_finish.scroll_to(driver)
        finishable = self.bottom_finish.get_attribute(driver, "disabled") == None \
            or self.bottom_finish.get_attribute(driver, "disabled") != "disabled"
        return finishable

    @classmethod
    def finish_submission(self, driver):
        self.bottom_finish.invisible_scroll_to(driver)
        self.bottom_finish.click(driver)



class EditHSSubmission(SubmitHydroshare):
    header_title = SiteElement(By.CSS_SELECTOR, ".text-h4")
    
    @classmethod
    def get_header_title(self, driver):
        return self.header_title.get_text(driver)
    
    @classmethod
    def check_required_elements(self, driver, auto):
        if not self.check_basic_info(driver, auto, auto, ["CZNet", auto]):
            return False
        if not self.check_funding_agency(driver, auto):
            return False
        return True
    
    @classmethod
    def check_funding_agency(self, driver, agency):
        self.expand_funding_agency.scroll_to(driver)
        return self.agency_name.get_value(driver) == agency
    
    @classmethod
    def check_basic_info(self, driver, title, abstract, keywords):
        self.title.scroll_to(driver)
        if self.title.get_value(driver) != title:
            return False
        self.abstract.scroll_to(driver)
        if self.abstract.get_value(driver) != abstract:
            return False
        return self.check_keywords(driver, keywords)
    
    @classmethod
    def check_keywords(self, driver, keywords=None):
        if isinstance(keywords, str):
            text = self.get_keyword_text(driver, 1)
            if text != keywords:
                print(f"\nThe keyword text is: {text}")
                return False
        else:
            for idx, keyword in enumerate(keywords):
                text = self.get_keyword_text(driver, idx+1)
                if text != keyword:
                    print(f"\nThe keyword text is: {text}")
                    return False
            return True
    
    @classmethod
    def get_keyword_text(self, driver, index):
        #TODO: this test fails because this CSS selector doesn't work for any but the first span
        span = SiteElement(By.CSS_SELECTOR, "div.v-select__selections span.v-chip__content:nth-of-type({})".format(index))
        return span.get_text(driver)

class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
