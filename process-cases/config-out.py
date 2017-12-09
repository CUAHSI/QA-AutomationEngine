import re

config_file = '../config.org'

def pull_states(config_lines, j):

    def get_state(config_line):
        space_split = config_line.split(' ')
        if 'TODO' in space_split:
            return {space_split[-1]:'TODO'}
        elif 'DONE' in space_split:
            return {space_split[-1]:'DONE'}
        else:
            return {space_split[-1]:'NONE'}

    state_set = {}
    while config_lines[j].split(' ')[0] != '*': # System line
        if config_lines[j].split(' ')[0] == '**': # Case line
            state_set.update(get_state(config_lines[j]))
        j += 1
        if j == len(config_lines):
            break
    return state_set

def system_sets(config_lines):
    all_suites = {}
    for i in range(0, len(config_lines)):
        if config_lines[i].split(' ')[0] == '*': # System line
            config_line_1 = config_lines[i].split('((')[1]
            config_line_2 = config_line_1.split('))')[0]
            system_filename = config_line_2
            case_states = pull_states(config_lines, i+1)
            all_suites.update({system_filename:case_states})
    return all_suites

def update_scripts(all_suites):

    def update_case(all_suites, system, system_line):
        line_parse_one = system_line.split('test_')[1]
        line_parse_two = line_parse_one.split('(')[0]
        case_num = line_parse_two
        status_setting = all_suites[system][case_num]
        if (status_setting == 'TODO'):
            prepend = 'todo'
        elif (status_setting == 'NONE'):
            prepend = 'off'
        else:
            prepend = ''
        if ('off' in system_line) and (prepend == ''):
            return system_line.replace('off_test_','test_')
        elif ('off' in system_line) and (prepend == 'todo'):
            return system_line.replace('off_test_','todo_test_')
        elif ('todo' in system_line) and (prepend == ''):
            return system_line.replace('todo_test_','test_')
        elif ('todo' in system_line) and (prepend == 'off'):
            return system_line.replace('todo_test_','off_test_')
        elif ('off' not in system_line) and ('todo' not in system_line) and \
             (prepend == 'off'):
            return system_line.replace('test_','off_test_')
        elif ('off' not in system_line) and ('todo' not in system_line) and \
             (prepend == 'todo'):
            return system_line.replace('test_','todo_test_')
        else:
            return system_line

    for system in all_suites.keys():
        new_lines = []
        with open(system) as sys_file:
            system_lines = sys_file.readlines()
        system_lines = [x.strip('\n') for x in system_lines]
        for k in range(0, len(system_lines)):
            system_line = system_lines[k]
            if ('def test_' in system_line) or \
               ('def off_test_' in system_line) or \
               ('def todo_test_' in system_line):
                new_lines += [update_case(all_suites, system, system_line)]
            else:
                new_lines += [system_line]

        with open(system, 'w') as sys_file:
            for new_line in new_lines:
                sys_file.write(new_line + '\n')

with open(config_file) as config:
    config_lines = config.readlines()
config_lines = [x.strip('\n') for x in config_lines]
all_suites = system_sets(config_lines)
update_scripts(all_suites)
