import os
from secrets import *

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8000
DEBUG = True

DB = {
    'dbname': 'coderclash',
    'host': '127.0.0.1',
    'port': 27017,
    'pool_id': 'coderclash',
    'maxcached': 10,
    'maxconnections': 50
}
