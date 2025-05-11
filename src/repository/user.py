from sqlalchemy.orm import Session
from src.models.users import User

class UserRepo:
    """Отвечает за запросы в таблицу users"""
    
    def __init__(self, session: Session):
        self.session = session
        self.model = User

    def back_information_from_user(self, id: int) -> User:
        try:
            return self.session.get(self.model, id) 
        except Exception:
            raise Exception
            