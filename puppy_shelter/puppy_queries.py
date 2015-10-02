__author__ = 'naren'

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from puppy_db import Base, Puppy, Shelter
engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.bind = engine
DBSession = sessionmaker(bind=engine)
session = DBSession()
