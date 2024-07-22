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