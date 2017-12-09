""" Creates a configuration file at repository root directory, which
is used to control which tests are ran and prioritization
"""
import re

hydroshare_file = '../hydroshare.py'
hydroclient_file = '../hydroclient.py'
config_file = '../config.org'

def add_cases(filename, config_lines):
    
    def add_description(config_lines, case_lines, j):
        description_line = ''
        if '"""' in case_lines[j]:
            reading_desc = True
            description_line += '*** '
        else:
            reading_desc = False
        while reading_desc:
            description_words = case_lines[j].split(' ')
            description_words = [x.strip('"""') for x in description_words]
            description_words = filter(None, description_words)
            description_line += ' '.join(description_words) + ' '
            if case_lines[j].count('"""') == 2:
                reading_desc = False # For single line docstring case
            else:
                j += 1
            if j == len(case_lines):
                reading_desc = False # For end of file
            elif case_lines[j].count('"""') == 1:
                reading_desc = False # For multiline docstring case
        if description_line != '':
            config_lines += [description_line]

    with open(filename) as cases_file:
        case_lines = cases_file.readlines()
    case_lines = [x.strip('\n') for x in case_lines]
            
    for i in range(0, len(case_lines)):
        case_line = case_lines[i]
        is_spec_line = False
        if ('def test_' in case_line):
            new_config_line = '** DONE '
            is_spec_line = True
        if ('def off_test_' in case_line):
            new_config_line = '** '
            is_spec_line = True
        if ('def todo_test_' in case_line):
            new_config_line = '** TODO '
            is_spec_line = True
        if is_spec_line:
            line_parse_one = case_line.split('test_')[1]
            line_parse_two = line_parse_one.split('(')[0]
            new_config_line += line_parse_two
            config_lines += [new_config_line]
            add_description(config_lines, case_lines, i+1)

config_lines = ['* HydroClient [%] [/] ((' + hydroclient_file + '))']
add_cases(hydroclient_file, config_lines)
config_lines += ['* HydroShare [%] [/] ((' + hydroshare_file + '))']
add_cases(hydroshare_file, config_lines)

with open(config_file, 'w') as config:
    for config_line in config_lines:
        config.write(config_line + '\n')

        
        
