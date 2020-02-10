from datetime import datetime, timedelta
from settings import DB_URL, DB_NAME, DB_USER, DB_PASSWORD


def get_db_url():
    if not all(map(lambda x: isinstance(x, str),
                   [DB_URL, DB_NAME, DB_USER, DB_PASSWORD])):
        raise ValueError('Database credentials must be set in your environment')

    return f'postgres://{DB_USER}:{DB_PASSWORD}@{DB_URL}/{DB_NAME}'


def get_expired_datetime():
    return datetime.utcnow() + timedelta(days=14)
