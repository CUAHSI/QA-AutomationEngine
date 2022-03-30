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
    NEW_SUBMISSION_SAVE,
    DEFAULT_TIMEOUT
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
    navigation_contact = SiteElement(By.ID, "navbar-nav-Contact")
    is_saving = SiteElement(By.ID, "new-submission-saving")

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
        self.wait_until_element_visible(driver, MySubmissions.title, MY_SUBMISSIONS_LOAD)

    @classmethod
    def drawer_to_my_submissions(self, driver):
        self.drawer_nav_my_submissions.click(driver)
        self.wait_until_element_visible(driver, MySubmissions.title, MY_SUBMISSIONS_LOAD)

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
        self.wait_until_element_visible(driver, self.orcid_login_continue, AUTH_WINDOW)
        self.orcid_login_continue.click(driver)
        External.switch_new_page(driver, num_windows_now, self.body_locator)

    @classmethod
    def wait_until_css_visible(self, driver, css_selector, timeout=DEFAULT_TIMEOUT):
        element = SiteElement(By.CSS_SELECTOR, css_selector)
        waited = 0
        while waited < timeout:
            if element.is_visible(driver):
                return
            else:
                time.sleep(1)
                waited += 1

    @classmethod
    def wait_until_css_dissapear(self, driver, css_selector, timeout=DEFAULT_TIMEOUT):
        element = SiteElement(By.CSS_SELECTOR, css_selector)
        waited = 0
        while waited < timeout:
            if not element.is_visible(driver):
                return
            else:
                time.sleep(1)
                waited += 1

    @classmethod
    def wait_until_element_visible(self, driver, element, timeout=DEFAULT_TIMEOUT):
        waited = 0
        while waited < timeout:
            if element.is_visible(driver):
                return
            else:
                time.sleep(1)
                waited += 1

    @classmethod
    def wait_until_element_not_visible(self, driver, element, timeout=DEFAULT_TIMEOUT):
        waited = 0
        while waited < timeout:
            # if not element.is_visible(driver):
            if not element.is_visible(driver):
                return
            else:
                time.sleep(1)
                waited += 1

    @classmethod
    def wait_until_element_not_exist(self, driver, element, timeout=DEFAULT_TIMEOUT):
        waited = 0
        while waited < timeout:
            # if not element.is_visible(driver):
            if not element.exists(driver):
                return
            else:
                time.sleep(1)
                waited += 1


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
    authorize = SiteElement(By.CSS_SELECTOR, '#authorizationForm input[name="allow"]')

    @classmethod
    def authorize_hs_backend(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)
        self.authorize.click(driver)


