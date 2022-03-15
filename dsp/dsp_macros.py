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
    MY_SUBMISSIONS_LOAD
)


class WebPage:
    body_locator = By.CSS_SELECTOR, "body"


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

    # navigation_login = SiteElement(By.CSS_SELECTOR, "#signin-menu a")
    # signout_menu = SiteElement(By.ID, "signout-menu")
    # footer = SiteElement(By.CSS_SELECTOR, "footer")
    # footer_terms = SiteElement(By.CSS_SELECTOR, "footer a[href='/terms-of-use']")
    # footer_privacy = SiteElement(By.CSS_SELECTOR, "footer a[href='/privacy']")
    # footer_sitemap = SiteElement(By.CSS_SELECTOR, "footer a[href='/sitemap/']")
    # footer_twitter = SiteElement(
    #     By.CSS_SELECTOR, ".content.social ul li:nth-child(1) > a"
    # )
    # footer_facebook = SiteElement(
    #     By.CSS_SELECTOR, ".content.social ul li:nth-child(2) > a"
    # )
    # footer_youtube = SiteElement(
    #     By.CSS_SELECTOR, ".content.social ul li:nth-child(3) > a"
    # )
    # footer_github = SiteElement(
    #     By.CSS_SELECTOR, ".content.social ul li:nth-child(4) > a"
    # )
    # footer_linkedin = SiteElement(
    #     By.CSS_SELECTOR, ".content.social ul li:nth-child(5) > a"
    # )
    # footer_version = SiteElement(By.CSS_SELECTOR, ".content p b")
    # page_tip = SiteElement(By.CSS_SELECTOR, ".page-tip > .container > .row > div > p")
    # notifications = SiteElement(By.CSS_SELECTOR, "#notifications-dropdown > a")
    # notifications_clear = SiteElement(By.CSS_SELECTOR, "#btn-notifications-clear")

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

    # @classmethod
    # def to_login(self, driver):
    #     self.navigation_login.click(driver)

    # @classmethod
    # def logout(self, driver):
    #     self.profile_menu.click(driver)
    #     self.signout_menu.click(driver)

    # @classmethod
    # def clear_notifications(self, driver):
    #     self.notifications.click(driver)
    #     self.notifications_clear.click(driver)
    #     self.notifications.click(driver)
    

class MySubmissions(Dsp):
    orcid_login = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login")
    
    @classmethod
    def is_visible_orcid_login(self, driver):
        return self.orcid_login.is_visible(driver)

"""
THE CLASSES BELOW ARE FROM HYDROSHARE AND ARE HERE AS EXAMPLES WHILE WRITING DSP MACROS
"""
class Home(Dsp):
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

class Login(Dsp):
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


class Resource(Dsp):
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
    resource_file_container = SiteElement(By.CSS_SELECTOR, "#fb-files-container")
    new_folder_button = SiteElement(By.ID, "fb-create-folder")
    new_folder = SiteElement(
        By.CSS_SELECTOR, "#fb-file-operations-controls > span.fa-folder"
    )
    # folder_name_input = SiteElement(By.ID, "txtFolderNamer")
    folder_name_input = SiteElement(By.CSS_SELECTOR, "#create-folder-dialog input")
    save_folder = SiteElement(By.ID, "btn-create-folder")
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
    folder_zip = SiteElement(
        By.CSS_SELECTOR, '#right-click-menu > li[data-fb-action="zip"]'
    )
    folder_zip_confirm = SiteElement(By.ID, "btn-confirm-zip")
    unzip_here = SiteElement(By.ID, "btn-unzip")
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
    def get_resource_filenames(self, driver):
        file_count = self.resource_file_container.get_immediate_child_count(driver)
        resource_files = [
            self.resource_file(i).get_text(driver) for i in range(1, file_count + 1)
        ]
        return resource_files

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
    def create_folder(self, driver, foldername):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        self.new_folder_button.click(driver)
        self.folder_name_input.click(driver)
        self.folder_name_input.inject_text(driver, foldername)
        self.save_folder.click(driver)

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
    def unzip_folder_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        self.resource_file(index).right_click(driver)
        self.unzip_here.javascript_click(driver)

    @classmethod
    def zip_folder_by_index(self, driver, index):
        self.file_browser.scroll_to(driver)
        self.resource_file(index).right_click(driver)
        self.folder_zip.javascript_click(driver)
        self.folder_zip_confirm.click(driver)

    @classmethod
    def get_file_index_by_name(self, driver, filename):
        self.file_browser.scroll_to(driver)
        time.sleep(RESOURCE_LANDING_PAGE_LOAD)
        filenames = self.get_resource_filenames(driver)
        # other index functions in this class are not zero-based
        return filenames.index(filename) + 1

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


class API(Dsp):
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


class Profile(Dsp):
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


class NewResource(Dsp):
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


class Registration(Dsp):
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


class SiteMap(Dsp):
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


class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
