
from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine

from sqlalchemy.ext.declarative import declarative_base
from src.database import base


class User(base):
    __tablename__ = 'usertable'
    public_id = Column(String(50), primary_key=True)
    name = Column(String(100))
    email = Column(String(70), unique=True)
    password = Column(String(150))

    def __repr__(self):
        # return ("favorite_color:" + self.favorite_color,
        #         "creation_time:" + self.creation_time,
        #         "hated_color:" + self.hated_color,
        #         "random_color:" + self.random_color,
        #         "lucky_color:" + self.lucky_color,
        #         "person:" + self.person)
        return ("public_id" +  self.public_id)
