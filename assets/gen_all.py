""" Generates sites and data values, provided folders with spec as folder name """
import argparse
import os

parser = argparse.ArgumentParser()
parser.add_argument("--sets")
parser.add_argument("--size")
parser.add_argument("--methods")
parser.add_argument("--sites")
parser.add_argument("--sources")
parser.add_argument("--variables")
args = parser.parse_args()

os.system("python3 gen_methods.py --count " + args.methods)
os.system("python3 gen_sites.py --count " + args.sites)
os.system("python3 gen_sources.py --count " + args.sources)
os.system("python3 gen_variables.py --count " + args.variables)
if args.size is not None:
    os.system(
        "python3 gen_datavalues.py"
        + " --sets "
        + args.sets
        + " --size "
        + args.size
        + " --methods "
        + args.methods
        + " --sites "
        + args.sites
        + " --sources "
        + args.sources
        + " --variables "
        + args.variables
    )
else:
    os.system(
        "python3 gen_datavalues.py"
        + " --sets "
        + args.sets
        + " --methods "
        + args.methods
        + " --sites "
        + args.sites
        + " --sources "
        + args.sources
        + " --variables "
        + args.variables
    )
