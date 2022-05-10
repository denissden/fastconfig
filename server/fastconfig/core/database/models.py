from re import L
from sqlalchemy import *
from .database import Base


class Token(Base):
    __tablename__ = "token"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    value = Column(String, index=True)
    permissions = Column(String)

class Group(Base):
    __tablename__ = "perm_group"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    permissions = Column(String)


class Folder(Base):
    __tablename__ = "folder"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)


class App(Base):
    __tablename__ = "app"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    config = Column(String)


class KeyValue(Base):
    __tablename__ = "kv"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, index=True)
    folder_id = Column(Integer, ForeignKey('folder.id'))
    value = Column(String)