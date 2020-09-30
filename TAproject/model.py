from sqlalchemy import Column, Integer, String, Date, ForeignKey, Float, Boolean, DateTime
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class User(Base):
	__tablename__='users'
	id = Column(Integer, primary_key = True)
	username = Column(String)
	password = Column(String)


class Photo(Base):
	__tablename__ = 'photos'
	id = Column(Integer, primary_key = True)
	link = Column(String)
	username = Column(String)