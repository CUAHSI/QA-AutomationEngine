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
    def scroll_map(self, driver, count=1):
        """ Make a large scroll with the map {{count}} times to the
        right
        """
        SearchPage.map_area.click(driver, SLEEP_TIME)
        for i in range(0, count):
            SearchPage.map_area.scroll_right(driver, SLEEP_TIME/count)

    def to_workspace(self, driver):
        """ Navigate to the Workspace using the button at the top of
        the search interface
        """
        SearchPage.workspace.click(driver, SLEEP_TIME)

    def to_quickstart(self, driver):
        """ Open the Quick Start modal using the button at the top of
        the search interface
        """
        SearchPage.quickstart.click(driver, SLEEP_TIME)

    def is_legend_visible(self, driver):
        """ Click on the legend tab, within the search interface sidebar """
        SearchPage.legend_tab.click(driver, SLEEP_TIME)
        # TODO Clean up below
        legend_vis = SearchPage.legend_img.get_attribute(driver, 'style')
        legend_vis = legend_vis.split(':')[-1]
        legend_vis = legend_vis.split(';')[0]
        legend_vis = legend_vis.split(' ')[-1]
        SearchPage.search_tab.click(driver, SLEEP_TIME)
        return legend_vis != 'none'

    def search(self, driver, count=1):
        """ Press the Search Now button {{count}} time(s) """
        for i in range(0, count):
            SearchPage.search.click(driver, SLEEP_TIME)

    def toggle_layer(self, driver, layer_name):
        """ Turn on the {{layer_name}} layer using the map search interface
        dropdown
        """
        SearchPage.layers.click(driver, SLEEP_TIME)
        SearchPage.layer(layer_name).click(driver, SLEEP_TIME)

    def to_map_marker(self, driver, results_count):
        """ Click on the map marker which displays {{results_count}}
        number of results
        """
        SearchPage.map_marker(results_count).click(driver, SLEEP_TIME)

    def search_location(self, driver, location):
        """ Use the search field to search for {{location}}, then click
        the first item in the dropdown of suggestions
        """
        SearchPage.map_search.click(driver, SLEEP_TIME)
        SearchPage.map_search.clear_all_text(driver, SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, location, SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, Keys.ARROW_DOWN, SLEEP_TIME)
        SearchPage.map_search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        time.sleep(SLEEP_TIME)

    def count_results(self, driver):
        """ Check the number of results using the "Time Series Found"
        area of the sidebar
        """
        return SearchPage.results_count.get_text(driver)

    def filter_dates(self, driver, start_date, end_date):
        """ Use the "Date Range" option when doing a map search to filter
        results.  Use the start date of {{start_date}} and the end date
        of {{end_date}}
        """
        SearchPage.date_filter.click(driver, SLEEP_TIME)
        SearchPage.date_start.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_start.inject_text(driver, start_date, SLEEP_TIME)
        SearchPage.date_clickout.passive_click(driver, SLEEP_TIME)
        SearchPage.date_end.clear_text(driver, 12, SLEEP_TIME)
        SearchPage.date_end.inject_text(driver, end_date, SLEEP_TIME)
        SearchPage.date_save.click(driver, SLEEP_TIME)
        SearchPage.search.click(driver, SLEEP_TIME)

    def reset(self, driver):
        """ Press the reset button in the sidebar """
        SearchPage.reset.click(driver, SLEEP_TIME)

    def zoom_in(self, driver, count=1):
        """ Use the + button on the map interface to zoom in {{count}} times
        """
        for i in range(0, count):
            SearchPage.zoom_in.click(driver, SLEEP_TIME)


class Marker:
    def to_workspace_all(self, driver):
        """ Export all these results to the workspace by selecting all
        results, clicking "Select Action", and then selecting the workspace
        export option
        """
        MarkerModal.sort('Data Type').click(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).click(driver, SLEEP_TIME)
        MarkerModal.sort('Data Type').click(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).scroll_to(driver, SLEEP_TIME)
        MarkerModal.cell(1, 1).range_click(driver, SLEEP_TIME)
        MarkerModal.action.click(driver, SLEEP_TIME)
        MarkerModal.to_workspace.click(driver, SLEEP_TIME)
        MarkerModal.workspace.click(driver, SLEEP_TIME)


