from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from datetime import datetime

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

class UserBase(BaseModel):
    username: str
    full_name: str

class MovieBase(BaseModel):
    username: str
    title: str
    date_watched: str  # Keep this as string and ensure the format is correct
    genre: str
    language: str
    personal_rating: float

class TVBase(BaseModel):
    username: str
    title: str
    date_watched: str
    genre: str
    language: str
    personal_rating: float

class TripsBase(BaseModel):
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

# Create a new user
@app.post("/users/create_user", status_code=status.HTTP_201_CREATED)
async def create_user(user: UserBase, db: Session = Depends(get_db)):
    db_user = models.Users(**user.dict())
    db.add(db_user)
    db.commit()
    return {'Message': 'User has been successfully created'}

# Get the detail of users through username
@app.get('/users/{user_id}', status_code=status.HTTP_200_OK)
async def read_users(user_name: str, db: Session = Depends(get_db)):
    user = db.query(models.Users).filter(models.Users.username==user_name).first()
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
    db_movie = models.Movies(**movie.dict())
    db.add(db_movie)
    db.commit()
    db.refresh(db_movie)
    return {'Message': 'Your movie has been successfully added to your database'}

# View movies with unique usernames
@app.get('/movies/{username}', status_code=status.HTTP_200_OK)
async def get_movies(username: str, db:Session = Depends(get_db)):
    movie = db.query(models.Movies).filter(models.Movies.username==username).all()
    if movie is None:
        return HTTPException(status_code=404, detail=f'No movie corresponding to {username} found')
    return movie

# Add a tvshow to the database
@app.post('/tv_shows/add_tvshow', status_code=status.HTTP_201_CREATED)
async def add_tvshow(show: TVBase, db: Session = Depends(get_db)):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    db_show = models.TV_Series(**show.dict())
    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return {'Message': 'Your TV Series has been successfully added to your database'}

# View TV Shows with unique usernames
@app.get('/tv_shows/{username}', status_code=status.HTTP_200_OK)
async def get_tvshow(username: str, db:Session = Depends(get_db)):
    show = db.query(models.TV_Series).filter(models.TV_Series.username==username).all()
    if show is None:
        return HTTPException(status_code=404, detail=f'No TV Show corresponding to {username} found')
    return show