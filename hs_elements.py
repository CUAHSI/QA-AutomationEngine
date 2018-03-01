from site_element import SiteElement

class HomePage:
    def __init__(self):
        self.discover_tab = SiteElement('li', el_id='dropdown-menu-search')

    def goto_discover(self, driver, SLEEP_TIME):
        self.discover_tab.click(driver, SLEEP_TIME)
        
class DiscoverPage:
    def __init__(self):
        self.start_date = SiteElement('input', el_id='id_start_date')
        self.end_date = SiteElement('input', el_id='id_end_date')
        self.map_tab = SiteElement('a', el_href='map-view')
        self.map_search = SiteElement('input', el_id='geocoder-address')
        self.map_submit = SiteElement('a', el_id='geocoder-submit')
        self.list_tab = SiteElement('a', el_content='List')
        self.filter_iutah_subject = SiteElement('input', el_id='subjects-iUTAH')
        self.filter_generic_resource = SiteElement('input', el_id='resource_type-Generic')
        self.filter_is_discoverable = SiteElement('input', el_id='discoverable-true')
        self.filter_is_public = SiteElement('input', el_id='public-true')
        self.beaver_divide = SiteElement('a', el_content='Beaver Divide Air Temperature')
        self.sort_order = SiteElement('select', el_id='id_sort_order')
        self.sort_direction = SiteElement('select', el_id='id_sort_direction')
        self.header_row = SiteElement('table', el_id='items-discovered',
                                      el_recursive=[SiteElement('thead'),
                                                    SiteElement('tr')])

    def discovered_column_ind(self, column_ind):
        """ Return the column header element, given the index """
        return SiteElement('table', el_id='items-discovered',
                           el_recursive=[SiteElement('thead'),
                                         SiteElement('tr'),
                                         SiteElement('th[' + str(column_ind) + ']')])
        
    def discovered_field(self, column_num, row_num):
        """ Return the cell in the discover table, given row and column
        indicies
        """
        return SiteElement('table', el_id='items-discovered',
                           el_recursive=[SiteElement('tbody'),
                                         SiteElement('tr[' + str(row_num) + ']'),
                                         SiteElement('td[' + str(column_num) + ']')])

    def discovered_field_href(self, column_num, row_num):
        """ Return the cell in the discover table, given row and column
        indicies.  Builds on discover_field method, but enables use for
        hyperlinked fields.
        """
        return SiteElement('table', el_id='items-discovered',
                           el_recursive=[SiteElement('tbody'),
                                         SiteElement('tr[' + str(row_num) + ']'),
                                         SiteElement('td[' + str(column_num) + ']'),
                                         SiteElement('a')])
                                         
    def discovered_field_strong_href(self, column_num, row_num):
        """ Return the cell in the discover table, given row and column
        indicies.  Builds on discover_field method, but enables use for
        bolded and hyperlinked fields.
        """
        return SiteElement('table', el_id='items-discovered',
                           el_recursive=[SiteElement('tbody'),
                                         SiteElement('tr[' + str(row_num) + ']'),
                                         SiteElement('td[' + str(column_num) + ']'),
                                         SiteElement('strong'),
                                         SiteElement('a')])
                                         
                           
    def open_resource(self, resource_title):
        return SiteElement('a', el_content=resource_title)

    def filter_author(self, author):
        return SiteElement('input', el_id='creators-' + author)
        
    def filter_subject(self, subject):
        return SiteElement('input', el_id='subjects-' + subject)

    def filter_resource_type(self, resource_type):
        return SiteElement('input', el_id='resource_type-' + resource_type)

    def filter_owner(self, owner):
        return SiteElement('input', el_id='owners_names-' + owner)

    def filter_variable(self, variable):
        return SiteElement('input', el_id='variable_names-' + variable)

    def filter_sample_medium(self, sample_medium):
        return SiteElement('input', el_id='sample_mediums-' + sample_medium)

    def filter_unit(self, unit):
        return SiteElement('input', el_id='units_names-' + unit)

    def filter_availability(self, availability):
        return SiteElement('input', el_id=availability + '-true')

class ResourceLandingPage:
    def __init__(self):
        self.download_bagit = SiteElement('a', el_id='btn-download-all', el_content='Download All Content as Zipped BagIt Archive')

HomePage = HomePage()
DiscoverPage = DiscoverPage()
ResourceLandingPage = ResourceLandingPage()

