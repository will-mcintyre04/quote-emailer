# models.py
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Email(Base):
    __tablename__ = 'emails'

    id = Column(Integer, primary_key=True)
    email = Column(String, unique=True)