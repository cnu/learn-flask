__author__ = 'naren'

import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Numeric, Date, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


association_table = Table('association', Base.metadata,
    Column('puppy_id', Integer, ForeignKey('puppy.id')),
    Column('adopters_id', Integer, ForeignKey('adopters.id'))
)

class Shelter(Base):
    __tablename__ = 'shelter'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(250), nullable=False)
    shelter = Column(String(100))
    name = Column(String(50))
    address = Column(String(500))
    city = Column(String(120))
    state = Column(String(120))
    zipCode = Column(String(10))
    email = Column(String(100))
    website = Column(String)
    maxCapacity = Column(Numeric(10))
    currentCapacity = Column(Numeric(10))


class Puppy(Base):
    __tablename__ = 'puppy'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    dateOfBirth = Column(Date)
    breed = Column(String(100))
    gender = Column(String(8))
    weight = Column(Numeric(10))
    picture = Column(String)
    shelter_id = Column(Integer, ForeignKey('shelter.id'))
    shelter = relationship(Shelter)
    profile = relationship('Profile', uselist=False, backref='puppy')
    adopters = relationship('Adopters', secondary=association_table)


class Profile(Base):
    __tablename__ = 'profile'
    id = Column(Integer, primary_key=True, autoincrement=True)
    url = Column(String(2000))
    description = Column(String(2000))
    specialNeeds = Column(String(2000))
    puppy_id = Column(Integer, ForeignKey('puppy.id'))


class Adopters(Base):
    __tablename__ = 'adopters'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(80), nullable=False)
    location = Column(String(80))



engine = create_engine('sqlite:///puppyshelter.db')
Base.metadata.create_all(engine)
