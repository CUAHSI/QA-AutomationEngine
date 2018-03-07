import time

from selenium.webdriver.common.keys import Keys

from hc_elements import SearchPage, MarkerModal, ServicesModal, \
    KeywordsModal, AdvancedModal, FilterModal, AboutModal, \
    QuickStartModal, ZendeskWidget, WorkspacePage
from modes import setup_mode

# Hydroclient testing parameters
MODE_SELECTION = 'safe-demo'  # quick, watch, demo, or safe-demo
global SLEEP_TIME
SLEEP_TIME = setup_mode(MODE_SELECTION)


class Search:
    """ Main search interface macros """
    # def map_scroll(self, driver, count=1):
    #     SearchPage.map_area.click(driver, SLEEP_TIME)
    #     for i in range(0, count):
    #         SearchPage.map_area.scroll_right(driver, SLEEP_TIME/count)

    def scroll_map(self, driver, count=1):
        SearchPage.map_area.click(driver, SLEEP_TIME)
        for i in range(0, count):
            SearchPage.map_area.scroll_right(driver, SLEEP_TIME/count)

    def to_workspace(self, driver):
        SearchPage.workspace.click(driver, SLEEP_TIME)

    # def about_helpcenter(self, driver):
    #     SearchPage.about.click(driver, SLEEP_TIME)
    #     AboutModal.helpcenter.click(driver, SLEEP_TIME)

    # def about_license_repo_top(self, driver):
    #     SearchPage.about.click(driver, SLEEP_TIME)
    #     AboutModal.licensing.click(driver, SLEEP_TIME)
    #     AboutModal.license_repo_top.click(driver, SLEEP_TIME)
    #     AboutModal.licensing_close.click(driver, SLEEP_TIME)

    # def about_license_repo_inline(self, driver):
    #     SearchPage.about.click(driver, SLEEP_TIME)
    #     AboutModal.licensing.click(driver, SLEEP_TIME)
    #     AboutModal.license_repo_inline.click(driver, SLEEP_TIME)
    #     AboutModal.licensing_close.click(driver, SLEEP_TIME)

    # def about_contact(self, driver):
    #     SearchPage.about.click(driver, SLEEP_TIME)
    #     AboutModal.contact.click(driver, SLEEP_TIME)
    #     AboutModal.contact_help.click(driver, SLEEP_TIME)
    #     AboutModal.contact_close.click(driver, SLEEP_TIME)

    # def zendesk_help(self, driver, search_text, article_text):
    #     SearchPage.zendesk.iframe_in(driver)
    #     Zendesk.helping.click(driver, SLEEP_TIME)
    #     SearchPage.zendesk.iframe_out(driver)
    #     Zendesk.results.iframe_in(driver)
    #     Zendesk.search.inject_text(driver, search_text,
    #                                           SLEEP_TIME)
    #     Zendesk.search.inject_text(driver, Keys.RETURN,
    #                                           SLEEP_TIME)
    #     Zendesk.pull(article_text).click(driver, SLEEP_TIME)
    #     Zendesk.more.scroll_to(driver, SLEEP_TIME)
    #     Zendesk.more.click(driver, SLEEP_TIME)

    # def quick_start(self, driver):
    #     SearchPage.quickstart.click(driver, SLEEP_TIME)

    def to_quickstart(self, driver):
        SearchPage.quickstart.click(driver, SLEEP_TIME)

    # def legend_visible(self, driver):
    #     SearchPage.legend_img.click(driver, SLEEP_TIME)
    #     legend_display = SearchPage.legend_img.get_attribute(driver, 'style')
    #     legend_display = legend_display.split(':')[-1]
    #     legend_display = legend_display.split(';')[0]
    #     legend_display = legend_display.split(' ')[-1]
    #     SearchPage.search_tab.click(driver, SLEEP_TIME)
    #     return legend_display != 'none'

    def is_legend_visible(self, driver):
        SearchPage.legend_img.click(driver, SLEEP_TIME)
        legend_vis = SearchPage.legend_img.get_attribute(driver, 'style')
        legend_vis = legend_vis.split(':')[-1]
        legend_vis = legend_vis.split(';')[0]
        legend_vis = legend_vis.split(' ')[-1]
        SearchPage.search_tab.click(driver, SLEEP_TIME)
        return legend_vis != 'none'

    def search(self, driver, count=1):
        for i in range(0, count):
            SearchPage.search.click(driver, SLEEP_TIME)

    # def layer_toggle(self, driver, layer_name):
    #     SearchPage.layers.click(driver, SLEEP_TIME)
    #     SearchPage.layer(layer_name).click(driver, SLEEP_TIME)

    def toggle_layer(self, driver, layer_name):
        SearchPage.layers.click(driver, SLEEP_TIME)
        SearchPage.layer(layer_name).click(driver, SLEEP_TIME)

    # def map_icon_open(self, driver, results_count):
    #     SearchPage.map_marker(results_count).click(driver, SLEEP_TIME)

    def to_map_marker(self, driver, results_count):
        SearchPage.map_marker(results_count).click(driver, SLEEP_TIME)

    # def location_search(self, driver, location):
    #     SearchPage.location_search.click(driver, SLEEP_TIME)
    #     SearchPage.location_search.clear_all_text(driver, SLEEP_TIME)
    #     SearchPage.location_search.inject_text(driver, location, SLEEP_TIME)
    #     SearchPage.location_search.inject_text(driver, Keys.ARROW_DOWN,
    #                                            SLEEP_TIME)
    #     SearchPage.location_search.inject_text(driver, Keys.RETURN,
    #                                            SLEEP_TIME)
    #     time.sleep(SLEEP_TIME)

    def search_location(self, driver, location):
        SearchPage.map_search.click(driver, SLEEP_TIME)
        SearchPage.map_search.clear_all_text(driver, SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, location, SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, Keys.ARROW_DOWN,
                                          SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, Keys.RETURN,
                                          SLEEP_TIME)
        time.sleep(SLEEP_TIME)

    # def results_count(self, driver):
    #     return SearchPage.results_count.get_text(driver)

    def count_results(self, driver):
        return SearchPage.results_count.get_text(driver)

    # def date_filter(self, driver, start_date, end_date):
    #     SearchPage.date_filter.click(driver, SLEEP_TIME)
    #     SearchPage.date_start.clear_text(driver, 12, SLEEP_TIME)
    #     SearchPage.date_start.inject_text(driver, start_date, SLEEP_TIME)
    #     SearchPage.date_clickout.passive_click(driver, SLEEP_TIME)
    #     SearchPage.date_end.clear_text(driver, 12, SLEEP_TIME)
    #     SearchPage.date_end.inject_text(driver, end_date, SLEEP_TIME)
    #     SearchPage.date_save.click(driver, SLEEP_TIME)
    #     SearchPage.search.click(driver, SLEEP_TIME)

    def filter_dates(self, driver, start_date, end_date):
        SearchPage.date_filter.click(driver, SLEEP_TIME)
        SearchPage.date_start.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_start.inject_text(driver, start_date, SLEEP_TIME)
        SearchPage.date_clickout.passive_click(driver, SLEEP_TIME)
        SearchPage.date_end.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_end.inject_text(driver, end_date, SLEEP_TIME)
        SearchPage.date_save.click(driver, SLEEP_TIME)
        SearchPage.search.click(driver, SLEEP_TIME)

    # def reset_params(self, driver):
    #     SearchPage.reset.click(driver, SLEEP_TIME)

    def reset(self, driver):
        SearchPage.reset.click(driver, SLEEP_TIME)

    # def map_zoomin(self, driver, count=1):
    #     for i in range(0, count):
    #         SearchPage.zoom_in.click(driver, SLEEP_TIME)

    def zoom_in(self, driver, count=1):
        for i in range(0, count):
            SearchPage.zoom_in.click(driver, SLEEP_TIME)


