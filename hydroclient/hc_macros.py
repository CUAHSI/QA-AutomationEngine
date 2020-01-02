import time
import re

from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

from hc_elements import (
    SearchPage,
    MarkerModal,
    ServicesModal,
    KeywordsModal,
    AdvancedModal,
    FilterModal,
    AboutModal,
    QuickStartModal,
    ZendeskWidget,
    WorkspacePage,
    ResourceCreatorPage,
)
from timing import (
    WORKSPACE_CREATE_ARCHIVE,
    SEARCH_IN_PROGRESS,
    SEARCH_AUTOCOMPLETE,
    WORKSPACE_TOOLTIP_DISAPPEAR,
    MODAL_FADE,
    RESULTS_MULTISELECT,
    APP_INITIALIZATION,
)


class Search:
    def scroll_map(self, driver, count=1):
        """ Make a large scroll with the map {{count}} times to the
        right
        """
        SearchPage.map_area.click(driver)
        for i in range(0, count):
            SearchPage.map_area.scroll_right(driver)

    def to_workspace(self, driver):
        """ Navigate to the Workspace using the button at the top of
        the search interface
        """
        SearchPage.workspace.click(driver)

    def to_quickstart(self, driver):
        """ Open the Quick Start modal using the button at the top of
        the search interface
        """
        SearchPage.quickstart.click(driver)

    def is_legend_visible(self, driver):
        """ Click on the legend tab, within the search interface sidebar """
        SearchPage.legend_tab.click(driver)
        return SearchPage.legend_img.is_visible(driver)

    def search(self, driver, count=1):
        """ Press the Search Now button {{count}} time(s) """
        for i in range(0, count):
            SearchPage.search.click(driver)
            time.sleep(SEARCH_IN_PROGRESS)

    def toggle_layer(self, driver, layer_name):
        """ Turn on the {{layer_name}} layer using the map search interface
        dropdown
        """
        SearchPage.layers.click(driver)
        SearchPage.layer(layer_name).click(driver)

    def to_random_map_marker(self, driver):
        """ Click on a map marker """
        marker_sizes = [22, 24, 28, 32]
        for marker_size in marker_sizes:
            try:
                SearchPage.random_map_marker(marker_size).click(driver)
                break
            except TimeoutException:
                continue

    def search_location(self, driver, location):
        """ Use the search field to search for {{location}}, then click
        the first item in the dropdown of suggestions
        """
        SearchPage.map_search.click(driver)
        SearchPage.map_search.clear_all_text(driver)
        SearchPage.map_search.inject_text(driver, location)
        time.sleep(SEARCH_AUTOCOMPLETE)
        SearchPage.map_search.inject_text(driver, Keys.ARROW_DOWN)
        SearchPage.map_search.inject_text(driver, Keys.RETURN)
        time.sleep(SEARCH_IN_PROGRESS)

    def count_results(self, driver):
        """ Check the number of results using the "Time Series Found"
        area of the sidebar
        """
        results_count = SearchPage.results_count.get_text(driver)
        # Account for multiple localization settings with respect to thousands
        # separator.  Safe since results count will always be integer.
        results_count = re.sub("[,]", "", results_count)
        results_count = re.sub("[.]", "", results_count)
        return int(results_count)

    def filter_dates(self, driver, start_date, end_date):
        """ Use the "Date Range" option when doing a map search to filter
        results.  Use the start date of {{start_date}} and the end date
        of {{end_date}}
        """
        SearchPage.date_filter.click(driver)
        SearchPage.date_start.clear_text(driver, 12)
        SearchPage.date_start.inject_text(driver, start_date)
        SearchPage.date_start.inject_text(driver, Keys.TAB)
        SearchPage.date_end.clear_text(driver, 12)
        SearchPage.date_end.inject_text(driver, end_date)
        SearchPage.date_start.inject_text(driver, Keys.TAB)
        SearchPage.date_save.click(driver)
        WebDriverWait(driver, MODAL_FADE + 1).until_not(
            EC.visibility_of_element_located(SearchPage.modal_fade_locator)
        )
        Search.search(driver)

    def clear_date_filter(self, driver):
        """ Clears any date filters with an "All Dates" selection """
        SearchPage.all_dates.click(driver)

    def reset(self, driver):
        """ Press the reset button in the sidebar """
        SearchPage.reset.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)

    def zoom_in(self, driver, count=1):
        """ Use the + button on the map interface to zoom in {{count}} times
        """
        for i in range(0, count):
            SearchPage.zoom_in.click(driver)

    def dismiss_no_results(self, driver):
        SearchPage.no_results_ok.click(driver)
        time.sleep(MODAL_FADE)

    def get_searchbox_text(self, driver):
        return SearchPage.map_search.get_attribute(driver, "value")

    def hybrid(self, driver):
        return SearchPage.hybrid.click(driver)

    def show_hide_panel(self, driver):
        SearchPage.show_hide_panel.click(driver)


