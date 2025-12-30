from datetime import datetime
from sqlalchemy import select
from sqlalchemy.orm import Session
from src.models.expenses import Expense
from src.models.subscription import Subscription

class ExpensesRepo:
    def __init__(self, session: Session):
        self.session = session
        self.model = Expense

    def get_list_expenses(self, user_id: int):
        stmt = select(Expense).where(Expense.user_id == user_id)
        result = self.session.execute(stmt)
        return result.scalars().all()

    def create(self, subscription: Subscription) -> Expense:
        new_expense = Expense(
        user_id=subscription.user_id,
        subscription_id=subscription.id,
        amount=1,
        description=subscription.name,
        currency=subscription.currency,
        date=datetime.now(),
        category =subscription.category
        )
        self.session.add(new_expense)
        self.session.commit()
        return new_expense

    def create_new(self, user_id, id, name, currency, category):
        return self.create()


# GET	/expenses/summary	Получить сводку расходов по категориям
#  def get_expenses_user_category()