class Marker:
    """ Macros for map-opened search results """
    # def all_to_workspace(self, driver):
    def to_workspace_all(self, driver):
        MarkerModal.sort('Data Type').click(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).click(driver, SLEEP_TIME)
        MarkerModal.sort('Data Type').click(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).scroll_to(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).range_click(driver, SLEEP_TIME)
        MarkerModal.action.click(driver, SLEEP_TIME)
        MarkerModal.to_workspace.click(driver, SLEEP_TIME)
        MarkerModal.workspace.click(driver, SLEEP_TIME)


# class ServiceSearch:
class Services:
    """ Narrow search results through service selections - associated
    macros
    """
    # def filter_services(self, driver, organizations=None, titles=None):
    def filters(self, driver, organizations=None, titles=None):
        SearchPage.services.click(driver, SLEEP_TIME)
        ServicesModal.table_count.select_option(driver, '100',
                                                SLEEP_TIME)
        ServicesModal.sort_organization.click(driver, SLEEP_TIME)
        if type(organizations) is list:
            for organization in organizations:
                ServicesModal.select_organization(organization).scroll_to(driver, SLEEP_TIME)
                ServicesModal.select_organization(organization).multi_click(driver, SLEEP_TIME)
        elif organizations is not None:
            ServicesModal.select_organization(organizations).click(driver, SLEEP_TIME)
        if type(titles) is list:
            for title in titles:
                ServicesModal.select_title(title).scroll_to(driver, SLEEP_TIME)
                ServicesModal.select_title(title).multi_click(driver, SLEEP_TIME)
        elif titles is not None:
            ServicesModal.select_title(titles).click(driver, SLEEP_TIME)
        ServicesModal.save.click(driver, SLEEP_TIME)
        SearchPage.search.click(driver, SLEEP_TIME)
        time.sleep(10)


