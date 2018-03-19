""" This module contains the definitions for site element locations.  These site
element locations can be defined in through a number of mechanisms, as further
detailed in the SiteElement class
"""
from site_element import SiteElement


class SearchPage:
    def __init__(self):
        self.workspace = SiteElement('*', el_id='tabbedDataMgrTab')
        self.map_area = SiteElement('div', el_id='map-canvas')
        self.zoom_in = SiteElement('button', el_title='Zoom in')
        self.search = SiteElement('button', el_id='btnSearchNow')
        self.reset = SiteElement('button', el_id='btnSetDefaults')
        self.map_filter = SiteElement('button', el_id='btnSearchSummary')
        self.map_search = SiteElement('input', el_id='pac-input')
        self.services = SiteElement('button', el_id='btnSelectDataServices',
                                    el_content='Data Service(s)...')
        self.keywords = SiteElement('button', el_id='btnSelectKeywords')
        self.advanced = SiteElement('button', el_id='btnAdvancedSearch')
        self.results_count = SiteElement('span',
                                         el_id='timeseriesFoundOrFilteredCount')
        self.date_filter = SiteElement('*', el_id='optionsDatesRange')
        self.date_start = SiteElement('*', el_id='startDateModal')
        self.date_end = SiteElement('*', el_id='endDateModal')
        self.date_clickout = SiteElement('h3',
                                         el_content='Please select your date range:')
        self.date_save = SiteElement('*', el_id='btnDateRangeModalSave')
        self.layers = SiteElement('*', el_id='Layer Control')
        self.legend_tab = SiteElement('a', el_content='LEGENDS')
        self.legend_img = SiteElement('*', el_id='nlcdColorClassUpdate')
        self.search_tab = SiteElement('a', el_content='SEARCH')
        self.about = SiteElement('*', el_id='ddAbout')
        self.quickstart = SiteElement('*', el_id='quickStartModalTab')
        self.zendesk = SiteElement('*', el_id='launcher')

    def layer(self, name):
        return SiteElement('label', el_content=name)

    def map_marker(self, results_count):
        return SiteElement('div', el_content=results_count)


class MarkerModal:
    def __init__(self):
        self.action = SiteElement('div', el_id='ddActionsMM')
        self.to_workspace = SiteElement('a',
                                        el_id='anchorAddSelectionsToWorkspaceMM')
        self.workspace = SiteElement('button', el_id='tableModal-DataMgr')

    def cell(self, row, col):
        return SiteElement('table', el_id='tblMapMarker',
                           el_recursive=(
                               [SiteElement(el_dom='./tbody'),
                                SiteElement(el_dom='./tr[{}]'.format(row)),
                                SiteElement(el_dom='./td[{}]'.format(col)),
                                SiteElement(el_dom='./div')]))

    def sort(self, sort_by):
        return SiteElement('div', el_id='tblMapMarker_wrapper',
                           el_recursive=(
                               [SiteElement('th', el_content=sort_by)]))


class ServicesModal:
    # TODO Need to use el_id approach and recursive identification.
    # Currently system relies on Services being first modal (not robust)
    def __init__(self):
        self.sort_org = SiteElement('th', el_content='Organization')
        self.save = SiteElement('button', el_id='btnServicesModalSave')
        self.search = SiteElement('button', el_id='btnServicesModalSearch')
        self.table_count = SiteElement('select', el_name='tblDataServices_length')
        self.archbold = SiteElement('td', el_content='Archbold Biological Station')
        self.nwis_uv = SiteElement('a', el_content='NWIS Unit Values',
                                   el_recursive=[SiteElement(el_dom='./../..'),
                                                 SiteElement(el_dom='./td[1]')])
        self.nasa_noah = SiteElement('a', el_content='NLDAS Hourly NOAH Data',
                                     el_recursive=[SiteElement(el_dom='./../..'),
                                                   SiteElement(el_dom='./td[1]')])
        self.nasa_forcing = \
            SiteElement('a', el_content='NLDAS Hourly Primary Forcing Data',
                        el_recursive=[SiteElement(el_dom='./../..'),
                                      SiteElement(el_dom='./td[1]')])

    def select_org(self, org):
        return SiteElement('td', el_content=org)

    def select_title(self, service_title):
        return SiteElement('a', el_content=service_title,
                           el_recursive=[SiteElement(el_dom='./../..'),
                                         SiteElement(el_dom='./td[1]')])


class KeywordsModal:
    def __init__(self):
        self.full_list = SiteElement('a', el_href='#tab2')
        self.search = SiteElement('*', el_id='btnFullKeywordModalSearch')

    def full_list_checkbox(self, item_name):
        return SiteElement('div', el_id='keywordTree',
                           el_recursive=(
                               [SiteElement('ul'),
                                SiteElement('span', el_content=item_name),
                                SiteElement(el_dom='./..'),
                                SiteElement('span',
                                            el_class='fancytree-checkbox')]))

    def full_list_expand(self, item_name):
        return SiteElement('div', el_id='keywordTree',
                           el_recursive=(
                               [SiteElement('ul'),
                                SiteElement('span', el_content=item_name),
                                SiteElement(el_dom='./..'),
                                SiteElement('span',
                                            el_class='fancytree-expander')]))


