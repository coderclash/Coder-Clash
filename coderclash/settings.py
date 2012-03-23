import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PORT = 8000
DEBUG = True

DB = {
    'NAME': 'coderclash',
    'HOST': '127.0.0.1',
    'PORT': 27017,
    'POOL_ID': '',
    'MAX_CACHED': 10,
    'MAX_CONNECTIONS': 50
}
