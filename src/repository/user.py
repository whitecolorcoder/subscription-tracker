from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.models.users import User


class NoUserInDb(Exception):
    "No user in db"

class UserRepo:
    """Отвечает за запросы в таблицу users"""
    
    def __init__(self, session: Session):
        self.session = session
        self.model = User

    def back_information_from_user(self, id: int) -> User:
        user = self.session.get(self.model, id) 
        if user is None:
            raise NoUserInDb 
        return user
         
    def get_user_by_email(self, email: str) -> User:
        stmt = select(self.model).where(self.model.email == email)
        try:
            user = self.session.execute(stmt).scalar_one()
        except NoResultFound:
            raise NoUserInDb
        return user

    def put_user_in_db(self, email: str, hashed_password: str) -> None:
        new_user = self.model(hashed_password=hashed_password, email=email)
        self.session.add(new_user)
        #try:
        self.session.commit()
        
        
    

