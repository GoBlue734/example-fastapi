from fastapi import APIRouter
from fastapi import Depends
from fastapi import HTTPException
from fastapi import Response
from fastapi import status
from fastapi.security import OAuth2PasswordRequestForm#used to extract the request body
from sqlalchemy.orm import Session
from .. import database, schemas, models, utils, oauth2

router = APIRouter(tags=["Authentication"])


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    
    #Oauth2PasswordRequestForm returns a dict with the username and password.
    #This uses form data instead of raw json data!
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")
    
    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=f"Invalid credentials")

    #create a jwt token
    #return token
    access_token = oauth2.create_access_token(data={"user_id": user.id})#create the access token passing in the user id

    return {"access_token": access_token, "token_type": "bearer"}