from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.subscription import Subscription

class SubscriptionRepo:
    """Отвечает за запросы в таблицу subscriptions"""
    
    def __init__(self, session: Session):
        self.session = session
        self.model = Subscription

    def get_subscriptions_by_user(self, user_id: int) -> list[Subscription]:
        try:
            stmt = select(self.model).where(self.model.user_id == user_id)
            result = self.session.execute(stmt)
            return result.scalars().all()
        except Exception as e:
            raise Exception from e
    
            