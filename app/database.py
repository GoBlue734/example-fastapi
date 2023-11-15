from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from . config import settings

'''
#Not needed because we are using SQLAlchemy
#import psycopg2#postgresql database driver
#from psycopg2.extras import RealDictCursor#used to convert the database result to a dictionary format
import time#used to sleep the api

'''

#SQLAlchemy database URL for the database. Confirm that the database is running
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}"

if SQLALCHEMY_DATABASE_URL is None:
    print("Cannot connect to the database")
    exit(1)
else:
    print("Connected to the database")


#Establish the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()#SQLAlchemy model for the database table. ORM model

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

'''
#This is unnecessary because we are using SQLAlchemy
#psycopg2 connection to the database using raw SQL
while True:
    try:
        conn = psycopg2.connect(host='localhost', database='fastapi', user='postgres',
        password='++He77@-!n2U++', cursor_factory=RealDictCursor)
        cursor = conn.cursor()
        print("Connected to the database")
        break
    except Exception as error:
        print("Failed to connect to the database")
        print(error)
        time.sleep(5)
'''