# class KeywordSearch:
class Keywords:
    """ Macros for the keyword search filtering modal """
    # def root_keywords(self, driver, keywords):
    def filter_root(self, driver, keywords):
        SearchPage.keywords.click(driver, SLEEP_TIME)
        KeywordsModal.full_list.click(driver, SLEEP_TIME)
        for keyword in keywords:
            KeywordsModal.full_list_checkbox((
                keyword).click(driver, SLEEP_TIME))
        KeywordsModal.search.click(driver, SLEEP_TIME)


# class AdvancedSearch:
class Advanced:
    """ Macros for all tabs within the advanced search modal """
    # def all_value_type(self, driver):
    def filter_all_value_types(self, driver):
        SearchPage.advanced.click(driver, SLEEP_TIME)
        AdvancedModal.value_type.click(driver, SLEEP_TIME)
        AdvancedModal.value_type_sort('Term').click(driver, SLEEP_TIME)
        AdvancedModal.value_type_cell(1, 1).click(driver, SLEEP_TIME)
        AdvancedModal.value_type_sort('Term').click(driver, SLEEP_TIME)
        AdvancedModal.value_type_cell(1, 1).range_click(driver, SLEEP_TIME)
        AdvancedModal.search.click(driver, SLEEP_TIME)


# class FilterResults:
class Filter:
    """ Detailed results view by pressing "Filter Results" button
    associated macros
    """
    # def any_to_workspace(self, driver):
    def to_workspace_cell(self, driver, row, col):
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.close.scroll_to(driver, SLEEP_TIME)
        # FilterModal.cell(row, 1).click(driver, SLEEP_TIME)
        FilterModal.cell(row, col).click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    # def model_sim_and_derived_value_to_workspace(self, driver):
    #     SearchPage.map_filter.click(driver, SLEEP_TIME)
    #     FilterModal.count.select_option(driver, '100',
    #                                                 SLEEP_TIME)
    #     FilterModal.cell_text('Model Simulation Result').click(driver,
    #                                                            SLEEP_TIME)
    #     FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
    #     FilterModal.cell_text('Derived Value').scroll_to(driver, SLEEP_TIME)
    #     FilterModal.cell_text('Derived Value').multi_click(driver,
    #                                                        SLEEP_TIME)
    #     FilterModal.action.click(driver, SLEEP_TIME)
    #     FilterModal.to_workspace.click(driver, SLEEP_TIME)
    #     FilterModal.workspace.click(driver, SLEEP_TIME)

    def to_workspace_texts_range(self, driver, texts):
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.cell_text(texts[0]).click(driver, SLEEP_TIME)
        FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
        FilterModal.cell_text(texts[1]).scroll_to(driver, SLEEP_TIME)
        FilterModal.cell_text(texts[1]).multi_click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    # def derived_value_to_workspace(self, driver):
    #     SearchPage.map_filter.click(driver, SLEEP_TIME)
    #     FilterModal.count.select_option(driver, '100',
    #                                                 SLEEP_TIME)
    #     FilterModal.cell_text('Derived Value').click(driver, SLEEP_TIME)
    #     FilterModal.action.click(driver, SLEEP_TIME)
    #     FilterModal.to_workspace.click(driver, SLEEP_TIME)
    #     FilterModal.workspace.click(driver, SLEEP_TIME)

    def to_workspace_text(self, driver, text):
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.cell_text(text).click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    # def search_filter_table(self, driver, search_string):
    #     SearchPage.map_filter.click(driver, SLEEP_TIME)
    #     FilterModal.search.inject_text(driver, search_string,
    #                                          SLEEP_TIME)
    #     FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
    #     FilterModal.count.select_option(driver, '100',
    #                                                 SLEEP_TIME)
    #     FilterModal.close.click(driver, SLEEP_TIME)

    def search_field(self, driver, search_string):
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.search.inject_text(driver, search_string, SLEEP_TIME)
        FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.close.click(driver, SLEEP_TIME)


