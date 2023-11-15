from fastapi import FastAPI# used to create the FastAPI instance
from fastapi import Depends# used to create a response
from fastapi import status# status codes for the response
from fastapi import HTTPException# the exception class will be used to raise exceptions
from fastapi import Response# response will be used to return a response with a status code
from fastapi import APIRouter# used to create a router
from sqlalchemy.orm import Session# imports the Session class from the sqlalchemy.orm module
from sqlalchemy import func# used to count the number of posts
from typing import List# used to create a list of posts
from typing import Optional# used to make a field optional

from ..database import get_db# imports the get_db function from the database.py file
from .. import schemas# import the schemas.py file
from .. import models# import the models.py file
from .. import oauth2# import the oauth2.py file

router = APIRouter(
    prefix="/posts",
    tags=["Posts"]
)

# get method for posts endpoint
#router.get("/", response_model=list[schemas.Post])
@router.get("/", response_model=List[schemas.PostOut])
def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user),
Limit: int = 10, skip: int = 0, search: Optional[str] = ""):#validate the request body using the Post model
    #SQL query to get all the posts from the database
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()#fetch all the posts from the database

    ''' We are making a social media app so we want users to be able to see all the posts
    #Only allow the user to see their own posts
    posts = db.query(models.Post).filter(models.Post.owner_id == current_user.id).all()
    '''
    
    #posts = db.query(models.Post).all()#fetch all the posts from the database
    #Limit the number of posts returned
    #posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()
    
    #First line is the query we want to execute in SQL. Second line is the SQLAlchemy equivalent
    #SELECT posts.*, COUNT(votes.post_id) as votes FROM posts LEFT JOIN votes on posts.id = votes.post_id GROUP BY posts.id;
    posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(Limit).offset(skip).all()

    return posts#return the posts as a response


# create a post method for the posts endpoint
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def make_post(post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):#validate the request body using the Post model
    '''
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """, 
    (post.title, post.content, post.published))
    new_post = cursor.fetchone()#fetch the newly created post
    conn.commit()#commit the changes to the database
    '''

    #Create the post
    new_post = models.Post(owner_id=current_user.id, **post.dict())#convert the post to a dictionary and unpack it
    #Add the post to the database
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post#return the newly created post

# get post by id
@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):#validate the id as an integer
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #post = cursor.fetchone()#fetch the post with the given id
    
    #post = db.query(models.Post).filter(models.Post.id == id).first()#fetch the post with the given id
    
    post = posts = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()

    if not post:#if the post is not found
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
        
        #used if we didn't have the exception above. would need function parameter response: Response
        #response.status_code = status.HTTP_404_NOT_FOUND#set the response status code to 404
        #return {"message": f"Post with id {id} not found"}

    '''We are making a social media app so we want users to be able to see all the posts
    #Only allow the user to see their own posts
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to view this post")
    '''

    return post#return the post as a response

# delete post by id
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #deleted_post = cursor.fetchone()#fetch the post with the given id
    #conn.commit()#commit the changes to the database

    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    #Check if the post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    #Check if the user is authorized to delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to delete this post")
    
    #Make database changes
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)#return the post as a response


# update post by id
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db),
current_user: int = Depends(oauth2.get_current_user)):
    
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING * """,
    #(post.title, post.content, post.published, str(id)))
    #updated_post = cursor.fetchone()
    #conn.commit()

    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    #Check if the post exists
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    #Check if the user is authorized to update the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="You are not authorized to update this post")

    #Make database changes
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()
