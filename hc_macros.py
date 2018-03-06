import time

from selenium.webdriver.common.keys import Keys

from hc_elements import SearchPage, ServiceSearchPage, \
    KeywordSearchPage, AdvancedSearchPage
from hc_elements import FilterResultsPage, WorkspacePage, \
    MapMarkerPage, QuickStartPage
from modes import setup_mode

# Hydroclient testing parameters
MODE_SELECTION = 'safe-demo'  # quick, watch, demo, or safe-demo
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)


class Search:
    """ Main search interface macros """
    def map_scroll(self, driver, count=1):
        SearchPage.map_area.click(driver, SLEEP_TIME)
        for i in range(0, count):
            SearchPage.map_area.scroll_right(driver, SLEEP_TIME/count)

    def about_helpcenter(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        SearchPage.about_helpcenter.click(driver, SLEEP_TIME)

    def about_license_repo_top(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        SearchPage.about_license.click(driver, SLEEP_TIME)
        SearchPage.about_license_repo_top.click(driver, SLEEP_TIME)
        SearchPage.about_license_close.click(driver, SLEEP_TIME)

    def about_license_repo_inline(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        SearchPage.about_license.click(driver, SLEEP_TIME)
        SearchPage.about_license_repo_inline.click(driver, SLEEP_TIME)
        SearchPage.about_license_close.click(driver, SLEEP_TIME)

    def about_contact(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        SearchPage.about_contact.click(driver, SLEEP_TIME)
        SearchPage.about_contact_help.click(driver, SLEEP_TIME)
        SearchPage.about_contact_close.click(driver, SLEEP_TIME)

    def zendesk_help(self, driver, search_text, article_text):
        SearchPage.zendesk_iframe.iframe_in(driver)
        SearchPage.zendesk_help.click(driver, SLEEP_TIME)
        SearchPage.zendesk_iframe.iframe_out(driver)
        SearchPage.zendesk_results.iframe_in(driver)
        SearchPage.zendesk_search.inject_text(driver, search_text,
                                              SLEEP_TIME)
        SearchPage.zendesk_search.inject_text(driver, Keys.RETURN,
                                              SLEEP_TIME)
        SearchPage.zendesk_return(article_text).click(driver, SLEEP_TIME)
        SearchPage.zendesk_more.scroll_to(driver, SLEEP_TIME)
        SearchPage.zendesk_more.click(driver, SLEEP_TIME)

    def quick_start(self, driver):
        SearchPage.quickstart.click(driver, SLEEP_TIME)

    def legend_visible(self, driver):
        SearchPage.legend_tab.click(driver, SLEEP_TIME)
        legend_display = SearchPage.legend.get_attribute(driver, 'style')
        legend_display = legend_display.split(':')[-1]
        legend_display = legend_display.split(';')[0]
        legend_display = legend_display.split(' ')[-1]
        SearchPage.search_tab.click(driver, SLEEP_TIME)
        return legend_display != 'none'

    def search(self, driver, count=1):
        for i in range(0, count):
            SearchPage.search_now.click(driver, SLEEP_TIME)

    def layer_toggle(self, driver, layer_name):
        SearchPage.layer_control.click(driver, SLEEP_TIME)
        SearchPage.map_layer(layer_name).click(driver, SLEEP_TIME)

    def map_icon_open(self, driver, results_count):
        SearchPage.map_indicator(results_count).click(driver, SLEEP_TIME)

    def location_search(self, driver, location):
        SearchPage.location_search.click(driver, SLEEP_TIME)
        SearchPage.location_search.clear_all_text(driver, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, location, SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN,
                                               SLEEP_TIME)
        SearchPage.location_search.inject_text(driver, Keys.RETURN,
                                               SLEEP_TIME)
        time.sleep(SLEEP_TIME)

    def results_count(self, driver):
        return SearchPage.results_found.get_text(driver)

    def date_filter(self, driver, start_date, end_date):
        SearchPage.date_filter.click(driver, SLEEP_TIME)
        SearchPage.date_start.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_start.inject_text(driver, start_date, SLEEP_TIME)
        SearchPage.date_clickout.passive_click(driver, SLEEP_TIME)
        SearchPage.date_end.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_end.inject_text(driver, end_date, SLEEP_TIME)
        SearchPage.date_save.click(driver, SLEEP_TIME)
        SearchPage.search_now.click(driver, SLEEP_TIME)

    def reset_params(self, driver):
        SearchPage.reset.click(driver, SLEEP_TIME)

    def map_zoomin(self, driver, count=1):
        for i in range(0, count):
            SearchPage.map_zoomin.click(driver, SLEEP_TIME)


class ServiceSearch:
    """ Narrow search results through service selections - associated
    macros
    """
    def filter_services(self, driver, organizations=None, titles=None):
        SearchPage.service_filter.click(driver, SLEEP_TIME)
        ServiceSearchPage.table_count.select_option(driver, '100',
                                                    SLEEP_TIME)
        ServiceSearchPage.sort_organization.click(driver, SLEEP_TIME)
        if type(organizations) is list:
            for organization in organizations:
                ServiceSearchPage.select_organization((
                    organization).scroll_to(driver, SLEEP_TIME))
                ServiceSearchPage.select_organization((
                    organization).multi_click(driver, SLEEP_TIME))
        elif organizations is not None:
            ServiceSearchPage.select_organization((
                organizations).click(driver, SLEEP_TIME))
        if type(titles) is list:
            for title in titles:
                ServiceSearchPage.select_title((
                    title).scroll_to(driver, SLEEP_TIME))
                ServiceSearchPage.select_title((
                    title).multi_click(driver, SLEEP_TIME))
        elif titles is not None:
            ServiceSearchPage.select_title(titles).click(driver, SLEEP_TIME)
        ServiceSearchPage.save.click(driver, SLEEP_TIME)
        SearchPage.search_now.click(driver, SLEEP_TIME)
        time.sleep(10)


class KeywordSearch:
    """ Macros for the keyword search filtering modal """
    def root_keywords(self, driver, keywords):
        SearchPage.keyword_filter.click(driver, SLEEP_TIME)
        KeywordSearchPage.full_list_tab.click(driver, SLEEP_TIME)
        for keyword in keywords:
            KeywordSearchPage.full_list_checkbox((
                keyword).click(driver, SLEEP_TIME))
        KeywordSearchPage.search.click(driver, SLEEP_TIME)


class AdvancedSearch:
    """ Macros for all tabs within the advanced search modal """
    def all_value_type(self, driver):
        SearchPage.advanced_search.click(driver, SLEEP_TIME)
        AdvancedSearchPage.value_type_tab.click(driver, SLEEP_TIME)
        AdvancedSearchPage.value_type_term_sort.click(driver, SLEEP_TIME)
        AdvancedSearchPage.value_type_first.click(driver, SLEEP_TIME)
        AdvancedSearchPage.value_type_term_sort.click(driver, SLEEP_TIME)
        AdvancedSearchPage.value_type_first.range_click(driver, SLEEP_TIME)
        AdvancedSearchPage.search.click(driver, SLEEP_TIME)


class FilterResults:
    """ Detailed results view by pressing "Filter Results" button
    associated macros
    """
    def any_to_workspace(self, driver):
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResultsPage.table_count.select_option(driver, '100',
                                                    SLEEP_TIME)
        FilterResultsPage.nav_close.scroll_to(driver, SLEEP_TIME)
        FilterResultsPage.select_any.click(driver, SLEEP_TIME)
        FilterResultsPage.choose_action.click(driver, SLEEP_TIME)
        FilterResultsPage.export_workspace.click(driver, SLEEP_TIME)
        FilterResultsPage.nav_workspace.click(driver, SLEEP_TIME)

    def model_sim_and_derived_value_to_workspace(self, driver):
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResultsPage.table_count.select_option(driver, '100',
                                                    SLEEP_TIME)
        FilterResultsPage.select_model_sim.click(driver, SLEEP_TIME)
        FilterResultsPage.sort_service.click(driver, SLEEP_TIME)
        FilterResultsPage.select_derived_value.scroll_to(driver, SLEEP_TIME)
        FilterResultsPage.select_derived_value.multi_click(driver,
                                                           SLEEP_TIME)
        FilterResultsPage.choose_action.click(driver, SLEEP_TIME)
        FilterResultsPage.export_workspace.click(driver, SLEEP_TIME)
        FilterResultsPage.nav_workspace.click(driver, SLEEP_TIME)

    def derived_value_to_workspace(self, driver):
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResultsPage.table_count.select_option(driver, '100',
                                                    SLEEP_TIME)
        FilterResultsPage.select_derived_value.click(driver, SLEEP_TIME)
        FilterResultsPage.choose_action.click(driver, SLEEP_TIME)
        FilterResultsPage.export_workspace.click(driver, SLEEP_TIME)
        FilterResultsPage.nav_workspace.click(driver, SLEEP_TIME)

    def search_filter_table(self, driver, search_string):
        SearchPage.filter_results.click(driver, SLEEP_TIME)
        FilterResultsPage.search.inject_text(driver, search_string,
                                             SLEEP_TIME)
        FilterResultsPage.sort_service.click(driver, SLEEP_TIME)
        FilterResultsPage.table_count.select_option(driver, '100',
                                                    SLEEP_TIME)
        FilterResultsPage.nav_close.click(driver, SLEEP_TIME)


class Workspace:
    """ Macros related to workspace page/modal """
    def goto_from_search(self, driver):
        SearchPage.workspace.click(driver, SLEEP_TIME)

    def select_all(self, driver):
        WorkspacePage.selections_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_all.click(driver, SLEEP_TIME)

    def clear_selected(self, driver):
        WorkspacePage.selections_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_clear.click(driver, SLEEP_TIME)

    def remove_selected(self, driver):
        WorkspacePage.selections_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_delete.click(driver, SLEEP_TIME)

    def export_csv(self, driver):
        WorkspacePage.select_tool.passive_click(driver, SLEEP_TIME)
        WorkspacePage.save_csv.click(driver, SLEEP_TIME)

    def export_data_viewer(self, driver):
        WorkspacePage.select_tool.passive_click(driver, SLEEP_TIME)
        WorkspacePage.data_viewer.click(driver, SLEEP_TIME)

    def export_none(self, driver):
        WorkspacePage.select_tool.passive_click(driver, SLEEP_TIME)
        WorkspacePage.export_none.click(driver, SLEEP_TIME)

    def completed_count(self, driver):
        time.sleep(50*SLEEP_TIME)
        return driver.page_source.count('<em> Completed</em>')

    def in_results(self, driver, strings):
        FilterResultsPage.nav_workspace.click(driver, SLEEP_TIME)
        time.sleep(10*SLEEP_TIME)
        if type(strings) is list:
            for string in strings:
                if string not in driver.page_source:
                    return False
        elif strings is not None:
            if strings not in driver.page_source:
                return False
        return True


class MapMarker:
    """ Macros for map-opened search results """
    def all_to_workspace(self, driver):
        MapMarkerPage.sort_data_type.click(driver, SLEEP_TIME)
        MapMarkerPage.select_any.click(driver, SLEEP_TIME)
        MapMarkerPage.sort_data_type.click(driver, SLEEP_TIME)
        MapMarkerPage.select_any.scroll_to(driver, SLEEP_TIME)
        MapMarkerPage.select_any.range_click(driver, SLEEP_TIME)
        MapMarkerPage.choose_action.click(driver, SLEEP_TIME)
        MapMarkerPage.export_workspace.click(driver, SLEEP_TIME)
        MapMarkerPage.nav_workspace.click(driver, SLEEP_TIME)


class QuickStart:
    """ Macros for the QuickStart modal """
    def help_expand(self, driver, help_item):
        QuickStartPage.help_item(help_item).click(driver, SLEEP_TIME)

    def help_more(self, driver, link_text):
        QuickStartPage.more_info(link_text).click(driver, SLEEP_TIME)


Search = Search()
ServiceSearch = ServiceSearch()
KeywordSearch = KeywordSearch()
AdvancedSearch = AdvancedSearch()
FilterResults = FilterResults()
Workspace = Workspace()
MapMarker = MapMarker()
QuickStart = QuickStart()
