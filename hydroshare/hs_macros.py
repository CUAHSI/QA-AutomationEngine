import os
import time

from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import TimeoutException
from dateutil import parser

from hs_elements import HomePage, AppsPage, DiscoverPage, ResourcePage, \
     HelpPage, AboutPage, APIPage, LoginPage, ProfilePage, GroupsPage, \
     GroupPage, NewGroupModal, MyResourcesPage, DashboardPage
from timing import HSAPI_GUI_RESPONSE, PROFILE_SAVE, HELP_DOCS_TREE_ANIMATIONS, \
     RESOURCE_CREATION, HOME_PAGE_SLIDER_ANIMATION, LABEL_CREATION, \
     HSAPI_RESPONSE_CODE


class Home:
    def to_home(self, driver):
        HomePage.to_home.click(driver)

    def to_my_resources(self, driver):
        HomePage.to_my_resources.click(driver)

    def to_discover(self, driver):
        HomePage.to_discover.click(driver)

    def to_apps(self, driver):
        HomePage.to_apps.click(driver)

    def to_help(self, driver):
        HomePage.to_help.click(driver)

    def to_about(self, driver):
        HomePage.to_about.click(driver)

    def to_collaborate(self, driver):
        HomePage.to_collaborate.click(driver)

    def login(self, driver, username, password):
        HomePage.to_login.click(driver)
        LoginPage.username.inject_text(driver, username)
        LoginPage.password.inject_text(driver, password)
        LoginPage.submit.click(driver)

    def to_profile(self, driver):
        HomePage.profile_image.click(driver)
        HomePage.profile_button.click(driver)

    def scroll_to_top(self, driver):
        HomePage.go_up.click(driver)

    def scroll_to_button(self, driver):
        HomePage.body.set_path(driver, Keys.CONTROL + Keys.ARROW_DOWN)

    def slider_right(self, driver):
        HomePage.scroll_slider_right.click(driver)
        time.sleep(HOME_PAGE_SLIDER_ANIMATION)

    def slider_left(self, driver):
        HomePage.scroll_slider_left.click(driver)
        time.sleep(HOME_PAGE_SLIDER_ANIMATION)

    def a_slider_is_active(self, driver):
        return HomePage.slider

    def slider_has_valid_img(self, driver, images):
        return HomePage.slider.get_attribute(driver, 'style') in images

    def to_site_map(self, driver):
        return HomePage.to_site_map.click(driver)

    def select_resource(self, driver, res):
        HomePage.select_resource(res).click(driver)

    def version(self, driver):
        return HomePage.version.get_text(driver).strip()


class Apps:
    def show_info(self, driver, num):
        AppsPage.info(num).click(driver)

    def count(self, driver):
        return AppsPage.container.get_immediate_child_count(driver)

    def to_resource(self, driver, num):
        AppsPage.resource(num).click(driver)

    def get_title(self, driver, num):
        return AppsPage.title(num).get_text(driver)


