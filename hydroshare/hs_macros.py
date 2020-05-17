import json
import os
import requests
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dateutil import parser
from urllib.request import urlretrieve, urlopen

from cuahsi_base.site_element import SiteElement, SiteElementsCollection
from cuahsi_base.utils import External, TestSystem

from timing import (
    HSAPI_GUI_RESPONSE,
    PROFILE_SAVE,
    HELP_DOCS_TREE_ANIMATIONS,
    RESOURCE_CREATION,
    HOME_PAGE_SLIDER_ANIMATION,
    LABEL_CREATION,
    DISCOVER_TABLE_UPDATE,
    EXTERNAL_PAGE_LOAD,
)


class Hydroshare:
    navigation_landing_page = SiteElement(By.ID, "img-brand-logo")
    navigation_home = SiteElement(By.ID, "dropdown-menu-home")
    navigation_my_resources = SiteElement(By.ID, "dropdown-menu-my-resources")
    navigation_discover = SiteElement(By.ID, "dropdown-menu-search")
    navigation_collaborate = SiteElement(By.CSS_SELECTOR, "#dropdown-menu-collaborate a")
    navigation_apps = SiteElement(By.ID, "dropdown-menu-https:--www.hydroshare.org-apps-")
    navigation_help = SiteElement(
        By.CSS_SELECTOR, 'a[href="{}"]'.format("http://help.hydroshare.org")
    )
    navigation_login = SiteElement(By.CSS_SELECTOR, "#signin-menu a")
    profile_button = SiteElement(
        By.CSS_SELECTOR, ".account div.dropdown-footer .btn.btn-primary"
    )
    profile_menu = SiteElement(By.ID, "profile-menu")
    sign_out = SiteElement(By.ID, "signout-menu")
    creation_resource = SiteElement(By.ID, "select-resource-type")
    footer = SiteElement(By.CSS_SELECTOR, "footer")
    footer_terms = SiteElement(By.CSS_SELECTOR, "footer a[href='/terms-of-use']")
    footer_privacy = SiteElement(By.CSS_SELECTOR, "footer a[href='/privacy']")
    footer_sitemap = SiteElement(By.CSS_SELECTOR, "footer a[href='/sitemap/']")
    twitter = SiteElement(By.CSS_SELECTOR, ".content.social ul li:nth-child(1) > a")
    facebook = SiteElement(By.CSS_SELECTOR, ".content.social ul li:nth-child(2) > a")
    youtube = SiteElement(By.CSS_SELECTOR, ".content.social ul li:nth-child(3) > a")
    github = SiteElement(By.CSS_SELECTOR, ".content.social ul li:nth-child(4) > a")
    linkedin = SiteElement(By.CSS_SELECTOR, ".content.social ul li:nth-child(5) > a")
    version = SiteElement(By.CSS_SELECTOR, ".content p b")
    support_email = SiteElement(By.CSS_SELECTOR, 'a[href="mailto:help@cuahsi.org"]')
    page_tip = SiteElement(By.CSS_SELECTOR, ".page-tip > .container > .row > div > p")

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
        self.sign_out.click(driver)

    @classmethod
    def resource_type(self, resource_type):
        return SiteElement(By.CSS_SELECTOR, 'a[data-value="{}"]'.format(resource_type))

    @classmethod
    def create_resource(self, driver, type):
        self.creation_resource.click(driver)
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
            "facebook": self.facebook,
            "twitter": self.twitter,
            "youtube": self.youtube,
            "github": self.github,
            "linkedin": self.linkedin,
        }
        return social_links[social].get_attribute(driver, "href")

    @classmethod
    def get_version(self, driver):
        return self.version.get_text(driver).strip()

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


