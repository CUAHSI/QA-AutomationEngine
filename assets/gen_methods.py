""" Generates methods for HIS system testing based on random data (seeded) """
import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument("--count")
args = parser.parse_args()

count = int(args.count)

with open("methods.csv", "w") as methods_file:
    methods_file.write("MethodCode,MethodDescription\n")

random.seed(4)

for i in range(0, count):
    method_code = str(i + 1)
    method_desc = [random.choice(string.ascii_letters) for i in range(0, 20)]
    method_desc = "".join(method_desc)
    unquoted_row = [method_code, method_desc]
    row = ['"{}"'.format(field) for field in unquoted_row]
    with open("methods.csv", "a") as methods_file:
        methods_file.write(",".join(row) + "\n")
