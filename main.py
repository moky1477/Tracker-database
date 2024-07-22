from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from datetime import datetime
import re

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str

class MovieBase(BaseModel):
    email: str
    username: str
    title: str
    date_watched: str  # Keep this as string and ensure the format is correct
    genre: str
    language: str
    personal_rating: float

class TVBase(BaseModel):
    email: str
    username: str
    title: str
    date_watched: str
    genre: str
    language: str
    personal_rating: float

class TripsBase(BaseModel):
    email: str
    username: str
    location: str
    date: str
    personal_rating: str

# Connect to the SQL database
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def check_email_validation(email: str) -> bool:
    email_expression = re.compile(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_expression.match(email):
        return False
    return True

# Create a new user
@app.post("/users/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    if not check_email_validation(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    return {'Message': 'User has been successfully created'}

# Get the detail of users through username
@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_users(email: str, db: Session = Depends(get_db)):
    if not check_email_validation(user.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    user = db.query(models.Users).filter(models.Users.email==email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Add a movie to the database
@app.post('/movies/add_movie', status_code=status.HTTP_201_CREATED)
async def add_movie(movie: MovieBase, db: Session = Depends(get_db)):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    if not check_email_validation(movie.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    db_movie = models.Movies(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return {'Message': 'Your movie has been successfully added to your database'}

# View movies with unique usernames
@app.get('/movies/{username}', status_code=status.HTTP_200_OK)
async def get_movies(email: str, db:Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    movie = db.query(models.Movies).filter(models.Movies.email==email).all()
    if movie is None:
        return HTTPException(status_code=404, detail=f'No movie corresponding to {email} found')
    return movie

# Add a tvshow to the database
@app.post('/tv_shows/add_tvshow', status_code=status.HTTP_201_CREATED)
async def add_tvshow(show: TVBase, db: Session = Depends(get_db)):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    if not check_email_validation(show.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    db_show = models.TV_Series(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return {'Message': 'Your TV Series has been successfully added to your database'}

# View TV Shows with unique usernames
@app.get('/tv_shows/{username}', status_code=status.HTTP_200_OK)
async def get_tvshow(email: str, db:Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    show = db.query(models.TV_Series).filter(models.TV_Series.email==email).all()
    if show is None:
        return HTTPException(status_code=404, detail=f'No TV Show corresponding to {email} found')
    return show

# Add a new trip to the database