class Marker:
    def to_workspace_all(self, driver):
        """ Export all these results to the workspace by selecting all
        results, clicking "Select Action", and then selecting the workspace
        export option
        """
        MarkerModal.table_count.select_option(driver, "100")
        MarkerModal.cell(1, 1).scroll_to(driver)
        MarkerModal.cell(1, 1).click(driver)
        MarkerModal.cell_last_row(1).scroll_to(driver)
        MarkerModal.cell_last_row(1).range_click(driver)
        MarkerModal.action.click(driver)
        MarkerModal.to_workspace.click(driver)
        MarkerModal.workspace.click(driver)

    def to_workspace_one(self, driver):
        MarkerModal.cell(1, 1).click(driver)
        MarkerModal.action.click(driver)
        MarkerModal.to_workspace.click(driver)
        MarkerModal.workspace.click(driver)


class Services:
    def filters(self, driver, orgs=None, titles=None, non_gridded_only=False):
        """ Click on the "Data Services" button to open the service filtering
        capabilities.  Next, filter the search results by multi-selecting
        the {{org}} organization(s) and the {{titles}} titles
        """
        SearchPage.services.click(driver)
        ServicesModal.table_count.select_option(driver, "100")
        ServicesModal.sort_org.click(driver)
        if type(orgs) is list:
            for org in orgs:
                ServicesModal.select_org(org).scroll_to(driver)
                ServicesModal.select_org(org).multi_click(driver)
        elif orgs is not None:
            ServicesModal.select_org(orgs).click(driver)
        if type(titles) is list:
            for title in titles:
                ServicesModal.select_title(title).scroll_to(driver)
                ServicesModal.select_title(title).multi_click(driver)
        elif titles is not None:
            ServicesModal.select_title(titles).click(driver)
        if non_gridded_only:
            ServicesModal.select_all_non_gridded.click(driver)
        ServicesModal.save.click(driver)
        WebDriverWait(driver, MODAL_FADE).until_not(
            EC.visibility_of_element_located(SearchPage.modal_fade_locator)
        )
        Search.search(driver)

    def search(self, driver, search_text, result_num):
        """ Click on the "Data Services" button to open the service filtering
        capabilities.  Next, use the searchbar and select a result from the list
        using result_num as the desired row index
        """
        SearchPage.services.click(driver)
        ServicesModal.input_search.inject_text(driver, search_text)
        ServicesModal.select_item_num("{}".format(result_num)).passive_click(driver)
        ServicesModal.search.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)

    def select_result(self, driver, num):
        ServicesModal.select_item_num(num).click(driver)

    def empty_services(self, driver):
        SearchPage.services.click(driver)
        ServicesModal.save.click(driver)
        time.sleep(MODAL_FADE)


class Keywords:
    def filter_root(self, driver, keywords):
        """ Filter the search results using the keywords filter.  Navigate
        to the "full list" tab, then click the checkboxes for the
        {{keywords}} keywords, which are at the "root" keywords level.
        Click the "Search" button at the bottom of the modal to confirm
        the filtering
        """
        SearchPage.keywords.click(driver)
        KeywordsModal.full_list.click(driver)
        for keyword in keywords:
            KeywordsModal.full_list_checkbox(keyword).click(driver)
        KeywordsModal.search.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)

    def empty_keywords(self, driver):
        SearchPage.keywords.click(driver)
        KeywordsModal.save.click(driver)
        time.sleep(MODAL_FADE)


