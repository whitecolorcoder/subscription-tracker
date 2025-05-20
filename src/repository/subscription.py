from sqlalchemy.orm import Session
from src.models.subscription import Subscription

class SubscriptionRepo:
    """Отвечает за запросы в таблицу subscriptions"""
    
    def __init__(self, session: Session):
        self.session = session
        self.model = Subscription

    def list_subscription_users(self, id: int) -> Subscription:
        try:
            return self.session.get(self.model, id) 
        except Exception:
            raise Exception
            