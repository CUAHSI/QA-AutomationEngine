import numpy as np
import pylab as plt

XLABEL = "Number of Users"
YLABEL = "Passing Rate"
TITLE = "Performance Profile"


class Plot:
    def __init__(self, name, subtitle, file_name, trials, failures):
        self.name = name
        self.subtitle = subtitle
        self.file_name = file_name
        self.trials = trials
        self.failures = failures
        self.failure_rates = [100 * failures[i] / trials[i] for i in range(len(trials))]
        self.pass_rates = [100 - failure_rate for failure_rate in self.failure_rates]
        self.avg_pass_rate = np.mean(self.pass_rates)
        self.min_pass_rate = min(self.pass_rates)
        self.max_pass_rate = max(self.pass_rates)
        self.validation_passed = len(trials) == len(failures)

    def avg_pass_vector(self):
        return [self.avg_pass_rate] * len(self.trials)

    def min_pass_vector(self):
        return [self.min_pass_rate] * len(self.trials)

    def max_pass_vector(self):
        return [self.max_pass_rate] * len(self.trials)


users = np.arange(1, 31, 1)
base = Plot(
    name="Base Case",
    subtitle="n=10",
    file_name="base-case",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        0,
        1,
        3,
        4,
        2,
        3,
        1,
        2,
        11,
        8,
        16,
        10,
        9,
        14,
        21,
        17,
        21,
        23,
        18,
        18,
        21,
        23,
        33,
        18,
        33,
        23,
        21,
    ],
)
base_vs_results = Plot(
    name="Base Case",
    subtitle="Results Count of 10",
    file_name="base-vs-results",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        0,
        1,
        3,
        4,
        2,
        3,
        1,
        2,
        11,
        8,
        16,
        10,
        9,
        14,
        21,
        17,
        21,
        23,
        18,
        18,
        21,
        23,
        33,
        18,
        33,
        23,
        21,
    ],
)
base_vs_delay = Plot(
    name="Base Case",
    subtitle="Delay Between Users of 3 sec",
    file_name="base-vs-delay",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        0,
        1,
        3,
        4,
        2,
        3,
        1,
        2,
        11,
        8,
        16,
        10,
        9,
        14,
        21,
        17,
        21,
        23,
        18,
        18,
        21,
        23,
        33,
        18,
        33,
        23,
        21,
    ],
)
base_vs_instances = Plot(
    name="Base Case",
    subtitle="Server Instance Count of 10",
    file_name="base-vs-instances",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        0,
        1,
        3,
        4,
        2,
        3,
        1,
        2,
        11,
        8,
        16,
        10,
        9,
        14,
        21,
        17,
        21,
        23,
        18,
        18,
        21,
        23,
        33,
        18,
        33,
        23,
        21,
    ],
)
base_vs_delay_and_results = Plot(
    name="Base Case",
    subtitle="Delay of 3 sec | Results Count of 100",
    file_name="base-vs-delay-and-results",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        0,
        1,
        3,
        4,
        2,
        3,
        1,
        2,
        11,
        8,
        16,
        10,
        9,
        14,
        21,
        17,
        21,
        23,
        18,
        18,
        21,
        23,
        33,
        18,
        33,
        23,
        21,
    ],
)
large = Plot(
    name="Larger Results Set",
    subtitle="Results Count of 10,000",
    file_name="large-results-set",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        0,
        2,
        2,
        0,
        2,
        0,
        2,
        2,
        7,
        15,
        6,
        12,
        12,
        15,
        17,
        14,
        18,
        13,
        13,
        24,
        32,
        25,
        26,
        31,
        24,
        41,
        29,
        30,
    ],
)
scale_out = Plot(
    name="More Server Instances",
    subtitle="Server Instance Count of 20",
    file_name="scaled-out",
    trials=np.arange(10, 301, 10),
    failures=[
        1,
        1,
        1,
        1,
        1,
        1,
        3,
        3,
        1,
        1,
        1,
        3,
        1,
        3,
        2,
        11,
        5,
        1,
        4,
        6,
        5,
        5,
        3,
        15,
        11,
        10,
        8,
        8,
        10,
        9,
    ],
)
scale_in = Plot(
    name="Fewer Server Instances",
    subtitle="Server Instance Count of 1",
    file_name="scaled-in",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        4,
        3,
        8,
        15,
        19,
        27,
        31,
        31,
        55,
        82,
        92,
        94,
        98,
        135,
        120,
        149,
        148,
        171,
        134,
        206,
        213,
        194,
        220,
        233,
        243,
        262,
        238,
        252,
        278,
    ],
)
long_stagger = Plot(
    name="Longer Delay",
    subtitle="Delay Between Users of 30 sec",
    file_name="long-stagger",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        1,
        3,
        1,
        3,
        2,
        0,
        3,
        1,
        6,
        4,
        3,
        5,
        4,
        7,
        3,
        7,
        4,
        3,
        2,
        7,
        8,
        5,
        3,
        4,
        7,
        7,
        7,
        5,
        7,
    ],
)
short_stagger = Plot(
    name="Shorter Delay",
    subtitle="Delay Between Users of 0.3 sec",
    file_name="short-stagger",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        2,
        4,
        7,
        9,
        8,
        13,
        8,
        18,
        18,
        16,
        14,
        31,
        22,
        35,
        40,
        26,
        24,
        40,
        44,
        50,
        50,
        67,
        38,
        54,
        55,
        96,
        66,
        86,
    ],
)
fast_large_load = Plot(
    name="Shorter Delay and Larger Results Set",
    subtitle="Delay of 0.3 | Results Count of 10,000",
    file_name="fast-large-load",
    trials=np.arange(10, 301, 10),
    failures=[
        0,
        0,
        1,
        2,
        7,
        0,
        5,
        7,
        5,
        11,
        15,
        23,
        11,
        16,
        27,
        25,
        24,
        28,
        26,
        36,
        44,
        55,
        53,
        54,
        58,
        55,
        65,
        63,
        80,
        75,
    ],
)
all_plots = [
    base,
    base_vs_results,
    base_vs_delay,
    base_vs_instances,
    base_vs_delay_and_results,
    large,
    scale_out,
    scale_in,
    long_stagger,
    short_stagger,
    fast_large_load,
]

