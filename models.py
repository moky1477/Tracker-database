from sqlalchemy import Column, Integer, String, Boolean, Date, Float
from database import Base

class Users(Base):
    __tablename__ = 'users'

    username = Column(String(50), primary_key=True)  # Specify length for VARCHAR
    full_name = Column(String(100))                  # Specify length for VARCHAR

class Movies(Base):
    __tablename__ = 'movies'

    username = Column(String(50))  # Specify length for VARCHAR
    title = Column(String(100), primary_key=True)         # Specify length for VARCHAR
    date_watched = Column(String(12))
    genre = Column(String(50))                       # Specify length for VARCHAR
    language = Column(String(50))                    # Specify length for VARCHAR
    personal_rating = Column(Float)

class TV_Series(Base):
    __tablename__ = 'tv_series'

    username = Column(String(50))  # Specify length for VARCHAR
    title = Column(String(100), primary_key=True)         # Specify length for VARCHAR
    date_watched = Column(String(12))
    genre = Column(String(50))                       # Specify length for VARCHAR
    language = Column(String(50))                    # Specify length for VARCHAR
    personal_rating = Column(Float)