class Discover:
    def sort_order(self, driver, option):
        """ Set the sort order to {{option}} """
        DiscoverPage.sort_order.select_option_text(driver, option)

    def sort_direction(self, driver, option):
        """ Set the sort direction to {{option}} """
        DiscoverPage.sort_direction.select_option_text(driver, option)

    def to_resource(self, driver, title):
        """ Navigate to the {{title}} resource landing page by clicking
        on it within the table.  If the resource is not visible will switch to
        the next result page
        """
        resource_found = False
        while not resource_found:
            try:
                DiscoverPage.to_resource(title).click(driver)
                resource_found = True
            except TimeoutException:
                DiscoverPage.next_page.click(driver)

    def to_last_updated_profile(self, driver):
        DiscoverPage.last_updated_by.click(driver)

    def col_index(self, driver, col_name):
        """ Indentify the index for a discover page column, given the
        column name.  Indexes here start at one since the
        end application here is xpath, and those indexes are 1 based
        """
        num_cols = DiscoverPage.col_headers.get_child_count(driver)
        for i in range(1, num_cols+1):
            name_to_check = DiscoverPage.col_index(i).get_text(driver)
            if name_to_check == col_name:
                return i
        return 0

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
                if not self.check_sorting_single(driver, column_name,
                                                 ascend_or_descend, i, i+j):
                    all_pass = False
        return all_pass

    def check_sorting_single(self, driver, column_name, ascend_or_descend,
                             row_one, row_two):
        """ Confirm that two rows are sorted correctly relative to
        eachother
        """
        col_ind = self.col_index(driver, column_name)
        if column_name == 'Title':
            first_element = DiscoverPage.cell_strong_href(col_ind, row_one)
            second_element = DiscoverPage.cell_strong_href(col_ind, row_two)
            first_two_vals = [first_element.get_text(driver),
                              second_element.get_text(driver)]
        elif column_name == 'First Author':
            first_element = DiscoverPage.cell_href(col_ind, row_one)
            second_element = DiscoverPage.cell_href(col_ind, row_two)
            first_two_vals = [first_element.get_text(driver),
                              second_element.get_text(driver)]
        else:
            first_element = DiscoverPage.cell(col_ind, row_one)
            second_element = DiscoverPage.cell(col_ind, row_two)
            first_two_vals = [first_element.get_text(driver),
                              second_element.get_text(driver)]
        if ('Date' in column_name) or (column_name == 'Last Modified'):
            date_one = parser.parse(first_two_vals[0])
            date_two = parser.parse(first_two_vals[1])
            if ascend_or_descend == 'Descending':
                return date_one >= date_two
            elif ascend_or_descend == 'Ascending':
                return date_one <= date_two
        else:
            value_one, value_two = first_two_vals
            if ascend_or_descend == 'Descending':
                return value_one >= value_two
            elif ascend_or_descend == 'Ascending':
                return value_one <= value_two

    def show_all(self, driver):
        DiscoverPage.show_all.click(driver)

    def filters(self, driver, author=None, subject=None, resource_type=None,
                owner=None, variable=None, sample_medium=None, unit=None,
                availability=None, contributor=None, content_type=None):
        """ Use the filters on the left side of the Discover interface.
        Filters should include author(s) {{author}}, subject(s) {{subject}},
        resource type(s) {{resource_type}}, owner(s) {{owner}}, variables
        {{variable}}, sample medium(s) {{sample_medium}}, unit(s) {{unit}},
        and availability(s) {{availability}}
        """
        if type(author) is list:
            for author_item in author:
                filter_el = DiscoverPage.filter_author(author_item)
                filter_el.click(driver)
        elif author is not None:
            filter_el = DiscoverPage.filter_author(author)
            filter_el.click(driver)
        if type(contributor) is list:
            for contributor_item in contributor:
                filter_el = DiscoverPage.filter_contributor(contributor_item)
                filter_el.click(driver)
        elif contributor is not None:
            filter_el = DiscoverPage.filter_contributor(contributor)
            filter_el.click(driver)
        if type(content_type) is list:
            for content_item in content_type:
                filter_el = DiscoverPage.filter_contributor(content_item)
                filter_el.click(driver)
        elif content_type is not None:
            filter_el = DiscoverPage.filter_content_type(content_type)
            filter_el.click(driver)
        if type(subject) is list:
            for subject_item in subject:
                filter_el = DiscoverPage.filter_subject(subject_item)
                filter_el.click(driver)
        elif subject is not None:
            filter_el = DiscoverPage.filter_subject(subject)
            filter_el.click(driver)
        if type(resource_type) is list:
            for resource_type_item in resource_type:
                filter_el = DiscoverPage.filter_resource_type(resource_type_item)
                filter_el.click(driver)
        elif resource_type is not None:
            filter_el = DiscoverPage.filter_resource_type(resource_type)
            filter_el.click(driver)
        if type(owner) is list:
            for owner_item in owner:
                filter_el = DiscoverPage.filter_owner(owner_item)
                filter_el.click(driver)
        elif owner is not None:
            filter_el = DiscoverPage.filter_owner(owner)
            filter_el.click(driver)
        if type(variable) is list:
            for variable_item in variable:
                filter_el = DiscoverPage.filter_variable(variable_item)
                filter_el.click(driver)
        elif variable is not None:
            filter_el = DiscoverPage.filter_variable(variable)
            filter_el.click(driver)
        if type(sample_medium) is list:
            for sample_medium_item in sample_medium:
                filter_el = DiscoverPage.filter_sample_medium(sample_medium_item)
                filter_el.click(driver)
        elif sample_medium is not None:
            filter_el = DiscoverPage.filter_sample_medium(sample_medium)
            filter_el.click(driver)
        if type(unit) is list:
            for unit_item in unit:
                filter_el = DiscoverPage.filter_unit(unit_item)
                filter_el.click(driver)
        elif unit is not None:
            filter_el = DiscoverPage.filter_unit(unit)
            filter_el.click(driver)
        if type(availability) is list:
            for availability_item in availability:
                filter_el = DiscoverPage.filter_availability(availability_item)
                filter_el.click(driver)
        elif availability is not None:
            filter_el = DiscoverPage.filter_availability(availability)
            filter_el.click(driver)

    def legend_text(self, driver):
        DiscoverPage.legend.click(driver)
        labels = str(DiscoverPage.legend_labels.get_text(driver))
        resources = str(DiscoverPage.legend_resources.get_text(driver))
        return labels, resources

    def search(self, driver, text):
        DiscoverPage.search.inject_text(driver, text)
        DiscoverPage.search.submit(driver)

    def to_search_result_item(self, driver, col_ind, row_one):
        DiscoverPage.cell_href(col_ind, row_one).click(driver)

    def click_on_link(self, driver, how_to=None, learn_more=None):
        if how_to:
            DiscoverPage.how_to_cite.click(driver)
        elif learn_more:
            DiscoverPage.learn_more.click(driver)