class Services:
    def filters(self, driver, orgs=None, titles=None):
        """ Click on the "Data Services" button to open the service filtering
        capabilities.  Next, filter the search results by multi-selecting
        the {{org}} organization(s) and the {{titles}} titles
        """
        SearchPage.services.click(driver, SLEEP_TIME)
        ServicesModal.table_count.select_option(driver, '100', SLEEP_TIME)
        ServicesModal.sort_org.click(driver, SLEEP_TIME)
        if type(orgs) is list:
            for org in orgs:
                ServicesModal.select_org(org).scroll_to(driver, SLEEP_TIME)
                ServicesModal.select_org(org).multi_click(driver, SLEEP_TIME)
        elif orgs is not None:
            ServicesModal.select_org(orgs).click(driver, SLEEP_TIME)
        if type(titles) is list:
            for title in titles:
                ServicesModal.select_title(title).scroll_to(driver, SLEEP_TIME)
                ServicesModal.select_title(title).multi_click(driver, SLEEP_TIME)
        elif titles is not None:
            ServicesModal.select_title(titles).click(driver, SLEEP_TIME)
        ServicesModal.save.click(driver, SLEEP_TIME)
        SearchPage.search.click(driver, SLEEP_TIME)
        time.sleep(10)


class Keywords:
    def filter_root(self, driver, keywords):
        """ Filter the search results using the keywords filter.  Navigate
        to the "full list" tab, then click the checkboxes for the
        {{keywords}} keywords, which are at the "root" keywords level.
        Click the "Search" button at the bottom of the modal to confirm
        the filtering
        """
        SearchPage.keywords.click(driver, SLEEP_TIME)
        KeywordsModal.full_list.click(driver, SLEEP_TIME)
        for keyword in keywords:
            KeywordsModal.full_list_checkbox(keyword).click(driver, SLEEP_TIME)
        KeywordsModal.search.click(driver, SLEEP_TIME)


class Advanced:
    def filter_all_value_types(self, driver):
        """ Navigate to the advanced search modal, then select all the
        "value type" rows on the associated tab.  Click the "Search"
        button at the bottom of the modal to confirm the filtering
        """
        SearchPage.advanced.click(driver, SLEEP_TIME)
        AdvancedModal.value_type.click(driver, SLEEP_TIME)
        AdvancedModal.value_type_sort('Term').click(driver, SLEEP_TIME)
        AdvancedModal.value_type_cell(1, 1).click(driver, SLEEP_TIME)
        AdvancedModal.value_type_sort('Term').click(driver, SLEEP_TIME)
        AdvancedModal.value_type_cell(1, 1).range_click(driver, SLEEP_TIME)
        AdvancedModal.search.click(driver, SLEEP_TIME)


class Filter:
    def to_workspace_cell(self, driver, row, col):
        """ Click on the "Filter Results" button.  Then, click on the
        cell in the {{row}} row and {{col}} column, then
        click "Select Action" and choose the workspace option
        """
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.close.scroll_to(driver, SLEEP_TIME)
        FilterModal.cell(row, col).click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    def to_workspace_texts_range(self, driver, texts):
        """ Click on the "Filter Results" button.  Find a cell which
        contains the text in the first item of this list: {{texts}}.
        Next, find a cell which contains the text in the
        second imem of this list: {{texts}}.  Click the first cell, then
        hold the Shift key and click the second cell.  Finally, click
        "Select Tool" and choose the workspace export option
        """
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.cell_text(texts[0]).click(driver, SLEEP_TIME)
        FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
        FilterModal.cell_text(texts[1]).scroll_to(driver, SLEEP_TIME)
        FilterModal.cell_text(texts[1]).multi_click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    def to_workspace_text(self, driver, text):
        """ Click on the "Filter Results" button.  Then, find a cell
        which contains the text {{text}} and click on it.  Next, click
        on "Select Tool" and choose the workspace option
        """
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.cell_text(text).click(driver, SLEEP_TIME)
        FilterModal.action.click(driver, SLEEP_TIME)
        FilterModal.to_workspace.click(driver, SLEEP_TIME)
        FilterModal.workspace.click(driver, SLEEP_TIME)

    def search_field(self, driver, search_string):
        """ Click on the "Filter Results" button.  Then, use the table
        search field to search for {{search_string}}.  Then, close the
        modal window
        """
        SearchPage.map_filter.click(driver, SLEEP_TIME)
        FilterModal.search.inject_text(driver, search_string, SLEEP_TIME)
        FilterModal.sort('Service Title').click(driver, SLEEP_TIME)
        FilterModal.count.select_option(driver, '100', SLEEP_TIME)
        FilterModal.close.click(driver, SLEEP_TIME)


