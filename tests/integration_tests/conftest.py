import random
from fastapi import Depends, FastAPI
from fastapi.testclient import TestClient
from typing import Annotated
from faker import Faker

from datetime import datetime, timedelta

import redis
from src.models.subscription import Subscription
from src.redis_repository.redis_repo import AnalyticsRedis
from src.repository.subscription import SubscriptionRepo
import pytest
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, Session
from fastapi import APIRouter
from src.config import settings
from src.repository.user import UserRepo
from pydantic import BaseModel, EmailStr
from src.__main__ import app
from src.models.users import User
from src.routes import user
from src.routes.subscription import SubscriptionResponceModel
from src.services.jwt_token_services import JWTService
from src.services.password_service import PasswordsService
from typing import Generator
from src.services.jwt_token_services import JWTService
from src.models.base import Base
from src.models.expenses import Expense
# Create engine outside fixture so it persists


@pytest.fixture
def get_app() -> TestClient:
    return TestClient(app=app)


@pytest.fixture(scope='function')
def test_engine():
    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    yield engine


@pytest.fixture(scope='function', autouse=True)
def clean_database(test_engine):
    """Automatically clean all data after each test"""
    yield  # Run the test first
    # Clean up after the test
    with test_engine.connect() as connection:
        # Get all table names and truncate them
        for table in reversed(Base.metadata.sorted_tables):
            connection.execute(text(f"DELETE FROM {table.name}"))
        connection.commit()


@pytest.fixture(scope='function')
def test_session_factory(test_engine):
    TestingSessionLocal = sessionmaker(bind=test_engine)
    yield TestingSessionLocal


@pytest.fixture(scope='function')
def get_session(test_session_factory) -> Session:
    session = test_session_factory()
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
def user_with_jwt(add_user):
    jwt_token = JWTService(config=settings).create_jwt(add_user.id)
    setattr(add_user, 'token', jwt_token )
    return add_user


@pytest.fixture(scope='function')
def add_expenses(add_subscriptions, get_session):
    total  = 0
    for i in range(5):
        amount = round(random.uniform(5.0, 100.0), 2)
        total += amount
        expence = Expense(
            subscription_id=add_subscriptions.id,
            user_id=add_subscriptions.user_id,
            amount=amount,
            currency=random.choice(["USD", "EUR", "RSD", "GBP"]),
            date=datetime.utcnow() - timedelta(days=random.randint(1, 30)),
            description=f"Expense {i+1}",
            category=random.choice(["Streaming", "Software", "Fitness", "Education"])
        )
        
        get_session.add(expence)
    
    
    get_session.commit()
    yield add_subscriptions, total
    
@pytest.fixture(scope='function')
def redis_client():
    client = redis.Redis(
        host='localhost',
        port=6379,
        db=0,
        decode_responses=True
    )
    return client

@pytest.fixture(scope='function')
def redis_repo(redis_client):
    return AnalyticsRedis(redis_client)