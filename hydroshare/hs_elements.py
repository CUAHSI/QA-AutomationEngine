from selenium.webdriver.common.by import By

from cuahsi_base.site_element import SiteElement, SiteElementsCollection


class HomePage:
    def __init__(self):
        self.to_home = SiteElement(By.ID, "dropdown-menu-home")
        self.to_my_resources = SiteElement(By.ID, "dropdown-menu-my-resources")
        self.to_discover = SiteElement(By.ID, "dropdown-menu-search")
        self.to_apps = SiteElement(
            By.ID, "dropdown-menu-https:--www.hydroshare.org-apps-"
        )
        self.to_help = SiteElement(
            By.CSS_SELECTOR, 'a[href="{}"]'.format("http://help.hydroshare.org")
        )
        self.to_login = SiteElement(By.CSS_SELECTOR, "#signin-menu a")
        self.to_collaborate = SiteElement(
            By.CSS_SELECTOR, "#dropdown-menu-collaborate a"
        )
        self.profile_image = SiteElement(By.ID, "profile-menu")
        self.profile_button = SiteElement(
            By.CSS_SELECTOR, ".account div.dropdown-footer .btn.btn-primary"
        )
        self.go_up = SiteElement(By.CSS_SELECTOR, ".scrolltotop")
        self.body = SiteElement(By.XPATH, "//body[1]")
        self.scroll_slider_right = SiteElement(
            By.CSS_SELECTOR, ".glyphicon-chevron-right"
        )
        self.scroll_slider_left = SiteElement(
            By.CSS_SELECTOR, ".glyphicon-chevron-left"
        )

        self.slider = SiteElement(By.CSS_SELECTOR, "div.item.parallax-window.active")

        # Links to social media accounts
        self.twitter = SiteElement(
            By.CSS_SELECTOR, ".content.social ul li:nth-child(1) > a"
        )
        self.facebook = SiteElement(
            By.CSS_SELECTOR, ".content.social ul li:nth-child(2) > a"
        )
        self.youtube = SiteElement(
            By.CSS_SELECTOR, ".content.social ul li:nth-child(3) > a"
        )
        self.github = SiteElement(
            By.CSS_SELECTOR, ".content.social ul li:nth-child(4) > a"
        )
        self.linkedin = SiteElement(
            By.CSS_SELECTOR, ".content.social ul li:nth-child(5) > a"
        )

        self.slider = SiteElement(By.CSS_SELECTOR, "div.item.parallax-window.active")
        self.to_site_map = SiteElement(By.LINK_TEXT, "Site Map")

        self.version = SiteElement(By.CSS_SELECTOR, ".content p b")
        self.create = SiteElement(By.ID, "select-resource-type")
        self.signup = SiteElement(By.CSS_SELECTOR, "a.btn-signup")
        self.footer = SiteElement(By.CSS_SELECTOR, "footer")

    def create_type(self, resource_type):
        return SiteElement(By.CSS_SELECTOR, 'a[data-value="{}"]'.format(resource_type))

    def select_resource(self, resource):
        return SiteElement(By.LINK_TEXT, "{}".format(resource))


class AppsPage:
    def __init__(self):
        self.container = SiteElement(*self.apps_container_locator)

    def info(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "div.container.apps-container div.row "
            "div:nth-of-type({}) a.app-info-toggle".format(num),
        )

    def resource(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "div.container.apps-container div.row "
            "div:nth-of-type({}) p.app-description a".format(num),
        )

    def title(self, num):
        return SiteElement(
            By.CSS_SELECTOR,
            "div.container.apps-container "
            "div.row div:nth-of-type({}) h3".format(num),
        )

    @property
    def apps_container_locator(self):
        return By.CSS_SELECTOR, "div.container.apps-container div.row"


