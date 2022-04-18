"""
Deliver the project environment information, e.g. used for logging or overall constants.
"""

###############
# Imports
###############
import logging
import pathlib

from datetime import datetime
    
###############
# Constants
###############    

# Create current date string
STR_CURRENT_DATE = datetime.today().strftime('%Y-%m-%d')    

# Paths to the root of the project, containing the main.py file,
# and the `data` subfolder.
PROJECT_ROOT = pathlib.Path(__file__).parent.resolve()
DATA_ROOT = PROJECT_ROOT / 'data'

# Path and test file information for testing.
TEST_NEO_FILE = PROJECT_ROOT / 'tests' / 'test-neos-2020.csv'
TEST_CAD_FILE = PROJECT_ROOT / 'tests' / 'test-cad-2020.json'


###############
# Coding
############### 

# Logging concept: simple logging with root logger
# see:
# https://docs.python.org/3/howto/logging.html#displaying-the-date-time-in-messages
def config_basic_root_logger():
    """ Configure the log format for root logger, append messages to log file. """
    logging.basicConfig(
        filename='./logs/neo_project_' + STR_CURRENT_DATE + '.log',
        level=logging.DEBUG, # future toDo: could be set with CLI argument
        filemode='a',
        format='%(asctime)s:%(levelname)s:%(name)s:%(message)s'
    )


def get_logger():
    """ Returns the root logger. """
    return logging.getLogger()
