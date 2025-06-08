from sqlalchemy import select
from src.models.users import User
from tests.integration_tests.conftest import add_user


def test_no_user_in_db(get_app):
    responce = get_app.get('/test/user/1')
    assert responce.status_code == 404

def test_user_in_db(get_app, add_user):
    responce = get_app.get(f'/test/user/{add_user.id}')
    assert responce.status_code == 200
    body = responce.json()
    assert body['id'] == add_user.id
    
def test_sucess_user_registration(get_app, get_session):
    email = "facebook@mail.ru"
    # Проверяем роутер
    responce = get_app.post('/auth/protected', json={"email": email,
    "password": "qwerty"})
    assert responce.status_code == 201
    
    #Проверяем базу данных
    stmt = select(User).where(User.email == email)
    user = get_session.execute(stmt).scalar_one()
    
    assert user.email == email
    assert user.hashed_password is not None
    
#def test_user_already_exsists
    
        
    