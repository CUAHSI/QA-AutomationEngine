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
    HSAPI_GUI_RESPONSE,
    PROFILE_SAVE,
    HELP_DOCS_TREE_ANIMATIONS,
    RESOURCE_CREATION,
    HOME_PAGE_SLIDER_ANIMATION,
    LABEL_CREATION,
    DISCOVER_TABLE_UPDATE,
    EXTERNAL_PAGE_LOAD,
    KEYS_RESPONSE,
    RESOURCE_LANDING_PAGE_LOAD,
)


class WebPage:
    body_locator = By.CSS_SELECTOR, "body"


class MatlabOnline:
    authorize_btn = SiteElement(By.CSS_SELECTOR, 'input[value="Authorize"]')
    accept_terms = SiteElement(By.ID, "btn_submit")

    @classmethod
    def authorize(self, driver):
        self.authorize_btn.click(driver)
        self.accept_terms.click(driver)


class Downloads(WebPage):
    latest_link = SiteElement(By.CSS_SELECTOR, "#show")

    @classmethod
    def check_successful_download(self, driver):
        download_time = 0
        while download_time < 3600:
            successful_downloads = TestSystem.return_from_javascript(
                driver,
                "return document.querySelector('downloads-manager').shadowRoot.querySelector('#downloadsList').items.filter(e => e.state === 'COMPLETE').length",
            )
            if successful_downloads > 0:
                return True
            else:
                TestSystem.wait(5)
                download_time += 5
        return False

    @classmethod
    def check_successful_download_new_tab(self, driver):
        num_windows_now = len(driver.window_handles)
        TestSystem.execute_javascript(
            driver, """window.open("https://google.com","_blank");"""
        )
        External.switch_new_page(driver, num_windows_now, self.body_locator)
        TestSystem.to_url(driver, "chrome://downloads")
        return self.check_successful_download(driver)


class Hydroshare(WebPage):
    navigation_landing_page = SiteElement(By.ID, "img-brand-logo")
    navigation_home = SiteElement(By.ID, "dropdown-menu-home")
    navigation_my_resources = SiteElement(By.ID, "dropdown-menu-my-resources")
    navigation_discover = SiteElement(By.ID, "dropdown-menu-search")
    navigation_collaborate = SiteElement(
        By.CSS_SELECTOR, "#dropdown-menu-collaborate a"
    )
    navigation_apps = SiteElement(
        By.ID, "dropdown-menu-https:--www.hydroshare.org-apps-"
    )
    navigation_help = SiteElement(
        By.CSS_SELECTOR, 'a[href="{}"]'.format("http://help.hydroshare.org")
    )
    navigation_login = SiteElement(By.CSS_SELECTOR, "#signin-menu a")
    profile_button = SiteElement(
        By.CSS_SELECTOR, ".account div.dropdown-footer .btn.btn-primary"
    )
    profile_menu = SiteElement(By.ID, "profile-menu")
    signout_menu = SiteElement(By.ID, "signout-menu")
    resource_creation = SiteElement(By.ID, "select-resource-type")
    footer = SiteElement(By.CSS_SELECTOR, "footer")
    footer_terms = SiteElement(By.CSS_SELECTOR, "footer a[href='/terms-of-use']")
    footer_privacy = SiteElement(By.CSS_SELECTOR, "footer a[href='/privacy']")
    footer_sitemap = SiteElement(By.CSS_SELECTOR, "footer a[href='/sitemap/']")
    footer_twitter = SiteElement(
        By.CSS_SELECTOR, ".content.social ul li:nth-child(1) > a"
    )
    footer_facebook = SiteElement(
        By.CSS_SELECTOR, ".content.social ul li:nth-child(2) > a"
    )
    footer_youtube = SiteElement(
        By.CSS_SELECTOR, ".content.social ul li:nth-child(3) > a"
    )
    footer_github = SiteElement(
        By.CSS_SELECTOR, ".content.social ul li:nth-child(4) > a"
    )
    footer_linkedin = SiteElement(
        By.CSS_SELECTOR, ".content.social ul li:nth-child(5) > a"
    )
    footer_version = SiteElement(By.CSS_SELECTOR, ".content p b")
    support_email = SiteElement(By.CSS_SELECTOR, 'a[href="mailto:help@cuahsi.org"]')
    page_tip = SiteElement(By.CSS_SELECTOR, ".page-tip > .container > .row > div > p")
    logged_in_full_name = SiteElement(By.ID, "profile-menu-fullname")
    logged_in_email = SiteElement(By.ID, "profile-menu-email")
    notifications = SiteElement(By.CSS_SELECTOR, "#notifications-dropdown > a")
    notifications_clear = SiteElement(By.CSS_SELECTOR, "#btn-notifications-clear")

    @classmethod
    def resource_type(self, resource_type):
        return SiteElement(By.CSS_SELECTOR, 'a[data-value="{}"]'.format(resource_type))

    @classmethod
    def to_landing_page(self, driver):
        self.navigation_landing_page.click(driver)

    @classmethod
    def to_home(self, driver):
        self.navigation_home.click(driver)

    @classmethod
    def to_my_resources(self, driver):
        self.navigation_my_resources.click(driver)

    @classmethod
    def to_discover(self, driver):
        self.navigation_discover.click(driver)

    @classmethod
    def to_collaborate(self, driver):
        self.navigation_collaborate.click(driver)

    @classmethod
    def to_apps(self, driver):
        num_windows_now = len(driver.window_handles)
        self.navigation_apps.click(driver)
        External.switch_new_page(driver, num_windows_now, Apps.apps_locator)

    @classmethod
    def to_help(self, driver):
        self.navigation_help.click(driver)
        time.sleep(EXTERNAL_PAGE_LOAD)

    @classmethod
    def to_about(self, driver):
        self.navigation_help.click(driver)
        time.sleep(EXTERNAL_PAGE_LOAD)
        Help.to_about.javascript_click(driver)

    @classmethod
    def to_login(self, driver):
        self.navigation_login.click(driver)

    @classmethod
    def to_profile(self, driver):
        self.profile_menu.click(driver)
        self.profile_button.click(driver)

    @classmethod
    def logout(self, driver):
        self.profile_menu.click(driver)
        self.signout_menu.click(driver)

    @classmethod
    def create_resource(self, driver, type):
        self.resource_creation.click(driver)
        self.resource_type(type).click(driver)

    @classmethod
    def to_terms(self, driver):
        self.footer_terms.click(driver)

    @classmethod
    def to_privacy(self, driver):
        self.footer_privacy.click(driver)

    @classmethod
    def to_sitemap(self, driver):
        self.footer_sitemap.click(driver)

    @classmethod
    def get_social_link(self, driver, social):
        social_links = {
            "facebook": self.footer_facebook,
            "twitter": self.footer_twitter,
            "youtube": self.footer_youtube,
            "github": self.footer_github,
            "linkedin": self.footer_linkedin,
        }
        return social_links[social].get_attribute(driver, "href")

    @classmethod
    def get_version(self, driver):
        return self.footer_version.get_text(driver).strip()

    @classmethod
    def get_latest_release(self, org, repo):
        """
        Retrieves the version of the latest published release of 'hydroshare'
        repository.
        """
        # See https://developer.github.com/v3/repos/
        # releases/#get-the-latest-release
        request_url = f"https://api.github.com/repos/{org}/" f"{repo}/releases/latest"
        response_data = urlopen(request_url).read()
        release_version = json.loads(response_data)["tag_name"]
        return release_version

    @classmethod
    def get_support_email(self, driver):
        return self.support_email.get_href(driver)

    @classmethod
    def get_logged_in_name(self, driver):
        self.profile_menu.click(driver)
        name = self.logged_in_full_name.get_text(driver)
        self.profile_menu.click(driver)
        return name

    @classmethod
    def get_logged_in_email(self, driver):
        self.profile_menu.click(driver)
        name = self.logged_in_email.get_text(driver)
        self.profile_menu.click(driver)
        return name

    @classmethod
    def clear_notifications(self, driver):
        self.notifications.click(driver)
        self.notifications_clear.click(driver)
        self.notifications.click(driver)


class LandingPage(Hydroshare):
    hero = SiteElement(By.CSS_SELECTOR, "div.item.parallax-window.active")
    hero_right = SiteElement(By.CSS_SELECTOR, ".glyphicon-chevron-right")
    hero_left = SiteElement(By.CSS_SELECTOR, ".glyphicon-chevron-left")
    navigation_top = SiteElement(By.CSS_SELECTOR, ".scrolltotop")
    navigation_registration = SiteElement(By.CSS_SELECTOR, "a.btn-signup")

    @classmethod
    def to_registration(self, driver):
        time.sleep(EXTERNAL_PAGE_LOAD)
        self.navigation_registration.click(driver)

    @classmethod
    def slide_hero_right(self, driver):
        self.hero_right.javascript_click(driver)
        time.sleep(HOME_PAGE_SLIDER_ANIMATION)

    @classmethod
    def slide_hero_left(self, driver):
        self.hero_left.javascript_click(driver)
        time.sleep(HOME_PAGE_SLIDER_ANIMATION)

    @classmethod
    def scroll_to_top(self, driver):
        self.navigation_top.click(driver)

    @classmethod
    def scroll_to_button(self, driver):
        self.footer.scroll_to(driver)

    @classmethod
    def hero_has_valid_img(self, driver, images):
        return self.hero.get_attribute(driver, "style") in images


