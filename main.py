from fastapi import FastAPI, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from sqlalchemy.orm import Session
from sqlalchemy import text
import models
from database import engine, SessionLocal
from datetime import datetime
import re
from enum import Enum

app = FastAPI()
models.Base.metadata.create_all(bind = engine)

from enum import Enum

class Genres(str, Enum):
    action = 'Action'
    thriller = 'Thriller'
    drama = 'Drama'
    comedy = 'Comedy'
    horror = 'Horror'
    romance = 'Romance'
    sci_fi = 'Sci-Fi'
    fantasy = 'Fantasy'
    mystery = 'Mystery'
    adventure = 'Adventure'
    animation = 'Animation'
    documentary = 'Documentary'
    musical = 'Musical'
    crime = 'Crime'
    family = 'Family'
    history = 'History'
    war = 'War'
    western = 'Western'
    sport = 'Sport'
    biography = 'Biography'

class UserBase(BaseModel):
    email: str
    username: str
    full_name: str

class MovieBase(BaseModel):
    email: str
    username: str
    title: str
    date_watched: str  # Keep this as string and ensure the format is correct
    language: str
    personal_rating: float

class TVBase(BaseModel):
    email: str
    username: str
    title: str
    date_watched: str
    # genre: str
    language: str
    personal_rating: float

class TripsBase(BaseModel):
    email: str
    username: str
    location: str
    date: str
    personal_rating: float

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

# Get the detail of users through email
@app.get('/users/{email}', status_code=status.HTTP_200_OK)
async def read_users(email: str, db: Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    user = db.query(models.Users).filter(models.Users.email==email).first()
    if user is None:
        raise HTTPException(status_code=404, detail='User not found')
    return user

# Add a movie to the database
@app.post('/movies/add_movie', status_code=status.HTTP_201_CREATED)
async def add_movie(genre: Genres, movie: MovieBase, db: Session = Depends(get_db)):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    if not check_email_validation(movie.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    # db_movie = models.Movies(**movie.dict())

    db_movie = models.Movies(
        email=movie.email,
        username=movie.username,
        title=movie.title,
        date_watched=movie.date_watched,
        genre=genre.value,
        language=movie.language,
        personal_rating=movie.personal_rating
    )
        
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
async def add_tvshow(genre: Genres, show: TVBase, db: Session = Depends(get_db)):
    # # Ensure the date string matches the expected format (e.g., '15-07-2024')
    # try:
    #     datetime.strptime(movie.date_watched, '%d-%m-%Y')
    # except ValueError:
    #     return {'Message': 'Incorrect date format. Expected format: DD-MM-YYYY'}
    if not check_email_validation(show.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    # db_show = models.TV_Series(**show.dict())

    db_show = models.TV_Series(
        email=show.email,
        username=show.username,
        title=show.title,
        date_watched=show.date_watched,
        genre=genre.value,
        language=show.language,
        personal_rating=show.personal_rating
    )

    db.add(db_show)
    db.commit()
    db.refresh(db_show)
    return {'Message': 'Your TV Series has been successfully added to your database'}

# View TV Shows with emails
@app.get('/tv_shows/{email}', status_code=status.HTTP_200_OK)
async def get_tvshow(email: str, db:Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    show = db.query(models.TV_Series).filter(models.TV_Series.email==email).all()
    if show is None:
        return HTTPException(status_code=404, detail=f'No TV Show corresponding to {email} found')
    return show

# Add a new trip to the database
@app.post('/trips/add_trips', status_code=status.HTTP_201_CREATED)
async def add_trip(trip: TripsBase, db: Session = Depends(get_db)):
    if not check_email_validation(trip.email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    db_trip = models.Trips(**trip.dict())
    db.add(db_trip)
    db.commit()
    db.refresh(db_trip)
    return {'Message': 'Your trip has been successfully added'}

# View Trips with emails
@app.get('/trips/{email}', status_code=status.HTTP_200_OK)
async def get_trips(email: str, db: Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    trip = db.query(models.Trips).filter(models.Trips.email == email).all()
    if trip is None:
        return HTTPException(status_code=404, detail=f'No Trips corresponding to {email} found')
    return trip

# Extract all user data based on the email input
@app.get('/user_data/{email}', status_code=status.HTTP_200_OK)
async def get_user_data(email: str, db: Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    
    # Fetch movies, TV series, and trips for the given email
    movies = db.query(models.Movies).filter(models.Movies.email == email).all()
    tv_series = db.query(models.TV_Series).filter(models.TV_Series.email == email).all()
    trips = db.query(models.Trips).filter(models.Trips.email == email).all()

    # Check if any of the queries return None (although `.all()` should return an empty list if no results are found)
    if not movies and not tv_series and not trips:
        raise HTTPException(status_code=404, detail=f'No data found for email: {email}')
    
    # Return a combined response
    return {
        'movies': movies,
        'tv_series': tv_series,
        'trips': trips
    }

# Extract all user data based on the email input
# @app.get('/user_data/{email}', status_code=status.HTTP_200_OK)
# async def get_user_data(email: str, db: Session = Depends(get_db)):
#     if not check_email_validation(email):
#         raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')
    
#     # SQL Query to fetch all Movies, TV Series, and Trips
#     query = text("""
#         SELECT
#             'movie' AS type,
#             m.title AS title, m.date_watched AS date_watched, m.genre AS genre, m.language AS language, m.personal_rating AS personal_rating,
#             NULL AS location, NULL AS trip_date
#         FROM movies m
#         WHERE m.email = :email
        
#         UNION ALL
        
#         SELECT
#             'tv_series' AS type,
#             t.title AS title, t.date_watched AS date_watched, t.genre AS genre, t.language AS language, t.personal_rating AS personal_rating,
#             NULL AS location, NULL AS trip_date
#         FROM tv_series t
#         WHERE t.email = :email
        
#         UNION ALL
        
#         SELECT
#             'trip' AS type,
#             NULL AS title, NULL AS date_watched, NULL AS genre, NULL AS language, NULL AS personal_rating,
#             t.location AS location, t.date AS trip_date
#         FROM trips t
#         WHERE t.email = :email
#     """)
    
#     result = db.execute(query, {'email': email})
#     rows = result.fetchall()

#     movies = []
#     tv_series = []
#     trips = []

#     for row in rows:
#         if row['type'] == 'movie':
#             movies.append({
#                 'title': row['title'],
#                 'date_watched': row['date_watched'],
#                 'genre': row['genre'],
#                 'language': row['language'],
#                 'personal_rating': row['personal_rating']
#             })
#         elif row['type'] == 'tv_series':
#             tv_series.append({
#                 'title': row['title'],
#                 'date_watched': row['date_watched'],
#                 'genre': row['genre'],
#                 'language': row['language'],
#                 'personal_rating': row['personal_rating']
#             })
#         elif row['type'] == 'trip':
#             trips.append({
#                 'location': row['location'],
#                 'date': row['trip_date']
#             })

#     return {
#         'movies': movies,
#         'tv_series': tv_series,
#         'trips': trips
#     }
