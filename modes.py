""" Establishes parameters for test execution timing """
def setup_mode(MODE_SELECTION):
    modes = {'quick' : {'sleep_time' : 1},
             'watch' : {'sleep_time' : 2},
             'demo' : {'sleep_time' : 3},
             'safe-demo' : {'sleep_time' : 4}}
    global SLEEP_TIME
    SLEEP_TIME = modes[MODE_SELECTION]['sleep_time']

