from site_element import SiteElement

class SearchPage:
    def __init__(self):
        self.search_now = SiteElement('button', el_id='btnSearchNow')
        self.reset = SiteElement('button', el_id='btnSetDefaults')
        self.filter_results = SiteElement('button', el_id='btnSearchSummary')
        self.location_search = SiteElement('input', el_id='pac-input')
        self.service_filter = SiteElement('button', el_id='btnSelectDataServices', el_content='Data Service(s)...')
        self.keyword_filter = SiteElement('button', el_id='btnSelectKeywords')
        self.advanced_search = SiteElement('button', el_id='btnAdvancedSearch')
        self.results_found = SiteElement('span', el_id='timeseriesFoundOrFilteredCount')
        self.date_filter = SiteElement('*', el_id='optionsDatesRange')
        self.date_start = SiteElement('*', el_id='startDateModal')
        self.date_end = SiteElement('*', el_id='endDateModal')
        self.date_clickout = SiteElement('h3', el_content='Please select your date range:')
        self.date_save = SiteElement('*', el_id='btnDateRangeModalSave')
        self.layer_control = SiteElement('*', el_id='Layer Control')
        self.legend_tab = SiteElement('a', el_content='LEGENDS')
        self.search_tab = SiteElement('a', el_content='SEARCH')
        self.legend = SiteElement('*', el_id='nlcdColorClassUpdate')
        self.quickstart = SiteElement('*', el_id='quickStartModalTab')
        self.zendesk_iframe = SiteElement('*', el_id='launcher')
        self.zendesk_help = SiteElement('div', el_id='Embed')
        self.zendesk_results = SiteElement('*', el_id='webWidget')
        self.zendesk_search = SiteElement('input', el_placeholder='How can we help?')
        self.zendesk_more = SiteElement('div', el_content='View original article')

    def zendesk_return(self, text):
        return SiteElement('a', el_content=text)
    
    def map_layer(self, name):
        return SiteElement('label', el_content=name)
        
    def map_indicator(self, results_count):
        return SiteElement('div', el_content=results_count)

class KeywordSearchPage:
    def __init__(self):
        self.full_list_tab = SiteElement('a', el_href='#tab2')
        self.search = SiteElement('*', el_id='btnFullKeywordModalSearch')

    def full_list_checkbox(self, item_name):
        return SiteElement('div', el_id='keywordTree', recursive_loc=[SiteElement('ul'), SiteElement('span', el_content=item_name), SiteElement(el_dom='./..'), SiteElement('span', el_class='fancytree-checkbox')])

    def full_list_expand(self, item_name):
        return SiteElement('div', el_id='keywordTree', recursive_loc=[SiteElement('ul'), SiteElement('span', el_content=item_name), SiteElement(el_dom='./..'), SiteElement('span', el_class='fancytree-expander')])

class AdvancedSearchPage:
    def __init__(self):
        self.value_type_tab = SiteElement('a', el_href='#valueTypePane')
        self.value_type_term_sort = SiteElement('table', el_id='tblCvValueType', recursive_loc=[SiteElement('thead'), SiteElement('tr'), SiteElement('th', el_content='Term')])
        self.value_type_first = SiteElement('table', el_id='tblCvValueType', recursive_loc=[SiteElement('tbody'), SiteElement('tr'), SiteElement('td')])
        self.search = SiteElement('*', el_id='btnAdvancedSearchModalSearch')
    
class ServiceSearchPage:
    def __init__(self):
        self.sort_organization = SiteElement('th', el_content='Organization')
        self.save = SiteElement('button', el_id='btnServicesModalSave')
        self.search = SiteElement('button', el_id='btnServicesModalSearch')
        self.table_count = SiteElement('select', el_name='tblDataServices_length')
        self.archbold = SiteElement('td', el_content='Archbold Biological Station')
        self.nwis_uv = SiteElement('a', el_content='NWIS Unit Values', recursive_loc=[SiteElement(el_dom='./../..'), SiteElement(el_dom='./td[1]')])
        self.nasa_noah = SiteElement('a', el_content='NLDAS Hourly NOAH Data', recursive_loc=[SiteElement(el_dom='./../..'), SiteElement(el_dom='./td[1]')])
        self.nasa_forcing = SiteElement('a', el_content='NLDAS Hourly Primary Forcing Data', recursive_loc=[SiteElement(el_dom='./../..'), SiteElement(el_dom='./td[1]')])

    def select_organization(self, service_organization):
        return SiteElement('td', el_content=service_organization)

    def select_title(self, service_title):
        return SiteElement('a', el_content=service_title, recursive_loc=[SiteElement(el_dom='./../..'), SiteElement(el_dom='./td[1]')])
        
class FilterResultsPage:
    def __init__(self):
        self.choose_action = SiteElement('div', el_id='ddActionsDSR')
        self.table_count = SiteElement('select', el_name='tblDetailedSearchResults_length')
        self.export_workspace = SiteElement('a', el_id='anchorAddSelectionsToWorkspaceDSR')
        self.nav_exports = SiteElement('button', el_id='tableModal-DownloadMgrSearchSummary')
        self.nav_workspace = SiteElement('button', el_id='tableModal-DataMgrSearchSummary')
        self.nav_close = SiteElement('button', el_id='closeSearchSummary')
        self.search = SiteElement('div', el_id='tblDetailedSearchResults_filter', recursive_loc=[SiteElement(el_dom='./label'), SiteElement(el_dom='./input')])
        self.select_any = SiteElement('table', el_id='tblDetailedSearchResults', recursive_loc=[SiteElement(el_dom='./tbody'), SiteElement(el_dom='./tr'), SiteElement(el_dom='./td'), SiteElement(el_dom='./div')])
        self.select_derived_value = SiteElement('td', el_content='Derived Value')
        self.select_model_sim = SiteElement('td', el_content='Model Simulation Result')
        self.sort_service = SiteElement('div', el_id='tblDetailedSearchResults_wrapper', recursive_loc=[SiteElement('th', el_content='Service Title')])

class MapMarkerPage:
    def __init__(self):
        self.choose_action = SiteElement('div', el_id='ddActionsMM')
        self.export_workspace = SiteElement('a', el_id='anchorAddSelectionsToWorkspaceMM')
        self.sort_data_type = SiteElement('div', el_id='tblMapMarker_wrapper', recursive_loc=[SiteElement('div', el_class='dataTables_scroll'), SiteElement('div', el_class='dataTables_scrollHead'), SiteElement('div', el_class='dataTables_scrollHeadInner'), SiteElement('table'), SiteElement('thead'), SiteElement('tr'), SiteElement('th', el_content='Data Type')])
        self.select_any = SiteElement('table', el_id='tblMapMarker', recursive_loc=[SiteElement(el_dom='./tbody'), SiteElement(el_dom='./tr'), SiteElement(el_dom='./td'), SiteElement(el_dom='./div')])
        self.nav_workspace = SiteElement('button', el_id='tableModal-DataMgr')

class QuickStartPage:
    def __init__(self):
        self.full = SiteElement('body')
    
    def help_item(self, name):
        return SiteElement('a', el_content=name)

    def more_info(self, name):
        return SiteElement('a', el_content=name)

class ExternalPage:
    def __init__(self):
        self.full = SiteElement('body')
    
SearchPage = SearchPage()
ServiceSearchPage = ServiceSearchPage()
KeywordSearchPage = KeywordSearchPage()
AdvancedSearchPage = AdvancedSearchPage()
FilterResultsPage = FilterResultsPage()
MapMarkerPage = MapMarkerPage()
QuickStartPage = QuickStartPage()
ExternalPage = ExternalPage()