class Resource:
    def size_download(self, driver, BASE_URL):
        """ Check the size of the BagIt download """
        download_href = ResourcePage.bagit.get_href(driver, BASE_URL)
        os.system('wget -q {}'.format(download_href))
        download_file = download_href.split('/')[-1]
        file_size = os.stat(download_file).st_size
        os.system('rm {}'.format(download_file))
        return file_size

    def open_with_jupyterhub(self, driver):
        ResourcePage.open_with.click(driver)
        ResourcePage.open_jupyterhub.click(driver)

    def get_title(self, driver):
        return ResourcePage.title.get_text(driver)


class Help:
    def open_core(self, driver, index):
        HelpPage.core_item(index).click(driver)

    def count_core(self, driver):
        return HelpPage.core_root.get_immediate_child_count(driver)

    def get_core_topic(self, driver, index):
        return HelpPage.core_item(index).get_text(driver)

    def to_core_breadcrumb(self, driver):
        HelpPage.core_breadcrumb.click(driver)

    def to_footer_terms(self, driver):
        HelpPage.footer_terms.click(driver)

    def to_footer_privacy(self, driver):
        HelpPage.footer_privacy.click(driver)

    def to_footer_sitemap(self, driver):
        HelpPage.footer_sitemap.click(driver)

    def get_title(self, driver):
        return HelpPage.title.get_text(driver)


class About:
    def toggle_tree(self, driver):
        AboutPage.tree_root.click(driver)
        time.sleep(HELP_DOCS_TREE_ANIMATIONS)

    def expand_tree_top(self, driver, item):
        item = item.replace(' ', '-').lower()
        AboutPage.tree_top(item).click(driver)

    def open_policy(self, driver, policy):
        policy = policy.replace(' ', '-').lower()
        AboutPage.tree_policy(policy).click(driver)

    def get_title(self, driver):
        return AboutPage.article_title.get_text(driver)