class About:
    def to_helpcenter(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.helpcenter.click(driver, SLEEP_TIME)

    def to_license_repo_top(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.licensing.click(driver, SLEEP_TIME)
        AboutModal.license_repo_top.click(driver, SLEEP_TIME)
        AboutModal.licensing_close.click(driver, SLEEP_TIME)

    def to_license_repo_inline(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.licensing.click(driver, SLEEP_TIME)
        AboutModal.license_repo_inline.click(driver, SLEEP_TIME)
        AboutModal.licensing_close.click(driver, SLEEP_TIME)

    def to_contact(self, driver):
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.contact.click(driver, SLEEP_TIME)
        AboutModal.contact_help.click(driver, SLEEP_TIME)
        AboutModal.contact_close.click(driver, SLEEP_TIME)


class QuickStart:
    """ Macros for the QuickStart modal """
    # def help_expand(self, driver, help_item):
    def section(self, driver, help_item):
        QuickStartModal.section(help_item).click(driver, SLEEP_TIME)

    # def help_more(self, driver, link_text):
    def more(self, driver, link_text):
        QuickStartModal.more(link_text).click(driver, SLEEP_TIME)


class Zendesk:
    def to_help(self, driver, search_text, article_text):
        SearchPage.zendesk.iframe_in(driver)
        ZendeskWidget.helping.click(driver, SLEEP_TIME)
        SearchPage.zendesk.iframe_out(driver)
        ZendeskWidget.results.iframe_in(driver)
        ZendeskWidget.search.inject_text(driver, search_text,
                                         SLEEP_TIME)
        ZendeskWidget.search.inject_text(driver, Keys.RETURN,
                                         SLEEP_TIME)
        ZendeskWidget.pull(article_text).click(driver, SLEEP_TIME)
        ZendeskWidget.more.scroll_to(driver, SLEEP_TIME)
        ZendeskWidget.more.click(driver, SLEEP_TIME)


class Workspace:
    """ Macros related to workspace page/modal """
    # def goto_from_search(self, driver):
    #     SearchPage.workspace.click(driver, SLEEP_TIME)
    # CHECK Search

    def select_all(self, driver):
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_all.click(driver, SLEEP_TIME)

    # def clear_selected(self, driver):
    def clear_select(self, driver):
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_clear.click(driver, SLEEP_TIME)

    # def remove_selected(self, driver):
    def remove_select(self, driver):
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_delete.click(driver, SLEEP_TIME)

    # def export_csv(self, driver):
    def to_csv(self, driver):
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_csv.click(driver, SLEEP_TIME)

    # def export_data_viewer(self, driver):
    def to_viewer(self, driver):
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_viewer.click(driver, SLEEP_TIME)

    # def export_none(self, driver):
    def to_none(self, driver):
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_none.click(driver, SLEEP_TIME)

    # def completed_count(self, driver):
    def count_complete(self, driver, time_mult):
        # time.sleep(50*SLEEP_TIME)
        time.sleep(time_mult*SLEEP_TIME)
        return driver.page_source.count('<em> Completed</em>')

    # def in_results(self, driver, strings):
    def is_in_results(self, driver, strings, time_mult):
        # time.sleep(10*SLEEP_TIME)
        time.sleep(time_mult*SLEEP_TIME)
        if type(strings) is list:
            for string in strings:
                if string not in driver.page_source:
                    return False
        elif strings is not None:
            if strings not in driver.page_source:
                return False
        return True


Search = Search()
Marker = Marker()
Services = Services()
Keywords = Keywords()
Advanced = Advanced()
Filter = Filter()
About = About()
QuickStart = QuickStart()
Zendesk = Zendesk()
Workspace = Workspace()
