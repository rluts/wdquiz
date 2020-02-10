import os

BASE_PATH = os.path.dirname(os.path.dirname(__file__))
DB_URL = os.getenv('DB_URL')
DB_NAME = os.getenv('DB_NAME')
DB_USER = os.getenv('DB_USER')
DB_PASSWORD = os.getenv('DB_PASSWORD')
TG_TOKEN = os.getenv('TG_TOKEN')