for plot in all_plots:
    assert plot.validation_passed
    plt.figure(figsize=(16 / 2, 9 / 2), dpi=320)
    plt.minorticks_on()
    plt.plot(  # core data
        users,  # x axis
        plot.pass_rates,  # y axis
        linestyle="solid",
        color="xkcd:royal blue",
    )
    plt.plot(  # average
        users,
        plot.avg_pass_vector(),
        linestyle="dashed",
        color="xkcd:dark green",
        alpha=0.34,
    )
    plt.plot(  # min bound
        users,  # x axis
        plot.min_pass_vector(),  # y axis
        linestyle="dashed",
        color="xkcd:lime green",
        alpha=0.21,  # make transparent
    )
    plt.plot(  # max bound
        users,  # x axis
        plot.max_pass_vector(),  # y axis
        linestyle="dashed",
        color="xkcd:lime green",
        alpha=0.21,  # make transparent
    )
    ax = plt.gca()
    ax.fill_between(  # shade region for data range
        users,  # x axis
        plot.min_pass_vector(),  # y min
        plot.max_pass_vector(),  # y max
        color="xkcd:lime green",
        alpha=0.21,  # make transparent
    )
    plt.suptitle(plot.name, fontsize=18)
    plt.title(" | ".join([TITLE, plot.subtitle]), fontsize=14)
    plt.xlabel(XLABEL)
    ax.set_xlim([1, 30])
    ax.xaxis.set_major_locator(
        plt.FixedLocator([1, 4, 7, 10, 13, 16, 19, 22, 25, 28, 30])
    )
    ax.xaxis.set_minor_locator(plt.FixedLocator(np.arange(1, 31, 1)))
    plt.ylabel(YLABEL)
    ax.set_ylim([0, 100])
    plt.savefig("{}.png".format(plot.file_name), bbox_inches="tight")
