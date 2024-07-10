from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

from connect_db import engine

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)
    description = Column(String)
    country_id = Column(Integer, ForeignKey('countries.country_id'))
    type_id = Column(Integer, ForeignKey('types.type_id'))
    file_path = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    image_path = Column(String)

    def as_dict(self):
        return {
            'project_id': self.project_id,
            'name': self.name,
            'description': self.description,
            'country_id': self.country_id,
            'type_id': self.type_id,
            'file_path': self.file_path,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_path': self.image_path,
        }


class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def as_dict(self):
        return {
            'country_id': self.country_id,
            'name': self.name
        }


class Type(Base):
    __tablename__ = 'types'

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    def as_dict(self):
        return {
            'type_id': self.type_id,
            'name': self.name
        }


Base.metadata.create_all(engine)
