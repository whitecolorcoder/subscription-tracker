from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing import Annotated
from faker import Faker

from datetime import datetime
from src.repository.subscription import SubscriptionRepo
import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter
from src.config import settings
from src.repository.user import UserRepo
from pydantic import BaseModel, EmailStr
from src.__main__ import app
from src.models.users import User


# Create engine outside fixture so it persists
engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
TestingSessionLocal = sessionmaker(bind=engine)


@pytest.fixture(scope='function')
def get_session() -> Session:
    session = TestingSessionLocal()
    try:
        yield session
    finally:
        session.close()


@pytest.fixture(scope='function')
def add_user(get_session):
    faker = Faker()
    user = User(email=faker.email(), hashed_password='qwerty')
    get_session.add(user)
    get_session.commit()
    get_session.refresh(user) 
    yield user
    get_session.delete(user)
    get_session.commit()


@pytest.fixture       
def get_app() -> TestClient:
    return TestClient(app=app)
    
'''
Создать фикстуру которая добавляет данные перед тестом в базу данных
а потом очищает базу данных
'''