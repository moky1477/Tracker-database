from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, EmailStr
import re

app = FastAPI()

class emailValid(BaseModel):
    user_email: str

@app.post('/users/')
async def validate(email_model: emailValid):
    email_expression = re.compile('^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$')
    if not email_expression.match(email_model.user_email):
        return {'Failure': 'Email not valid, please enter again'}
    return {'Message': 'Email is valid', 'user_email': email_model.user_email}

@app.get('/user_data/{email}', status_code=status.HTTP_200_OK)
async def get_user_data(email: str, db: Session = Depends(get_db)):
    if not check_email_validation(email):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail='Please enter a valid email')

    # SQL query to fetch all movies and TV series for the given email
    query = text("""
        SELECT
            m.title AS movie_title, m.date_watched AS movie_date_watched, m.genre AS movie_genre, m.language AS movie_language, m.personal_rating AS movie_personal_rating,
            t.title AS tv_title, t.date_watched AS tv_date_watched, t.genre AS tv_genre, t.language AS tv_language, t.personal_rating AS tv_personal_rating
        FROM movies m
        LEFT JOIN tv_series t ON m.email = t.email
        WHERE m.email = :email
    """)
    
    result = db.execute(query, {'email': email})
    rows = result.fetchall()

    movies = []
    tv_series = []

    # Process rows to separate the results into movies and TV series
    for row in rows:
        if row['movie_title']:
            movies.append({
                'title': row['movie_title'],
                'date_watched': row['movie_date_watched'],
                'genre': row['movie_genre'],
                'language': row['movie_language'],
                'personal_rating': row['movie_personal_rating']
            })
        if row['tv_title']:
            tv_series.append({
                'title': row['tv_title'],
                'date_watched': row['tv_date_watched'],
                'genre': row['tv_genre'],
                'language': row['tv_language'],
                'personal_rating': row['tv_personal_rating']
            })

    # Fetch trips separately
    trips = db.query(models.Trips).filter(models.Trips.email == email).all()
    
    return {
        'movies': movies,
        'tv_series': tv_series,
        'trips': trips
    }
