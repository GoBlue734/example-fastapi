from fastapi import FastAPI# used to create the FastAPI instance
from fastapi import Depends# used to create a response
from fastapi import status# status codes for the response
from fastapi import HTTPException# the exception class will be used to raise exceptions
from fastapi import Response# response will be used to return a response with a status code
from fastapi import APIRouter# used to create a router
from sqlalchemy.orm import Session# imports the Session class from the sqlalchemy.orm module

from .. import schemas# import the schemas.py file
from .. import models# import the models.py file
from .. import utils# import the utils.py file
from ..database import get_db# imports the get_db function from the database.py file

router = APIRouter(
    prefix="/users",
    tags=["Users"]
)


# Create a user
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    #Hash the password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

# Get user by id
@router.get('/{id}', response_model=schemas.UserOut)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User with id {id} not found")
    return user