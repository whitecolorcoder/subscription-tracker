from sqlalchemy.orm import Session, joinedload
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from src.models.users import User


class NoUserInDb(Exception):
    "No user in db"

class UserRepo:
    """Репозиторий для работы с таблицей users."""

    def __init__(self, session: Session):
        """Инициализирует репозиторий с SQLAlchemy-сессией."""
        self.session = session
        self.model = User

    def back_information_from_user(self, id: int) -> User:
        """Возвращает пользователя по ID или выбрасывает ошибку."""
        user = self.session.get(self.model, id)
        if user is None:
            raise NoUserInDb
        return user

    def get_user_by_email(self, email: str) -> User:
        """Возвращает пользователя по email или выбрасывает ошибку."""
        stmt = select(self.model).where(self.model.email == email)
        try:
            user = self.session.execute(stmt).scalar_one()
        except NoResultFound:
            raise NoUserInDb
        return user

    def put_user_in_db(self, email: str, hashed_password: str) -> None:
        """Создаёт нового пользователя в базе данных."""
        new_user = self.model(hashed_password=hashed_password, email=email)
        self.session.add(new_user)
        self.session.commit()

    def hard_delete_user(self, user_id: int) -> bool:
        """Полностью удаляет пользователя из базы данных."""
        user = self.session.get(self.model, user_id)
        if not user:
            return False
        self.session.delete(user)
        self.session.commit()
        return True

    def soft_delete_user(self, user_id: int) -> bool:
        """Помечает пользователя как неактивного."""
        user = self.session.get(self.model, user_id)
        if not user or not user.is_active:
            return False
        user.is_active = False
        self.session.commit()
        return True

    def get_all_users(self) -> list[User]:
        """Возвращает всех пользователей с их подписками."""
        stmt = select(self.model).options(joinedload(self.model.subscriptions))
        users_with_subscriptions = self.session.scalars(stmt).unique().all()
        return users_with_subscriptions





