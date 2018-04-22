""" This module contains the definitions for site element locations.  These site
element locations can be defined in through a number of mechanisms, as further
detailed in the SiteElement class
"""
from selenium.webdriver.common.by import By

from site_element import SiteElement


class SearchPage:
    def __init__(self):
        self.workspace = SiteElement(By.ID, 'tabbedDataMgrTab')
        self.map_area = SiteElement(By.ID, 'map-canvas')
        self.zoom_in = SiteElement(By.CSS_SELECTOR,
                                   'div.gmnoprint.gm-bundled-control '
                                   'div div button:nth-of-type(1)')
        self.search = SiteElement(By.ID, 'btnSearchNow')
        self.reset = SiteElement(By.ID, 'btnSetDefaults')
        self.map_filter = SiteElement(By.ID, 'btnSearchSummary')
        self.map_search = SiteElement(By.ID, 'pac-input')
        self.services = SiteElement(By.ID, 'btnSelectDataServices')
        self.keywords = SiteElement(By.ID, 'btnSelectKeywords')
        self.advanced = SiteElement(By.ID, 'btnAdvancedSearch')
        self.results_count = SiteElement(By.ID, 'timeseriesFoundOrFilteredCount')
        self.date_filter = SiteElement(By.ID, 'optionsDatesRange')
        self.date_start = SiteElement(By.ID, 'startDateModal')
        self.date_end = SiteElement(By.ID, 'endDateModal')
        self.date_save = SiteElement(By.ID, 'btnDateRangeModalSave')
        self.layers = SiteElement(By.ID, 'Layer Control')
        self.legend_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#legend"]')
        self.legend_img = SiteElement(By.ID, 'nlcdColorClassUpdate')
        self.search_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#search"]')
        self.about = SiteElement(By.ID, 'ddAbout')
        self.quickstart = SiteElement(By.ID, 'quickStartModalTab')
        self.zendesk = SiteElement(By.ID, 'launcher')

    def layer(self, name):
        return SiteElement(By.XPATH, '//label[contains(text(), "{}")]'.format(name))

    def random_map_marker(self, marker_size):
        return SiteElement(By.CSS_SELECTOR, 'div.GblueLabel{}'.format(marker_size))

    @property
    def search_progress_locator(self):
        return By.ID, 'pageloaddiv'

    @property
    def modal_fade_locator(self):
        return By.CSS_SELECTOR, 'div.modal-backdrop.fade'


class MarkerModal:
    def __init__(self):
        self.action = SiteElement(By.ID, 'ddActionsMM')
        self.to_workspace = SiteElement(By.ID, 'anchorAddSelectionsToWorkspaceMM')
        self.workspace = SiteElement(By.ID, 'tableModal-DataMgr')
        self.table_count = SiteElement(By.CSS_SELECTOR,
                                       'select[name="tblMapMarker_length"]')

    def cell(self, row, col):
        return SiteElement(By.CSS_SELECTOR,
                           '#tblMapMarker tbody tr:nth-of-type({}) '
                           'td:nth-of-type({}) div'.format(row, col))

    def sort(self, sort_by):
        return SiteElement(By.XPATH,
                           '//div[@id="tblMapMarker_wrapper"]//'
                           'th[contains(text(), "{}")]'.format(sort_by))

    def cell_last_row(self, col):
        return SiteElement(By.CSS_SELECTOR,
                           '#tblMapMarker tbody tr:last-of-type '
                           'td:nth-of-type({}) div'.format(col))


class ServicesModal:
    def __init__(self):
        self.sort_org = SiteElement(By.XPATH,
                                    '//thead//th[contains(text(), "Organization")]')
        self.save = SiteElement(By.ID, 'btnServicesModalSave')
        self.search = SiteElement(By.ID, 'btnServicesModalSearch')
        self.table_count = SiteElement(By.CSS_SELECTOR,
                                       'select[name="tblDataServices_length"]')

    def select_org(self, org):
        return SiteElement(By.XPATH,
                           '//table[@id="tblDataServices"]/tbody/'
                           'tr/td[contains(text(), "{}")]'.format(org))

    def select_title(self, service_title):
        return SiteElement(By.XPATH,
                           '//table[@id="tblDataServices"]/tbody/tr/td[2]/'
                           'a[contains(text(), "{}")]'
                           '/../../td[2]'.format(service_title))


class KeywordsModal:
    def __init__(self):
        self.full_list = SiteElement(By.CSS_SELECTOR, 'a[href="#tab2"]')
        self.search = SiteElement(By.ID, 'btnFullKeywordModalSearch')

    def full_list_checkbox(self, item_name):
        return SiteElement(By.XPATH,
                           '//div[@id="keywordTree"]/ul//'
                           'span[contains(text(), "{}")]/../'
                           'span[@class="fancytree-checkbox"]'.format(item_name))

    def full_list_expand(self, item_name):
        return SiteElement(By.XPATH,
                           '//div[@id="keywordTree"]/ul//'
                           'span[contains(text(), "{}")]/../'
                           'span[@class="fancytree-expander"]'.format(item_name))