class Advanced:
    def filter_all_value_types(self, driver):
        """ Navigate to the advanced search modal, then select all the
        "value type" rows on the associated tab.  Click the "Search"
        button at the bottom of the modal to confirm the filtering
        """
        SearchPage.advanced.click(driver)
        AdvancedModal.value_type.click(driver)
        AdvancedModal.value_type_sort("Term").click(driver)
        AdvancedModal.value_type_cell(1, 1).click(driver)
        AdvancedModal.value_type_sort("Term").click(driver)
        AdvancedModal.value_type_cell(1, 1).range_click(driver)
        AdvancedModal.search.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)

    def empty_advanced(self, driver):
        SearchPage.advanced.click(driver)
        AdvancedModal.save.click(driver)
        time.sleep(MODAL_FADE)


class Filter:
    def count_results(self, driver):
        results_info = FilterModal.info.get_text(driver)
        results_info = results_info.replace(",", "")
        nums = re.findall(r"\d+", results_info)
        return nums

    def empty_filters(self, driver):
        SearchPage.map_filter.click(driver)
        FilterModal.close.click(driver)
        time.sleep(MODAL_FADE)

    def open(self, driver):
        SearchPage.map_filter.click(driver)

    def close(self, driver):
        FilterModal.close.click(driver)
        time.sleep(MODAL_FADE)

    def to_workspace_cell(self, driver, row, col):
        """ Click on the "Filter Results" button.  Then, click on the
        cell in the {{row}} row and {{col}} column, then
        click "Select Action" and choose the workspace option
        """
        FilterModal.count.select_option(driver, "100")
        FilterModal.close.scroll_to(driver)
        FilterModal.cell(row, col).click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def to_workspace_cell_range(self, driver, first_row, last_row):
        """ Select a range of rows from the Filter Results modal """
        FilterModal.count.select_option(driver, "100")
        FilterModal.cell(first_row, 3).scroll_to(driver)
        FilterModal.cell(first_row, 3).click(driver)
        FilterModal.cell(last_row, 3).scroll_to(driver)
        FilterModal.cell(last_row, 3).range_click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.scroll_to(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def to_workspace_cell_multi(self, driver, rows):
        """ Select multiple rows within Filter Results modal """
        FilterModal.count.select_option(driver, "100")
        FilterModal.cell(rows[0], 3).scroll_to(driver)
        FilterModal.cell(rows[0], 3).click(driver)
        for i in range(1, len(rows)):
            FilterModal.cell(rows[i], 3).scroll_to(driver)
            time.sleep(RESULTS_MULTISELECT)
            FilterModal.cell(rows[i], 3).multi_click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def to_workspace_texts_range(self, driver, texts):
        """ Click on the "Filter Results" button.  Find a cell which
        contains the text in the first item of this list: {{texts}}.
        Next, find a cell which contains the text in the
        second imem of this list: {{texts}}.  Click the first cell, then
        hold the Shift key and click the second cell.  Finally, click
        "Select Tool" and choose the workspace export option
        """
        FilterModal.count.select_option(driver, "100")
        FilterModal.cell_text(texts[0]).click(driver)
        FilterModal.sort("Service Title").click(driver)
        FilterModal.cell_text(texts[1]).scroll_to(driver)
        FilterModal.cell_text(texts[1]).multi_click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def to_workspace_text(self, driver, text):
        """ Click on the "Filter Results" button.  Then, find a cell
        which contains the text {{text}} and click on it.  Next, click
        on "Select Tool" and choose the workspace option
        """
        FilterModal.count.select_option(driver, "100")
        FilterModal.cell_text(text).click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def search_field(self, driver, search_string):
        """ Click on the "Filter Results" button.  Then, use the table
        search field to search for {{search_string}}.  Then, close the
        modal window
        """
        FilterModal.search.inject_text(driver, search_string)
        time.sleep(SEARCH_AUTOCOMPLETE)
        FilterModal.sort("Service Title").click(driver)
        FilterModal.count.select_option(driver, "100")

    def to_workspace_all(self, driver):
        """ Select all the results in the Filter Results dialog, then
        export them to the workspace """
        FilterModal.selections.click(driver)
        FilterModal.select_all.click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        FilterModal.workspace.click(driver)

    def complex_selection_to_workspace(self, driver, double=False, to_workspace=False):
        """ Use double click for workspace selections,
        instead of single click selections,
        due to issues with single-click selection of large result sets
        """
        FilterModal.selections.click(driver)
        FilterModal.selections.scroll_to(driver)
        if double:
            FilterModal.select_all.double_click(driver)
        else:
            FilterModal.select_all.click(driver)
        FilterModal.action.click(driver)
        FilterModal.to_workspace.click(driver)
        if to_workspace:
            FilterModal.workspace.click(driver)

    def show_25(self, driver):
        FilterModal.count.select_option(driver, "25")

    def selection(self, driver):
        FilterModal.selections.click(driver)
        FilterModal.select_all.click(driver)

    def find_in_table(self, driver, text):
        FilterModal.find_in_table.inject_text(driver, text)
        time.sleep(SEARCH_IN_PROGRESS)
        FilterModal.close.click(driver)
        time.sleep(MODAL_FADE)

    def set_data_props(self, driver, data_props):
        data_props_list = FilterModal.data_props_list
        count_data_props = data_props_list.get_immediate_child_count(driver)
        for i in range(0, count_data_props):
            checkbox_label = FilterModal.data_prop_list_label(i).get_text(driver)
            if checkbox_label in data_props:
                FilterModal.data_prop_list_checkbox(i).click(driver)
        FilterModal.apply_filters.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)
        FilterModal.close.click(driver)
        time.sleep(MODAL_FADE)

    def data_prop_is_selected(self, driver, prop):
        data_props_list = FilterModal.data_props_list
        count_data_props = data_props_list.get_immediate_child_count(driver)
        for i in range(0, count_data_props):
            checkbox_label = FilterModal.data_prop_list_label(i).get_text(driver)
            if checkbox_label == prop:
                aria_selected = FilterModal.data_prop_list_entry(i).get_attribute(
                    driver, "aria-selected"
                )
                return aria_selected == "true"
        return False

    def set_data_services(self, driver, data_services):
        data_services_list = FilterModal.data_services_list
        count_data_services = data_services_list.get_immediate_child_count(driver)
        for i in range(0, count_data_services):
            checkbox_label = FilterModal.data_service_list_label(i).get_text(driver)
            if checkbox_label in data_services:
                FilterModal.data_service_list_checkbox(i).click(driver)
        FilterModal.apply_filters.click(driver)
        time.sleep(SEARCH_IN_PROGRESS)
        FilterModal.close.click(driver)
        time.sleep(MODAL_FADE)

    def data_service_is_selected(self, driver, service):
        data_services_list = FilterModal.data_services_list
        count_data_services = data_services_list.get_immediate_child_count(driver)
        for i in range(0, count_data_services):
            checkbox_label = FilterModal.data_service_list_label(i).get_text(driver)
            if checkbox_label == service:
                aria_selected = FilterModal.data_service_list_entry(i).get_attribute(
                    driver, "aria-selected"
                )
                return aria_selected == "true"
        return False

    def ok_is_visible(self, driver):
        if FilterModal.ok:
            return True
        else:
            return False

    def apply_filters(self, driver):
        return FilterModal.apply_filters.click(driver)


