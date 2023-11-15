from pydantic import BaseModel#Basemodel is used to create a model for the request body
from pydantic import EmailStr#used to validate the email
from datetime import datetime#used to get the current date and time
from typing import Optional#used to make a field optional
from pydantic import conint#used to set the minimum and maximum value of a field


# Pydanctic model for the request body
#This Post class is different than the Post class in the models.py file which is a SQLAlchemy model
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    #rating: Optional[int] = None

#extends the PostBase class
class PostCreate(PostBase):
    pass#accepts all the fields from the PostBase class


#This class is used to return the user data
class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

#Used to show the user when someone searches all posts or a specific post. Used in the Post class
class ShowUser(BaseModel):
    id: int
    email: EmailStr

    class Config:
        from_attributes = True

#This class is used to return the post data
class Post(PostBase):
    id: int
    created_at: datetime
    owner_id: int
    owner: ShowUser#Using ShowUser instead of UserOut because we don't want to show the created_at field in the response
    #rating: Optional[int] = None

    #Pydantic model will only read dictionaries.
    #This class makes Pydantic compatible with SQLAlchemy (ORM models). Converts the SQLAlchemy model to a dictionary
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int

    class Config:
        from_attributes = True


#This class is used to return the post data for creating a user
class UserCreate(BaseModel):
    email: EmailStr
    password: str



#This is used to return the user data for the login
class UserLogin(BaseModel):
    email: EmailStr
    password: str

#This class is used to return the access token
class Token(BaseModel):
    access_token: str
    token_type: str

class Tokendata(BaseModel):
    id: Optional[int] = None

class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)#used to set the minimum and maximum value of a field

    class Config:
        from_attributes = True