class Home(Hydroshare):
    get_started_toggle = SiteElement(By.ID, "id-getting-started-toggle")
    recently_visited_list = SiteElement(
        By.CSS_SELECTOR, "#recently-visited-resources > tbody"
    )

    @classmethod
    def links_by_row_and_index(self, row, column):
        return SiteElement(
            By.CSS_SELECTOR, "#row-{} > div:nth-child({}) > a".format(row, column)
        )

    @classmethod
    def recent_activity_resource(self, row):
        return SiteElement(
            By.CSS_SELECTOR,
            "#recently-visited-resources > tbody > tr:nth-child({}) > td:nth-child(2) > strong > a".format(
                row
            ),
        )

    @classmethod
    def recent_activity_author(self, row):
        return SiteElement(
            By.CSS_SELECTOR,
            "#recently-visited-resources > tbody > tr:nth-child({}) > td:nth-child(3) > a".format(
                row
            ),
        )

    @classmethod
    def featured_app(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "div.main-container > div:nth-child(2) > div:nth-child(2) > div.row.big-app-row > div:nth-child({}) > div.app-text-block > div.app-text-block-header > strong > a".format(
                index
            ),
        )

    @classmethod
    def cuahsi_app(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "div.main-container > div:nth-child(2) > div:nth-child(3) > div.row.big-app-row > div:nth-child({}) > div.app-text-block > div.app-text-block-header > strong > a".format(
                index
            ),
        )

    @classmethod
    def toggle_get_started(self, driver):
        self.get_started_toggle.click(driver)

    @classmethod
    def is_get_started_showing(self, driver):
        return self.get_started_toggle.get_text(driver) == "Hide Getting Started"

    @classmethod
    def check_getting_started_link(self, driver, row, column):
        self.links_by_row_and_index(row, column).click(driver)
        time.sleep(EXTERNAL_PAGE_LOAD / 2)

    @classmethod
    def get_recent_activity_length(self, driver):
        return self.recently_visited_list.get_immediate_child_count(driver)

    @classmethod
    def check_recent_activity_resource(self, driver, row):
        link_title = self.recent_activity_resource(row).get_text(driver)
        self.recent_activity_resource(row).click(driver)
        resource_title = Resource.title.get_text(driver)
        TestSystem.back(driver)
        return link_title, resource_title

    @classmethod
    def check_recent_activity_author(self, driver, row):
        link_author = self.recent_activity_author(row).get_text(driver)
        self.recent_activity_author(row).click(driver)
        profile_author = Profile.name.get_text(driver)
        TestSystem.back(driver)
        return link_author, profile_author

    @classmethod
    def to_app(self, driver, app_type, index):
        if app_type == "Featured":
            num_windows_now = len(driver.window_handles)
            self.featured_app(index).click(driver)
            External.switch_new_page(driver, num_windows_now, self.body_locator)
        if app_type == "CUAHSI":
            num_windows_now = len(driver.window_handles)
            self.cuahsi_app(index).click(driver)
            External.switch_new_page(driver, num_windows_now, self.body_locator)


class Login(Hydroshare):
    username = SiteElement(By.ID, "id_username")
    password = SiteElement(By.ID, "id_password")
    submit = SiteElement(By.CSS_SELECTOR, "input.btn.btn-primary[type='submit']")
    error = SiteElement(By.CSS_SELECTOR, ".alert-danger")
    notification = SiteElement(
        By.CSS_SELECTOR, "div.page-tip-error.animated.slideInDown > div > div > div > p"
    )

    @classmethod
    def get_login_error(self, driver):
        return self.error.get_text(driver)

    @classmethod
    def get_notification(self, driver):
        return self.notification.get_text(driver)

    @classmethod
    def login(self, driver, username, password):
        self.username.inject_text(driver, username)
        self.password.inject_text(driver, password)
        self.submit.click(driver)


class Apps(Hydroshare):
    apps = SiteElementsCollection(By.CSS_SELECTOR, ".webapp")
    apps_locator = By.CSS_SELECTOR, ".webapp"

    @classmethod
    def info(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "#body > div.main-container > div.container.apps-container > div "
            "div:nth-of-type({}) a.app-info-toggle".format(num),
        )

    @classmethod
    def resource(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "#body > div.main-container > div.container.apps-container > div "
            "div:nth-of-type({}) p.app-description a".format(num),
        )

    @classmethod
    def title(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "#body > div.main-container > div.container.apps-container > div "
            "div:nth-of-type({}) h3".format(num),
        )

    @classmethod
    def show_info(self, driver, num):
        self.info(num).click(driver)

    @classmethod
    def get_count(self, driver):
        return len(self.apps.items(driver))

    @classmethod
    def to_resource(self, driver, num):
        self.resource(num).click(driver)

    @classmethod
    def get_title(self, driver, num):
        return self.title(num).get_text(driver)
    
    @classmethod
    def add_photo(self, driver, link):
        self.image_upload.set_path(driver, link)

    @classmethod
    def remove_photo(self, driver):
        self.delete_image.click(driver)
        self.submit_delete_image.click(driver)

    @classmethod
    def confirm_photo_uploaded(self, driver, contains):
        return contains in self.image.get_style(driver)


