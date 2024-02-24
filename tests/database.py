from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
import pytest
#import alembic.command as command (to use this instead of sqlalchemy for creating and dropping tables)

#SQLAlchemy database URL for the database. Confirm that the database is running
SQLALCHEMY_DATABASE_URL = f"postgresql://{settings.database_username}:{settings.database_password}@{settings.database_hostname}:{settings.database_port}/{settings.database_name}_test"

if SQLALCHEMY_DATABASE_URL is None:
    print("Cannot connect to the database")
    exit(1)
else:
    print("Connected to the database")


#Establish the connection to the database
engine = create_engine(SQLALCHEMY_DATABASE_URL)

#Create a session factory
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a new session for the tests
@pytest.fixture()
def session():
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


# Return a TestClient instance that will be used in the tests
@pytest.fixture()
def client(session):# use session fixture to create and drop tables
    def override_get_db():

        try:
            yield session
        finally:
            session.close()
    
    app.dependency_overrides[get_db] = override_get_db

    yield TestClient(app)