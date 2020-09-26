import os
import json
from sqlalchemy.orm import joinedload
from datetime import datetime
from sqlalchemy import inspect

from sqlalchemy import ForeignKey, desc, create_engine, func, Column, BigInteger, Integer, Float, String, Boolean, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship, subqueryload
from geoalchemy2 import Geometry
from geoalchemy2.shape import to_shape
from shapely.geometry import mapping, shape
import json
from pprint import pprint

if os.environ.get('DATABASE') is not None:
  connectionString = os.environ.get('DATABASE')

engine = create_engine(connectionString, echo=False)

Base = declarative_base()

def json_object(_object):
  data = dict(_object.__dict__)
  data.pop('_sa_instance_state', None)
  return data

def json_child_list(data, name):
  if name in data:
    data[name] = [_object.json() for _object in data[name]]

def json_child_object(data, name):
  if name in data:
    data[name] = data[name].json()

class City(Base):
  __tablename__ = 'cities'

  Id = Column('id', Integer, primary_key=True)
  Name = Column('name', Text)

  def __init__(self, name):
    self.Name = name

  def json(self):
    data = json_object(self)
    return data

class Tour(Base):
  __tablename__ = 'tours'

  Id = Column('id', Integer, primary_key=True)
  CityId = Column('CityId', Integer, ForeignKey('cities.id'))
  Name = Column('name', Text)
  Description = Column('description', Text)
  Duration = Column('duration', Integer)
  Path = relationship("Path", lazy='joined')

  def __init__(self, data):
    self.CityId = data['CityId']
    self.Name = data['Name']
    self.Description = data['Description']
    self.Duration = data['Duration']

  def json(self):
    data = json_object(self)
    json_child_list(data, 'Path')
    return data

class Path(Base):
  __tablename__ = 'paths'

  Id = Column('id', Integer, primary_key=True)
  TourId = Column('TourId', Integer, ForeignKey('tours.id'))
  Coordinate = Column('coordinate', Geometry('POINT'))
  Stop = relationship("Stop", lazy='joined')

  def __init__(self, data):
    self.TourId = data['TourId']
    self.Coordinate = "POINT({} {})".format(data['latitude'], data['longitude'])

  def json(self):
    data = json_object(self)
    data['x'] = to_shape(data['Coordinate']).x
    data['y'] = to_shape(data['Coordinate']).y
    data.pop('Coordinate', None)
    json_child_list(data, 'Stop')
    return data

class Stop(Base):
  __tablename__ = 'stops'

  Id = Column('id', Integer, primary_key=True)
  PathId = Column('PathId', Integer, ForeignKey('paths.id'))
  Content = Column('content', Text)

  def __init__(self, data):
    self.PathId = data['PathId']
    self.Content = data['content']

  def json(self):
    data = json_object(self)
    return data


Base.metadata.create_all(engine)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

class Operations:

  def GetCities(as_dict = True):
    return list(map(City.json, session.query(City).all()))

  def SaveCity(name):
    session.add(City(name))
    session.commit()

  def GetTourByCity(city_id):
    data = session.query(Tour).filter_by(CityId=city_id).all()

    return [x.json() for x in data]

  def GetTour(tour_id):
    data = session.query(Tour).options(
      subqueryload('Path').subqueryload('Stop')).get(tour_id)

    return data.json()

  def SaveTour(data):
    pprint(data)
    tour = Tour(data)
    session.add(tour)
    session.flush()

    for item in data['Path']:
      item['TourId'] = tour.Id
      path = Path(item)
      session.add(path)
      session.flush()
      item['PathId'] = path.Id
      session.add(Stop(item))

    session.commit()



if __name__ == "__main__":
  pprint(Operations.GetTourByCity(6))
