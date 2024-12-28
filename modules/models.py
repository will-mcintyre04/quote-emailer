# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    address = Column(String, unique=True)

class Quote(Base):
    __tablename__ = 'quotes'

    id = Column(Integer, primary_key=True, autoincrement=True)
    quote = Column(String)
    author = Column(String)