class LandingPage(Hydroshare):
    hero = SiteElement(By.CSS_SELECTOR, "div.item.parallax-window.active")
    hero_right = SiteElement(By.CSS_SELECTOR, ".glyphicon-chevron-right")
    hero_left = SiteElement(By.CSS_SELECTOR, ".glyphicon-chevron-left")
    navigation_top = SiteElement(By.CSS_SELECTOR, ".scrolltotop")
    navigation_registration = SiteElement(By.CSS_SELECTOR, "a.btn-signup")

    @classmethod
    def to_registration(self, driver):
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
    body = SiteElement(By.XPATH, "//body[1]")
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
    def app(self, index):
        return SiteElement(
            By.CSS_SELECTOR, ".app-text-block-header:nth-of-type({})".format(index)
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
    def to_app(self, driver, index):
        self.app(index).click(driver)


class Login(Hydroshare):
    username = SiteElement(By.ID, "id_username")
    password = SiteElement(By.ID, "id_password")
    submit = SiteElement(By.CSS_SELECTOR, "input.btn.btn-primary[type='submit']")
    error = SiteElement(By.CSS_SELECTOR, ".alert-danger")
    notification = SiteElement(
        By.CSS_SELECTOR, 'div[class="page-tip animated slideInDown"] p'
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
    last_updated_by = SiteElement(
        By.XPATH, '//th[text() = "Last updated:"]/following-sibling::td/a'
    )
    search = SiteElement(By.ID, "id_q")
    show_all_btn = SiteElement(By.ID, "btn-show-all")
    user_modal_to_profile = SiteElement(
        By.CSS_SELECTOR,
        ".open > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) "
        "> div:nth-child(2) > h4:nth-child(1) > a:nth-child(1)",
    )

    @classmethod
    def resource_link(self, title):
        return SiteElement(By.XPATH, "//a[contains(text(), '{}')]".format(title))

    @classmethod
    def col_header(self, col_index):
        """ Return the column header element, given the index """
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
            "td:nth-of-type({})".format(row, col),
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
        return SiteElement(By.ID, "creator-{}".format(author))

    @classmethod
    def filter_contributor(self, author):
        return SiteElement(By.ID, "contributor-{}".format(author))

    @classmethod
    def filter_content_type(self, content_type):
        return SiteElement(By.ID, "content_type-{}".format(content_type))

    @classmethod
    def filter_subject(self, subject):
        return SiteElement(By.ID, "subject-{}".format(subject))

    @classmethod
    def filter_resource_type(self, resource_type):
        return SiteElement(By.ID, "content_type-{}".format(resource_type))

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
        return SiteElement(By.ID, "availability-{}".format(availability))

    @classmethod
    def set_sort_order(self, driver, option):
        """ Set the sort order to {{option}} """
        self.sort_order.select_option_text(driver, option)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def set_sort_direction(self, driver, option):
        """ Set the sort direction to {{option}} """
        self.sort_direction.select_option_text(driver, option)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def to_resource(self, driver, title):
        """ Navigate to the {{title}} resource landing page by clicking
        on it within the table.  If the resource is not visible will switch to
        the next result page
        """
        resource_found = False
        while not resource_found:
            try:
                self.next_page.scroll_to(driver)
                self.resource_link(title).click(driver)
                resource_found = True
            except TimeoutException:
                self.next_page.scroll_to(driver)
                self.next_page.javascript_click(driver)

    @classmethod
    def to_last_updated_profile(self, driver):
        self.last_updated_by.click(driver)
        self.user_modal_to_profile.click(driver)

    @classmethod
    def col_index(self, driver, col_name):
        """ Indentify the index for a discover page column, given the
        column name.  Indexes here start at one since the
        end application here is xpath, and those indexes are 1 based
        """
        num_cols = self.col_headers.get_child_count(driver)
        for i in range(1, num_cols + 1):
            name_to_check = self.col_header(i).get_text(driver)
            if name_to_check == col_name:
                return i
        return 0

    @classmethod
    def check_sorting_multi(self, driver, column_name, ascend_or_descend):
        """ Check discover page rows are sorted correctly.  The automated
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
        """ Confirm that two rows are sorted correctly relative to
        eachother
        """
        col_ind = self.col_index(driver, column_name)
        if column_name == "Title":
            first_element = self.cell_strong_href(col_ind, row_one)
            second_element = self.cell_strong_href(col_ind, row_two)
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
        """ Use the filters on the left side of the Discover interface.
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
        self.search.inject_text(driver, text)
        self.search.submit(driver)
        time.sleep(DISCOVER_TABLE_UPDATE)

    @classmethod
    def to_search_result_item(self, driver, col_ind, row_one):
        self.cell_href(col_ind, row_one).click(driver)

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
    def get_bagit_size(self, driver, BASE_URL):
        """ Check the size of the BagIt download """
        download_href = self.bagit.get_href(driver, BASE_URL)
        r = requests.get(download_href)
        return len(r.content)

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
    core_root = SiteElement(By.CSS_SELECTOR, "#content div.row")

    @classmethod
    def core_item(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#content "
            "div.row div:nth-of-type({}) "
            "div.topic-name div".format(index),
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
    def update_about(self, driver, description, country, province):
        self.description.click(driver)
        self.description.clear_all_text(driver)
        self.description.inject_text(driver, description)
        self.country.select_option_text(driver, country)
        self.province.click(driver)
        self.province.clear_all_text(driver)
        self.province.inject_text(driver, province)


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


class JupyterHub:
    login = SiteElement(By.CSS_SELECTOR, "#login-main > div > a")
    authorize = SiteElement(By.CSS_SELECTOR, 'input[value="Authorize"]')
    scientific_spawner = SiteElement(By.ID, "profile-item-1")
    spawn = SiteElement(By.CSS_SELECTOR, 'input[value="Spawn"]')
    sort_name = SiteElement(By.ID, "sort-name")

    def to_hs_login(self, driver):
        self.login.click(driver)

    def authorize_jupyterhub(self, driver):
        self.authorize.javascript_click(driver)

    def select_scientific_spawner(self, driver):
        self.scientific_spawner.click(driver)
        self.spawn.click(driver)

    def sort_notebooks_by_name(self, driver):
        JupyterHubNotebooks.sort_name.click(driver)
