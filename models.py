from sqlalchemy import Column, Integer, String, Float, DateTime
from database import Base
from datetime import datetime

class Users(Base):
    __tablename__ = 'users'

    email = Column(String(100), unique=True)
    username = Column(String(50), primary_key=True)  # Specify length for VARCHAR
    full_name = Column(String(100))                  # Specify length for VARCHAR
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Movies(Base):
    __tablename__ = 'movies'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    username = Column(String(50))  # Specify length for VARCHAR
    title = Column(String(100))         # Specify length for VARCHAR
    date_watched = Column(String(12))
    genre = Column(String(50))                       # Specify length for VARCHAR
    language = Column(String(50))                    # Specify length for VARCHAR
    personal_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class TV_Series(Base):
    __tablename__ = 'tv_series'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100), unique=True)
    username = Column(String(50))  # Specify length for VARCHAR
    title = Column(String(100))         # Specify length for VARCHAR
    date_watched = Column(String(12))
    genre = Column(String(50))                       # Specify length for VARCHAR
    language = Column(String(50))                    # Specify length for VARCHAR
    personal_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())

class Trips(Base):
    __tablename__ = 'trips'

    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(100))
    username = Column(String(50))
    location = Column(String(200))
    date = Column(String(100))
    personal_rating = Column(Float)
    created_at = Column(DateTime, default=datetime.now())
    updated_at = Column(DateTime, default=datetime.now(), onupdate=datetime.now())
