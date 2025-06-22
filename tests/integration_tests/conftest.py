import random
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing import Annotated
from faker import Faker

from datetime import datetime, timedelta
from src.models.subscription import Subscription
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
from src.routes import user
from src.routes.subscription import SubscriptionResponceModel
from src.services.password_service import PasswordsService
from typing import Generator

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
def add_user(get_session)-> User:
    faker = Faker()
    pasword_service = PasswordsService()
    password = 'qwerty123'
    user = User(email=faker.email(), hashed_password=pasword_service.create_hash(password))
    get_session.add(user)
    get_session.commit()
    get_session.refresh(user) 
    yield user
    get_session.delete(user)
    get_session.commit()

@pytest.fixture(scope='function')
def add_subscriptions(get_session, add_user):
    faker = Faker()
    now = datetime.utcnow()
    trial_days = random.randint(7, 30)

    subscription = Subscription(
        user_id=add_user.id,
        name=faker.company(),
        category=random.choice(["Streaming", "Software", "Fitness", "Education"]),
        price=round(random.uniform(5.0, 100.0), 2),
        currency=random.choice(["USD", "EUR", "RSD", "GBP"]),
        billing_period=random.choice(["monthly", "yearly"]),
        next_payment=now + timedelta(days=random.randint(1, 30)),
        trial_ends_at=now + timedelta(days=trial_days),
        is_active=random.choice([True, False]),
        auto_renew=random.choice([True, False]),
        notes=faker.sentence(nb_words=6),
        logo_url=faker.image_url(),
        created_at=now)
                                 
    get_session.add(subscription)
    get_session.commit()
    get_session.refresh(subscription) 
    yield subscription
    get_session.delete(subscription)
    get_session.commit()

@pytest.fixture       
def get_app() -> TestClient:
    return TestClient(app=app)
    
'''
Создать фикстуру которая добавляет данные перед тестом в базу данных
а потом очищает базу данных
'''