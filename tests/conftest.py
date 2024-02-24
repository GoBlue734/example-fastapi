from fastapi.testclient import TestClient
from app.main import app
from app import schemas
from app.config import settings
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from app.database import get_db
from app.database import Base
from app.oauth2 import create_access_token
from app import models
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

@pytest.fixture
def test_user(client):
    user_data = {"email": "mike@test.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def test_user2(client):
    user_data = {"email": "beth@test.com", "password": "password123"}
    response = client.post("/users/", json=user_data)
    assert response.status_code == 201
    new_user = response.json()
    new_user["password"] = user_data["password"]
    return new_user

@pytest.fixture
def token(test_user):
    return create_access_token({"user_id": test_user["id"]})

@pytest.fixture
def authorized_client(client, token):
    client.headers = {
        **client.headers,
        "Authorization": f"Bearer {token}"
    }
    return client

@pytest.fixture
def test_posts(test_user, test_user2, session):
    posts_data = [{
        "title": "first title",
        "content": "first content",
        "owner_id": test_user['id']
    }, {
        "title": "2nd title",
        "content": "2nd content",
        "owner_id": test_user['id']
    },
        {
        "title": "3rd title",
        "content": "3rd content",
        "owner_id": test_user['id']
    }, {
        "title": "4th title",
        "content": "4th content",
        "owner_id": test_user2['id']
    }]

    # session.add_all([models.Post(title="first title", content="first content", owner_id=test_user['id']),
    #                 models.Post(title="2nd title", content="2nd content", owner_id=test_user['id']), models.Post(title="3rd title", content="3rd content", owner_id=test_user['id'])])

    def create_post_model(post):
        return models.Post(**post)

    post_map = map(create_post_model, posts_data)
    posts = list(post_map)

    session.add_all(posts)
    session.commit()

    posts = session.query(models.Post).all()
    return posts