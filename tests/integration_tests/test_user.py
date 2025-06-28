

from datetime import datetime
import select

from src.models.users import User
from src.services.jwt_token_services import JWTService

import pytest
from datetime import datetime
from sqlalchemy import select
from fastapi.testclient import TestClient

from src.config import settings

def test_no_user_in_db(get_app):
    responce = get_app.get('/test/user/1')
    assert responce.status_code == 404

# def test_user_in_db(get_app, add_user):
#     responce = get_app.get(f'/test/user/{add_user.id}')
#     assert responce.status_code == 200
#     body = responce.json()
#     assert body['id'] == add_user.id

# def test_sucess_user_registration(get_app, get_session):
#     email = "facebook@mail.ru"
#     # Проверяем роутер
#     responce = get_app.post('/auth/protected', json={"email": email,
#     "password": "qwerty"})
#     assert responce.status_code == 201

#     #Проверяем базу данных
#     stmt = select(User).where(User.email == email)
#     user = get_session.execute(stmt).scalar_one()

#     assert user.email == email
#     assert user.hashed_password is not None
#     get_session.delete(user)
#     get_session.commit()

# def test_user_already_exsists(get_app, add_user):
#     duplicate_response = get_app.post(
#         '/auth/protected',
#         json={
#             "email": add_user.email,
#             "password": add_user.hashed_password,
#         }
#     )
#     assert duplicate_response.status_code == 400


# def test_sucess_login(get_app, add_user):
#     responce = get_app.post('/auth/login', json={"email": add_user.email,
#     "password": 'qwerty123'})
#     assert responce.status_code == 200
#     body = responce.json()
#     assert isinstance(body['token'], str)


# def test_not_sucess_login(get_app, add_user):
#     responce = get_app.post('/auth/login', json={"email": add_user.email,
#     "password": 'dfdfsdfsdf'})
#     assert responce.status_code == 401
#     body = responce.json()
#     assert body['detail'] == 'Invalid credentials'

# def test_get_user_subscriptions(get_app, add_subscriptions, add_user):
#     jwt = JWTService(config=settings).create_jwt(add_user.id)
#     response = get_app.get('/subscription?jwt_token={jwt}')
#     assert response.status_code == 201
#     body = response.json()
#     assert len(body) == 1

# def test_create_new_subscription(get_app, add_user):
#     jwt = JWTService(config=settings).create_jwt(add_user.id)
#     response = get_app.post('/subscription', headers={'Bearer token': jwt},
#                             body={
#                             "subscription_name":"Netflix Premium",
#                             "price": 15.99,
#                             "start_date": datetime(2023, 6, 1),
#                             "end_date": datetime(2023, 7, 1),
#                             "auto_renewal": True})
#     assert response == 201



