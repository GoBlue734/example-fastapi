from fastapi import FastAPI# used to create the FastAPI instance
from fastapi import Depends# used to create a response
from fastapi import status# status codes for the response
from fastapi import HTTPException# the exception class will be used to raise exceptions
from fastapi import Response# response will be used to return a response with a status code
from fastapi import APIRouter# used to create a router
from sqlalchemy.orm import Session# imports the Session class from the sqlalchemy.orm module

from .. import schemas, database, models, oauth2# importing the schemas, database, models and oauth2 files from the parent directory

router = APIRouter(
    prefix="/vote",
    tags=["Vote"]
)

@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(database.get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id: {vote.post_id} not found")

    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id, models.Vote.user_id == current_user.id)
    found_vote = vote_query.first()

    if(vote.direction == 1):
        if(found_vote):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=f"User {current_user.id} has already voted on post {vote.post_id}")
        new_vote = models.Vote(post_id = vote.post_id, user_id = current_user.id)
        db.add(new_vote)
        db.commit()
        return{"message": "Vote created"}
    else:
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"User {current_user.id} has not voted on post {vote.post_id}")

        vote_query.delete(synchronize_session=False)#synchronize_session=False is used to prevent the error "This Session's transaction has been rolled back due to a previous exception during flush."
        db.commit()

        return{"message": "Vote deleted"}