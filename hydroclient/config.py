import os
from dotenv import dotenv_values
config = {
    **dotenv_values(".env"),  # load shared development variables
    **os.environ,  # override loaded values with environment variables
}

BASE_URL = config['HC_BASE_URL']
