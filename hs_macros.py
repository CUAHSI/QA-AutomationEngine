import sys
import os
from dateutil import parser
from hs_elements import *
from modes import setup_mode

# Testing parameters
MODE_SELECTION = 'demo'
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)

class ResourceLanding:
    """ Individual resource info/download page macros """
    def download_size(self, driver, BASE_URL):
        download_href = ResourceLandingPage.download_bagit.get_href(driver, BASE_URL)
        os.system('wget ' + download_href)
        download_file = download_href.split('/')[-1]
        file_size = os.stat(download_file).st_size
        return file_size

class Discover:
    """ Discover tool macros """
    def goto(self, driver):
        HomePage.goto_discover(driver, SLEEP_TIME)
        
    def sort_order(self, driver, option):
        DiscoverPage.sort_order.select_option_text(driver, option, SLEEP_TIME)

    def sort_direction(self, driver, option):
        DiscoverPage.sort_direction.select_option_text(driver, option, SLEEP_TIME)
    
    def open_resource(self, driver, resource_title):
        DiscoverPage.open_resource(resource_title).click(driver, SLEEP_TIME)

    def discovered_column_ind(self, driver, column_name):
        """ Identifies the index for a discover page column, given the 
        column name.  Indexes here start at one since the
        end application here is xpath, and those indexes are 1 based
        """
        num_cols = DiscoverPage.header_row.get_child_count(driver)
        for i in range(1, num_cols+1):
            if DiscoverPage.discovered_column_ind(i).get_text(driver) == column_name:
                return i
        return 0    

    def check_sorting(self, driver, column_name, ascend_or_descend):
        """ Checks discover page rows are sorted correctly by checking each
        of the first eight rows against the rows that are 1, 2, and 3
        positions down, relative to the base row.  So total of 24 checks.
        """
        first_n_rows_to_check = 8
        all_pass = True
        for i in range(1, first_n_rows_to_check):
            for j in range(1, 4):
                if not self.check_sorting_single(driver, column_name,
                                                 ascend_or_descend, i, i+j):
                    all_pass = False
        return all_pass
    
    def check_sorting_single(self, driver, column_name, ascend_or_descend, row_one, row_two):
        """ Confirms that two rows are sorted correctly relative
        to eachother
        """
        col_ind = self.discovered_column_ind(driver, column_name)
        if column_name == 'Title':
            first_two_vals = [DiscoverPage.discovered_field_strong_href(col_ind, row_one).get_text(driver),
                              DiscoverPage.discovered_field_strong_href(col_ind, row_two).get_text(driver)]
        elif column_name == 'First Author':
            first_two_vals = [DiscoverPage.discovered_field_href(col_ind, row_one).get_text(driver),
                              DiscoverPage.discovered_field_href(col_ind, row_two).get_text(driver)]
        else:
            first_two_vals = [DiscoverPage.discovered_field(col_ind, row_one).get_text(driver),
                              DiscoverPage.discovered_field(col_ind, row_two).get_text(driver)]
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
        
    def discover_resources(self, driver, author=None, subject=None,
                           resource_type=None, owner=None, variable=None,
                           sample_medium=None, unit=None, availability=None):
        HomePage.goto_discover(driver, SLEEP_TIME)
        if type(author) is list:
            for author_item in author:
                DiscoverPage.filter_author(author_item).click(driver, SLEEP_TIME)
        elif author is not None:
            DiscoverPage.filter_author(author).click(driver, SLEEP_TIME)
        if type(subject) is list:
            for subject_item in subject:
                DiscoverPage.filter_subject(subject_item).click(driver, SLEEP_TIME)
        elif subject is not None:
            DiscoverPage.filter_subject(subject).click(driver, SLEEP_TIME)
        if type(resource_type) is list:
            for resource_type_item in resource_type:
                DiscoverPage.filter_resource_type(resource_type_item).click(driver, SLEEP_TIME)
        elif resource_type is not None:
            DiscoverPage.filter_resource_type(resource_type).click(driver, SLEEP_TIME)
        if type(owner) is list:
            for owner_item in owner:
                DiscoverPage.filter_owner(owner_item).click(driver, SLEEP_TIME)
        elif owner is not None:
            DiscoverPage.filter_owner(owner).click(driver, SLEEP_TIME)
        if type(variable) is list:
            for variable_item in variable:
                DiscoverPage.filter_variable(variable_item).click(driver, SLEEP_TIME)
        elif variable is not None:
            DiscoverPage.filter_variable(variable).click(driver, SLEEP_TIME)
        if type(sample_medium) is list:
            for sample_medium_item in sample_medium:
                DiscoverPage.filter_sample_medium(sample_medium_item).click(driver, SLEEP_TIME)
        elif sample_medium is not None:
            DiscoverPage.filter_sample_medium(sample_medium).click(driver, SLEEP_TIME)
        if type(unit) is list:
            for unit_item in unit:
                DiscoverPage.filter_unit(unit_item).click(driver, SLEEP_TIME)
        elif unit is not None:
            DiscoverPage.filter_unit(unit).click(driver, SLEEP_TIME)
        if type(availability) is list:
            for availability_item in availability:
                DiscoverPage.filter_availability(availability_item).click(driver, SLEEP_TIME)
        elif availability is not None:
            DiscoverPage.filter_availability(availability).click(driver, SLEEP_TIME)
    
ResourceLanding = ResourceLanding()
Discover = Discover()
