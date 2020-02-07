from sqlalchemy import create_engine, Column, Table, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import (
    Integer, SmallInteger, String, Date, DateTime, Float, Boolean, Text, LargeBinary, UnicodeText)

from scrapy.utils.project import get_project_settings

DeclarativeBase = declarative_base()


def db_connect():
    """
    Performs database connection using database settings from settings.py.
    Returns sqlalchemy engine instance
    """
    return create_engine(get_project_settings().get("CONNECTION_STRING"))


def create_table(engine):
    DeclarativeBase.metadata.create_all(engine)


class Threads(DeclarativeBase):
    """
    Database model for Threads table
    """
    __tablename__ = "threads"

    id = Column(Integer, primary_key=True)
    # forum_id = Column(Integer, ForeignKey('forums.id'))
    thread = Column(Text)
    forum = Column(Text)
    url = Column(Text)


class Posts(DeclarativeBase):
    """
    Database model for Posts table
    """
    __tablename__ = 'posts'
    id = Column(Integer, primary_key=True)
    thread_id = Column(Integer, ForeignKey('threads.id'))
    body = Column(Text)
    author = Column(Text)


class Forums(DeclarativeBase):
    """
    Database model for Forums table
    """
    __tablename__ = 'forums'
    id = Column(Integer, primary_key=True)
    forum = Column(Text)
