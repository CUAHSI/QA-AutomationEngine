""" Establishes parameters for test execution timing """


def setup_mode(mode_choice):
    """ Sets up sleep_time (wait time between browser manipulations)
    based on chosen mode of execution
    """
    modes = {'quick': {'sleep_time': 1},
             'watch': {'sleep_time': 2},
             'demo': {'sleep_time': 3},
             'safe-demo': {'sleep_time': 4}}
    sleep_time = modes[mode_choice]['sleep_time']
    return sleep_time
