""" Creates an XML of test cases for executor bidding """

CONFIG_FILE = '../../config.org'
XML_FILE = 'auction_page/templates/auctions.xml'

class TestCase:
    """ Test case class for storing status and env information """

    def __init__(self, test_id=None, status=None, op_sys=None, browser=None):
        self.test_id = test_id
        self.status = status
        self.op_sys = op_sys
        self.browser = browser

    def pull_os(self, line_with_os):
        """ Parse config file line and set OS property """
        strings_to_remove = ['***', ' ', '{', '}', '[', ']']
        for string_to_remove in strings_to_remove:
            line_with_os = line_with_os.replace(string_to_remove, '')
        first_split = line_with_os.split('OS:')[-1]
        second_split = first_split.split(',BROWSER:')
        print('OS', second_split[0].split(',')[0:-1])
        self.op_sys = second_split[0].split(',')[0:-1]

    def pull_browser(self, line_with_browser):
        """ Parse config file line and set browser property """
        strings_to_remove = ['***', ' ', '{', '}', '[', ']']
        for string_to_remove in strings_to_remove:
            line_with_browser = line_with_browser.replace(string_to_remove, '')
        first_split = line_with_browser.split('OS:')[-1]
        second_split = first_split.split(',BROWSER:')
        print('Browser', second_split[-1].split(',')[0:-1])
        self.browser = second_split[-1].split(',')[0:-1]

    def pull_id(self, line_with_id):
        """ Parse config file line and set id property """
        space_split = line_with_id.split(' ')
        self.test_id = space_split[-1]
        
    def pull_status(self, line_with_status):
        """ Parse config file line and set status property """
        space_split = line_with_status.split(' ')
        if 'TODO' in space_split:
            self.status = 'TODO'
        elif 'DONE' in space_split:
            self.status = 'DONE'
        else:
            self.status = 'NONE'

def system_cases(config_lines, j):
    """ Pulls state and environment information from configuration file
    lines
    """
    state_set = []
    while config_lines[j].split(' ')[0] != '*': # System line
        if config_lines[j].split(' ')[0] == '**': # Case line
            state_set += [TestCase()]
            state_set[-1].pull_id(config_lines[j])
            state_set[-1].pull_status(config_lines[j])
        elif config_lines[j].split(' ')[0] == '***': # Env/desc line
            if ('BROWSER' in config_lines[j]) and ('OS' in config_lines[j]):
                state_set[-1].pull_os(config_lines[j])
                state_set[-1].pull_browser(config_lines[j])
        j += 1
        if j == len(config_lines):
            break
    return state_set

def system_sets(config_lines):
    """ Compile dictionary of systems and associated test cases """
    all_suites = {}
    for i in range(0, len(config_lines)):
        if config_lines[i].split(' ')[0] == '*': # System line
            config_line_1 = config_lines[i].split('((')[1]
            config_line_2 = config_line_1.split('))')[0]
            system_filename = config_line_2
            case_states = system_cases(config_lines, i+1)
            all_suites.update({system_filename:case_states})
    return all_suites

def create_cases_xml(all_suites):
    """ Create the XML structure and populate with test case
    information
    """
    def write_xml(xml_lines):
        """ Write out the Python list of XML to XML file """
        with open(XML_FILE, 'w') as out_file:
            for xml_line in xml_lines:
                out_file.write(xml_line + '\n')

    xml_lines = ['<systems>']
    for system in all_suites.keys():
        xml_lines += ['<system>']
        xml_lines += ['<system_name>' + system + '</system_name>']
        xml_lines += ['<tests>']
        for test_case in all_suites[system]:
            case_name = test_case.test_id
            case_status = test_case.status
            case_op_sys = test_case.op_sys
            case_browser = test_case.browser
            if case_status == 'DONE':
                xml_lines += ['<test>']
                xml_lines += ['<test_id>' + case_name + '</test_id>']
                xml_lines += ['<env>']
                xml_lines += ['<os>']
                for op_sys in case_op_sys:
                    xml_lines += ['<os_item>' + op_sys + '</os_item>']
                xml_lines += ['</os>']
                xml_lines += ['<browsers>']
                for browser in case_browser:
                    xml_lines += ['<browser_item>' + browser + '</browser_item>']
                xml_lines += ['</browsers>']
                xml_lines += ['</env>']
                xml_lines += ['</test>']
        xml_lines += ['</tests>']
        xml_lines += ['</system>']
    xml_lines += ['</systems>']
    write_xml(xml_lines)

with open(CONFIG_FILE) as config:
    config_lines = config.readlines()
config_lines = [x.strip('\n') for x in config_lines]
all_suites = system_sets(config_lines)
create_cases_xml(all_suites)
