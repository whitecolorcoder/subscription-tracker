from datetime import datetime, timedelta
from sqlalchemy import select
from sqlalchemy.orm import Session

from src.models.expenses import Expense
from src.models.subscription import Subscription
import typing

from fastapi.websockets import WebSocket

if typing.TYPE_CHECKING:
    from src.routes.subscription import SubscriptionCreate
from sqlalchemy.orm import joinedload
from sqlalchemy import func


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

    def get_one_subscription(self, user_id: int, subscription_id: int) -> Subscription:
        """Получение одной подписки по user_id и subscription_id."""

        stmt = select(self.model).where(
                self.model.user_id == user_id,
                self.model.id == subscription_id
            )
        result = self.session.execute(stmt)
        subscription = result.scalar_one_or_none()
        if not subscription:
            raise ValueError("Subscription not found")
        return subscription

    def create_subscription(self, user_id: int, subscription_data: 'SubscriptionCreate') -> Subscription:
        """Создание подписки в БД."""
        subscription_dict = subscription_data.model_dump()
        subscription_dict["user_id"] = user_id


        new_subscription = self.model(**subscription_dict)
        self.session.add(new_subscription)
        self.session.commit()
        self.session.refresh(new_subscription)
        return new_subscription

    def get_filtered_subscriptions_sync(self, user_id: int, filters: dict[str:str])-> list[Subscription]:
        query = self.session.query(Subscription).filter(Subscription.user_id == user_id)

        if "categories" in filters:
            query = query.filter(Subscription.category.in_(filters["categories"]))

        if "min_price" in filters:
            query = query.filter(Subscription.price >= filters["min_price"])

        return query.all()

    def update_subscription(self, user_id: int, subscription_id: int, **kwargs):
        if self.get_one_subscription(user_id, subscription_id):
            stmt = (
                select(self.model)
                .where(self.model.user_id == user_id, self.model.id == subscription_id)
            )
            result = self.session.execute(stmt)
            subscription = result.scalar_one_or_none()

            for key, value in kwargs.items():
                setattr(subscription, key, value)

            self.session.commit()
            self.session.refresh(subscription)
            return subscription

    def delete_subscription(self, user_id: int, subscription_id: int) -> bool:
        subscription = self.get_one_subscription(user_id, subscription_id)
        self.session.delete(subscription)
        self.session.commit()
        return subscription

    def sum_price_by_category(self, category: str, user_id: int) -> int:
        user_subcriptions = self.get_filtered_subscriptions_sync(user_id, filters={'category': category})
        count = 0
        for i in user_subcriptions:
            count +=i.price
        return count

    def get_nextpayment_user(self) -> list[Subscription]:
        threshold_date = datetime.now() + timedelta(days=3)

        # Filter directly in the database
        subscriptions = (
            self.session.query(Subscription.user_id)
            .filter(Subscription.next_payment <= threshold_date)
            .all()
        )
        return subscriptions

    def get_subs_from_bd(self) -> list[Subscription]:
        stmt = self.session.query(Subscription).filter(Subscription.next_payment - datetime.now() <= timedelta(days=3))
        return stmt.all()
    
    def get_overview_by_analytics(self, user_id: int, last_data: datetime.date = None):
        stmt = (
            self.session.query(Subscription)
            .add_columns(func.coalesce(func.sum(Expense.amount), 0).label("total_expenses"))
            .outerjoin(Expense, Subscription.id == Expense.subscription_id)
            .filter(Subscription.user_id == user_id)
            .group_by(Subscription.id)
            .order_by(Subscription.next_payment)
            ) 
        
        if last_data:
            today = datetime.now().date()
            stmt = stmt.filter(Expense.date >= last_data, Expense.date <= today) 
            
        result = stmt.all()

        for i in result:
            setattr(i[0], "sum_expenses", i[1])
            
        return result
    
    # разобраться с методом 