class MySubmissions(Dsp):
    """ Page displaying users submissions """
    title = SiteElement(By.CSS_SELECTOR, ".text-h4:nth-of-type(1)")
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
    hydroshare_repo = SiteElement(By.ID, "HydroShare-card")
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
    alert = SiteElement(By.CSS_SELECTOR, ".v-alert .v-alert__content")
    top_save = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-top button.submission-save")
    title = SiteElement(By.CSS_SELECTOR, '[data-id*="BasicInformation"] input[data-id*="Title"]')

    # required_elements = SiteElementsCollection(By.CSS_SELECTOR, "input[required='required']")
    # required_elements = SiteElementsCollection(By.CSS_SELECTOR, "input[data-id$="*")

    # Basic info
    abstract = SiteElement(By.ID, "#/properties/abstract-input")
    subject_keyword_input = SiteElement(By.CSS_SELECTOR, 'input[data-id*="Subjectkeywords"]')
    # TODO: this selector is still fragile to additions of other v-select items withing the basic info
    subject_keywords = SiteElementsCollection(By.CSS_SELECTOR, 'fieldset[data-id*="group-BasicInformation"] span.v-chip__content')
    subject_keyword_container = SiteElement(By.CSS_SELECTOR, '[data-id="group-BasicInformation"] .v-select__selections')

    # Contributors
    expand_contributors = SiteElement(By.CSS_SELECTOR, '[data-id*="Contributors"] button.btn-add')

    # Spatial coverage
    expand_spatial = SiteElement(By.CSS_SELECTOR, '[data-id*="Spatialcoverage"] button.btn-add')

    # Additional metadata
    expand_metadata = SiteElement(By.CSS_SELECTOR, '[data-id*="Additionalmetadata"] button.btn-add')

    # Related resources
    expand_related_resources = SiteElement(By.CSS_SELECTOR, '[data-id*="Relatedresources"] button.btn-add')

    # Temporal
    temporal_name_input = SiteElement(By.CSS_SELECTOR, 'div[data-id*="Temporalcoverage"] input[data-id*="Name"]')
    start_input = SiteElement(By.CSS_SELECTOR, '[data-id*="Temporalcoverage"] input[data-id*="Start"]')
    end_input = SiteElement(By.CSS_SELECTOR, '[data-id*="Temporalcoverage"] input[data-id*="End"]')

    # Funding agency
    expand_funding_agency = SiteElement(By.CSS_SELECTOR, 'button[aria-label*="Funding agency"]')
    agency_name = SiteElement(By.ID, "#/properties/funding_agency_name-input")

    # Rights
    rights_statement = SiteElement(By.ID, "#/properties/statement-input")
    rights_url = SiteElement(By.ID, "#/properties/url-input")

    bottom_save = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-save")
    bottom_finish = SiteElement(By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-finish")

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
        self.fill_basic_info(driver, auto)
        if isinstance(auto, str):
            self.fill_funding_agency(driver, auto)
        else:
            self.fill_funding_agency(driver, auto["funding_agency_name-input"])

    @classmethod
    def fill_basic_info(self, driver, basic_info):
        if isinstance(basic_info, str):
            title = basic_info
            abstract = basic_info
            subject_keyword_input = basic_info
        else:
            title = basic_info["title-input"]
            abstract = basic_info["abstract-input"]
            subject_keyword_input = basic_info["subjects-input"]

        self.title.scroll_to(driver)
        self.title.inject_text(driver, title)
        self.abstract.inject_text(driver, abstract)
        self.subject_keyword_container.click(driver)
        if isinstance(subject_keyword_input, str):
            self.subject_keyword_input.inject_text(driver, subject_keyword_input)
            self.subject_keyword_input.submit(driver)
        else:
            for keyword in subject_keyword_input:
                self.subject_keyword_input.inject_text(driver, keyword)
                self.subject_keyword_input.submit(driver)

    @classmethod
    def fill_funding_agency(self, driver, agency):
        self.expand_funding_agency.scroll_to(driver)
        self.expand_funding_agency.javascript_click(driver)
        self.agency_name.inject_text(driver, agency)
        self.agency_name.submit(driver)

    @classmethod
    def click_expand_contributors(self, driver):
        self.expand_contributors.scroll_to(driver)
        self.expand_contributors.javascript_click(driver)

    @classmethod
    def click_expand_spatial(self, driver):
        self.expand_spatial.scroll_to(driver)
        self.expand_spatial.javascript_click(driver)

    @classmethod
    def click_expand_metadata(self, driver):
        self.expand_metadata.scroll_to(driver)
        self.expand_metadata.javascript_click(driver)

    @classmethod
    def click_expand_related_resources(self, driver):
        self.expand_related_resources.scroll_to(driver)
        self.expand_related_resources.javascript_click(driver)

    @classmethod
    def fill_related_resources(self, driver, relation_type, value, n):
        self.click_expand_related_resources(driver)

        sel = f'div[data-id*="Relatedresources"] input[data-id*="RelationType"]:nth-of-type({n})'
        relation_type_input = SiteElement(By.CSS_SELECTOR, sel)
        sel = f'div[data-id*="Relatedresources"] input[data-id*="Value"]:nth-of-type({n})'
        related_resources_value = SiteElement(By.CSS_SELECTOR, sel)
        sel = f'div[data-id*="Relatedresources"] div.v-select:nth-of-type({n})'
        relation_type_container = SiteElement(By.CSS_SELECTOR, sel)

        relation_type_container.scroll_to(driver)
        relation_type_container.javascript_click(driver)
        relation_type_input.inject_text(driver, relation_type)
        relation_type_input.submit(driver)
        related_resources_value.inject_text(driver, value)
        related_resources_value.submit(driver)

    # @classmethod
    # def fill_related_resources(self, driver, related_resources):
    #     self.click_expand_related_resources(driver)
    #     self.relation_type_input.scroll_to(driver)
    #     self.relation_type_input.click(driver)
    #     self.relation_type_input.inject_text(driver, title)
    #     self.related_resources_value.inject_text(driver, abstract)
    #     self.subject_keyword_container.click(driver)
    #     if isinstance(subject_keyword_input, str):
    #         self.subject_keyword_input.inject_text(driver, subject_keyword_input)
    #         self.subject_keyword_input.submit(driver)
    #     else:
    #         for keyword in subject_keyword_input:
    #             self.subject_keyword_input.inject_text(driver, keyword)
    #             self.subject_keyword_input.submit(driver)

    @classmethod
    def save_bottom(self, driver):
        self.bottom_save.scroll_to(driver)
        self.bottom_save.click(driver)
        self.wait_until_element_not_visible(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def is_finishable(self, driver):
        self.bottom_finish.scroll_to(driver)
        finishable = self.bottom_finish.get_attribute(driver, "disabled") is None \
            or self.bottom_finish.get_attribute(driver, "disabled") != "disabled"
        return finishable

    @classmethod
    def finish_submission(self, driver):
        self.bottom_finish.scroll_to(driver)
        self.bottom_finish.click(driver)
        self.wait_until_element_not_exist(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def get_did_in_section(self, driver, section=None, data_id="", nth=1):
        selector = f'div[data-id*="{section}"] [data-id*="{data_id}"]:nth-of-type({nth})'
        return SiteElement(By.CSS_SELECTOR, selector)

    @classmethod
    def get_css_in_section(self, driver, section=None, css="", nth=1):
        selector = f'div[data-id*="{section}"] {css}'
        return SiteElement(By.CSS_SELECTOR, selector)

    @classmethod
    def fill_inputs_by_data_ids(self, driver, dict, section=None, nth=1):
        for k, v in dict.items():
            try:
                if section and nth:
                    selector = f'div[data-id*="{section}"] [data-id*="{k}"]:nth-of-type({nth})'
                    element = SiteElement(By.CSS_SELECTOR, selector)
                else:
                    element = SiteElement(By.CSS_SELECTOR, f'[data-id*="{k}"]:nth-of-type(1)')
            except TimeoutException as e:
                print(f"{e}\nElement not found for key: {k}")
                return False
            if element.exists_in_dom(driver):
                element.scroll_to(driver)
                element.javascript_click(driver)
                element.inject_text(driver, v)
                element.submit(driver)
            else:
                return False
        return True

    @classmethod
    def unfill_text_by_page_property(self, driver, element):
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.javascript_click(driver)".format(element))
        eval("self.{}.clear_all_text(driver)".format(element))

    @classmethod
    def fill_text_by_page_property(self, driver, element, text_to_fill):
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.javascript_click(driver)".format(element))
        eval("self.{}.inject_text(driver, '{}')".format(element, text_to_fill))


class EditHSSubmission(SubmitHydroshare):
    header_title = SiteElement(By.CSS_SELECTOR, ".text-h4")

    @classmethod
    def get_header_title(self, driver):
        return self.header_title.get_text(driver)

    @classmethod
    def check_required_elements(self, driver, auto):
        if not self.check_basic_info(driver, auto, auto, ["CZNet", auto]):
            return False
        if not self.check_funding_agency_name(driver, auto):
            return False
        return True

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
    def check_funding_agency_name(self, driver, agency):
        self.expand_funding_agency.scroll_to(driver)
        return self.agency_name.get_value(driver) == agency

    @classmethod
    def get_keywords(self, driver):
        keywords = self.subject_keyword_container.get_texts_from_xpath(driver, './/span/span[contains(@class, "v-chip__content")]')
        return keywords

    @classmethod
    def get_nth_relation_type(self, driver, n):
        sel = f'div[data-id*="Relatedresources"] input[data-id*="RelationType"]:nth-of-type({n})'
        relation_type_input = SiteElement(By.CSS_SELECTOR, sel)
        return relation_type_input.get_texts_from_xpath(driver, './preceding::div[1]')

    @classmethod
    def check_keywords(self, driver, keywords=None):
        saved_keywords = self.get_keywords(driver)
        if isinstance(keywords, str):
            if keywords not in saved_keywords:
                return False
        else:
            if not all(elem in saved_keywords for elem in keywords):
                return False
        return True

    @classmethod
    def get_nth_keyword_text(self, driver, n):
        span = SiteElement(By.CSS_SELECTOR, ".v-select__selections span:nth-of-type({}) span.v-chip__content".format(n))
        return span.get_text(driver)

    @classmethod
    def check_fields_by_dict(self, driver, dict):
        for k, v in dict.items():
            element = SiteElement(By.ID, "#/properties/" + k)
            element.scroll_to(driver)
            value = element.get_value(driver)
            if value != v:
                print(f"\nMismatch when checking field: {k}. Expected {v} got {value}")
                return False
        return True

    @classmethod
    def check_inputs_by_data_ids(self, driver, dict, section=None, nth=1):
        for k, v in dict.items():
            if section and nth:
                selector = f'div[data-id*="{section}"] [data-id*="{k}"]:nth-of-type({nth})'
                elem = SiteElement(By.CSS_SELECTOR, selector)
            else:
                elem = SiteElement(By.CSS_SELECTOR, f'[data-id*="{k}"]:nth-of-type(1)')
            elem.scroll_to(driver)
            value = elem.get_value(driver)
            if value != v:
                print(f"\nMismatch when checking field: {k}. Expected {v} got {value}")
                return False
        return True


class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
