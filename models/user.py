#!/usr/bin/python3
""" holds class User"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
import hashlib


class User(BaseModel, Base):
    """Representation of a user """
    if models.storage_t == 'db':
        __tablename__ = 'users'
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship("Place", backref="user")
        reviews = relationship("Review", backref="user")
    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""

    def __init__(self, *args, **kwargs):
        """initializes user"""
        super().__init__(*args, **kwargs)
        self.password = self.__hash_password(self.password)

    @staticmethod
    def __hash_password(password):
        """Hashes a password with MD5"""
        if password:
            return hashlib.md5(password.encode()).hexdigest()
        return None

    def to_dict(self, save_to_disk=False):
        """Converts User object to dictionary representation"""
        dict_repr = super().to_dict()
        if not save_to_disk:
            dict_repr.pop("password", None)
        return dict_repr
