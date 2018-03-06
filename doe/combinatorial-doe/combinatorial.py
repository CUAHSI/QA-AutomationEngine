""" Brute force approach to combinatorial DOE solutions """
import argparse
from random import randint
from time import sleep

# TODO seed random numbers for reproducability
# TODO generalize to include n-way design of experiments (any n>2)

# Arguments parsing
parser = argparse.ArgumentParser()
parser.add_argument('--factors')
parser.add_argument('--goal')
parser.add_argument('--spec')
args = parser.parse_args()

def parse_args(args):
    """ Parse spec argument and convert to integers """
    depths = args.spec.split(',')
    depths = [int(i) for i in depths]
    num_experiments = int(args.goal)
    num_factors = int(args.factors)
    return depths, num_experiments, num_factors

def validate_arguments(depths, num_experiments, num_factors):
    """ Confirm goal is theoretically possible.  Confirm length of
    spec is long enough, given number of factors.
    """
    # Confirm number of factors is equal to or less than spec length
    # Note: number of factors equal to spec length is just full combinatorial
    assert(len(depths) >= int(args.factors))
    
    # Establish the highest two values in the spec
    depths_copy = [i for i in depths]
    depth_max_one = max(depths_copy) # largest number in depths_copy
    depths_copy.pop(depths_copy.index(depth_max_one)) # remove largest number
    depth_max_two = max(depths_copy) # second largest number in depths_copy

    # Confirm goal is theoretically possible
    theoretical_min_experiments = depth_max_one * depth_max_two
    assert(num_experiments >= theoretical_min_experiments)

def create_random_experiments(depths, num_experiments):
    """ Create random set of experiments """
    experiments_set = []
    for i in range(0, num_experiments):
        experiment = []
        for j in range(0, len(depths)):
            experiment.append(randint(0, depths[j]-1))
        experiments_set.append(experiment)
    return experiments_set

def check_two_way(depths, experiments):
    # Two way check
    for i in range(0, len(depths)-1):
        for j in range(i+1, len(depths)):
            combinations = []
            combinations_needed = depths[i] * depths[j]
            for k in range(0, len(experiments)):
                if (experiments[k][i], experiments[k][j]) not in combinations:
                    combinations.append((experiments[k][i], experiments[k][j]))
            if len(combinations) != combinations_needed:
                return False
    return True

def check_three_way(depths, experiments):
    # Three way check
    for i in range(0, len(depths)-2):
        for j in range(i+1, len(depths)-1):
            for k in range(i+2, len(depths)):
                combinations = []
                combinations_needed = depths[i] * depths[j] * depths[k]
                for l in range(0, len(experiments)):
                    if (experiments[l][i], experiments[l][j], experiments[l][k]) not in combinations:
                        combinations.append((experiments[l][i], experiments[l][j], experiments[l][k]))
                if len(combinations) != combinations_needed:
                    return False
    return True

def check_four_way(depths, experiments):
    # Four way check
    for i in range(0, len(depths)-3):
        for j in range(i+1, len(depths)-2):
            for k in range(i+2, len(depths)-1):
                for l in range(i+3, len(depths)):
                    combinations = []
                    combinations_needed = depths[i] * depths[j] * depths[k] * depths[l]
                    for m in range(0, len(experiments)):
                        if (experiments[m][i], experiments[m][j], experiments[m][k], experiments[m][l]) not in combinations:
                            combinations.append((experiments[m][i], experiments[m][j], experiments[m][k], experiments[m][l]))
                    if len(combinations) != combinations_needed:
                        return False
    return True

# Parse and validate user-provided arguments
depths, num_experiments, num_factors = parse_args(args)
validate_arguments(depths, num_experiments, num_factors)

attempts = 0
solved = False
while not solved:
    experiments = create_random_experiments(depths, num_experiments)
    assert(2 <= num_factors and num_factors <= 4)
    if num_factors == 2:
        solved = check_two_way(depths, experiments)
    elif num_factors == 3:
        solved = check_three_way(depths, experiments)
    elif num_factors == 4:
        solved = check_four_way(depths, experiments)
    if solved:
        print('Solution Found:')
        for i in range(0, len(experiments)):
            print(experiments[i])
    else:
        attempts += 1
        print('Solution Not Found - Try #' + str(attempts))
