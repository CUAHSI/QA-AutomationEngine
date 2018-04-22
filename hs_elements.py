from selenium.webdriver.common.by import By

from site_element import SiteElement


class HomePage:
    def __init__(self):
        self.to_discover = SiteElement(By.ID, 'dropdown-menu-search')
        self.to_apps = \
            SiteElement(By.ID,
                        'dropdown-menu-https:--www.hydroshare.org-apps-')
        self.to_help = SiteElement(By.ID,
                                   'dropdown-menu-http:--help.hydroshare.org')
        self.to_about = SiteElement(By.ID,
                                    'dropdown-menu-https:--help.hydroshare.org' +
                                    '-about-hydroshare-')


class AppsPage:
    def __init__(self):
        self.container = \
            SiteElement(*self.apps_container_locator)

    def info(self, num):
        return SiteElement(By.CSS_SELECTOR,
                           "div.container.apps-container div.row "
                           "div:nth-of-type({}) "
                           "a.app-info-toggle".format(num))

    def resource(self, num):
        return SiteElement(By.CSS_SELECTOR,
                           "div.container.apps-container div.row "
                           "div:nth-of-type({}) "
                           "p.app-description a".format(num))

    def title(self, num):
        return SiteElement(By.CSS_SELECTOR,
                           "div.container.apps-container "
                           "div.row div:nth-of-type({}) h3".format(num))

    @property
    def apps_container_locator(self):
        return By.CSS_SELECTOR, "div.container.apps-container div.row"


class DiscoverPage:
    def __init__(self):
        self.start_date = SiteElement(By.ID, 'id_start_date')
        self.end_date = SiteElement(By.ID, 'id_end_date')
        self.map_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#map-view"]')
        self.map_search = SiteElement(By.ID, 'geocoder-address')
        self.map_submit = SiteElement(By.ID, 'geocoder-submit')
        self.list_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#list-view"]')
        self.sort_order = SiteElement(By.ID, 'id_sort_order')
        self.sort_direction = SiteElement(By.ID, 'id_sort_direction')
        self.col_headers = SiteElement(By.CSS_SELECTOR,
                                       '#items-discovered thead tr')

    def to_resource(self, title):
        return SiteElement(By.XPATH,
                           "//a[contains(text(), '{}')]".format(title))

    def col_index(self, col_index):
        """ Return the column header element, given the index """
        return SiteElement(By.CSS_SELECTOR,
                           '#items-discovered thead tr '
                           'th:nth-of-type({})'.format(col_index))

    def cell(self, col, row):
        """
        Return the cell in the discover table, given row and column indicies
        """
        return SiteElement(By.CSS_SELECTOR,
                           '#items-discovered tbody tr:nth-of-type({}) '
                           'td:nth-of-type({})'.format(row, col))

    def cell_href(self, col, row):
        """
        Return the cell's hyperlink in the discover table, given row and column
        indicies.
        """
        return SiteElement(By.CSS_SELECTOR,
                           '#items-discovered tbody tr:nth-of-type({}) '
                           'td:nth-of-type({}) a'.format(row, col))

    def cell_strong_href(self, col, row):
        """
        Return the cell's bolded hyperlink in the discover table,
        given row and column indicies.
        """
        return SiteElement(By.CSS_SELECTOR,
                           '#items-discovered tbody tr:nth-of-type({}) '
                           'td:nth-of-type({}) strong a'.format(row, col))

    def filter_author(self, author):
        return SiteElement(By.ID, 'creator-{}'.format(author))

    def filter_subject(self, subject):
        return SiteElement(By.ID, 'subject-{}'.format(subject))

    def filter_resource_type(self, resource_type):
        return SiteElement(By.ID, 'resource_type-{}'.format(resource_type))

    def filter_owner(self, owner):
        return SiteElement(By.ID, 'owner_names-{}'.format(owner))

    def filter_variable(self, variable):
        return SiteElement(By.ID, 'variable_name-{}'.format(variable))

    def filter_sample_medium(self, sample_medium):
        return SiteElement(By.ID, 'sample_medium-{}'.format(sample_medium))

    def filter_unit(self, unit):
        return SiteElement(By.ID, 'units_name-{}'.format(unit))

    def filter_availability(self, availability):
        return SiteElement(By.ID, 'availability-{}'.format(availability))


class ResourcePage:
    def __init__(self):
        self.bagit = SiteElement(By.ID, 'btn-download-all')


class HelpPage:
    def __init__(self):
        self.core_root = SiteElement(By.CSS_SELECTOR, '#content div.row')
        self.core_breadcrumb = SiteElement(By.ID, 'breadcrumb-menu-home')

    def core_item(self, index):
        return SiteElement(By.CSS_SELECTOR, '#content '
                           'div.row div:nth-of-type({}) '
                           'div.topic-name div'.format(index))


class AboutPage:
    def __init__(self):
        self.tree_root = SiteElement(By.CSS_SELECTOR,
                                     '#tree-menu-about-hydroshare '
                                     'div.tree-menu-item i')
        self.article_title = SiteElement(By.CSS_SELECTOR, 'h1.page-title')

    def tree_top(self, item):
        return SiteElement(By.CSS_SELECTOR,
                           '#tree-menu-about-hydroshare '
                           '#tree-menu-about-hydroshare-{} '
                           'div.tree-menu-item i'.format(item))

    def tree_policy(self, item):
        return SiteElement(By.CSS_SELECTOR,
                           '#tree-menu-about-hydroshare '
                           '#tree-menu-about-hydroshare-policies-{} '
                           'div.tree-menu-item a'.format(item))


class APIPage:
    def __init__(self):
        self.hsapi = SiteElement(By.ID, 'endpointListTogger_hsapi')
        self.endpoint_list = SiteElement(By.ID, 'hsapi_endpoint_list')

    def path_by_index(self, index):
        return SiteElement(By.CSS_SELECTOR,
                           '#hsapi_endpoint_list '
                           'li:nth-of-type({}) '
                           'span.path a'.format(index))

    def type_by_index(self, index):
        return SiteElement(By.CSS_SELECTOR,
                           '#hsapi_endpoint_list '
                           'li:nth-of-type({}) '
                           'span.http_method a'.format(index))

    def parameter_by_index(self, index):
        return SiteElement(By.CSS_SELECTOR,
                           '#hsapi_endpoint_list '
                           'li:nth-of-type({}) '
                           'tbody.operation-params '
                           'input.parameter.required'.format(index))

    def submit(self, index):
        return SiteElement(By.CSS_SELECTOR,
                           '#hsapi_endpoint_list '
                           'li:nth-of-type({}) '
                           'input.submit'.format(index))

    def response_code(self, index):
        return SiteElement(By.CSS_SELECTOR,
                           '#hsapi_endpoint_list '
                           'li:nth-of-type({}) '
                           'div.block.response_code pre'.format(index))


HomePage = HomePage()
AppsPage = AppsPage()
DiscoverPage = DiscoverPage()
ResourcePage = ResourcePage()
HelpPage = HelpPage()
AboutPage = AboutPage()
APIPage = APIPage()
