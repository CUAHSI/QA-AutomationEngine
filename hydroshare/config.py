import os
from dotenv import dotenv_values
config = {
    **dotenv_values(".env.default"),
    **dotenv_values(".env"),
    **os.environ,  # override loaded values with environment variables
}

BASE_URL = config['HS_BASE_URL']

USERNAME = config['HS_USERNAME']
PASSWORD = config['HS_PASSWORD']

GITHUB_ORG = config['HS_GITHUB_ORG']
GITHUB_REPO = config['HS_GITHUB_REPO']
