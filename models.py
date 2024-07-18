from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy.sql import func

from connect_db import engine

Base = declarative_base()


class Project(Base):
    __tablename__ = 'projects'

    project_id = Column(Integer, primary_key=True, autoincrement=True)
    id = Column(Integer)
    name = Column(String)
    description = Column(String)
    country_id = Column(Integer, ForeignKey('countries.country_id', ondelete='SET NULL'), nullable=True)
    type_id = Column(Integer, ForeignKey('types.type_id', ondelete='SET NULL'), nullable=True)
    file_path = Column(String)
    latitude = Column(String)
    longitude = Column(String)
    image_path = Column(String)
    version = Column(Integer, default=1)
    created_at = Column(DateTime, server_default=func.now())
    deleted_at = Column(DateTime, nullable=True)

    country = relationship('Country', back_populates='projects')
    type = relationship('Type', back_populates='projects')

    def as_dict(self):
        return {
            'project_id': self.project_id,
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'country_id': self.country_id,
            'type_id': self.type_id,
            'file_path': self.file_path,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'image_path': self.image_path,
            'version': self.version,
            'created_at': self.created_at,
            'deleted_at': self.deleted_at,
        }


class Country(Base):
    __tablename__ = 'countries'

    country_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    projects = relationship('Project', back_populates='country')

    def as_dict(self):
        return {
            'country_id': self.country_id,
            'name': self.name
        }


class Type(Base):
    __tablename__ = 'types'

    type_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String)

    projects = relationship('Project', back_populates='type')

    def as_dict(self):
        return {
            'type_id': self.type_id,
            'name': self.name
        }


Base.metadata.create_all(engine)