class About:
    def to_helpcenter(self, driver):
        """ Navigate to the Help Center, by using the About button
        at the top of the page
        """
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.helpcenter.click(driver, SLEEP_TIME)

    def to_license_repo_top(self, driver):
        """ Open the License Agreement using the About button at the top of
        the page, then click on the GitHub repository link near the top
        of the modal
        """
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.licensing.click(driver, SLEEP_TIME)
        AboutModal.license_repo_top.click(driver, SLEEP_TIME)
        AboutModal.licensing_close.click(driver, SLEEP_TIME)

    def to_license_repo_inline(self, driver):
        """ Open the License Agreement using the About button at the top of
        the page, then click on the GitHub repository link that is inline
        with the paragraph content of the modal
        """
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.licensing.click(driver, SLEEP_TIME)
        AboutModal.license_repo_inline.click(driver, SLEEP_TIME)
        AboutModal.licensing_close.click(driver, SLEEP_TIME)

    def to_contact(self, driver):
        """ Open the contact modal using the About button at the top of
        the page, then click on the need additional help button and
        close the modal
        """
        SearchPage.about.click(driver, SLEEP_TIME)
        AboutModal.contact.click(driver, SLEEP_TIME)
        AboutModal.contact_help.click(driver, SLEEP_TIME)
        AboutModal.contact_close.click(driver, SLEEP_TIME)


class QuickStart:
    def section(self, driver, help_item):
        """ Open the Quick Start section labeled {{help_item}} """
        QuickStartModal.section(help_item).click(driver, SLEEP_TIME)

    def more(self, driver, link_text):
        """ Use the Quick Start link {{link_text}} to open up a
        page with more information on the topic
        """
        QuickStartModal.more(link_text).click(driver, SLEEP_TIME)


class Zendesk:
    def to_help(self, driver, search_text, article_text):
        """ Use the ZenDesk widget to search for {{search_text}}.  Click
        on the {{article_text}} option and click on the link to open the
        page in a new window
        """
        SearchPage.zendesk.iframe_in(driver)
        ZendeskWidget.helping.click(driver, SLEEP_TIME)
        SearchPage.zendesk.iframe_out(driver)
        ZendeskWidget.results.iframe_in(driver)
        ZendeskWidget.search.inject_text(driver, search_text, SLEEP_TIME)
        ZendeskWidget.search.inject_text(driver, Keys.RETURN, SLEEP_TIME)
        ZendeskWidget.pull(article_text).click(driver, SLEEP_TIME)
        ZendeskWidget.more.scroll_to(driver, SLEEP_TIME)
        ZendeskWidget.more.click(driver, SLEEP_TIME)


class Workspace:
    def select_all(self, driver):
        """ Select all the items in the workspace using the selection
        dropdown
        """
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_all.click(driver, SLEEP_TIME)

    def clear_select(self, driver):
        """ Clear all workspace selections using the selection dropdown """
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_clear.click(driver, SLEEP_TIME)

    def remove_select(self, driver):
        """ Remove all the selected workspace rows by using the selection
        dropdown
        """
        WorkspacePage.select_dropdown.passive_click(driver, SLEEP_TIME)
        WorkspacePage.select_delete.click(driver, SLEEP_TIME)

    def to_csv(self, driver):
        """ Open the tools dropdown and choose the option to generate
        a CSV file
        """
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_csv.click(driver, SLEEP_TIME)

    def to_viewer(self, driver):
        """ Open the tools dropdown and choose the option to explore
        the data using the Data Viewer
        """
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_viewer.click(driver, SLEEP_TIME)

    def to_none(self, driver):
        """ Open the tools dropdown and choose the "None" option """
        WorkspacePage.tools.passive_click(driver, SLEEP_TIME)
        WorkspacePage.to_none.click(driver, SLEEP_TIME)

    def count_complete(self, driver, time_mult):
        """ Check the number of rows in the workspace which are processed
        and show a status of "Completed"
        """
        time.sleep(time_mult*SLEEP_TIME)
        return driver.page_source.count('<em> Completed</em>')

    def is_in_results(self, driver, strings, time_mult):
        """ Check the table to see if the text(s) {{strings}} are present
        somewhere in the cells
        """
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