class Discover(Hydroshare):
    start_date = SiteElement(By.ID, "id_start_date")
    end_date = SiteElement(By.ID, "id_end_date")
    map_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#map-view"]')
    map_search = SiteElement(By.ID, "geocoder-address")
    map_submit = SiteElement(By.ID, "geocoder-submit")
    list_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#list-view"]')
    sort_order = SiteElement(By.ID, "id_sort_order")
    sort_direction = SiteElement(By.ID, "id_sort_direction")
    col_headers = SiteElement(By.CSS_SELECTOR, "#items-discovered thead tr")
    legend = SiteElement(By.CSS_SELECTOR, "#headingLegend h4 a")
    legend_labels = SiteElement(
        By.CSS_SELECTOR,
        "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-5",
    )
    legend_resources = SiteElement(
        By.CSS_SELECTOR,
        "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-7",
    )
    next_page = SiteElement(By.XPATH, '//a[contains(text(), "Next")][1]')
    page = SiteElement(By.ID, "page-number-upper")
    last_updated_by = SiteElement(
        By.XPATH, '//th[text() = "Last updated:"]/following-sibling::td/a'
    )
    search_field = SiteElement(By.ID, "search-input")
    show_all_btn = SiteElement(By.ID, "btn-show-all")
    user_modal_to_profile = SiteElement(
        By.CSS_SELECTOR,
        ".open > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) "
        "> div:nth-child(2) > h4:nth-child(1) > a:nth-child(1)",
    )
    author_list = SiteElement(By.ID, "list-group-creator")
    result_rows = SiteElement(By.CSS_SELECTOR, "#items-discovered > tbody")
    type_list = SiteElement(By.ID, "list-group-type")
    map_mode = SiteElement(By.ID, "map-mode-button")
    page_left = SiteElement(By.ID, "page-left-upper")
    page_right = SiteElement(By.ID, "page-right-upper")

    @classmethod
    def column_header(index):
        return SiteElement(
            By.CSS_SELECTOR, "thead > tr:nth-child(1) > th:nth-child({})".format(index)
        )

    @classmethod
    def resource_link(self, title):
        return SiteElement(By.XPATH, "//a[contains(text(), '{}')]".format(title))

    @classmethod
    def col_header(self, col_index):
        """Return the column header element, given the index"""
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered thead tr " "th:nth-of-type({})".format(col_index),
        )

    @classmethod
    def cell(self, col, row):
        """
        Return the cell in the discover table, given row and column indicies
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({}) span".format(row, col),
        )

    @classmethod
    def cell_href(self, col, row):
        """
        Return the cell's hyperlink in the discover table, given row and column
        indicies.
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({}) a".format(row, col),
        )

    @classmethod
    def cell_strong_href(self, col, row):
        """
        Return the cell's bolded hyperlink in the discover table,
        given row and column indicies.
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({}) strong a".format(row, col),
        )

    @classmethod
    def filter_author(self, author):
        return SiteElement(By.ID, "author-{}".format(author))

    @classmethod
    def filter_contributor(self, author):
        return SiteElement(By.ID, "contrib-{}".format(author))

    @classmethod
    def filter_content_type(self, content_type):
        return SiteElement(By.ID, "content_type-{}".format(content_type))

    @classmethod
    def filter_subject(self, subject):
        return SiteElement(By.ID, "subj-{}".format(subject))

    @classmethod
    def filter_resource_type(self, resource_type):
        return SiteElement(By.ID, "type-{}".format(resource_type))

    @classmethod
    def filter_owner(self, owner):
        return SiteElement(By.ID, "owner-{}".format(owner))

    @classmethod
    def filter_variable(self, variable):
        return SiteElement(By.ID, "variable_name-{}".format(variable))

    @classmethod
    def filter_sample_medium(self, sample_medium):
        return SiteElement(By.ID, "sample_medium-{}".format(sample_medium))

    @classmethod
    def filter_unit(self, unit):
        return SiteElement(By.ID, "units_name-{}".format(unit))

    @classmethod
    def filter_availability(self, availability):
        return SiteElement(By.ID, "avail-{}".format(availability))

    @classmethod
    def author_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-creator > li:nth-of-type({}) input".format(index),
        )

    @classmethod
    def author_resource_count_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-creator > li:nth-of-type({}) > span".format(index),
        )

    @classmethod
    def contributor_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-contributor > li:nth-of-type({}) input".format(index),
        )

    @classmethod
    def contributor_resource_count_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-contributor > li:nth-of-type({}) > span".format(index),
        )

    @classmethod
    def owner_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-owner > li:nth-of-type({}) input".format(index),
        )

    @classmethod
    def owner_resource_count_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-owner > li:nth-of-type({}) > span".format(index),
        )

    @classmethod
    def type_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-type > li:nth-of-type({}) input".format(index),
        )

    @classmethod
    def type_resource_count_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#list-group-type > li:nth-of-type({}) > span".format(index),
        )

    @classmethod
    def resource_icon_by_index(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered > tbody > tr:nth-child({}) > td:nth-child(1) > span > img:nth-child(1)".format(
                index
            ),
        )

    @classmethod
    def set_sort_order(self, driver, option):
        """Set the sort order to {{option}}"""
        self.sort_order.select_option_text(driver, option)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def set_sort_direction(self, driver, option):
        """Set the sort direction to {{option}}"""
        self.sort_direction.select_option_text(driver, option)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def set_sort(self, driver, col_index):
        self.col_header(col_index).click(driver)

    @classmethod
    def to_resource(self, driver, title):
        """Navigate to the {{title}} resource landing page by clicking
        on it within the table.  If the resource is not visible will switch to
        the next result page
        """
        num_windows_now = len(driver.window_handles)
        resource_found = False
        time.sleep(DISCOVER_TABLE_UPDATE)
        while not resource_found:
            try:
                self.resource_link(title).click(driver)
                resource_found = True
            except TimeoutException:
                self.page_right.click(driver)
        # Switch to new resource page
        External.switch_new_page(driver, num_windows_now, Resource.authors_locator)

    @classmethod
    def to_last_updated_profile(self, driver):
        self.last_updated_by.click(driver)
        self.user_modal_to_profile.click(driver)

    @classmethod
    def col_index(self, driver, col_name):
        """Indentify the index for a discover page column, given the
        column name.  Indexes here start at one since the
        end application here is xpath, and those indexes are 1 based
        """
        num_cols = self.col_headers.get_immediate_child_count(driver)
        for i in range(1, num_cols + 1):
            name_to_check = self.col_header(i).get_text(driver).replace("\n", " ")
            if name_to_check == col_name:
                return i
        return 0

    @classmethod
    def check_sorting_multi(self, driver, column_name, ascend_or_descend):
        """Check discover page rows are sorted correctly.  The automated
        testing system checks the first eight rows against the rows that
        are 1, 2, and 3 positions down, relative to the base row (a total
        of 24 checks)
        """
        baseline_rows = 8
        all_pass = True
        for i in range(1, baseline_rows):
            for j in range(1, 4):
                if not self.check_sorting_single(
                    driver, column_name, ascend_or_descend, i, i + j
                ):
                    all_pass = False
        return all_pass

    @classmethod
    def check_sorting_single(
        self, driver, column_name, ascend_or_descend, row_one, row_two
    ):
        """Confirm that two rows are sorted correctly relative to
        eachother
        """
        col_ind = self.col_index(driver, column_name)
        if column_name == "Title":
            first_element = self.cell_href(col_ind, row_one)
            second_element = self.cell_href(col_ind, row_two)
            first_two_vals = [
                first_element.get_text(driver),
                second_element.get_text(driver),
            ]
        elif column_name == "First Author":
            first_element = self.cell_href(col_ind, row_one)
            second_element = self.cell_href(col_ind, row_two)
            first_two_vals = [
                first_element.get_text(driver),
                second_element.get_text(driver),
            ]
        else:
            first_element = self.cell(col_ind, row_one)
            second_element = self.cell(col_ind, row_two)
            first_two_vals = [
                first_element.get_text(driver),
                second_element.get_text(driver),
            ]
        if ("Date" in column_name) or (column_name == "Last Modified"):
            date_one = parser.parse(first_two_vals[0])
            date_two = parser.parse(first_two_vals[1])
            if ascend_or_descend == "Descending":
                return date_one >= date_two
            elif ascend_or_descend == "Ascending":
                return date_one <= date_two
        else:
            value_one, value_two = first_two_vals
            if ascend_or_descend == "Descending":
                return value_one >= value_two
            elif ascend_or_descend == "Ascending":
                return value_one <= value_two

    @classmethod
    def show_all(self, driver):
        self.show_all_btn.click(driver)

    @classmethod
    def add_filters(
        self,
        driver,
        author=None,
        subject=None,
        resource_type=None,
        owner=None,
        variable=None,
        sample_medium=None,
        unit=None,
        availability=None,
        contributor=None,
        content_type=None,
    ):
        """Use the filters on the left side of the Discover interface.
        Filters should include author(s) {{author}}, subject(s) {{subject}},
        resource type(s) {{resource_type}}, owner(s) {{owner}}, variables
        {{variable}}, sample medium(s) {{sample_medium}}, unit(s) {{unit}},
        and availability(s) {{availability}}
        """
        if type(author) is list:
            for author_item in author:
                filter_el = self.filter_author(author_item)
                filter_el.javascript_click(driver)
        elif author is not None:
            filter_el = self.filter_author(author)
            filter_el.javascript_click(driver)
        if type(contributor) is list:
            for contributor_item in contributor:
                filter_el = self.filter_contributor(contributor_item)
                filter_el.javascript_click(driver)
        elif contributor is not None:
            filter_el = self.filter_contributor(contributor)
            filter_el.javascript_click(driver)
        if type(content_type) is list:
            for content_item in content_type:
                filter_el = self.filter_contributor(content_item)
                filter_el.javascript_click(driver)
        elif content_type is not None:
            filter_el = self.filter_content_type(content_type)
            filter_el.javascript_click(driver)
        if type(subject) is list:
            for subject_item in subject:
                filter_el = self.filter_subject(subject_item)
                filter_el.javascript_click(driver)
        elif subject is not None:
            filter_el = self.filter_subject(subject)
            filter_el.javascript_click(driver)
        if type(resource_type) is list:
            for resource_type_item in resource_type:
                filter_el = self.filter_resource_type(resource_type_item)
                filter_el.javascript_click(driver)
        elif resource_type is not None:
            filter_el = self.filter_resource_type(resource_type)
            filter_el.javascript_click(driver)
        if type(owner) is list:
            for owner_item in owner:
                filter_el = self.filter_owner(owner_item)
                filter_el.javascript_click(driver)
        elif owner is not None:
            filter_el = self.filter_owner(owner)
            filter_el.javascript_click(driver)
        if type(variable) is list:
            for variable_item in variable:
                filter_el = self.filter_variable(variable_item)
                filter_el.javascript_click(driver)
        elif variable is not None:
            filter_el = self.filter_variable(variable)
            filter_el.javascript_click(driver)
        if type(sample_medium) is list:
            for sample_medium_item in sample_medium:
                filter_el = self.filter_sample_medium(sample_medium_item)
                filter_el.javascript_click(driver)
        elif sample_medium is not None:
            filter_el = self.filter_sample_medium(sample_medium)
            filter_el.javascript_click(driver)
        if type(unit) is list:
            for unit_item in unit:
                filter_el = self.filter_unit(unit_item)
                filter_el.javascript_click(driver)
        elif unit is not None:
            filter_el = self.filter_unit(unit)
            filter_el.javascript_click(driver)
        if type(availability) is list:
            for availability_item in availability:
                filter_el = self.filter_availability(availability_item)
                filter_el.javascript_click(driver)
        elif availability is not None:
            filter_el = self.filter_availability(availability)
            filter_el.javascript_click(driver)

    @classmethod
    def legend_text(self, driver):
        self.legend.click(driver)
        labels = str(self.legend_labels.get_text(driver))
        resources = str(self.legend_resources.get_text(driver))
        return labels, resources

    @classmethod
    def search(self, driver, text):
        self.search_field.click(driver)
        self.search_field.clear_all_text(driver)
        self.search_field.inject_text(driver, text)
        self.search_field.submit(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def to_search_result_item(self, driver, col_ind, row_one):
        self.cell_href(col_ind, row_one).click(driver)

    @classmethod
    def to_resource_by_index(self, driver, index):
        num_windows_now = len(driver.window_handles)
        self.cell_href(2, index).click(driver)
        External.switch_new_page(driver, num_windows_now, Resource.authors_locator)

    @classmethod
    def is_selected(
        self,
        driver,
        author=None,
        contributor=None,
        owner=None,
        content_type=None,
        subject=None,
        availability=None,
    ):
        if author is not None:
            return self.filter_author(author).is_selected(driver)
        elif contributor is not None:
            return self.filter_contributor(contributor).is_selected(driver)
        elif owner is not None:
            return self.filter_owner(owner).is_selected(driver)
        elif content_type is not None:
            return self.filter_content_type(content_type).is_selected(driver)
        elif subject is not None:
            return self.filter_subject(subject).is_selected(driver)
        elif availability is not None:
            return self.filter_availability(availability).is_selected(driver)

    @classmethod
    def toggle_author_filter_by_index(self, driver, index):
        self.author_by_index(index).javascript_click(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def get_author_resource_count_by_index(self, driver, index):
        return int(self.author_resource_count_by_index(index).get_text(driver))

    @classmethod
    def toggle_contributor_filter_by_index(self, driver, index):
        self.contributor_by_index(index).javascript_click(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def get_contributor_resource_count_by_index(self, driver, index):
        return int(self.contributor_resource_count_by_index(index).get_text(driver))

    @classmethod
    def toggle_owner_filter_by_index(self, driver, index):
        self.owner_by_index(index).javascript_click(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def get_owner_resource_count_by_index(self, driver, index):
        return int(self.owner_resource_count_by_index(index).get_text(driver))

    @classmethod
    def toggle_type_filter_by_index(self, driver, index):
        self.type_by_index(index).javascript_click(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def get_type_resource_count_by_index(self, driver, index):
        return int(self.type_resource_count_by_index(index).get_text(driver))

    @classmethod
    def get_count_of_types(self, driver):
        time.sleep(DISCOVER_TABLE_UPDATE)
        return int(self.type_list.get_immediate_child_count(driver))

    @classmethod
    def count_results_in_table(self, driver):
        last_page = 0
        count = 0
        while True:
            time.sleep(DISCOVER_TABLE_UPDATE)
            current_page = self.page.get_value(driver)
            if current_page == last_page:
                break
            TestSystem.wait()
            self.page_right.click(driver)
            last_page = current_page
            time.sleep(DISCOVER_TABLE_UPDATE)
            count += self.result_rows.get_immediate_child_count(driver)
        return count

    @classmethod
    def uses_consistent_date_formatting(self, driver):
        last_page = 0
        while True:
            time.sleep(DISCOVER_TABLE_UPDATE)
            for i in range(1, self.result_rows.get_immediate_child_count(driver) + 1):
                # date_created = "/".join([number.zfill(2) for number in self.cell(4, i).get_text(driver).split("/")])
                date_created = self.cell(4, i).get_text(driver)
                last_modified = self.cell(5, i).get_text(driver)
                datetime.strptime(date_created, "%m/%d/%Y")
                datetime.strptime(last_modified, "%m/%d/%Y")
            current_page = self.page.get_value(driver)
            if current_page == last_page:
                break
            self.page.click(driver)
            self.page.clear_all_text(driver)
            self.page.inject_text(driver, "{}".format(int(current_page) + 1))
            self.page.inject_text(driver, Keys.ENTER)
            last_page = current_page
        return True

    @classmethod
    def get_first_author_by_resource_index(self, driver, index):
        try:
            first_author = self.cell_href(3, index).get_text(driver)
        except TimeoutException:
            first_author = self.cell(3, index).get_text(driver)
        return first_author

    @classmethod
    def uses_consistent_icon(self, driver):
        reference_src = self.resource_icon_by_index(1).get_attribute(driver, "src")
        for i in range(2, self.result_rows.get_immediate_child_count(driver) + 1):
            if (
                self.resource_icon_by_index(i).get_attribute(driver, "src")
                == reference_src
            ):
                return True
            if (
                self.resource_icon_by_index(i).get_attribute(driver, "src")
                == BASE_URL + "/static/img/resource-icons/composite48x48.png"
            ):
                return True
            if (
                reference_src
                == BASE_URL + "/static/img/resource-icons/composite48x48.png"
            ):
                return True
        return False


class Resource(Hydroshare):
    bagit = SiteElement(By.ID, "btn-download-all")
    open_with = SiteElement(By.ID, "apps-dropdown")
    open_jupyterhub = SiteElement(By.CSS_SELECTOR, 'li[title="CUAHSI JupyterHub"]')
    title = SiteElement(By.ID, "resource-title")
    resource_view = SiteElement(By.CSS_SELECTOR, ".glyphicon-circle-arrow-left")
    edit_resource = SiteElement(By.ID, "edit-metadata")
    metadata_entry = SiteElement(By.CSS_SELECTOR, 'a[title="Add New Entry"]')
    metadata_name = SiteElement(By.ID, "extra_meta_name_input")
    metadata_value = SiteElement(By.ID, "extra_meta_value_input")
    confirm_metadata = SiteElement(By.ID, "btn-confirm-extended-metadata")
    learn_more = SiteElement(By.PARTIAL_LINK_TEXT, "Learn more")
    how_to_cite = SiteElement(
        By.CSS_SELECTOR, "#rights > span:nth-child(2) > a:nth-child(1)"
    )
    comment_text = SiteElement(By.CSS_SELECTOR, "#comment textarea")
    comment_submit = SiteElement(By.CSS_SELECTOR, 'input[value="Comment"]')
    comment_section = SiteElement(By.ID, "comments")
    new_relation = SiteElement(By.CSS_SELECTOR, "a#add-relation")
    relation_type = SiteElement(By.ID, "id_type")
    relation_value = SiteElement(By.ID, "id_related_to_input")
    relation_submit = SiteElement(
        By.CSS_SELECTOR,
        "#add-relation-dialog button.btn.btn-primary.btn-disable-after-valid",
    )
    derived_from = SiteElement(By.ID, "id_derived_from")
    save_reference = SiteElement(
        By.CSS_SELECTOR, "#add-source-dialog button.btn-primary"
    )
    trash_reference = SiteElement(By.CSS_SELECTOR, "span.glyphicon-trash.table-icon")
    confirm_delete = SiteElement(By.CSS_SELECTOR, "a.btn-danger.btn-disable-after")
    new_file = SiteElement(
        By.CSS_SELECTOR, "#fb-file-operations-controls > a.upload-toggle"
    )
    abstract = SiteElement(By.ID, "id_abstract")
    abstract_save = SiteElement(By.CSS_SELECTOR, "#div_id_abstract button")
    public_resource_notice = SiteElement(By.ID, "missing-metadata-or-file")
    subject_keywords = SiteElement(By.ID, "txt-keyword")
    subject_keyword_save = SiteElement(
        By.CSS_SELECTOR, "#cv-add-keyword-wrapper button"
    )
    access_management = SiteElement(By.CSS_SELECTOR, 'a[data-target="#manage-access"')
    copy = SiteElement(By.ID, "copy-resource")
    accept_terms = SiteElement(By.ID, "agree-chk-copy")
    confirm_copy = SiteElement(By.ID, "copy-btn")
    new_version = SiteElement(By.ID, "new-version")
    new_version_confirm = SiteElement(By.ID, "new-version-btn")
    delete = SiteElement(By.ID, "delete")
    delete_text = SiteElement(By.ID, "confirm-res-id-text")
    delete_confirmation = SiteElement(By.ID, "btn-delete-resource")
    title_input = SiteElement(By.ID, "txt-title")
    title_save = SiteElement(By.ID, "title-save-button")
    grant_input = SiteElement(By.ID, "user-autocomplete")
    access_add = SiteElement(By.ID, "btn-confirm-add-access")
    access_close = SiteElement(
        By.CSS_SELECTOR, "#manage-access > div > div > div.modal-footer > a"
    )
    access_table = SiteElement(By.CSS_SELECTOR, ".access-table > tbody")
    access_type = SiteElement(By.ID, "roles_list")
    access_type_editor = SiteElement(By.CSS_SELECTOR, 'a[data-role="edit"]')
    access_type_owner = SiteElement(By.CSS_SELECTOR, 'a[data-role="owner"]')
    access_sharable = SiteElement(
        By.CSS_SELECTOR, "#sharing-status input[type=checkbox]"
    )
    access_public = SiteElement(By.ID, "btn-public")
    access_discoverable = SiteElement(By.ID, "btn-discoverable")
    authors = SiteElement(By.CSS_SELECTOR, ".authors-wrapper")
    authors_locator = By.CSS_SELECTOR, ".authors-wrapper"
    download_status = SiteElement(By.ID, "download-status-info")
    # If your download does not start automatically
    file_download = SiteElement(
        By.CSS_SELECTOR, '#right-click-menu > li[data-fb-action="download"]'
    )
    file_download_zip = SiteElement(
        By.CSS_SELECTOR, '#right-click-menu > li[data-fb-action="downloadZipped"]'
    )
    file_link = SiteElement(
        By.CSS_SELECTOR, '#right-click-menu > li[data-fb-action="getLink"]'
    )
    file_delete = SiteElement(
        By.CSS_SELECTOR, '#right-click-menu > li[data-fb-action="delete"]'
    )
    file_link_field = SiteElement(By.ID, "txtFileURL")
    spatial_north_limit = SiteElement(By.ID, "id_northlimit")
    spatial_east_limit = SiteElement(By.ID, "id_eastlimit")
    spatial_south_limit = SiteElement(By.ID, "id_southlimit")
    spatial_west_limit = SiteElement(By.ID, "id_westlimit")
    spatial_latitude = SiteElement(By.ID, "id_north")
    spatial_longitude = SiteElement(By.ID, "id_east")
    spatial_save = SiteElement(By.CSS_SELECTOR, "#coverage-header > button")
    spatial_delete = SiteElement(By.ID, "id-delete-spatial-resource")
    spatial_set_box = SiteElement(By.ID, "id_type_1")
    spatial_set_point = SiteElement(By.ID, "id_type_2")
    file_delete_confirm = SiteElement(By.ID, "btn-confirm-delete")
    sharing_status = SiteElement(By.ID, "hl-sharing-status")
    file_browser_alerts = SiteElement(By.ID, "fb-alerts")
    file_browser = SiteElement(By.ID, "hs-file-browser")

    @classmethod
    def open_with_title(self, title):
        return SiteElement(By.XPATH, '//li[@title="{}"]/a'.format(title))

    @classmethod
    def name(self, name):
        return SiteElement(By.XPATH, '//td[text()= "{}"]'.format(name))

    @classmethod
    def value(self, value):
        return SiteElement(By.XPATH, '//td[text()= "{}"]'.format(value))

    @classmethod
    def author(self, index):
        return SiteElement(
            By.CSS_SELECTOR, ".authors-wrapper > a:nth-of-type({})".format(index)
        )

    @classmethod
    def notification_link(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#app-notifications .task:nth-of-type({}) .notification--name a".format(
                index
            ),
        )

    @classmethod
    def resource_file(self, index):
        return SiteElement(
            By.CSS_SELECTOR, "#fb-files-container > li:nth-of-type({})".format(index)
        )

    @classmethod
    def download_bagit(self, driver):
        self.bagit.click(driver)

    @classmethod
    def open_with_jupyterhub(self, driver):
        self.open_with.click(driver)
        self.open_jupyterhub.click(driver)

    @classmethod
    def open_with_by_title(self, driver, title):
        self.open_with.click(driver)
        self.open_with_title(title).click(driver)

    @classmethod
    def get_title(self, driver):
        return self.title.get_text(driver)

    @classmethod
    def view(self, driver):
        self.resource_view.click(driver)
        TestSystem.wait(EXTERNAL_PAGE_LOAD)

    @classmethod
    def edit(self, driver):
        self.edit_resource.click(driver)

    @classmethod
    def add_metadata(self, driver, name, value):
        self.metadata_entry.click(driver)
        self.metadata_name.inject_text(driver, name)
        self.metadata_value.inject_text(driver, value)
        self.confirm_metadata.click(driver)

    @classmethod
    def exists_name(self, driver, name):
        self.name(name).get_text(driver)

    @classmethod
    def exists_value(self, driver, value):
        self.value(value).get_text(driver)

    @classmethod
    def to_reference_citation(self, driver):
        self.how_to_cite.click(driver)

    @classmethod
    def to_reference_bagit(self, driver):
        self.learn_more.click(driver)

    @classmethod
    def add_comment(self, driver, text):
        self.comment_text.scroll_to(driver)
        self.comment_text.inject_text(driver, text)
        self.comment_submit.click(driver)

    @classmethod
    def get_comment_count(self, driver):
        return self.comment_section.get_immediate_child_count(driver) - 4

    @classmethod
    def is_downloadable(self, driver):
        return self.bagit.exists(driver)

    @classmethod
    def add_reference(self, driver, reference_text):
        self.new_relation.click(driver)
        self.relation_type.select_option_text(driver, "This resource is referenced by")
        self.relation_value.inject_text(driver, "https://google.com")
        self.relation_submit.click(driver)

    @classmethod
    def delete_reference(self, driver):
        self.trash_reference.click(driver)
        self.confirm_delete.click(driver)

    @classmethod
    def upload_file(self, driver, path):
        self.new_file.set_path(driver, path)

    @classmethod
    def populate_abstract(self, driver, text):
        self.abstract.inject_text(driver, text)
        self.abstract_save.javascript_click(driver)

    @classmethod
    def is_visible_public_resource_notice(self, driver):
        self.public_resource_notice.is_visible(driver)

    @classmethod
    def add_subject_keyword(self, driver, keyword):
        self.subject_keywords.inject_text(driver, keyword)
        self.subject_keyword_save.click(driver)

    @classmethod
    def make_public(self, driver):
        self.access_management.click(driver)
        self.access_public.click(driver)
        self.access_close.click(driver)

    @classmethod
    def make_discoverable(self, driver):
        self.access_management.click(driver)
        self.access_discoverable.click(driver)
        self.access_close.click(driver)

    @classmethod
    def copy_resource(self, driver):
        self.copy.click(driver)
        self.accept_terms.click(driver)
        self.confirm_copy.click(driver)

    @classmethod
    def create_version(self, driver):
        self.new_version.click(driver)
        self.new_version_confirm.click(driver)

    @classmethod
    def delete_resource(self, driver):
        self.delete.click(driver)
        self.delete_text.click(driver)
        self.delete_text.inject_text(driver, "DELETE")
        self.delete_confirmation.click(driver)

    @classmethod
    def set_title(self, driver, title):
        self.title_input.click(driver)
        self.title_input.clear_all_text(driver)
        self.title_input.inject_text(driver, title)
        self.title_save.click(driver)

    @classmethod
    def grant_viewer(self, driver, username):
        self.access_management.click(driver)
        self.grant_input.inject_text(driver, username)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ARROW_DOWN)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ENTER)
        time.sleep(KEYS_RESPONSE)
        self.access_add.click(driver)
        self.access_close.click(driver)

    @classmethod
    def grant_editor(self, driver, username):
        self.access_management.click(driver)
        self.access_type.click(driver)
        self.access_type_editor.click(driver)
        self.grant_input.inject_text(driver, username)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ARROW_DOWN)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ENTER)
        time.sleep(KEYS_RESPONSE)
        self.access_add.click(driver)
        self.access_close.click(driver)

    @classmethod
    def grant_owner(self, driver, username):
        self.access_management.click(driver)
        self.access_type.click(driver)
        self.access_type_owner.click(driver)
        self.grant_input.inject_text(driver, username)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ARROW_DOWN)
        time.sleep(KEYS_RESPONSE)
        self.grant_input.inject_text(driver, Keys.ENTER)
        time.sleep(KEYS_RESPONSE)
        self.access_add.click(driver)
        self.access_close.click(driver)

    @classmethod
    def get_user_access_count(self, driver):
        self.access_management.click(driver)
        count = self.access_table.get_immediate_child_count(driver)
        self.access_close.click(driver)
        return count

    @classmethod
    def toggle_sharable(self, driver):
        self.access_management.click(driver)
        self.access_sharable.click(driver)
        self.access_close.click(driver)

    @classmethod
    def get_authors(self, driver):
        authors_count = self.authors.get_immediate_child_count(driver)
        authors = [self.author(i).get_text(driver) for i in range(1, authors_count + 1)]
        return authors

    @classmethod
    def use_notification_link(self, driver, index):
        self.notification_link(index).click(driver)

    @classmethod
    def wait_on_task_completion(self, driver, index, timeout):
        elapsed = 0
        while elapsed < timeout:
            try:
                self.notification_link(index).click(driver)
                break
            except TimeoutException:
                time.sleep(1)
                elapsed += 1

    @classmethod
    def wait_on_download_notification(self, driver):
        while "Please wait" in self.download_status.get_text(driver):
            time.sleep(1)

    @classmethod
    def download_file_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        self.resource_file(index).right_click(driver)
        self.file_download.javascript_click(driver)

    @classmethod
    def download_file_zip_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        self.resource_file(index).right_click(driver)
        self.file_download_zip.javascript_click(driver)

    @classmethod
    def get_file_download_link_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        self.resource_file(index).right_click(driver)
        self.file_link.javascript_click(driver)
        return self.file_link_field.get_value(driver)

    @classmethod
    def set_spatial_coverage_box(self, driver, north, east, south, west):
        self.spatial_set_box.click(driver)
        self.spatial_north_limit.inject_text(driver, str(north))
        self.spatial_east_limit.inject_text(driver, str(east))
        self.spatial_south_limit.inject_text(driver, str(south))
        self.spatial_west_limit.inject_text(driver, str(west))
        self.spatial_save.click(driver)

    @classmethod
    def set_spatial_coverage_point(self, driver, latitude, longitude):
        self.spatial_set_point.click(driver)
        self.spatial_latitude.inject_text(driver, str(latitude))
        self.spatial_longitude.inject_text(driver, str(longitude))
        self.spatial_save.click(driver)

    @classmethod
    def delete_spatial_coverage(self, driver):
        self.spatial_delete.click(driver)

    @classmethod
    def delete_file_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        self.resource_file(index).right_click(driver)
        self.file_delete.javascript_click(driver)
        self.file_delete_confirm.click(driver)

    @classmethod
    def get_sharing_status(self, driver):
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        return self.sharing_status.get_text(driver)


class WebApp(Resource):
    save_supported_resource_types = SiteElement(
        By.CSS_SELECTOR, "#id-supportedrestypes button.btn-form-submit"
    )
    add_open_with = SiteElement(By.ID, "btnOpenWithApp")
    app_launching_url = SiteElement(
        By.CSS_SELECTOR, "form#id-requesturlbase input#id_value"
    )
    save_app_launching_url = SiteElement(
        By.CSS_SELECTOR, "#id-requesturlbase button.btn-form-submit"
    )

    @classmethod
    def supported_resource_type(self, resource_type):
        return SiteElement(By.CSS_SELECTOR, 'input[value="{}"]'.format(resource_type))

    @classmethod
    def support_resource_type(self, driver, resource_type):
        self.supported_resource_type(resource_type).click(driver)
        self.save_supported_resource_types.click(driver)

    @classmethod
    def set_app_launching_url(self, driver, url):
        self.app_launching_url.inject_text(driver, url)
        self.save_app_launching_url.click(driver)

    @classmethod
    def add_to_open_with(self, driver):
        self.add_open_with.click(driver)


class Help(Hydroshare):
    to_about = SiteElement(By.CSS_SELECTOR, 'a[href="{}"]'.format("/about-hydroshare"))
    core_root = SiteElement(By.CSS_SELECTOR, "#help-topics-grid")

    @classmethod
    def core_item(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#help-topics-grid > a:nth-of-type({}) > div.topic-body > div".format(
                index
            ),
        )

    @classmethod
    def get_core_count(self, driver):
        return self.core_root.get_immediate_child_count(driver)

    @classmethod
    def get_core_topic(self, driver, index):
        return self.core_item(index).get_text(driver)

    @classmethod
    def open_core(self, driver, index):
        self.core_item(index).click(driver)


class HelpArticle(Hydroshare):
    core_breadcrumb = SiteElement(By.ID, "breadcrumb-menu-home")
    title = SiteElement(By.CSS_SELECTOR, "h1.page-title")

    @classmethod
    def to_help_breadcrumb(self, driver):
        self.core_breadcrumb.click(driver)

    @classmethod
    def get_title(self, driver):
        return self.title.get_text(driver)


class About(Hydroshare):
    tree_root = SiteElement(
        By.CSS_SELECTOR, "#tree-menu-about-hydroshare div.tree-menu-item i"
    )
    article_title = SiteElement(By.CSS_SELECTOR, "h1.page-title")

    @classmethod
    def tree_top(self, item):
        return SiteElement(
            By.CSS_SELECTOR,
            "#tree-menu-about-hydroshare "
            "#tree-menu-about-hydroshare-{} "
            "div.tree-menu-item i".format(item),
        )

    @classmethod
    def tree_policy(self, item):
        return SiteElement(
            By.CSS_SELECTOR,
            "#tree-menu-about-hydroshare "
            "#tree-menu-about-hydroshare-policies-{} "
            "div.tree-menu-item a".format(item),
        )

    @classmethod
    def toggle_tree(self, driver):
        self.tree_root.click(driver)
        time.sleep(HELP_DOCS_TREE_ANIMATIONS)

    @classmethod
    def expand_tree_top(self, driver, item):
        item = item.replace(" ", "-").lower()
        self.tree_top(item).click(driver)

    @classmethod
    def open_policy(self, driver, policy):
        policy = policy.replace(" ", "-").lower()
        self.tree_policy(policy).click(driver)

    @classmethod
    def get_title(self, driver):
        return self.article_title.get_text(driver)


class API(Hydroshare):
    hsapi = SiteElement(By.ID, "endpointListTogger_hsapi")
    endpoint_list = SiteElement(
        By.CSS_SELECTOR, "div.opblock-tag-section div:first-child"
    )
    try_out = SiteElement(By.CSS_SELECTOR, "div.try-out > button.btn:nth-child(1)")
    execute = SiteElement(By.CSS_SELECTOR, ".execute")
    response_code = SiteElement(By.CSS_SELECTOR, ".response_current > td:nth-child(1)")

    @classmethod
    def path(self, endpoint):
        return SiteElement(By.CSS_SELECTOR, "#{} > div:nth-child(1)".format(endpoint))

    @classmethod
    def parameter(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            ".parameters > tbody:nth-child(2) > tr:nth-child({}) > "
            "td:nth-child(2) > input:nth-child(1)".format(index),
        )

    @classmethod
    def toggle_endpoint(self, driver, endpoint):
        self.path(endpoint).click(driver)

    @classmethod
    def try_endpoint(self, driver):
        self.try_out.click(driver)

    @classmethod
    def set_parameter(self, driver, param_ind, param_val):
        self.parameter(param_ind).click(driver)
        self.parameter(param_ind).inject_text(driver, param_val)

    @classmethod
    def execute_request(self, driver):
        self.execute.click(driver)
        time.sleep(HSAPI_GUI_RESPONSE)

    @classmethod
    def get_response_code(self, driver):
        return self.response_code.get_text(driver)


class Profile(Hydroshare):
    edit = SiteElement(By.ID, "btn-edit-profile")
    organizations = SiteElement(By.CSS_SELECTOR, 'input[placeholder="Organization(s)"]')
    save = SiteElement(By.CSS_SELECTOR, "button.btn-save-profile:first-of-type")
    image_upload = SiteElement(By.CSS_SELECTOR, "input.upload-picture")
    image = SiteElement(By.CSS_SELECTOR, "div.profile-pic.round-image")
    delete_image = SiteElement(By.CSS_SELECTOR, "#btn-delete-profile-pic")
    submit_delete_image = SiteElement(By.CSS_SELECTOR, "#picture-clear_id")
    add_cv = SiteElement(By.XPATH, '//input[@type="file"]')
    view_cv = SiteElement(By.XPATH, '(//a[@class= "btn btn-default"]/span)[3]')
    delete_cv = SiteElement(By.ID, "btn-delete-cv")
    confirm_delete_cv = SiteElement(By.ID, "cv-clear_id")
    contribution = SiteElement(By.CSS_SELECTOR, 'a[aria-controls="profile"]')
    contribution_types_breakdown = SiteElement(
        By.CSS_SELECTOR, "table.table-user-contributions tbody"
    )
    contributions_list = SiteElement(
        By.CSS_SELECTOR, "#contributions > .row > .col-md-9"
    )
    password_change = SiteElement(By.XPATH, '//a[contains(text(), "Change password")]')
    current_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password"]')
    new_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password1"]')
    confirm_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password2"]')
    password_confirm = SiteElement(By.XPATH, '//button[contains(text(), "Confirm")]')
    description = SiteElement(By.CSS_SELECTOR, 'textarea[name="details"]')
    country = SiteElement(By.CSS_SELECTOR, 'select[name="country"]')
    province = SiteElement(By.CSS_SELECTOR, 'input[name="state"]')
    name = SiteElement(By.CSS_SELECTOR, "h2")
    phone1 = SiteElement(By.ID, "phone1")
    phone2 = SiteElement(By.ID, "phone2")
    email = SiteElement(By.ID, "id_email")
    website = SiteElement(By.CSS_SELECTOR, 'input[name="website"]')
    user_type = SiteElement(By.ID, "db-user-type")
    user_overview_0 = SiteElement(
        By.CSS_SELECTOR,
        "#body > div.main-container > div.container > div.row > div > div > div.col-xs-12.col-sm-6 > div > table",
    )
    user_overview_1 = SiteElement(
        By.CSS_SELECTOR, "#overview div.panel:nth-of-type(1) table.overview"
    )
    user_overview_2 = SiteElement(
        By.CSS_SELECTOR, "#overview div.panel:nth-of-type(2) table.overview"
    )
    headline = SiteElement(
        By.CSS_SELECTOR,
        "#body > div.main-container > div.container > div.row > div > div > div.col-xs-12.col-sm-6 > div > h4",
    )
    view_description = SiteElement(By.ID, "profile-description")
    profile_picture = SiteElement(By.CSS_SELECTOR, "#profile-pic-container > div")

    @classmethod
    def contribution_type(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "table.table-user-contributions tbody tr:nth-of-type({})".format(index + 1),
        )

    @classmethod
    def contribution_type_count(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "table.table-user-contributions tbody "
            + "tr:nth-of-type({})".format(index + 1)
            + " td:nth-of-type(2) span",
        )

    @classmethod
    def organization_deletion(self, index):
        return SiteElement(By.CSS_SELECTOR, "span.tag:nth-of-type({}) a".format(index))

    @classmethod
    def to_editor(self, driver):
        self.edit.click(driver)

    @classmethod
    def add_organization(self, driver, org):
        self.organizations.inject_text(driver, org)
        self.organizations.inject_text(driver, Keys.ARROW_DOWN)
        self.organizations.inject_text(driver, Keys.ENTER)

    @classmethod
    def delete_organization(self, driver, index):
        self.organization_deletion(index).click(driver)

    @classmethod
    def save_changes(self, driver):
        self.save.javascript_click(driver)
        time.sleep(PROFILE_SAVE)

    @classmethod
    def add_photo(self, driver, link):
        self.image_upload.set_path(driver, link)

    @classmethod
    def remove_photo(self, driver):
        self.delete_image.click(driver)
        self.submit_delete_image.click(driver)

    @classmethod
    def confirm_photo_uploaded(self, driver, contains):
        return contains in self.image.get_style(driver)

    @classmethod
    def view_cv(self, driver):
        self.view_cv.click(driver)

    @classmethod
    def delete_cv(self, driver):
        self.delete_cv.click(driver)
        self.confirm_delete_cv.click(driver)

    @classmethod
    def view_contributions(self, driver):
        self.contribution.click(driver)

    @classmethod
    def view_contribution_type(self, driver, ind):
        self.contribution_type(ind).javascript_click(driver)

    @classmethod
    def get_resource_type_count(self, driver):
        contribution_types_breakdown = self.contribution_types_breakdown
        return contribution_types_breakdown.get_immediate_child_count(driver)

    @classmethod
    def get_contribution_type_count(self, driver, ind):
        type_count = self.contribution_type_count(ind).get_text(driver)
        return int(type_count)

    @classmethod
    def get_contributions_list_length(self, driver):
        return self.contributions_list.get_immediate_child_count(driver)

    @classmethod
    def upload_cv(self, driver, cv):
        urlretrieve(cv, "cv-test.pdf")
        cwd = os.getcwd()
        cv_path = os.path.join(cwd, "cv-test.pdf")
        TestSystem.execute_javascript(
            driver, "document.getElementsByName('cv').path={}".format(cv_path)
        )

    @classmethod
    def reset_password(self, driver, old_password, new_password):
        self.password_change.click(driver)
        self.current_password.inject_text(driver, old_password)
        self.new_password.inject_text(driver, new_password)
        self.confirm_password.inject_text(driver, new_password)
        self.password_confirm.scroll_to(driver)
        self.password_confirm.click(driver)

    @classmethod
    def queue_password_change(self, driver, old_password, new_password):
        self.password_change.click(driver)
        self.current_password.inject_text(driver, old_password)
        self.new_password.inject_text(driver, new_password)
        self.confirm_password.inject_text(driver, new_password)

    @classmethod
    def update_about(self, driver, description, country, province):
        self.description.click(driver)
        self.description.clear_all_text(driver)
        self.description.inject_text(driver, description)
        self.country.select_option_text(driver, country)
        self.province.click(driver)
        self.province.clear_all_text(driver)
        self.province.inject_text(driver, province)

    @classmethod
    def update_contact(
        self, driver, phone1=None, phone2=None, email=None, website=None
    ):
        if phone1 is not None:
            self.phone1.click(driver)
            self.phone1.clear_all_text(driver)
            self.phone1.inject_text(driver, phone1)
        if phone2 is not None:
            self.phone2.click(driver)
            self.phone2.clear_all_text(driver)
            self.phone2.inject_text(driver, phone2)
        if email is not None:
            self.email.click(driver)
            self.email.clear_all_text(driver)
            self.email.inject_text(driver, email)
        if website is not None:
            self.website.click(driver)
            self.website.clear_all_text(driver)
            self.website.inject_text(driver, website)

    @classmethod
    def get_name(self, driver):
        return self.name.get_text(driver)

    @classmethod
    def get_email(self, driver):
        return self.email.get_value(driver)

    @classmethod
    def get_data(self, driver):
        html_strip = re.compile("<.*?>")
        email_strip = re.compile("send email to")
        email = re.search('mailto:(.+?)"', TestSystem.page_source(driver)).group(1)
        name = self.name.get_text(driver) if self.name.exists(driver) else ""
        headline = (
            self.headline.get_text(driver) if self.headline.exists(driver) else ""
        )
        description = (
            self.view_description.get_text(driver)
            if self.view_description.exists(driver)
            else ""
        )
        profile_picture = (
            self.profile_picture.get_style(driver)
            .replace('background-image: url("', "")
            .replace('");', "")
        )
        # if profile_picture in [None, ""]:
        #     profile_picture = "/static/media/profile/NoProfileImage.png"
        overview0 = (
            re.sub(
                html_strip, "", self.user_overview_0.get_attribute(driver, "innerHTML")
            )
            if self.user_overview_0.exists(driver)
            else ""
        )
        overview1 = (
            re.sub(
                html_strip, "", self.user_overview_1.get_attribute(driver, "innerHTML")
            )
            if self.user_overview_1.exists(driver)
            else ""
        )
        overview2 = (
            re.sub(
                email_strip, "", self.user_overview_2.get_attribute(driver, "innerHTML")
            )
            if self.user_overview_2.exists(driver)
            else ""
        )
        overview2 = re.sub(html_strip, "", overview2)
        overview2 = overview2.replace("Email\n", "\n")
        return {
            "name": name,
            "headline": headline,
            "email": email,
            "profile_picture": profile_picture,
            "description": description,
            "overview_0": "\n".join(
                [ll.lstrip() for ll in overview0.splitlines() if ll.strip()]
            ),
            "overview_1": "\n".join(
                [ll.lstrip() for ll in overview1.splitlines() if ll.strip()]
            ),
            "overview_2": "\n".join(
                [ll.lstrip() for ll in overview2.splitlines() if ll.strip()]
            ),
        }


class Collaborate(Hydroshare):
    groups = SiteElement(By.CSS_SELECTOR, 'a[href="/groups"]')

    @classmethod
    def to_groups(self, driver):
        self.groups.click(driver)


class Groups(Hydroshare):
    group_creation = SiteElement(
        By.CSS_SELECTOR, 'a[data-target="#create-group-dialog"]'
    )
    my_groups = SiteElement(By.CSS_SELECTOR, 'a[href="/my-groups/"]')
    title = SiteElement(By.CSS_SELECTOR, ".page-title")
    name = SiteElement(By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(1) textarea")
    purpose = SiteElement(By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(2) textarea")
    about = SiteElement(By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(3) textarea")
    public = SiteElement(By.CSS_SELECTOR, 'input[value="public"]')
    discoverable = SiteElement(By.CSS_SELECTOR, 'input[value="discoverable"]')
    private = SiteElement(By.CSS_SELECTOR, 'input[value="private"]')
    submit = SiteElement(By.CSS_SELECTOR, 'button[type="submit"]')

    @classmethod
    def to_my_groups(self, driver):
        self.my_groups.click(driver)

    @classmethod
    def get_title(self, driver):
        return self.title.get_text(driver)

    @classmethod
    def create_group(self, driver, name, purpose, about, privacy):
        self.group_creation.click(driver)
        self.name.inject_text(driver, name)
        self.purpose.inject_text(driver, purpose)
        self.about.inject_text(driver, about)
        if privacy.lower() == "public":
            self.public.click(driver)
        elif privacy.lower() == "discoverable":
            self.discoverable.click(driver)
        else:
            self.private.click(driver)
        self.submit.click(driver)


class Group(Hydroshare):
    name = SiteElement(By.CSS_SELECTOR, ".group-title")

    @classmethod
    def check_title(self, driver):
        return self.name.get_text(driver)


class MyResources(Hydroshare):
    resource_type_selector = SiteElement(By.ID, "select-resource-type")
    cancel_resource = SiteElement(By.CSS_SELECTOR, ".btn-cancel-create-resource")
    resource_types = SiteElement(By.CSS_SELECTOR, "#input-resource-type")
    search_options = SiteElement(By.CSS_SELECTOR, ".btn.btn-default.dropdown-toggle")
    search = SiteElement(By.CSS_SELECTOR, "#resource-search-input")
    author = SiteElement(By.CSS_SELECTOR, "#input-author")
    subject = SiteElement(By.CSS_SELECTOR, "#input-subject")
    search_clear = SiteElement(By.CSS_SELECTOR, "#btn-clear-search-input")
    author_search_clear = SiteElement(By.CSS_SELECTOR, "#btn-clear-author-input")
    subject_search_clear = SiteElement(By.CSS_SELECTOR, "#btn-clear-subject-input")
    label = SiteElement(By.CSS_SELECTOR, "#btn-label")
    create_label_icon = SiteElement(By.XPATH, '//li[@data-target="#modalCreateLabel"]')
    new_label_name = SiteElement(By.CSS_SELECTOR, "#txtLabelName")
    create_label_submit = SiteElement(By.CSS_SELECTOR, "#btn-create-label")
    add_label = SiteElement(
        By.CSS_SELECTOR,
        "tr.data-row:nth-child(1) > td:nth-child(1) > "
        + 'span[data-toggle="dropdown"]:nth-child(5)',
    )
    manage_labels = SiteElement(By.XPATH, '//li[@data-target="#modalManageLabels"]')
    remove_label = SiteElement(By.CSS_SELECTOR, ".btn-label-remove")
    legend = SiteElement(By.CSS_SELECTOR, "#headingLegend h4 a")
    legend_labels = SiteElement(
        By.CSS_SELECTOR,
        "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-5",
    )
    legend_resources = SiteElement(
        By.CSS_SELECTOR,
        "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-7",
    )

    @classmethod
    def label_checkbox(self, label_name):
        return SiteElement(
            By.XPATH,
            '//td[@class="open"]//label[contains(text(), "{}")]'.format(label_name),
        )

    @classmethod
    def resource_type(self, option):
        return SiteElement(By.XPATH, '//option[contains(text(), "{}")]'.format(option))

    @classmethod
    def resource_creation_type(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#dropdown-resource-type ul li:nth-of-type({})".format(index),
        )

    @classmethod
    def resource_title(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#item-selectors > tbody > tr:nth-child({}) > td:nth-child(3)".format(
                index
            ),
        )

    @classmethod
    def resource_link(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#item-selectors > tbody > tr:nth-child({}) > td:nth-child(3) > strong > a".format(
                index
            ),
        )

    @classmethod
    def resource_author(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#item-selectors > tbody > tr:nth-child({}) > td:nth-child(4)".format(
                index
            ),
        )

    @classmethod
    def resource_favorite(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#item-selectors > tbody > tr:nth-child({}) > td:nth-child(1) > span.glyphicon-star".format(
                index
            ),
        )

    @classmethod
    def table_filter(self, data_facet):
        return SiteElement(By.CSS_SELECTOR, 'input[data-facet="{}"]'.format(data_facet))

    @classmethod
    def get_resource_type_indexes(self, driver):
        self.resource_type_selector.click(driver)
        resource_creation_list = self.resource_creation_list
        count = resource_creation_list.get_immediate_child_count(driver)
        resource_type_indexes = []
        for i in range(1, count + 1):
            el_class = self.resource_creation_type(i).get_class(driver)
            if el_class not in ["dropdown-header", "divider"]:
                resource_type_indexes.append(i)
        self.resource_type_selector.click(driver)
        return resource_type_indexes

    @classmethod
    def select_resource_type(self, driver, index):
        self.resource_type_selector.click(driver)
        self.resource_creation_type(index).click(driver)

    @classmethod
    def enter_search(self, driver, text):
        self.search.inject_text(driver, text)

    @classmethod
    def search_resource_type(self, driver):
        self.search_options.click(driver)

    @classmethod
    def search_type(self, driver, option):
        self.resource_type(option).click(driver)

    @classmethod
    def search_author(self, driver, author):
        self.author.inject_text(driver, author)

    @classmethod
    def search_subject(self, driver, subject):
        self.subject.inject_text(driver, subject)

    @classmethod
    def clear_search(self, driver):
        self.search_clear.click(driver)

    @classmethod
    def clear_author_search(self, driver):
        self.author_search_clear.click(driver)

    @classmethod
    def clear_subject_search(self, driver):
        self.subject_search_clear.click(driver)

    @classmethod
    def read_searchbar(self, driver):
        return self.search.get_value(driver)

    @classmethod
    def create_label(self, driver, new_name):
        self.label.click(driver)
        self.create_label_icon.click(driver)
        self.new_label_name.inject_text(driver, new_name)
        self.create_label_submit.click(driver)
        time.sleep(LABEL_CREATION)

    @classmethod
    def toggle_label(self, driver, label):
        self.add_label.click(driver)
        self.label_checkbox(label).click(driver)
        self.add_label.click(driver)

    @classmethod
    def check_label_applied(self, driver):
        return "has-labels" in self.add_label.get_class(driver)

    @classmethod
    def delete_label(self, driver):
        self.label.click(driver)
        self.manage_labels.click(driver)
        self.remove_label.click(driver)

    @classmethod
    def legend_text(self, driver):
        self.legend.click(driver)
        labels = str(self.legend_labels.get_text(driver))
        resources = str(self.legend_resources.get_text(driver))
        return labels, resources

    @classmethod
    def to_resource_from_table(self, driver, index):
        self.resource_link(index).click(driver)

    @classmethod
    def get_resource_link(self, driver, index):
        return self.resource_link(index).get_attribute(driver, "href")

    @classmethod
    def to_author_from_table(self, driver, index):
        self.resource_author(index).click(driver)

    @classmethod
    def favorite_resource(self, driver, index):
        self.resource_favorite(index).click(driver)

    @classmethod
    def filter_table(self, driver, data_facet):
        self.table_filter(data_facet).click(driver)


class NewResource(Hydroshare):
    title = SiteElement(By.ID, "input-title")
    create_btn = SiteElement(By.ID, "btn-resource-create")
    cancel_btn = SiteElement(
        By.CSS_SELECTOR,
        "#submit-title-dialog div.modal-dialog div.modal-content div.modal-footer "
        + "button:nth-of-type(1)",
    )

    @classmethod
    def configure(self, driver, title):
        self.title.click(driver)
        self.title.clear_all_text(driver)
        self.title.inject_text(driver, title)

    @classmethod
    def cancel(self, driver):
        self.cancel_btn.click(driver)
        time.sleep(RESOURCE_CREATION / 2)

    @classmethod
    def create(self, driver):
        self.create_btn.click(driver)
        time.sleep(RESOURCE_CREATION)


class Registration(Hydroshare):
    first_name = SiteElement(By.ID, "id_first_name")
    last_name = SiteElement(By.ID, "id_last_name")
    email = SiteElement(By.ID, "id_email")
    username = SiteElement(By.ID, "id_username")
    organizations = SiteElement(By.CSS_SELECTOR, 'input[placeholder="Organization(s)"]')
    password1 = SiteElement(By.ID, "id_password1")
    password2 = SiteElement(By.ID, "id_password2")
    signup = SiteElement(By.ID, "signup")
    error = SiteElement(By.CSS_SELECTOR, "p.alert")

    @classmethod
    def signup_user(
        self,
        driver,
        first_name=None,
        last_name=None,
        email=None,
        username=None,
        organizations=[],
        password=None,
    ):
        if first_name is not None:
            self.first_name.click(driver)
            self.first_name.inject_text(driver, first_name)
        if last_name is not None:
            self.last_name.click(driver)
            self.last_name.inject_text(driver, last_name)
        if email is not None:
            self.email.click(driver)
            self.email.inject_text(driver, email)
        if username is not None:
            self.username.click(driver)
            self.username.inject_text(driver, username)
        for organization in organizations:
            self.organizations.click(driver)
            self.organizations.inject_text(driver, organization)
            self.organizations.inject_text(driver, Keys.ENTER)
        if password is not None:
            self.password1.click(driver)
            self.password1.inject_text(driver, username)
            self.password2.click(driver)
            self.password2.inject_text(driver, username)
        self.signup.click(driver)

    @classmethod
    def check_error(self, driver):
        return self.error.get_text(driver)


class SiteMap(Hydroshare):
    @classmethod
    def resource_link(self, index):
        return SiteElement(By.CSS_SELECTOR, "h4:nth-of-type({}) a".format(index + 1))

    @classmethod
    def resource_selection(self, resource):
        return SiteElement(By.LINK_TEXT, "{}".format(resource))

    @classmethod
    def all_resource_links(self, driver):
        return SiteElementsCollection(By.CSS_SELECTOR, 'a[href*="/resource"]').items(
            driver
        )

    @classmethod
    def get_resource_list(self, driver):
        return list(self.all_resource_links(driver))

    @classmethod
    def select_resource(self, driver, res):
        self.resource_selection(res).click(driver)
        time.sleep(EXTERNAL_PAGE_LOAD)

    @classmethod
    def select_resource_by_index(self, driver, index):
        self.resource_link(index).click(driver)


class JupyterHub:
    login = SiteElement(By.CSS_SELECTOR, "#login-main > div > a")
    authorize = SiteElement(By.CSS_SELECTOR, 'input[value="Authorize"]')
    minimal_spawner = SiteElement(By.ID, "profile-item-0")
    scientific_spawner = SiteElement(By.ID, "profile-item-1")
    r_scientific_spawner = SiteElement(By.ID, "profile-item-2")
    spawn = SiteElement(By.CSS_SELECTOR, 'input[value="Start"]')
    sort_name = SiteElement(By.ID, "sort-name")
    terms_of_use = SiteElement(By.ID, "chk-tou")

    @classmethod
    def to_hs_login(self, driver):
        self.login.click(driver)

    @classmethod
    def authorize_jupyterhub(self, driver):
        self.authorize.javascript_click(driver)

    @classmethod
    def select_minimal_spawner(self, driver):
        self.minimal_spawner.click(driver)
        self.spawn.click(driver)

    @classmethod
    def select_scientific_spawner(self, driver):
        self.scientific_spawner.click(driver)
        self.spawn.click(driver)

    @classmethod
    def select_r_scientific_spawner(self, driver):
        self.r_scientific_spawner.click(driver)
        self.spawn.click(driver)

    @classmethod
    def agree_to_terms_of_use(self, driver):
        JupyterHub.terms_of_use.click(driver)


class JupyterHubNotebooks:
    sort_name = SiteElement(By.ID, "sort-name")
    top_panel = SiteElement(By.ID, "jp-top-panel")
    notebook_spawner = SiteElement(By.CSS_SELECTOR, 'div[data-category="Notebook"]')

    @classmethod
    def wait_on_server_creation(self, driver):
        JupyterHubNotebooks.top_panel.wait_on_visibility(driver, 600)

    @classmethod
    def sort_notebooks_by_name(self, driver):
        JupyterHubNotebooks.sort_name.click(driver)

    @classmethod
    def select_notebook_spawner(self, driver):
        self.notebook_spawner.click(driver)

    @classmethod
    def is_spawner_set(self, driver):
        try:
            self.notebook_spawner.wait_on_visibility(driver, 30)
        except TimeoutException:
            return True
        return False


class JupyterHubNotebook:
    save = SiteElement(
        By.CSS_SELECTOR,
        'button[title="Save the notebook contents and create checkpoint"]',
    )

    @classmethod
    def save_notebook(self, driver):
        self.save.click(driver)


class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
