""" Brute force approach to combinatorial DOE solutions """
import argparse
from functools import reduce
from itertools import combinations
import random
import time


def validate_arguments(depths, experiments_count, factors):
    """ Confirm number of experiments is theoretically possible.  Confirm
    length of specification is long enough, given number of factors.
    """
    assert factors > 1, '"factors" should be > 1'
    # Confirm number of factors is equal to or less than spec length
    # Note: number of factors equal to spec length is just full combinatorial
    assert len(depths) >= int(factors)
    # Confirm goal is theoretically possible
    depth_max = sorted(depths, reverse=True)[:factors]
    experiments_min = reduce(lambda x, y: x * y, depth_max)
    assert experiments_count >= experiments_min, (
        "Experiments count can not be less than product of {} largest "
        "numbers in specification ({})".format(factors, experiments_min)
    )


def create_random_experiments(depths, experiments_count, seed=None):
    """ Create random set of experiments """
    experiments = []
    if seed is None:
        seed = random.randrange(int(time.time()))
    random.seed(seed)

    for i in range(experiments_count):
        experiments.append([int(random.random() * spec) for spec in depths])

    return experiments, seed


def combinations_met(to_compare, depths, experiments):
    combinations = []
    combinations_needed = 1
    for n in to_compare:
        combinations_needed *= depths[n]
    for p in range(0, len(experiments)):
        combination = [experiments[p][q] for q in to_compare]
        if combination not in combinations:
            combinations.append(combination)
    if len(combinations) != combinations_needed:
        return False
    else:
        return True


def passes_n_way(n, depths, experiments):
    depths_indexes = [item[0] for item in enumerate(depths)]
    for to_compare in combinations(depths_indexes, n):
        if not combinations_met(to_compare, depths, experiments):
            return False
    return True


def main():
    # Parse and validate user-provided arguments
    parser = argparse.ArgumentParser(
        description="Creates a covering array for a given specification "
        "using brute-force (that is, generates random "
        "experiments and checks whether we've achieved "
        "full coverage for a given factor). "
        "See https://math.nist.gov/coveringarrays/"
        "coveringarray.html for explanation about covering "
        "arrays."
    )
    parser.add_argument(
        "--experiments",
        type=int,
        required=True,
        help="Number of random experiments to generate. "
        "A higher value increases the chance to "
        "find a solution.",
    )
    parser.add_argument(
        "--factors",
        type=int,
        required=True,
        help='Specifies a "covering" strength of resulting '
        "array. --factors == length of --specification "
        "means a full coverage.",
    )
    parser.add_argument(
        "--specification",
        type=int,
        nargs="+",
        required=True,
        help="Specifies a number of possible variables and "
        "a number of possible values each variable "
        "can take on. "
        'E.g., "specification = 2 2 2" means 3 '
        "possible variables with 2 possible values "
        "for each variable.",
    )
    parser.add_argument(
        "--seed",
        type=int,
        help="Specifies random seed to use when generate " "experiments.",
    )
    args = parser.parse_args()

    depths, experiments_count, factors, seed = (
        args.specification,
        args.experiments,
        args.factors,
        args.seed,
    )
    validate_arguments(depths, experiments_count, factors)

    attempts = 1
    solved = False
    while not solved:
        experiments, solution_seed = create_random_experiments(
            depths, experiments_count, seed
        )
        solved = passes_n_way(factors, depths, experiments)
        if solved:
            print("Solution Found:")
            experiments_wo_duplicates = [
                list(uniq_item)
                for uniq_item in set(tuple(item) for item in experiments)
            ]
            for exp in experiments_wo_duplicates:
                print(exp)
            print("Random seed for this solution is " "{}".format(solution_seed))
        else:
            attempts += 1
            print("Solution Not Found - Try #{}".format(attempts))


if __name__ == "__main__":
    main()
