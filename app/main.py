from fastapi import FastAPI#used to create the FastAPI instance
from fastapi.middleware.cors import CORSMiddleware#used to enable CORS


from . import models#imports the models.py file
from .database import engine#imports the engine variable from the database.py file
from .routers import posts#imports the posts.py file
from . routers import user#imports the user.py file
from . routers import auth#imports the auth.py file
from . routers import vote#imports the vote.py file
from .config import settings#used to get the settings from the .env file


# This line will create the database tables when starting up using the SQLAlchemy models
# This is no longer needed because we are using alembic to create the database tables
#models.Base.metadata.create_all(bind=engine)

# create the FastAPI instance
app = FastAPI()

origins = ["https://www.google.com"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(posts.router)#include the posts router
app.include_router(user.router)#include the user router
app.include_router(auth.router)#include the auth router
app.include_router(vote.router)#include the vote router


#get method for the api endpoint
@app.get("/")#decorator for the api endpoint. path operation decorator
def root():
    return {"message": "Welcome to my API!!!"}
