from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from fastapi import FastAPI
from src.config import settings
from src.repository.user import UserRepo

app = FastAPI()


@app.get("user/")
def root(id:int):
    engine=create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    session=sessionmaker(engine=engine)
    
    create_UserRepo = UserRepo(session=session).back_information_from_user(id)
    