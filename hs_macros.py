import os

from dateutil import parser
from hs_elements import HomePage, AppsPage, DiscoverPage, ResourcePage
from modes import setup_mode

# Testing parameters
MODE_SELECTION = 'demo'
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)


class Home:
    def to_discover(self, driver):
        """ Navigate to the Discover page using the menu at the top
        of the home page
        """
        HomePage.to_discover.click(driver, SLEEP_TIME)

    def to_apps(self, driver):
        HomePage.to_apps.click(driver, SLEEP_TIME)


class Apps:
    def show_info(self, driver, num):
        AppsPage.info(num).click(driver, SLEEP_TIME)

    def count(self, driver):
        return AppsPage.container.get_immediate_child_count(driver)

    def to_resource(self, driver, num):
        AppsPage.resource(num).click(driver, SLEEP_TIME)

    def get_title(self, driver, num):
        return AppsPage.title(num).get_text(driver)


class Discover:
    def sort_order(self, driver, option):
        """ Set the sort order to {{option}} """
        DiscoverPage.sort_order.select_option_text(driver, option, SLEEP_TIME)

    def sort_direction(self, driver, option):
        """ Set the sort direction to {{option}} """
        DiscoverPage.sort_direction.select_option_text(driver, option, SLEEP_TIME)

    def to_resource(self, driver, title):
        """ Navigate to the {{title}} resource landing page by clicking
        on it within the table
        """
        DiscoverPage.to_resource(title).click(driver, SLEEP_TIME)

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

    def filters(self, driver, author=None, subject=None, resource_type=None,
                owner=None, variable=None, sample_medium=None, unit=None,
                availability=None):
        """ Use the filters on the left side of the Discover interface.
        Filters should include author(s) {{author}}, subject(s) {{subject}},
        resource type(s) {{resource_type}}, owner(s) {{owner}}, variables
        {{variable}}, sample medium(s) {{sample_medium}}, unit(s) {{unit}},
        and availability(s) {{availability}}
        """
        HomePage.to_discover.click(driver, SLEEP_TIME)
        if type(author) is list:
            for author_item in author:
                filter_el = DiscoverPage.filter_author(author_item)
                filter_el.click(driver, SLEEP_TIME)
        elif author is not None:
            filter_el = DiscoverPage.filter_author(author)
            filter_el.click(driver, SLEEP_TIME)
        if type(subject) is list:
            for subject_item in subject:
                filter_el = DiscoverPage.filter_subject(subject_item)
                filter_el.click(driver, SLEEP_TIME)
        elif subject is not None:
            filter_el = DiscoverPage.filter_subject(subject)
            filter_el.click(driver, SLEEP_TIME)
        if type(resource_type) is list:
            for resource_type_item in resource_type:
                filter_el = DiscoverPage.filter_resource_type(resource_type_item)
                filter_el.click(driver, SLEEP_TIME)
        elif resource_type is not None:
            filter_el = DiscoverPage.filter_resource_type(resource_type)
            filter_el.click(driver, SLEEP_TIME)
        if type(owner) is list:
            for owner_item in owner:
                filter_el = DiscoverPage.filter_owner(owner_item)
                filter_el.click(driver, SLEEP_TIME)
        elif owner is not None:
            filter_el = DiscoverPage.filter_owner(owner)
            filter_el.click(driver, SLEEP_TIME)
        if type(variable) is list:
            for variable_item in variable:
                filter_el = DiscoverPage.filter_variable(variable_item)
                filter_el.click(driver, SLEEP_TIME)
        elif variable is not None:
            filter_el = DiscoverPage.filter_variable(variable)
            filter_el.click(driver, SLEEP_TIME)
        if type(sample_medium) is list:
            for sample_medium_item in sample_medium:
                filter_el = DiscoverPage.filter_sample_medium(sample_medium_item)
                filter_el.click(driver, SLEEP_TIME)
        elif sample_medium is not None:
            filter_el = DiscoverPage.filter_sample_medium(sample_medium)
            filter_el.click(driver, SLEEP_TIME)
        if type(unit) is list:
            for unit_item in unit:
                filter_el = DiscoverPage.filter_unit(unit_item)
                filter_el.click(driver, SLEEP_TIME)
        elif unit is not None:
            filter_el = DiscoverPage.filter_unit(unit)
            filter_el.click(driver, SLEEP_TIME)
        if type(availability) is list:
            for availability_item in availability:
                filter_el = DiscoverPage.filter_availability(availability_item)
                filter_el.click(driver, SLEEP_TIME)
        elif availability is not None:
            filter_el = DiscoverPage.filter_availability(availability)
            filter_el.click(driver, SLEEP_TIME)


class Resource:
    def size_download(self, driver, BASE_URL):
        """ Check the size of the BagIt download """
        download_href = ResourcePage.bagit.get_href(driver, BASE_URL)
        os.system('wget -q {}'.format(download_href))
        download_file = download_href.split('/')[-1]
        file_size = os.stat(download_file).st_size
        os.system('rm {}'.format(download_file))
        return file_size


Home = Home()
Apps = Apps()
Discover = Discover()
Resource = Resource()
