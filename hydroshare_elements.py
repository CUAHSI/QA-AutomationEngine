from site_element import SiteElement

class HomePage:
    def __init__(self):
        self.discover_tab = SiteElement('li', el_id='dropdown-menu-search')

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

class ResourceLanding:
    def __init__(self):
        self.download_bagit = SiteElement('a', el_id='btn-download-all', el_content='Download All Content as Zipped BagIt Archive')

HomePage = HomePage()
DiscoverPage = DiscoverPage()
ResourceLanding = ResourceLanding()

