#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import Base
from models.base_model import BaseModel
from sqlalchemy import Column
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import relationship

"""
This is a Python class that models a City class but inherits from the BaseModel
class as the Parent Class
"""


class City(BaseModel, Base):
    """
    This is a class modelling the City object for AirBnB Clone project.
    It inherits BaseModel and Base as Parent Classes

    Attributes:
    tablename: cities
        places (sqlalchemy relationship): The user-Place relationship.
        state_id (str): the id of the State where the city is
        name (str): the name of the city
    """
    __tablename__ = 'cities'
    name = Column(String(128), nullable=False)
    state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
    places = relationship("Place", backref="cities", cascade="delete")
