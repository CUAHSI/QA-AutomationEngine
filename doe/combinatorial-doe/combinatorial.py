""" Brute force approach to combinatorial DOE solutions """
import argparse
from random import randint

# TODO seed random numbers for reproducability
# TODO generalize to include n-way design of experiments (any n>2)

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument('--experiments')
parser.add_argument('--factors')
parser.add_argument('--specification')
args = parser.parse_args()


def parse_args(args):
    """ Parse spec argument and convert to integers """
    depths = args.specification.split(',')
    depths = [int(i) for i in depths]
    experiments_count = int(args.experiments)
    factors = int(args.factors)
    return depths, experiments_count, factors


def validate_arguments(depths, experiments_count, factors):
    """ Confirm number of experiments is theoretically possible.  Confirm
    length of specification is long enough, given number of factors.
    """
    # Confirm number of factors is equal to or less than spec length
    # Note: number of factors equal to spec length is just full combinatorial
    assert(len(depths) >= int(args.factors))

    # Establish the highest two values in the spec
    depths_cp = [i for i in depths]
    depth_max = [max(depths_cp)]  # largest number in depths copy
    depths_cp.pop(depths_cp.index(depth_max[0]))  # remove largest
    depth_max += [max(depths_cp)]  # second largest number in depths copy

    # Confirm goal is theoretically possible
    experiments_min = depth_max[0] * depth_max[1]
    assert(experiments_count >= experiments_min)


def create_random_experiments(depths, experiments_count):
    """ Create random set of experiments """
    experiments = []
    for i in range(0, experiments_count):
        experiment = []
        for j in range(0, len(depths)):
            experiment.append(randint(0, depths[j]-1))
        experiments.append(experiment)
    return experiments


def combinations_met(depths, experiments, factors):
    combinations = []
    combinations_needed = 1
    for n in range(0, len(depths)):
        combinations_needed *= depths[n]
    for p in range(0, len(experiments)):
        combination = []
        for q in range(0, factors):
            combination.append(experiments[p][q])
        if combination not in combinations:
            combinations.append(combination)
    if len(combinations) != combinations_needed:
        return False
    else:
        return True


def passes_two_way(depths, experiments):
    # Two way check
    for i in range(0, len(depths)-1):
        for j in range(i+1, len(depths)):
            if not combinations_met(depths, experiments, factors):
                return False
    return True


def passes_three_way(depths, experiments):
    # Three way check
    for i in range(0, len(depths)-2):
        for j in range(i+1, len(depths)-1):
            for k in range(i+2, len(depths)):
                if not combinations_met(depths, experiments, factors):
                    return False
    return True


def passes_four_way(depths, experiments):
    # Four way check
    for i in range(0, len(depths)-3):
        for j in range(i+1, len(depths)-2):
            for k in range(i+2, len(depths)-1):
                for l in range(i+3, len(depths)):
                    if not combinations_met(depths, experiments, factors):
                        return False
    return True


# Parse and validate user-provided arguments
depths, experiments_count, factors = parse_args(args)
validate_arguments(depths, experiments_count, factors)

attempts = 0
solved = False
while not solved:
    experiments = create_random_experiments(depths, experiments_count)
    assert(2 <= factors and factors <= 4)
    if factors == 2:
        solved = passes_two_way(depths, experiments)
    elif factors == 3:
        solved = passes_three_way(depths, experiments)
    elif factors == 4:
        solved = passes_four_way(depths, experiments)
    if solved:
        print('Solution Found:')
        for i in range(0, len(experiments)):
            print(experiments[i])
    else:
        attempts += 1
        print('Solution Not Found - Try #' + str(attempts))
