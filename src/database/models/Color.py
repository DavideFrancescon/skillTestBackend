from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import relationship

from sqlalchemy.ext.declarative import declarative_base

from src.database.models.User import User

from src.database import base

import datetime
import math

import re


class Colors(base):
    __tablename__ = 'colors'
    id = Column(Integer, primary_key=True)
    favorite_color = Column(String(255), nullable=False)
    hated_color = Column(String(255))
    random_color = Column(String(255))
    lucky_color = Column(String(255))
    person = Column(String(50), ForeignKey(User.public_id))
    creation_time = Column(DateTime, default=datetime.datetime.utcnow)

    def toJson(self) -> str:
        return {
            "id": self.id,
            "favorite_color": self.favorite_color,
            "hated_color": self.hated_color,
            "random_color": self.random_color,
            "lucky_color": self.lucky_color,
            "person": self.person,
            "creation_time": self.creation_time,
        }


def mixColors(color1, color2):
    c1 = hex_to_rgb(color1[1:])
    c2 = hex_to_rgb(color2[1:])
    mixed = colorMixer(c1, c2, 0.5)
    result = "#{}".format(rgb_to_hex(mixed))
    print(result)
    return result


def colorChannelMixer(colorChannelA, colorChannelB, amountToMix):
    channelA = colorChannelA * amountToMix
    channelB = colorChannelB * (1 - amountToMix)
    res = math.floor(channelA + channelB)
    return res


def colorMixer(rgbA, rgbB, amountToMix):
    r = colorChannelMixer(rgbA[0], rgbB[0], amountToMix)
    g = colorChannelMixer(rgbA[1], rgbB[1], amountToMix)
    b = colorChannelMixer(rgbA[2], rgbB[2], amountToMix)
    return [r,g,b]


def hex_to_rgb(hex):
    rgb = []
    for i in (0, 2, 4):
        decimal = int(hex[i:i+2], 16)
        rgb.append(decimal)
    return rgb


def rgb_to_hex(rgb):
    return ('{:X}{:X}{:X}').format(rgb[0], rgb[1], rgb[2])
