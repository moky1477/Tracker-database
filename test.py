from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from database import engine, SessionLocal
from datetime import datetime
import re

app = FastAPI()

class MovieBase(BaseModel):
    email: str
    username: str
    title: str
    date_watched: str  # Keep this as string and ensure the format is correct
    genre: str
    language: str
    personal_rating: float

# Add a movie to the database
@app.post('/movies/add_movie', status_code=status.HTTP_201_CREATED)
async def add_movie(movie: MovieBase):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    db_movie = models.Movies(**movie.dict())
    db_movie.genre = db_movie.genre.replace(" ", "")
    genre_list = db_movie.genre.split(',')
    
    return genre_list
