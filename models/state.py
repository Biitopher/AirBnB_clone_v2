#!/usr/bin/python3
""" State Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """
    if models.storage_type == "db":
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship("City", backref="state")
    else:
        name = ""

    def __init__(self, *args, **kwargs):
        """Init state"""
        super().__init__(*args, **kwargs)

    def cities(self):
        """Returns list of City objects linked to current State."""
        cities_list = []
        for city in list(storage.all(City).values()):
            if city.state_id == self.id:
                cities_list.append(city)
        return cities_list