class AdvancedModal:
    def __init__(self):
        self.value_type = SiteElement(By.CSS_SELECTOR, 'a[href="#valueTypePane"]')
        self.search = SiteElement(By.ID, 'btnAdvancedSearchModalSearch')

    def value_type_sort(self, sort_by):
        return SiteElement(By.XPATH, '//table[@id="tblCvValueType"]/thead/tr/'
                                     'th[contains(text(), "{}")]'.format(sort_by))

    def value_type_cell(self, row, col):
        return SiteElement(By.XPATH,
                           '//table[@id="tblCvValueType"]/'
                           'tbody/tr[{}]/td[{}]'.format(row, col))


class FilterModal:
    def __init__(self):
        self.action = SiteElement(By.ID, 'ddActionsDSR')
        self.count = SiteElement(By.CSS_SELECTOR,
                                 'select[name="tblDetailedSearchResults_length"]')
        self.to_workspace = SiteElement(By.ID, 'anchorAddSelectionsToWorkspaceDSR')
        self.exports = SiteElement(By.ID, 'tableModal-DownloadMgrSearchSummary')
        self.workspace = SiteElement(By.ID, 'tableModal-DataMgrSearchSummary')
        self.close = SiteElement(By.ID, 'closeSearchSummary')
        self.search = SiteElement(By.CSS_SELECTOR,
                                  '#tblDetailedSearchResults_filter input')

    def cell(self, row, col):
        return SiteElement(By.XPATH,
                           '//table[@id="tblDetailedSearchResults"]/'
                           'tbody/tr[{}]/td[{}]/div'.format(row, col))

    def cell_text(self, text):
        return SiteElement(By.XPATH,
                           '//table[@id="tblDetailedSearchResults"]/'
                           'tbody//td[contains(text(), "{}")]'.format(text))

    def sort(self, sort_by):
        return SiteElement(By.XPATH,
                           '//div[@id="tblDetailedSearchResults_wrapper"]//'
                           'thead/tr/th[contains(text(), "{}")]'.format(sort_by))

    @property
    def window_locator(self):
        return By.ID, 'SearchSummaryModal'


class AboutModal:
    def __init__(self):
        self.helpcenter = SiteElement(By.CSS_SELECTOR, '#liZendeskTab span a')
        self.licensing = SiteElement(By.CSS_SELECTOR, '#liLicenseTab span a')
        self.licensing_close = SiteElement(By.CSS_SELECTOR,
                                           '#licenseModal button.close')
        self.license_repo_top = SiteElement(By.CSS_SELECTOR,
                                            '#licenseModal '
                                            'a[href="http://www.github.com/cuahsi"]')
        self.license_repo_inline = SiteElement(By.XPATH,
                                               '//div[@id="licenseModal"]//'
                                               'a[contains(text(), '
                                               '"http://www.github.com/cuahsi")]')
        self.contact = SiteElement(By.CSS_SELECTOR, '#liContactTab span a')
        self.contact_close = SiteElement(By.CSS_SELECTOR,
                                         '#contactModal button.close')
        self.contact_help = SiteElement(By.XPATH,
                                        '//a[contains(text(), '
                                        '"Need additional help")]')


class QuickStartModal:
    def section(self, name):
        return SiteElement(By.XPATH, '//a[contains(text(), "{}")]'.format(name))

    def more(self, name):
        return SiteElement(By.XPATH, '//a[contains(text(), "{}")]'.format(name))


class ZendeskWidget:
    def __init__(self):
        self.helping = SiteElement(By.ID, 'Embed')
        self.results = SiteElement(By.ID, 'webWidget')
        self.search = SiteElement(By.CSS_SELECTOR,
                                  'input.src-component-'
                                  'field-SearchInput-searchInput')
        self.more = SiteElement(By.CSS_SELECTOR,
                                'div.src-component-helpCenter-HelpCenterArticle-'
                                'originalArticleButton')

    def pull(self, text):
        return SiteElement(By.XPATH, '//a[contains(text(), "{}")]'.format(text))


class ZendeskArticlePage:

    @property
    def article_header_locator(self):
        return By.CSS_SELECTOR, 'article.main-column header.article-header h1'


class WorkspacePage:
    def __init__(self):
        self.select_dropdown = SiteElement(By.ID, 'dropdownMenu1')
        self.select_all = SiteElement(By.ID, 'anchorAllSelectionsDataMgr')
        self.select_clear = SiteElement(By.ID, 'spanClearSelectionsDM')
        self.select_delete = SiteElement(By.ID, 'spanRemoveSelectionsDM')
        self.tools = SiteElement(By.ID, 'ddHydrodataToolDataMgr')
        self.to_csv = SiteElement(By.ID, 'idDownloadToClient')
        self.to_viewer = SiteElement(By.CSS_SELECTOR, '#byuApps ul li a')
        self.to_none = SiteElement(By.ID, 'idNone')

    @property
    def tooltip_locator(self):
        return By.CSS_SELECTOR, 'div.tooltip-inner'


class ExternalPage:
    def __init__(self):
        self.body = SiteElement(By.CSS_SELECTOR, 'body')


SearchPage = SearchPage()
MarkerModal = MarkerModal()
ServicesModal = ServicesModal()
KeywordsModal = KeywordsModal()
AdvancedModal = AdvancedModal()
FilterModal = FilterModal()
AboutModal = AboutModal()
QuickStartModal = QuickStartModal()
ZendeskWidget = ZendeskWidget()
WorkspacePage = WorkspacePage()
ExternalPage = ExternalPage()
ZendeskArticlePage = ZendeskArticlePage()
