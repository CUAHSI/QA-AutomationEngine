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

    # login
    orcid_login_modal = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login")
    orcid_login_continue = SiteElement(By.CSS_SELECTOR, ".v-dialog .cz-login button.primary")

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

    @classmethod
    def is_visible_orcid_modal(self, driver):
        return self.orcid_login_modal.is_visible(driver)
    
    @classmethod
    def to_orcid_window(self, driver):
        num_windows_now = len(driver.window_handles)
        self.orcid_login_continue.click(driver)
        External.switch_new_page(driver, num_windows_now, OrcidWindow.username)

class OrcidWindow(WebPage):
    username = SiteElement(By.ID, "username")

class MySubmissions(Dsp):
    # TODO: tests for my_submissions
    pass


class SubmitLandingPage(Dsp):
    hydroshare_repo = SiteElement(By.CSS_SELECTOR, 'div.repositories img[alt="HydroShare"]')

    @classmethod
    def to_hydroshare_repo(self, driver):
        self.hydroshare_repo.click(driver)


class SubmitHydroshare(Dsp):
    pass


class Utilities:
    run_test = SiteElement(By.ID, "run-test")
    confirm_test = SiteElement(By.ID, "view39")

    @classmethod
    def run_speed_test(self, driver):
        self.run_test.click(driver)
        self.confirm_test.click(driver)