class DiscoverPage:
    def __init__(self):
        self.start_date = SiteElement(By.ID, "id_start_date")
        self.end_date = SiteElement(By.ID, "id_end_date")
        self.map_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#map-view"]')
        self.map_search = SiteElement(By.ID, "geocoder-address")
        self.map_submit = SiteElement(By.ID, "geocoder-submit")
        self.list_tab = SiteElement(By.CSS_SELECTOR, 'a[href="#list-view"]')
        self.sort_order = SiteElement(By.ID, "id_sort_order")
        self.sort_direction = SiteElement(By.ID, "id_sort_direction")
        self.col_headers = SiteElement(By.CSS_SELECTOR, "#items-discovered thead tr")
        self.legend = SiteElement(By.CSS_SELECTOR, "#headingLegend h4 a")
        self.legend_labels = SiteElement(
            By.CSS_SELECTOR,
            "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-5",
        )
        self.legend_resources = SiteElement(
            By.CSS_SELECTOR,
            "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-7",
        )
        self.next_page = SiteElement(By.XPATH, '//a[contains(text(), "Next")][1]')
        self.last_updated_by = SiteElement(
            By.XPATH, '//th[text() = "Last updated:"]/following-sibling::td/a'
        )
        self.search = SiteElement(By.ID, "id_q")
        self.show_all = SiteElement(By.ID, "btn-show-all")
        self.user_modal_to_profile = SiteElement(
            By.CSS_SELECTOR,
            ".open > ul:nth-child(2) > li:nth-child(1) > div:nth-child(1) "
            "> div:nth-child(2) > h4:nth-child(1) > a:nth-child(1)",
        )

    def to_resource(self, title):
        return SiteElement(By.XPATH, "//a[contains(text(), '{}')]".format(title))

    def col_index(self, col_index):
        """ Return the column header element, given the index """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered thead tr " "th:nth-of-type({})".format(col_index),
        )

    def cell(self, col, row):
        """
        Return the cell in the discover table, given row and column indicies
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({})".format(row, col),
        )

    def cell_href(self, col, row):
        """
        Return the cell's hyperlink in the discover table, given row and column
        indicies.
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({}) a".format(row, col),
        )

    def cell_strong_href(self, col, row):
        """
        Return the cell's bolded hyperlink in the discover table,
        given row and column indicies.
        """
        return SiteElement(
            By.CSS_SELECTOR,
            "#items-discovered tbody tr:nth-of-type({}) "
            "td:nth-of-type({}) strong a".format(row, col),
        )

    def filter_author(self, author):
        return SiteElement(By.ID, "creator-{}".format(author))

    def filter_contributor(self, author):
        return SiteElement(By.ID, "contributor-{}".format(author))

    def filter_content_type(self, content_type):
        return SiteElement(By.ID, "content_type-{}".format(content_type))

    def filter_subject(self, subject):
        return SiteElement(By.ID, "subject-{}".format(subject))

    def filter_resource_type(self, resource_type):
        return SiteElement(By.ID, "content_type-{}".format(resource_type))

    def filter_owner(self, owner):
        return SiteElement(By.ID, "owner-{}".format(owner))

    def filter_variable(self, variable):
        return SiteElement(By.ID, "variable_name-{}".format(variable))

    def filter_sample_medium(self, sample_medium):
        return SiteElement(By.ID, "sample_medium-{}".format(sample_medium))

    def filter_unit(self, unit):
        return SiteElement(By.ID, "units_name-{}".format(unit))

    def filter_availability(self, availability):
        return SiteElement(By.ID, "availability-{}".format(availability))


class ResourcePage:
    def __init__(self):
        self.bagit = SiteElement(By.ID, "btn-download-all")
        self.open_with = SiteElement(By.ID, "apps-dropdown")
        self.open_jupyterhub = SiteElement(
            By.CSS_SELECTOR, 'li[title="CUAHSI JupyterHub"]'
        )
        self.title = SiteElement(By.ID, "resource-title")
        self.view = SiteElement(By.CSS_SELECTOR, ".glyphicon-circle-arrow-left")
        self.edit_resource = SiteElement(By.ID, "edit-metadata")
        self.add_metadata = SiteElement(By.CSS_SELECTOR, 'a[title="Add New Entry"]')
        self.metadata_name = SiteElement(By.ID, "extra_meta_name_input")
        self.metadata_value = SiteElement(By.ID, "extra_meta_value_input")
        self.confirm_metadata = SiteElement(By.ID, "btn-confirm-extended-metadata")
        self.learn_more = SiteElement(By.PARTIAL_LINK_TEXT, "Learn more")
        self.how_to_cite = SiteElement(
            By.CSS_SELECTOR, "#rights > span:nth-child(2) > a:nth-child(1)"
        )
        self.comment_text = SiteElement(By.CSS_SELECTOR, '#comment textarea')
        self.comment_submit = SiteElement(By.CSS_SELECTOR, 'input[value="Comment"]')
        self.comment_section = SiteElement(By.ID, "comments")

    def open_with_title(self, title):
        return SiteElement(By.XPATH, '//li[@title="{}"]/a'.format(title))

    def name(self, name):
        return SiteElement(By.XPATH, '//td[text()= "{}"]'.format(name))

    def value(self, value):
        return SiteElement(By.XPATH, '//td[text()= "{}"]'.format(value))