class About:
    def to_helpcenter(self, driver):
        """ Navigate to the Help Center, by using the About button
        at the top of the page
        """
        SearchPage.about.click(driver)
        AboutModal.helpcenter.click(driver)

    def to_license_repo_top(self, driver):
        """ Open the License Agreement using the About button at the top of
        the page, then click on the GitHub repository link near the top
        of the modal
        """
        SearchPage.about.click(driver)
        AboutModal.licensing.click(driver)
        AboutModal.license_repo_top.click(driver)

    def to_license_repo_inline(self, driver):
        """ Open the License Agreement using the About button at the top of
        the page, then click on the GitHub repository link that is inline
        with the paragraph content of the modal
        """
        SearchPage.about.click(driver)
        AboutModal.licensing.click(driver)
        AboutModal.license_repo_inline.click(driver)

    def licensing_close(self, driver):
        AboutModal.licensing_close.click(driver)
        WebDriverWait(driver, MODAL_FADE).until_not(
            EC.visibility_of_element_located(SearchPage.modal_fade_locator)
        )

    def to_contact(self, driver):
        """ Open the contact modal using the About button at the top of
        the page, then click on the need additional help button and
        close the modal
        """
        SearchPage.about.click(driver)
        AboutModal.contact.click(driver)
        AboutModal.contact_help.click(driver)

    def contact_close(self, driver):
        AboutModal.contact_close.click(driver)
        WebDriverWait(driver, MODAL_FADE).until_not(
            EC.visibility_of_element_located(SearchPage.modal_fade_locator)
        )


