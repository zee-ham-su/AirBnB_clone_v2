#!/usr/bin/python3
""" Place Module for HBNB project """
import models
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from os import getenv


class Place(BaseModel, Base):
    """ A place to stay """
    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'),
                     nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'),
                     nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []

    # Define the relationship between Place and Review
    if getenv("HBNB_TYPE_STORAGE") == "db":
        reviews = relationship("Review",
                               backref="place",
                               cascade="all, delete-orphan")

    else:
        @property
        def reviews(self):
            """
            Getter attribute for reviews that returns
            a list of Review instances
            with place_id equal to the current Place.id
            """
            from models import storage
            review_list = []
            for review in storage.all(Review).values():
                if review.place_id == self.id:
                    review_list.append(review)
                    return review_list