class WebAppPage(ResourcePage):
    def __init__(self):
        ResourcePage.__init__()
        self.save_supported_resource_types = SiteElement(
            By.CSS_SELECTOR, "#id-supportedrestypes button.btn-form-submit"
        )
        self.add_open_with = SiteElement(By.ID, "btnOpenWithApp")
        self.app_launching_url = SiteElement(
            By.CSS_SELECTOR, "form#id-requesturlbase input#id_value"
        )
        self.save_app_launching_url = SiteElement(
            By.CSS_SELECTOR, "#id-requesturlbase button.btn-form-submit"
        )

    def supported_resource_type(self, resource_type):
        return SiteElement(By.CSS_SELECTOR, 'input[value="{}"]'.format(resource_type))


class HelpPage:
    def __init__(self):
        self.core_root = SiteElement(By.CSS_SELECTOR, "#content div.row")
        self.core_breadcrumb = SiteElement(By.ID, "breadcrumb-menu-home")
        self.footer_terms = SiteElement(
            By.CSS_SELECTOR, "footer a[href='/terms-of-use']"
        )
        self.footer_privacy = SiteElement(By.CSS_SELECTOR, "footer a[href='/privacy']")
        self.footer_sitemap = SiteElement(By.CSS_SELECTOR, "footer a[href='/sitemap/']")
        self.title = SiteElement(By.CSS_SELECTOR, "h1.page-title")
        self.to_about = SiteElement(
            By.CSS_SELECTOR, 'a[href="{}"]'.format("/about-hydroshare")
        )

    def core_item(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#content "
            "div.row div:nth-of-type({}) "
            "div.topic-name div".format(index),
        )


class AboutPage:
    def __init__(self):
        self.tree_root = SiteElement(
            By.CSS_SELECTOR, "#tree-menu-about-hydroshare div.tree-menu-item i"
        )
        self.article_title = SiteElement(By.CSS_SELECTOR, "h1.page-title")

    def tree_top(self, item):
        return SiteElement(
            By.CSS_SELECTOR,
            "#tree-menu-about-hydroshare "
            "#tree-menu-about-hydroshare-{} "
            "div.tree-menu-item i".format(item),
        )

    def tree_policy(self, item):
        return SiteElement(
            By.CSS_SELECTOR,
            "#tree-menu-about-hydroshare "
            "#tree-menu-about-hydroshare-policies-{} "
            "div.tree-menu-item a".format(item),
        )


class APIPage:
    def __init__(self):
        self.hsapi = SiteElement(By.ID, "endpointListTogger_hsapi")
        self.endpoint_list = SiteElement(
            By.CSS_SELECTOR, "div.opblock-tag-section div:first-child"
        )
        self.try_endpoint = SiteElement(
            By.CSS_SELECTOR, "div.try-out > button.btn:nth-child(1)"
        )
        self.submit = SiteElement(By.CSS_SELECTOR, ".execute")
        self.response_code = SiteElement(
            By.CSS_SELECTOR, ".response_current > td:nth-child(1)"
        )

    def path(self, endpoint):
        return SiteElement(By.CSS_SELECTOR, "#{} > div:nth-child(1)".format(endpoint))

    def parameter(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            ".parameters > tbody:nth-child(2) > tr:nth-child({}) > "
            "td:nth-child(2) > input:nth-child(1)".format(index),
        )


class LoginPage:
    def __init__(self):
        self.username = SiteElement(By.ID, "id_username")
        self.password = SiteElement(By.ID, "id_password")
        self.submit = SiteElement(
            By.CSS_SELECTOR, "input.btn.btn-primary[type='submit']"
        )
        self.error = SiteElement(By.CSS_SELECTOR, ".alert-danger")
        self.notification = SiteElement(
            By.CSS_SELECTOR,
            'div[class="page-tip animated slideInDown"] p'
        )