class AdvancedModal:
    def __init__(self):
        self.value_type = SiteElement('a', el_href='#valueTypePane')
        self.search = SiteElement('*', el_id='btnAdvancedSearchModalSearch')

    def value_type_sort(self, sort_by):
        return SiteElement('table', el_id='tblCvValueType',
                           el_recursive=[SiteElement('thead'),
                                         SiteElement('tr'),
                                         SiteElement('th', el_content=sort_by)])

    def value_type_cell(self, row, col):
        return SiteElement('table', el_id='tblCvValueType',
                           el_recursive=[SiteElement('tbody'),
                                         SiteElement('tr[{}]'.format(row)),
                                         SiteElement('td[{}]'.format(col))])


class FilterModal:
    def __init__(self):
        self.action = SiteElement('div', el_id='ddActionsDSR')
        self.count = SiteElement('select', el_name='tblDetailedSearchResults_length')
        self.to_workspace = SiteElement('a',
                                        el_id='anchorAddSelectionsToWorkspaceDSR')
        self.exports = SiteElement('button',
                                   el_id='tableModal-DownloadMgrSearchSummary')
        self.workspace = SiteElement('button',
                                     el_id='tableModal-DataMgrSearchSummary')
        self.close = SiteElement('button', el_id='closeSearchSummary')
        self.search = SiteElement('div', el_id='tblDetailedSearchResults_filter',
                                  el_recursive=[SiteElement(el_dom='./label'),
                                                SiteElement(el_dom='./input')])

    def cell(self, row, col):
        return SiteElement('table', el_id='tblDetailedSearchResults',
                           el_recursive=(
                               [SiteElement('tbody'),
                                SiteElement(el_dom='./tr[{}]'.format(row)),
                                SiteElement(el_dom='./td[{}]'.format(col)),
                                SiteElement(el_dom='./div')]))

    def cell_text(self, text):
        return SiteElement('table', el_id='tblDetailedSearchResults',
                           el_recursive=[SiteElement('tbody'),
                                         SiteElement('td', el_content=text)])

    def sort(self, sort_by):
        return SiteElement('div', el_id='tblDetailedSearchResults_wrapper',
                           el_recursive=[SiteElement('thead'),
                                         SiteElement('th', el_content=sort_by)])


class AboutModal:
    def __init__(self):
        self.helpcenter = SiteElement('li', el_id='liZendeskTab',
                                      el_recursive=[SiteElement('span'),
                                                    SiteElement('a')])
        self.licensing = SiteElement('li', el_id='liLicenseTab',
                                     el_recursive=[SiteElement('span'),
                                                   SiteElement('a')])
        self.licensing_close = \
            SiteElement('div', el_id='licenseModal',
                        el_recursive=[SiteElement('button', el_class='close')])
        self.license_repo_top = \
            SiteElement('div', el_id='licenseModal',
                        el_recursive=[SiteElement('a', el_href=(
                            'http://www.github.com/cuahsi'))])
        self.license_repo_inline = \
            SiteElement('div', el_id='licenseModal',
                        el_recursive=[SiteElement('a', el_content=(
                            'http://www.github.com/cuahsi'))])
        self.contact = \
            SiteElement('li', el_id='liContactTab',
                        el_recursive=[SiteElement('span'), SiteElement('a')])
        self.contact_close = \
            SiteElement('div', el_id='contactModal',
                        el_recursive=[SiteElement('button', el_class='close')])
        self.contact_help = SiteElement('a', el_content='Need additional help')


class QuickStartModal:
    def section(self, name):
        return SiteElement('a', el_content=name)

    def more(self, name):
        return SiteElement('a', el_content=name)


class ZendeskWidget:
    def __init__(self):
        self.helping = SiteElement('div', el_id='Embed')
        self.results = SiteElement('*', el_id='webWidget')
        self.search = SiteElement('input', el_placeholder='How can we help?')
        self.more = SiteElement('a', el_title='View original article')

    def pull(self, text):
        return SiteElement('a', el_content=text)


class WorkspacePage:
    def __init__(self):
        self.select_dropdown = SiteElement('*', el_id='dropdownMenu1')
        self.select_all = SiteElement('*', el_id='anchorAllSelectionsDataMgr')
        self.select_clear = SiteElement('*', el_id='spanClearSelectionsDM')
        self.select_delete = SiteElement('*', el_id='spanRemoveSelectionsDM')
        self.tools = SiteElement('*', el_id='ddHydrodataToolDataMgr')
        self.to_csv = SiteElement('*', el_id='idDownloadToClient')
        self.to_viewer = SiteElement('li', el_id='byuApps',
                                     el_recursive=[SiteElement('ul'),
                                                   SiteElement('li'),
                                                   SiteElement('a')])
        self.to_none = SiteElement('*', el_id='idNone')


class ExternalPage:
    def __init__(self):
        self.body = SiteElement('body')


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
