import os
import json

from datetime import datetime
from sqlalchemy import inspect

from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from geoalchemy2 import Geometry

if os.environ.get('DATABASE') is not None:
  connectionString = os.environ.get('DATABASE')

engine = create_engine(connectionString, echo=False)

Base = declarative_base()

class City(Base):
  __tablename__ = 'cities'

  Id = Column('id', Integer, primary_key=True)
  Name = Column('name', Text)

  def JSON(self):
    data = {}
    data['Id'] = self.Id
    data['Name'] = self.Name

    return data

class Tour(Base):
  __tablename__ = 'tours'

  Id = Column('id', Integer, primary_key=True)
  CityId = Column('CityId', Integer, ForeignKey('cities.id'))
  Name = Column('name', Text)
  Description = Column('description', Text)
  Duration = Column('duration', Integer)

class Path(Base):
  __tablename__ = 'paths'

  Id = Column('id', Integer, primary_key=True)
  TourId = Column('TourId', Integer, ForeignKey('tours.id'))
  Coordinate = Column('coordinate', Geometry('POINT'))

class Stop(Base):
  __tablename__ = 'stops'

  Id = Column('id', Integer, primary_key=True)
  PathId = Column('PathId', Integer, ForeignKey('paths.id'))
  Content = Column('content', Text)


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Operations:

  def object_as_dict(obj):
    return {c.key: getattr(obj, c.key)
            for c in inspect(obj).mapper.column_attrs}

  def GetCities(as_dict = True):
    data = session.query(City).all()

    if as_dict:
      data = [Operations.object_as_dict(x) for x in data]

    return data

if __name__ == "__main__":
  print(Operations.GetCities())