class ProfilePage:
    def __init__(self):
        self.edit = SiteElement(By.ID, "btn-edit-profile")
        self.add_org = SiteElement(
            By.CSS_SELECTOR, 'input[placeholder="Organization(s)"]'
        )
        self.save = SiteElement(
            By.CSS_SELECTOR, "button.btn-save-profile:first-of-type"
        )
        self.image_upload = SiteElement(By.CSS_SELECTOR, "input.upload-picture")
        self.image = SiteElement(By.CSS_SELECTOR, "div.profile-pic.round-image")
        self.delete_image = SiteElement(By.CSS_SELECTOR, "#btn-delete-profile-pic")
        self.submit_delete_image = SiteElement(By.CSS_SELECTOR, "#picture-clear_id")
        self.add_cv = SiteElement(By.XPATH, '//input[@type="file"]')
        self.view_cv = SiteElement(By.XPATH, '(//a[@class= "btn btn-default"]/span)[3]')
        self.delete_cv = SiteElement(By.ID, "btn-delete-cv")
        self.confirm_delete_cv = SiteElement(By.ID, "cv-clear_id")
        self.contribution = SiteElement(By.CSS_SELECTOR, 'a[aria-controls="profile"]')
        self.contribution_types_breakdown = SiteElement(
            By.CSS_SELECTOR, "table.table-user-contributions tbody"
        )
        self.contributions_list = SiteElement(By.CSS_SELECTOR, "#contributions > .row > .col-md-9")
        self.reset_password = SiteElement(By.XPATH, '//a[contains(text(), "Change password")]')
        self.current_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password"]')
        self.new_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password1"]')
        self.confirm_password = SiteElement(By.CSS_SELECTOR, 'input[id="id_password2"]')
        self.password_confirm = SiteElement(By.XPATH, '//button[contains(text(), "Confirm")]')
        self.description = SiteElement(By.CSS_SELECTOR, 'textarea[name="details"]')
        self.country = SiteElement(By.CSS_SELECTOR, 'select[name="country"]')
        self.province = SiteElement(By.CSS_SELECTOR, 'input[name="state"]')

    def contribution_type(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "table.table-user-contributions tbody tr:nth-of-type({})".format(index + 1),
        )

    def contribution_type_count(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "table.table-user-contributions tbody "
            + "tr:nth-of-type({})".format(index + 1)
            + " td:nth-of-type(2) span",
        )

    def delete_org(self, index):
        return SiteElement(By.CSS_SELECTOR, "span.tag:nth-of-type({}) a".format(index))


class CollaboratePage:
    def __init__(self):
        self.to_groups = SiteElement(By.CSS_SELECTOR, 'a[href="/groups"]')


class GroupsPage:
    def __init__(self):
        self.create_group = SiteElement(
            By.CSS_SELECTOR, 'a[data-target="#create-group-dialog"]'
        )


class GroupPage:
    def __init__(self):
        self.name = SiteElement(By.CSS_SELECTOR, ".group-title")


class NewGroupModal:
    def __init__(self):
        self.name = SiteElement(
            By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(1) textarea"
        )
        self.purpose = SiteElement(
            By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(2) textarea"
        )
        self.about = SiteElement(
            By.CSS_SELECTOR, "fieldset.col-sm-12:nth-child(3) textarea"
        )
        self.public = SiteElement(By.CSS_SELECTOR, 'input[value="public"]')
        self.discoverable = SiteElement(By.CSS_SELECTOR, 'input[value="discoverable"]')
        self.private = SiteElement(By.CSS_SELECTOR, 'input[value="private"]')
        self.submit = SiteElement(By.CSS_SELECTOR, 'button[type="submit"]')