class QuickStart:
    def section(self, driver, help_item):
        """ Open the Quick Start section labeled {{help_item}} """
        QuickStartModal.section(help_item).click(driver)

    def more(self, driver, link_text):
        """ Use the Quick Start link {{link_text}} to open up a
        page with more information on the topic
        """
        QuickStartModal.more(link_text).click(driver)


class Zendesk:
    def to_help(self, driver, search_text, article_text):
        """ Use the ZenDesk widget to search for {{search_text}}.  Click
        on the {{article_text}} option and click on the link to open the
        page in a new window
        """
        SearchPage.zendesk.click(driver)
        ZendeskWidget.results.iframe_in(driver)
        ZendeskWidget.search.inject_text(driver, search_text)
        ZendeskWidget.search.inject_text(driver, Keys.RETURN)
        ZendeskWidget.pull(article_text).click(driver)
        ZendeskWidget.more.scroll_to(driver)
        ZendeskWidget.more.click(driver)


class Workspace:
    def select_all(self, driver):
        """ Select all the items in the workspace using the selection
        dropdown
        """
        WorkspacePage.select_dropdown.passive_click(driver)
        WorkspacePage.select_all.click(driver)

    def clear_select(self, driver):
        """ Clear all workspace selections using the selection dropdown """
        WorkspacePage.select_dropdown.passive_click(driver)
        WorkspacePage.select_clear.click(driver)

    def remove_select(self, driver):
        """ Remove all the selected workspace rows by using the selection
        dropdown
        """
        WorkspacePage.select_dropdown.passive_click(driver)
        WorkspacePage.select_delete.click(driver)

    def to_csv(self, driver):
        """ Open the tools dropdown and choose the option to generate
        a CSV file
        """
        WorkspacePage.tools.passive_click(driver)
        WebDriverWait(driver, WORKSPACE_TOOLTIP_DISAPPEAR).until_not(
            EC.visibility_of_element_located(WorkspacePage.tooltip_locator)
        )
        WorkspacePage.to_csv.click(driver)

    def to_viewer(self, driver):
        """ Open the tools dropdown and choose the option to explore
        the data using the Data Viewer """
        WorkspacePage.tools.passive_click(driver)
        WorkspacePage.to_viewer.click(driver)

    def to_hydroshare(self, driver):
        """ Open the tools dropdown and choose the option to
        Export to HydroShare """
        WorkspacePage.tools.passive_click(driver)
        WorkspacePage.to_hydroshare.click(driver)

    def launch_tool(self, driver):
        """ Click on the Launch Tool button """
        WorkspacePage.launch_tool.passive_click(driver)

    def to_none(self, driver):
        """ Open the tools dropdown and choose the "None" option """
        WorkspacePage.tools.passive_click(driver)
        WorkspacePage.to_none.click(driver)

    def count_complete(self, driver, wait_multiplier=1):
        """ Check the number of rows in the workspace which are processed
        and show a status of "Completed"
        """
        time.sleep(WORKSPACE_CREATE_ARCHIVE * wait_multiplier)
        return driver.page_source.count("<em> Completed</em>")

    def is_in_results(self, driver, strings, time_mult):
        """ Check the table to see if the text(s) {{strings}} are present
        somewhere in the cells
        """
        if type(strings) is list:
            for string in strings:
                if string not in driver.page_source:
                    return False
        elif strings is not None:
            if strings not in driver.page_source:
                return False
        return True

    def launch_is_disabled(self, driver):
        return FilterModal.launch_tool.get_attribute(driver, "disabled") is None


class ResourceCreator:
    def create_resource(self, driver):
        """ Clicks on the Create Time Series Resource button """
        time.sleep(APP_INITIALIZATION)
        ResourceCreatorPage.create_time_resource.click(driver)

    def is_initialized(self, driver):
        return ResourceCreatorPage.login_button.is_visible(self.driver)


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
ResourceCreator = ResourceCreator()
