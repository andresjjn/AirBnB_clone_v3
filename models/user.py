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
        if kwargs:
            password = kwargs.pop("password", None)
            if password:
                self.update_password(password)
        super().__init__(*args, **kwargs)

    def update_password(self, password):
        """ function that updates the password using hash algorithm"""
        m = hashlib.md5()
        encode_pass = password.encode('utf-8')
        m.update(encode_pass)
        new_passw = m.hexdigest()
        setattr(self, "password", new_passw)
