from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from .utils import get_db_url

engine = create_engine(get_db_url())

session = sessionmaker(bind=engine)()

Base = declarative_base()