class MyResourcesPage:
    def __init__(self):
        self.resource_type_selector = SiteElement(By.ID, "select-resource-type")
        self.cancel_resource = SiteElement(
            By.CSS_SELECTOR, ".btn-cancel-create-resource"
        )
        self.resource_types = SiteElement(By.CSS_SELECTOR, "#input-resource-type")
        self.search_options = SiteElement(
            By.CSS_SELECTOR, ".btn.btn-default.dropdown-toggle"
        )
        self.search = SiteElement(By.CSS_SELECTOR, "#resource-search-input")
        self.search_author = SiteElement(By.CSS_SELECTOR, "#input-author")
        self.search_subject = SiteElement(By.CSS_SELECTOR, "#input-subject")
        self.clear_search = SiteElement(By.CSS_SELECTOR, "#btn-clear-search-input")
        self.clear_author_search = SiteElement(
            By.CSS_SELECTOR, "#btn-clear-author-input"
        )
        self.clear_subject_search = SiteElement(
            By.CSS_SELECTOR, "#btn-clear-subject-input"
        )
        self.label = SiteElement(By.CSS_SELECTOR, "#btn-label")
        self.create_label = SiteElement(
            By.XPATH, '//li[@data-target="#modalCreateLabel"]'
        )
        self.new_label_name = SiteElement(By.CSS_SELECTOR, "#txtLabelName")
        self.create_label_submit = SiteElement(By.CSS_SELECTOR, "#btn-create-label")
        self.add_label = SiteElement(
            By.CSS_SELECTOR,
            "tr.data-row:nth-child(1) > td:nth-child(1) > "
            + 'span[data-toggle="dropdown"]:nth-child(5)',
        )
        self.manage_labels = SiteElement(
            By.XPATH, '//li[@data-target="#modalManageLabels"]'
        )
        self.remove_label = SiteElement(By.CSS_SELECTOR, ".btn-label-remove")
        self.legend = SiteElement(By.CSS_SELECTOR, "#headingLegend h4 a")
        self.legend_labels = SiteElement(
            By.CSS_SELECTOR,
            "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-5",
        )
        self.legend_resources = SiteElement(
            By.CSS_SELECTOR,
            "#legend-collapse div:first-child div:first-child div.col-xs-12.col-sm-7",
        )

    def label_checkbox(self, label_name):
        return SiteElement(
            By.XPATH,
            '//td[@class="open"]//label[contains(text(), "{}")]'.format(label_name),
        )

    def resource_type(self, option):
        return SiteElement(By.XPATH, '//option[contains(text(), "{}")]'.format(option))

    def resource_creation_type(self, index):
        return SiteElement(
            By.CSS_SELECTOR,
            "#dropdown-resource-type ul li:nth-of-type({})".format(index),
        )


class DashboardPage:
    def __init__(self):
        self.get_started_toggle = SiteElement(By.ID, "id-getting-started-toggle")


class NewResourceModal:
    def __init__(self):
        self.title = SiteElement(By.ID, "input-title")
        self.create = SiteElement(By.ID, "btn-resource-create")
        self.cancel = SiteElement(
            By.CSS_SELECTOR,
            "#submit-title-dialog div.modal-dialog div.modal-content div.modal-footer "
            + "button:nth-of-type(1)",
        )


class RegistrationPage:
    def __init__(self):
        self.first_name = SiteElement(By.ID, "id_first_name")
        self.last_name = SiteElement(By.ID, "id_last_name")
        self.email = SiteElement(By.ID, "id_email")
        self.username = SiteElement(By.ID, "id_username")
        self.organizations = SiteElement(
            By.CSS_SELECTOR, 'input[placeholder="Organization(s)"]'
        )
        self.password1 = SiteElement(By.ID, "id_password1")
        self.password2 = SiteElement(By.ID, "id_password2")
        self.signup = SiteElement(By.ID, "signup")
        self.error = SiteElement(By.CSS_SELECTOR, "p.alert")


class SiteMapPage:
    def all_resource_links(self, driver):
        return SiteElementsCollection(By.CSS_SELECTOR, 'a[href*="/resource"]').items(
            driver
        )


class JupyterHubPage:
    def __init__(self):
        self.login = SiteElement(By.CSS_SELECTOR, "#login-main > div > a")
        self.authorize = SiteElement(By.CSS_SELECTOR, 'input[value="Authorize"]')
        self.scientific_spawner = SiteElement(By.ID, 'profile-item-1')
        self.spawn = SiteElement(By.CSS_SELECTOR, 'input[value="Spawn"]')

class JupyterHubNotebooks:
    def __init__(self):
        self.sort_name = SiteElement(By.ID, 'sort-name')

HomePage = HomePage()
AppsPage = AppsPage()
DiscoverPage = DiscoverPage()
ResourcePage = ResourcePage()
WebAppPage = WebAppPage()
HelpPage = HelpPage()
AboutPage = AboutPage()
APIPage = APIPage()
LoginPage = LoginPage()
ProfilePage = ProfilePage()
CollaboratePage = CollaboratePage()
GroupsPage = GroupsPage()
GroupPage = GroupPage()
NewGroupModal = NewGroupModal()
MyResourcesPage = MyResourcesPage()
DashboardPage = DashboardPage()
NewResourceModal = NewResourceModal()
RegistrationPage = RegistrationPage()
SiteMapPage = SiteMapPage()
JupyterHubPage = JupyterHubPage()
JupyterHubNotebooks = JupyterHubNotebooks()