class API:
    def expand_hsapi(self, driver):
        APIPage.hsapi.click(driver)

    def endpoint_index(self, driver, path, method):
        num_endpoints = APIPage.endpoint_list.get_immediate_child_count(driver)
        for i in range(1, num_endpoints+1):
            check_path = APIPage.path_by_index(i).get_text(driver)
            check_method = APIPage.type_by_index(i).get_text(driver)
            if check_path == path and check_method == method:
                return i
        return 0

    def toggle_endpoint(self, driver, path, method):
        endpoint_ind = self.endpoint_index(driver, path, method)
        APIPage.path_by_index(endpoint_ind).click(driver)

    def set_resource_id(self, driver, path, method, resource_id):
        endpoint_ind = self.endpoint_index(driver, path, method)
        APIPage.parameter_by_index(endpoint_ind).inject_text(driver, resource_id)

    def submit(self, driver, path, method):
        endpoint_ind = self.endpoint_index(driver, path, method)
        APIPage.submit(endpoint_ind).click(driver)
        time.sleep(HSAPI_GUI_RESPONSE)

    def response_code(self, driver, path, method):
        time.sleep(HSAPI_RESPONSE_CODE)
        endpoint_ind = self.endpoint_index(driver, path, method)
        return APIPage.response_code(endpoint_ind).get_text(driver)


class Profile:
    def to_editor(self, driver):
        ProfilePage.edit.click(driver)

    def add_org(self, driver, org):
        ProfilePage.add_org.inject_text(driver, org)
        ProfilePage.add_org.inject_text(driver, Keys.ARROW_DOWN)
        ProfilePage.add_org.inject_text(driver, Keys.ENTER)

    def delete_org(self, driver, index):
        ProfilePage.delete_org(index).click(driver)

    def add_cv(self, driver, link):
        ProfilePage.add_cv.set_path(driver, link)

    def save(self, driver):
        ProfilePage.save.click(driver)
        time.sleep(PROFILE_SAVE)

    def add_photo(self, driver, link):
        ProfilePage.image_upload.set_path(driver, link)

    def remove_photo(self, driver):
        ProfilePage.delete_image.click(driver)
        ProfilePage.submit_delete_image.click(driver)

    def confirm_photo_uploaded(self, driver, contains):
        return contains in ProfilePage.image.get_style(driver)

    def view_cv(self, driver):
        ProfilePage.view_cv.click(driver)

    def delete_cv(self, driver):
        ProfilePage.delete_cv.click(driver)
        ProfilePage.confirm_delete_cv.click(driver)

    def view_contributions(self, driver):
        ProfilePage.contribution.click(driver)

    def view_contribution_type(self, driver, ind):
        ProfilePage.contribution_type(ind).javascript_click(driver)

    def get_resource_type_count(self, driver):
        contribution_types_breakdown = ProfilePage.contribution_types_breakdown
        return contribution_types_breakdown.get_immediate_child_count(driver)

    def get_contribution_type_count(self, driver, ind):
        type_count = ProfilePage.contribution_type_count(ind).get_text(driver)
        return int(type_count)


class Groups:
    def create_group(self, driver, name, purpose, about, privacy):
        GroupsPage.create_group.click(driver)
        NewGroupModal.name.inject_text(driver, name)
        NewGroupModal.purpose.inject_text(driver, purpose)
        NewGroupModal.about.inject_text(driver, about)
        if privacy.lower() == 'public':
            NewGroupModal.public.click(driver)
        elif privacy.lower() == 'discoverable':
            NewGroupModal.discoverable.click(driver)
        else:
            NewGroupModal.private.click(driver)
        NewGroupModal.submit.click(driver)


class Group:
    def check_title(self, driver):
        return GroupPage.name.get_text(driver)


