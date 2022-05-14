from enum import Enum, unique
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)
    value = Column(String, index=True)
    groups = Column(String)

class Group(Base):
    __tablename__ = "token_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True, unique=True)

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    parent_id = Column(Integer, ForeignKey('item.id'))
    value = Column(String)
    permissions = Column(String)

    children = relationship('Item')