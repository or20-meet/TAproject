from model import Base, User, Photo

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

engine = create_engine('sqlite:///databases.db', connect_args={'check_same_thread': False})

Base.metadata.create_all(engine)
DBSession = sessionmaker(bind=engine)
session = DBSession()


#User functions

def add_user(username, password):
	new = User(username=username, password = password)
	session.add(new)
	session.commit()

def get_all_users():
	return session.query(User).all()

def get_user_by_id(id):
	return session.query(User).filter_by(id=id).first()

def get_user_by_username(username):
	return session.query(User).filter_by(username = username).first()

def del_all_users():
	session.query(User).delete()
	session.commit()


#Photo functions

def add_photo(link, username):
	newp = Photo(link=link, username = username)
	session.add(newp)
	session.commit()

def get_all_photos():
	return session.query(Photo).all()

def get_photo_by_id(id):
	return session.query(Photo).filter_by(id=id).first()


def del_all_photos():
	session.query(Photo).delete()
	session.commit()

def get_photos_by_user(user):
	return session.query(Photo).filter_by(username = user.username).all()
