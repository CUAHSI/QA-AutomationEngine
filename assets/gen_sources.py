""" Generates variables for HIS system testing based on random data (seeded) """
import argparse
import random
import string

parser = argparse.ArgumentParser()
parser.add_argument('--count')
args = parser.parse_args()

count = int(args.count)

with open('sources.csv', 'w') as variables_file:
    variables_file.write('SourceCode,Organization,SourceDescription,SourceLink,' +
                         'ContactName,Email,Citation\n')

random.seed(4)

for i in range(0, count):
    source_code = str(i+1)
    organization = [random.choice(string.ascii_letters) for i in range(0, 64)]
    organization = ''.join(organization)
    source_desc = [random.choice(string.ascii_letters) for i in range(0, 64)]
    source_desc = ''.join(source_desc)
    source_link = ''
    contact_name = [random.choice(string.ascii_letters) for i in range(0, 64)]
    contact_name = ''.join(contact_name)
    email = [random.choice(string.ascii_letters) for i in range(0, 64)]
    email = ''.join(email)
    citation = [random.choice(string.ascii_letters) for i in range(0, 64)]
    citation = ''.join(citation)
    source = [source_code, organization, source_desc, source_link,
              contact_name, email, citation]
    source = ['"' + field + '"' for field in source]
    with open('sources.csv', 'a') as sources_file:
        sources_file.write(','.join(source) + '\n')
