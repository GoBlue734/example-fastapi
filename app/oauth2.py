from jose import JWTError# this will help us handle the errors
from jose import jwt# this is the library that will help us create the jwt token
from passlib.context import CryptContext# this will help us hash the password
from datetime import datetime# this will help us get the current date and time
from datetime import timedelta# this will help us create the expiration time for the jwt token
from fastapi import Depends# this will help us create a dependency
from fastapi import HTTPException# this will help us raise exceptions
from fastapi import status# this will help us get the status codes
from fastapi.security import OAuth2PasswordBearer# this will help us create the oauth2 scheme
from sqlalchemy.orm import Session# this will help us create a session

from . import schemas# this will help us import the schemas.py file
from . import database# this will help us import the database.py file
from . import models# this will help us import the models.py file
from . config import settings#this will import the settings from config.py

#Login endpoint
oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')#this will help us create the oauth2 scheme

#Need 4 pieces of information to create a jwt token
#1. Secret key
#2. Algorithm
#3. Expiration time
#4. Payload

#Secret key to sign the jwt token
SECRET_KEY = settings.secret_key#secret key to sign the jwt token
ALGORITHM = settings.algorithm#algorithm to sign the jwt token
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes#expiration time for the jwt token

#Create the encoded_token
def create_access_token(data: dict):
    to_encode = data.copy()#jwt.encode will modify the data dictionary so we create a copy of it

    #create the expiration time
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp": expire})#add the expiration time to the dictionary

    #create the jwt token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

    return encoded_jwt

#Verify the jwt token, if it is valid, return the token data to get_current_user
def veryify_access_token(token: str, credentials_exception):
    
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])#decode the jwt token
        id: str = payload.get("user_id")#get the user id from the payload
        if id is None:
            raise credentials_exception
        token_data = schemas.Tokendata(id=id)
    except JWTError:
        raise credentials_exception
    
    return token_data

#Once we have the token verified, we can get the current user w/ the id
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail=f"Invalid credentials",
        headers={"WWW-Authenticate": "Bearer"}
    )

    token = veryify_access_token(token, credentials_exception)#verify the token
    user = db.query(models.User).filter(models.User.id == token.id).first()#get the user from the database

    return user#This allows the routes in posts.py to get the current user w/ current_user: int = Depends(oauth2.get_current_user)