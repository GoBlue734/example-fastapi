from .database import Base#used to create the database table
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.sql.sqltypes import TIMESTAMP#used to set the created_at column to a timestamp
from sqlalchemy.sql.expression import text#used to set the default value of the created_at column to the current time
from sqlalchemy.orm import relationship#used to create a relationship between the posts and users table

#SQLAlchemy model for the database table. ORM model
#This Post class is different than the Post class in the main.py file which is a Pydantic model
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, server_default="True", nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    #Foreign key to the users table
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable = False)#ondelete="CASCADE" will delete all the posts of the user when the user is deleted

    owner = relationship("User")#creates a relationship between the posts and users table


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)
    created_at = Column(TIMESTAMP(timezone=True), server_default=text('now()'), nullable=False)
    phone_numner = Column(String)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True)