import time

from selenium.webdriver.common.by import By
from selenium.common.exceptions import TimeoutException, NoSuchElementException

from cuahsi_base.site_element import SiteElement
from cuahsi_base.utils import External, TestSystem

from timing import (
    MY_SUBMISSIONS_LOAD,
    RETURN_PREVIOUS,
    AUTH_WINDOW,
    NEW_SUBMISSION_SAVE,
    DEFAULT_TIMEOUT,
    PAUSE_AFTER_FILL_BEFORE_SUBMIT,
    REPO_LOAD,
    SUBMIT_LANDING_PAGE_LOAD,
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
    navigation_login = SiteElement(By.ID, "navbar-login")

    # responsive
    navigation_hamburger = SiteElement(By.CSS_SELECTOR, "#app-bar .v-app-bar__nav-icon")
    navigation_drawer = SiteElement(By.CSS_SELECTOR, ".v-navigation-drawer")
    drawer_nav_home = SiteElement(By.ID, "drawer-nav-home")
    drawer_nav_my_submissions = SiteElement(By.ID, "drawer-nav-MySubmissions")
    drawer_nav_resources = SiteElement(By.ID, "drawer-nav-Resources")
    drawer_nav_submit = SiteElement(By.ID, "drawer-nav-SubmitData")
    drawer_nav_about = SiteElement(By.ID, "drawer-nav-About")
    drawer_nav_contact = SiteElement(By.ID, "drawer-nav-Contact")
    drawer_nav_login = SiteElement(By.ID, "drawer-nav-login")

    # login
    orcid_login_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login")
    orcid_login_continue = SiteElement(By.ID, "orcid_login_continue")

    @classmethod
    def app_contains_text(self, text):
        try:
            _ = SiteElement(By.XPATH, f"//*[@id='app']/child::*[contains(., '{text}')]")
            return True
        except TimeoutException:
            return False

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
        self.wait_until_element_visible(
            driver, MySubmissions.title, MY_SUBMISSIONS_LOAD
        )

    @classmethod
    def drawer_to_my_submissions(self, driver):
        self.drawer_nav_my_submissions.click(driver)
        self.wait_until_element_visible(
            driver, MySubmissions.title, MY_SUBMISSIONS_LOAD
        )

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
        return self.orcid_login_modal.exists(driver)

    @classmethod
    def to_orcid_window(self, driver):
        num_windows_now = len(driver.window_handles)
        self.wait_until_element_visible(driver, self.orcid_login_continue, AUTH_WINDOW)
        # artifact is getting in the way of button click
        self.wait_until_css_dissapear(driver, ".v-card__actions", AUTH_WINDOW)
        self.orcid_login_continue.click(driver)
        External.switch_new_page(driver, num_windows_now, self.body_locator)

    @classmethod
    def to_hs_repo(self, driver):
        External.switch_last_page(
            driver, new_tab_locator=HSResourcePage.logo, time=REPO_LOAD
        )

    @classmethod
    def to_zenodo_repo(self, driver):
        External.switch_last_page(
            driver, new_tab_locator=ZenodoResourcePage.logo, time=REPO_LOAD
        )

    @classmethod
    def to_earthchem_repo(self, driver):
        External.switch_last_page(
            driver, new_tab_locator=EarthchemResourcePage.logo, time=REPO_LOAD
        )

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
    def wait_until_app_contains_text(self, driver, text, timeout=DEFAULT_TIMEOUT):
        try:
            element = SiteElement(
                By.XPATH, f"//*[@id='app']/child::*[contains(., '{text}')]"
            )
            self.wait_until_element_exist(driver, element, timeout)
            return True
        except TimeoutException:
            return False

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

    @classmethod
    def wait_until_element_exist(
        self, driver, element, timeout=SUBMIT_LANDING_PAGE_LOAD
    ):
        waited = 0
        while waited < timeout:
            if element.exists(driver):
                return
            else:
                time.sleep(1)
                waited += 1
        raise Exception(element.locator)


class OrcidWindow(WebPage):
    """Orcid window"""

    username = SiteElement(By.ID, "username")
    password = SiteElement(By.ID, "password")
    submit = SiteElement(By.ID, "signin-button")

    @classmethod
    def fill_credentials(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)


class HydroshareAuthWindow(WebPage):
    """Authentication window to use Hydroshare as Backend"""

    username = SiteElement(By.ID, "id_username")
    password = SiteElement(By.ID, "id_password")
    submit = SiteElement(By.CSS_SELECTOR, ".account-form .btn-primary")
    authorize = SiteElement(By.CSS_SELECTOR, '#authorizationForm input[name="allow"]')

    @classmethod
    def authorize_repo(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)
        self.authorize.click(driver)


class ZenodoAuthWindow(WebPage):
    """Authentication window to use Zenodo as Backend"""

    github_button = SiteElement(By.CSS_SELECTOR, '.social-signup .btn[href*="github"]')
    orcid_button = SiteElement(By.CSS_SELECTOR, '.social-signup .btn[href*="orcid"]')
    email = SiteElement(By.ID, "email")
    password = SiteElement(By.ID, "password")
    login_button = SiteElement(By.CSS_SELECTOR, 'button[type="submit"]')
    authorize_czhub_button = SiteElement(By.CSS_SELECTOR, 'form button[value="yes"]')

    @classmethod
    def authorize_via_orcid(self, driver):
        self.orcid_button.click(driver)

    @classmethod
    def authorize_via_github(self, driver):
        self.github_button.click(driver)

    @classmethod
    def authorize_email_password(self, driver, email, password):
        self.email.inject_text(driver, email)
        self.password.inject_text(driver, password)
        self.login_button.click(driver)
        self.authorize_czhub_button.click(driver)


class EarthchemAuthWindow(WebPage):
    """Authentication window to use Earthchem as Backend"""

    github_button = SiteElement(By.CSS_SELECTOR, '.social-signup .btn[href*="github"]')
    orcid_button = SiteElement(By.ID, "social-orcid")
    username = SiteElement(By.ID, "username")
    password = SiteElement(By.ID, "password")
    login_button = SiteElement(By.ID, "kc-login")
    authorize_czhub_button = SiteElement(By.CSS_SELECTOR, 'form button[value="yes"]')

    @classmethod
    def authorize_via_orcid(self, driver):
        self.orcid_button.click(driver)

    @classmethod
    def authorize_username_password(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.login_button.click(driver)


class MySubmissions(Dsp):
    """Page displaying users submissions"""

    title = SiteElement(By.CSS_SELECTOR, ".text-h4:nth-of-type(1)")
    total_submissions = SiteElement(By.ID, "total_submissions")
    top_submission = SiteElement(By.ID, "submission-0")
    top_submission_name = SiteElement(By.ID, "sub-0-title")
    top_submission_date = SiteElement(By.ID, "sub-0-date")
    sort_order_select = SiteElement(By.ID, "sort-order")
    my_submissions_search = SiteElement(By.ID, "my_submissions_search")
    top_submission_edit = SiteElement(By.ID, "sub-0-edit")
    top_submission_view_repo = SiteElement(By.ID, "sub-0-view")

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

    @classmethod
    def view_top_submission(self, driver):
        self.top_submission_view_repo.click(driver)


class RepoAuthWindow(WebPage):
    submit_to_repo_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog div.cz-authorize")
    submit_to_repo_authorize = SiteElement(
        By.CSS_SELECTOR, ".cz-authorize button.primary"
    )

    @classmethod
    def to_repo_auth_window(self, driver):
        TestSystem.wait(AUTH_WINDOW)
        num_windows_now = len(driver.window_handles)
        self.submit_to_repo_authorize.click(driver)
        External.switch_new_page(driver, num_windows_now, self.body_locator)


class SubmitLandingPage(Dsp, RepoAuthWindow):
    """Page containing options for submitting data"""

    repositories_header = SiteElement(
        By.XPATH, "//*[@id='app']/child::*[contains(., 'Repositories')]"
    )

    register_dataset_other = SiteElement(
        By.XPATH, "//*[contains(text(),'Register a dataset from a different repository')]/.."
    )

    @classmethod
    def select_external_dataset(self, driver):
        self.register_dataset_other.click(driver)

    @classmethod
    def select_nth_dialog_choice(self, driver, n):
        dialog_item = SiteElement(By.CSS_SELECTOR, f".v-dialog--active .choice-container .v-card:nth-of-type({n+1})")
        dialog_item.scroll_to(driver)
        dialog_item.click(driver)

    @classmethod
    def select_repo_by_id(self, driver, id):
        repo_card = SiteElement(By.CSS_SELECTOR, f'div[id*="{id}"]')
        repo_card.scroll_to(driver)
        repo_card.click(driver)

    @classmethod
    def select_nth_repo(self, driver, n):
        repo_card = SiteElement(
            By.CSS_SELECTOR, f"div.repositories div.v-card:nth-of-type({n+1})"
        )
        repo_card.scroll_to(driver)
        repo_card.click(driver)

    @classmethod
    def to_repo_form(self, driver, id):
        Dsp.show_mobile_nav(driver)
        Dsp.drawer_to_submit(driver)
        self.select_repo_by_id(driver, id)


class GeneralSubmitToRepo(Dsp, RepoAuthWindow):
    header = SiteElement(By.CSS_SELECTOR, ".text-heading-4")
    alert = SiteElement(By.CSS_SELECTOR, ".v-alert .v-alert__content")
    top_save = SiteElement(
        By.CSS_SELECTOR, "#cz-new-submission-actions-top button.submission-save"
    )
    instructions = SiteElement(By.CSS_SELECTOR, "#instructions")

    # required_elements = SiteElementsCollection(By.CSS_SELECTOR, "input[data-id$="*")

    bottom_save = SiteElement(
        By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-save"
    )
    bottom_finish = SiteElement(
        By.CSS_SELECTOR, "#cz-new-submission-actions-bottom button.submission-finish"
    )

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
    def open_tab(self, driver, section, tab_number):
        box_coverage_tab = self.get_tab(section, tab_number)
        box_coverage_tab.scroll_to(driver)
        box_coverage_tab.javascript_click(driver)

    @classmethod
    def save_bottom(self, driver):
        self.bottom_save.scroll_to(driver)
        self.bottom_save.click(driver)
        self.wait_until_element_not_visible(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def is_finishable(self, driver):
        self.bottom_finish.scroll_to_hidden(driver)
        finishable = (
            self.bottom_finish.get_attribute_hidden(driver, "disabled") is None
            or self.bottom_finish.get_attribute_hidden(driver, "disabled") != "disabled"
        )
        return finishable

    @classmethod
    def finish_submission(self, driver):
        self.bottom_finish.scroll_to(driver)
        self.bottom_finish.click(driver)
        try:
            self.wait_until_element_visible(
                driver, self.is_saving, PAUSE_AFTER_FILL_BEFORE_SUBMIT
            )
        except NoSuchElementException as e:
            print(f"\n{e}... \nThis exception is ignored")
        self.wait_until_element_not_exist(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def get_did_in_section(self, section=None, data_id="", nth=0):
        selector = (
            f':is(fieldset, div)[data-id*="{section}"]'
            f' [data-id*="{data_id}"]:nth-of-type({nth+1})'
        )
        return SiteElement(By.CSS_SELECTOR, selector)

    @classmethod
    def get_css_in_section(self, section=None, css="", nth=0):
        selector = f':is(fieldset, div)[data-id*="{section}"] {css}'
        return SiteElement(By.CSS_SELECTOR, selector)

    @classmethod
    def expand_section_by_did(self, driver, data_id):
        element = SiteElement(
            By.CSS_SELECTOR, f':is(fieldset, div)[data-id*="{data_id}"] legend'
        )
        if not element.exists_in_dom(driver):
            # print(f"\n Ignoring attempt to expand static section: {data_id}")
            return False
        element.scroll_to(driver)
        element.javascript_click(driver)

    @classmethod
    def add_form_array_item_by_did(self, driver, data_id):
        element = SiteElement(
            By.CSS_SELECTOR, f'div[data-id*="{data_id}"] button:first-of-type'
        )
        if not element.exists_in_dom(driver):
            # print(f"\n Ignoring attempt to expand static section: {data_id}")
            return False
        element.scroll_to(driver)
        element.javascript_click(driver)

    @classmethod
    def fill_inputs_by_data_ids(self, driver, dict, section=None, nth=0, array=False):
        self.expand_section_by_did(driver, data_id=section)
        for k, v in dict.items():
            if not self.fill_input_by_data_id(driver, k, v, section, nth, array):
                return False
        TestSystem.wait(PAUSE_AFTER_FILL_BEFORE_SUBMIT)
        return True

    @classmethod
    def fill_input_by_data_id(
        self, driver, data_id, value, section=None, nth=0, array=False
    ):
        try:
            if section and nth is not None:
                if array:
                    selector = (
                        f'[data-id*="{section}"] .array-list-item:nth-of-type({nth+1})'
                        f' [data-id*="{data_id}"]'
                    )
                else:
                    selector = (
                        f'[data-id*="{section}"]'
                        f' [data-id*="{data_id}"]:nth-of-type({nth+1})'
                    )
                element = SiteElement(By.CSS_SELECTOR, selector)
            else:
                element = SiteElement(
                    By.CSS_SELECTOR, f'[data-id*="{data_id}"]:nth-of-type(1)'
                )
        except TimeoutException as e:
            print(f"{e}\nElement not found for key: {data_id}")
            return False
        if element.exists_in_dom(driver):
            if isinstance(value, list):
                # assume this is a v-multi-select
                self.fill_v_multi_select(
                    driver, container_id=section, input_id=data_id, values=value
                )
            else:
                element.javascript_click(driver)
                element.inject_text(driver, value)
                element.submit_hidden(driver)
        else:
            print(
                f"\nAttempt to fill element {data_id} in section {section} failed. Not"
                f' in DOM                 \nSelector used="{selector}"'
            )
            return False
        return True

    @classmethod
    def unfill_and_refill(self, driver, section, did, value):
        selector = f'[data-id*="{section}"] [data-id*="{did}"]'
        element = SiteElement(By.CSS_SELECTOR, selector)
        if element.exists_in_dom(driver):
            element.scroll_to_hidden(driver)
            element.javascript_click(driver)
            element.clear_all_text(driver)
            element.submit(driver)
            element.javascript_click(driver)
            element.inject_text(driver, value)
            element.submit(driver)
        else:
            print(
                f"\nAttempt to fill element {did} in section {section} failed. Not in"
                f' DOM                 \nSelector used="{selector}"'
            )
            return False
        return True

    @classmethod
    def fill_v_multi_select(
        self, driver, container_id, input_id, values=["default_value"]
    ):
        selector = (
            f'fieldset[data-id*="{container_id}"] .v-select__selections'
            f' input[data-id*="{input_id}"]'
        )
        input = SiteElement(By.CSS_SELECTOR, selector)
        input.javascript_click_hidden(driver)
        if isinstance(values, str):
            input.inject_text(driver, values)
            input.submit(driver)
        else:
            for value in values:
                checklist_item = SiteElement(
                    By.XPATH, f"//*[@class='v-list-item__title' and text()='{value}']"
                )
                if checklist_item.exists(driver):
                    checklist_item.click(driver)
                else:
                    input.inject_text(driver, value)
                    input.submit(driver)

    @classmethod
    def click_a_safe_place(self, driver):
        footer = SiteElement(By.XPATH, "//*[contains(text(),'2012893')]")
        footer.scroll_to(driver)
        footer.click(driver)

    @classmethod
    def unfill_v_multi_select(self, driver, container_id, input_id):
        input = SiteElement(
            By.CSS_SELECTOR,
            f'fieldset[data-id*="{container_id}"] .v-select__selections'
            f' input[data-id*="{input_id}"]',
        )
        input.javascript_click_hidden(driver)
        input.clear_all_text(driver)

    @classmethod
    def get_tab(self, section=None, tab_number=1):
        # tab index is off by 1 because one hidden?
        selector = (
            f'fieldset[data-id*="{section}"] .v-tabs .v-tab:nth-of-type({tab_number+1})'
        )
        return SiteElement(By.CSS_SELECTOR, selector)

    @classmethod
    def unfill_text_by_page_property(self, driver, element):
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.javascript_click(driver)".format(element))
        eval("self.{}.clear_all_text(driver)".format(element))

    @classmethod
    def unfill_text_by_data_id(self, driver, data_id, section=None, nth=0, array=False):
        try:
            if section and nth is not None:
                if array:
                    selector = (
                        f'[data-id*="{section}"] .array-list-item:nth-of-type({nth+1})'
                        f' [data-id*="{data_id}"]'
                    )
                else:
                    selector = (
                        f'[data-id*="{section}"]'
                        f' [data-id*="{data_id}"]:nth-of-type({nth+1})'
                    )
                element = SiteElement(By.CSS_SELECTOR, selector)
            else:
                element = SiteElement(
                    By.CSS_SELECTOR, f'[data-id*="{data_id}"]:nth-of-type(1)'
                )
        except TimeoutException as e:
            print(f"{e}\nElement not found for key: {data_id}")
            return False
        try:
            element.scroll_to_hidden(driver)
            element.javascript_click(driver)
            element.clear_all_text(driver)
        except TimeoutException:
            self.unfill_v_multi_select(driver, section, data_id)

    @classmethod
    def fill_text_by_page_property(self, driver, element, text_to_fill):
        eval("self.{}.scroll_to(driver)".format(element))
        eval("self.{}.javascript_click(driver)".format(element))
        eval("self.{}.inject_text(driver, '{}')".format(element, text_to_fill))

    @classmethod
    def autofill_required_elements(self, driver, required):
        for section, dict in required.items():
            self.expand_section_by_did(driver, section)
            self.fill_inputs_by_data_ids(driver, dict, section, nth=0)

    @classmethod
    def fill_related_resources(self, driver, relation_type, value, n):
        self.expand_section_by_did(driver, "Relatedresources")

        sel = (
            ':is(fieldset, div)[data-id*="Relatedresources"]'
            f' input[data-id*="RelationType"]:nth-of-type({n+1})'
        )
        relation_type_input = SiteElement(By.CSS_SELECTOR, sel)
        sel = (
            ':is(fieldset, div)[data-id*="Relatedresources"]'
            f' input[data-id*="Value"]:nth-of-type({n+1})'
        )
        related_resources_value = SiteElement(By.CSS_SELECTOR, sel)
        sel = (
            ':is(fieldset, div)[data-id*="Relatedresources"]'
            f" div.v-select:nth-of-type({n+1})"
        )
        relation_type_container = SiteElement(By.CSS_SELECTOR, sel)

        relation_type_container.scroll_to(driver)
        relation_type_container.javascript_click(driver)
        relation_type_input.inject_text(driver, relation_type)
        relation_type_input.submit(driver)
        related_resources_value.inject_text(driver, value)
        related_resources_value.submit(driver)


class GeneralEditSubmission(Dsp):
    header_title = SiteElement(By.CSS_SELECTOR, ".text-h4")

    @classmethod
    def get_nth_relation_type(self, driver, n):
        sel = (
            ':is(fieldset, div)[data-id*="Relatedresources"]'
            f' .array-list-item:nth-of-type({n+1}) input[data-id*="RelationType"]'
        )
        relation_type_input = SiteElement(By.CSS_SELECTOR, sel)
        return relation_type_input.get_texts_from_xpath(driver, "./preceding::div[1]")

    @classmethod
    def get_header_title(self, driver):
        return self.header_title.get_text(driver)

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
    def expand_section_by_did(self, driver, data_id):
        element = SiteElement(
            By.CSS_SELECTOR, f':is(fieldset, div)[data-id*="{data_id}"] legend'
        )
        if not element.exists_in_dom(driver):
            # print(f"\n Ignoring attempt to expand static section: {data_id}")
            return False
        element.scroll_to(driver)
        element.javascript_click(driver)

    @classmethod
    def check_inputs_by_data_ids(self, driver, dict, section=None, nth=0, array=False):
        self.expand_section_by_did(driver, data_id=section)
        for k, v in dict.items():
            if isinstance(v, list):
                # assume this is a v-multi-select
                check = self.check_v_multi_select(
                    driver, container_id=section, input_id=k, values=v
                )
                if not check:
                    print(f"\nMismatch when checking field: |{k}|. Expected |{v}|.")
                    return False
            else:
                # not a v-multi-select
                if section and nth is not None:
                    if array:
                        selector = (
                            f':is(fieldset, div)[data-id*="{section}"]'
                            f' .array-list-item:nth-of-type({nth+1}) [data-id*="{k}"]'
                        )
                        elem = SiteElement(By.CSS_SELECTOR, selector)
                    else:
                        selector = (
                            f':is(fieldset, div)[data-id*="{section}"]'
                            f' [data-id*="{k}"]:nth-of-type({nth+1})'
                        )
                        elem = SiteElement(By.CSS_SELECTOR, selector)
                else:
                    selector = f'[data-id*="{k}"]:nth-of-type(1)'
                    elem = SiteElement(By.CSS_SELECTOR, selector)
                elem.scroll_to(driver)
                value = elem.get_value(driver)
                if value != v:
                    if value.strip() == v:
                        # Allow additional whitespace padding
                        # print(
                        #     f"\nWARNING: while checking field: |{k}|.\nExpected:"
                        #     f" |{v}|\nBut got : |{value}|                        "
                        #     " \nWhitespace will be ignored and this field considered"
                        #     " valid"
                        # )
                        pass
                    else:
                        print(
                            f"\nMismatch when checking field: |{k}|.\nExpected |{v}|"
                            f" got |{value}|"
                        )
                        print(f"\nSelector used: {selector}")
                        return False
        return True

    @classmethod
    def check_required_elements(self, driver, required_elements):
        """Unless otherwise defined, Editsubmission pages should check required fields
        by dict"""
        for section, dict_to_check in required_elements.items():
            return self.check_inputs_by_data_ids(
                driver, dict=dict_to_check, section=section, nth=0
            )

    @classmethod
    def get_v_multi_select_vals(self, driver, container_id, input_id):
        input = SiteElement(
            By.CSS_SELECTOR,
            f'fieldset[data-id*="{container_id}"] input[data-id*="{input_id}"]',
        )
        values = input.get_texts_from_xpath(
            driver, './preceding-sibling::*/span[contains(@class, "v-chip__content")]'
        )
        return values

    @classmethod
    def check_v_multi_select(self, driver, container_id, input_id, values=None):
        saved_values = self.get_v_multi_select_vals(driver, container_id, input_id)
        if isinstance(values, str):
            if values not in saved_values:
                return False
        else:
            if not all(elem in saved_values for elem in values):
                return False
        return True

    @classmethod
    def get_nth_v_multi_select(self, driver, container_id, input_id, n):
        saved_values = self.get_v_multi_select_vals(driver, container_id, input_id)
        return saved_values[n]


class SubmitHydroshare(GeneralSubmitToRepo):
    """Page containing forms for submitting data with HS backend"""

    # Basic info
    title = SiteElement(
        By.CSS_SELECTOR, '[data-id*="BasicInformation"] input[data-id*="Title"]'
    )
    abstract = SiteElement(By.ID, "#/properties/abstract-input")
    subject_keyword_container = SiteElement(
        By.CSS_SELECTOR, '[data-id="group-BasicInformation"] .v-select__selections'
    )

    # Temporal
    temporal_name_input = SiteElement(
        By.CSS_SELECTOR,
        ':is(fieldset, div)[data-id*="Temporalcoverage"] input[data-id*="Name"]',
    )
    start_input = SiteElement(
        By.CSS_SELECTOR, '[data-id*="Temporalcoverage"] input[data-id*="Start"]'
    )
    end_input = SiteElement(
        By.CSS_SELECTOR, '[data-id*="Temporalcoverage"] input[data-id*="End"]'
    )

    # Funding agency
    agency_name = SiteElement(By.ID, "#/properties/funding_agency_name-input")

    # Rights
    rights_statement = SiteElement(By.ID, "#/properties/statement-input")
    rights_url = SiteElement(By.ID, "#/properties/url-input")


class SubmitExternal(GeneralSubmitToRepo):
    """Page containing forms for submitting data with EXTERNAL backend"""

    pass


class SubmitZenodo(GeneralSubmitToRepo):
    """Page containing forms for submitting data with Zenodo backend"""

    @classmethod
    def finish_submission(self, driver, uname, pw):
        """Override general finish submission to account for extra Zenodo auth window"""
        self.bottom_finish.scroll_to(driver)
        self.bottom_finish.click(driver)

        try:
            SubmitLandingPage.to_repo_auth_window(driver)
            ZenodoAuthWindow.authorize_email_password(
                driver, email=uname, password=pw
            )
            ZenodoAuthWindow.to_origin_window(driver, wait=True)
        except TimeoutException as e:
            print(f"\n{e}... \nThis exception is ignored")
        try:
            self.wait_until_element_visible(
                driver, self.is_saving, PAUSE_AFTER_FILL_BEFORE_SUBMIT
            )
        except NoSuchElementException as e:
            print(f"\n{e}... \nThis exception is ignored")
        self.wait_until_element_not_exist(driver, self.is_saving, NEW_SUBMISSION_SAVE)


class EditExternalSubmission(SubmitHydroshare, GeneralEditSubmission):
    """Page containing forms for editing existing submission with Zenodo backend"""

    pass


class EditZenodoSubmission(SubmitHydroshare, GeneralEditSubmission):
    """Page containing forms for editing existing submission with Zenodo backend"""

    pass


class SubmitEarthchem(GeneralSubmitToRepo):
    """Page containing forms for submitting data with Earthchem backend"""

    finish_later = SiteElement(
        By.XPATH, "//*[@class='v-btn__content' and contains(text(),'later')]/.."
    )
    submit_review = SiteElement(
        By.XPATH,
        "//*[@class='v-btn__content' and contains(text(),'Submit for review')]/..",
    )
    license = SiteElement(By.CSS_SELECTOR, '[data-id*="License"] .v-select__selection')

    @classmethod
    def finish_submission_later(self, driver):
        self.bottom_finish.scroll_to(driver)
        self.bottom_finish.click(driver)
        self.finish_later.click(driver)
        self.wait_until_element_not_exist(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def submit_for_review(self, driver):
        self.bottom_finish.scroll_to(driver)
        self.bottom_finish.click(driver)
        self.submit_review.click(driver)
        self.wait_until_element_not_exist(driver, self.is_saving, NEW_SUBMISSION_SAVE)

    @classmethod
    def get_license(self, driver):
        return self.license.get_text(driver)


class EditEarthchemSubmission(SubmitHydroshare, GeneralEditSubmission):
    """Page containing forms for editing existing submission with Earthchem backend"""

    pass


class EditHSSubmission(SubmitHydroshare, GeneralEditSubmission):
    """Page containing forms for editing existing submission with Hydroshare backend"""

    @classmethod
    def get_keywords(self, driver):
        return self.get_v_multi_select_vals(
            driver, "BasicInformation", "Subjectkeywords"
        )

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


class HSResourcePage(WebPage):
    """Landing page for a HS resource"""

    logo = By.CSS_SELECTOR, "#img-brand-logo"
    title = SiteElement(By.CSS_SELECTOR, "#resource-title")

    @classmethod
    def get_title(self, driver):
        return self.title.get_text(driver)


class ZenodoResourcePage(WebPage):
    """Landing page for a Zenodo resource"""

    logo = By.CSS_SELECTOR, "img.navbar-brand"
    title = SiteElement(By.CSS_SELECTOR, "#title")

    @classmethod
    def get_title(self, driver):
        return self.title.get_value(driver)


class EarthchemResourcePage(WebPage):
    """Landing page for an ECL resource"""

    logo = By.CSS_SELECTOR, "#navbarBrand"
    page_title = SiteElement(By.CSS_SELECTOR, "#page-title h1")
    resource_title = SiteElement(By.CSS_SELECTOR, "#title_display")
    login_orcid = SiteElement(
        By.XPATH, "//*[@id='connect-button' and contains(.,'ORCID')]/.."
    )

    @classmethod
    def get_title(self, driver):
        return self.resource_title.get_text(driver)

    @classmethod
    def authenticate_if_needed(self, driver):
        if "Login" in self.page_title.get_text(driver):
            self.login_orcid.click(driver)
            self.resource_title.wait_on_visibility(driver, REPO_LOAD)


class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
