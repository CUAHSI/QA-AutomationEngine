import os
from dotenv import dotenv_values
config = {
    **dotenv_values(".env.default"),
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

BASE_URL = config['CZ_BASE_URL']

USERNAME = config['CZ_USERNAME']
PASSWORD = config['CZ_PASSWORD']

HS_USERNAME = config['HS_USERNAME']
HS_PASSWORD = config['HS_PASSWORD']

GITHUB_ORG = config['CZ_GITHUB_ORG']
GITHUB_REPO = config['CZ_GITHUB_REPO']

EARTHCHEM_USERNAME = config['CZ_EARTHCHEM_USERNAME']
EARTHCHEM_PASSWORD = config['CZ_EARTHCHEM_PASSWORD']