class MyResources:
    def setup_new_resource_title(self, driver, title):
        MyResourcesPage.create_new.click(driver)
        MyResourcesPage.title.click(driver)
        MyResourcesPage.title.inject_text(driver, title)

    def get_resource_type_indexes(self, driver):
        MyResourcesPage.resource_type_selector.click(driver)
        resource_creation_list = MyResourcesPage.resource_creation_list
        count = resource_creation_list.get_immediate_child_count(driver)
        resource_type_indexes = []
        for i in range(1, count+1):
            el_class = MyResourcesPage.resource_creation_type(i).get_class(driver)
            if el_class not in ['dropdown-header', 'divider']:
                resource_type_indexes.append(i)
        MyResourcesPage.resource_type_selector.click(driver)
        return resource_type_indexes

    def select_resource_type(self, driver, index):
        MyResourcesPage.resource_type_selector.click(driver)
        MyResourcesPage.resource_creation_type(index).click(driver)

    def create_resource(self, driver, title):
        """ Creates new resource with provided title"""
        MyResourcesPage.create_new.click(driver)
        MyResourcesPage.title.click(driver)
        MyResourcesPage.title.inject_text(driver, title)
        MyResourcesPage.create_resource.scroll_to(driver)
        MyResourcesPage.create_resource.javascript_click(driver)
        time.sleep(RESOURCE_CREATION)

    def edit_this_resource(self, driver):
        MyResourcesPage.edit_resource.click(driver)

    def add_metadata(self, driver, name, value):
        MyResourcesPage.extend_metadata.click(driver)
        MyResourcesPage.add_new_entry.click(driver)
        MyResourcesPage.metadata_name.inject_text(driver, name)
        MyResourcesPage.metadata_value.inject_text(driver, value)
        MyResourcesPage.confirm_extend_metadata.click(driver)

    def search_resource_type(self, driver):
        MyResourcesPage.search_options.click(driver)

    def search_type(self, driver, option):
        MyResourcesPage.resource_type(option).click(driver)

    def search_author(self, driver, author):
        MyResourcesPage.search_author.inject_text(driver, author)

    def search_subject(self, driver, subject):
        MyResourcesPage.search_subject.inject_text(driver, subject)

    def clear_search(self, driver):
        MyResourcesPage.clear_search.click(driver)

    def clear_author_search(self, driver):
        MyResourcesPage.clear_author_search.click(driver)

    def clear_subject_search(self, driver):
        MyResourcesPage.clear_subject_search.click(driver)

    def read_searchbar(self, driver):
        return MyResourcesPage.search.get_value(driver)

    def create_label(self, driver, new_name):
        MyResourcesPage.label.click(driver)
        MyResourcesPage.create_label.click(driver)
        MyResourcesPage.new_label_name.inject_text(driver, new_name)
        MyResourcesPage.create_label_submit.click(driver)
        time.sleep(LABEL_CREATION)

    def toggle_label(self, driver, label):
        MyResourcesPage.add_label.click(driver)
        MyResourcesPage.label_name(label).click(driver)
        MyResourcesPage.add_label.click(driver)

    def check_label_applied(self, driver):
        return 'has-labels' in MyResourcesPage.add_label.get_class(driver)

    def delete_label(self, driver):
        MyResourcesPage.label.click(driver)
        MyResourcesPage.manage_labels.click(driver)
        MyResourcesPage.remove_label.click(driver)

    def legend_text(self, driver):
        MyResourcesPage.legend.click(driver)
        labels = str(MyResourcesPage.legend_labels.get_text(driver))
        resources = str(MyResourcesPage.legend_resources.get_text(driver))
        return labels, resources

    def exists_create_btn(self, driver):
        return 'disabled' not in MyResourcesPage.create_resource.get_class(driver)

    def exists_cancel_btn(self, driver):
        return 'disabled' not in MyResourcesPage.cancel_resource.get_class(driver)

class Dashboard:
    def toggle_get_started(self, driver): 
        DashboardPage.get_started_toggle.click(driver)

    def is_get_started_showing(self, driver):
        return DashboardPage.get_started_toggle.get_text(driver) == "Hide Getting Started"

Home = Home()
Apps = Apps()
Discover = Discover()
Resource = Resource()
Help = Help()
About = About()
API = API()
Profile = Profile()
Groups = Groups()
Group = Group()
MyResources = MyResources()
Dashboard = Dashboard()
