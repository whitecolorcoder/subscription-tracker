import datetime
from src.models.subscription import Subscription
from src.repository.subscription import SubscriptionRepo
from src.repository.user import UserRepo
from src.repository.expenses import ExpensesRepo
from src.routes.deps import get_expenses_repo, get_user_repo, get_session


class DateSubscriptionTime:
#Класс, считающий время подписок

    def __init__(self, expenses_repo: ExpensesRepo, user_repo: UserRepo):
        self.expenses_repo = expenses_repo
        self.user_repo = user_repo

    def calculate(self):
        users = self.user_repo.get_all_users()
        for user in users:
            self._handle_subscription(user.subscriptions)

    def _handle_subscription(self, subscriptions : list[Subscription]):
        for sub in subscriptions:
            if self._need_to_update_record(sub):
                self.expenses_repo.create(sub)

    def _need_to_update_record(self, subscription: Subscription) -> bool:
        if subscription.next_payment > datetime.datetime.now() and subscription.is_active and subscription.auto_renew:
            return True
        else:
            return False

    def __call__(self):
        self.calculate()



def build_class():
    # Create a session directly instead of using the generator
    from sqlalchemy.orm import sessionmaker
    from src.config import settings
    from sqlalchemy import create_engine

    engine = create_engine(str(settings.SQLALCHEMY_DATABASE_URI))
    Session = sessionmaker(bind=engine)
    session = Session()

    return DateSubscriptionTime(
        expenses_repo=ExpensesRepo(session=session),
        user_repo=UserRepo(session=session)
    )





#Собрать DateSubscriptionTime класс
#Передеать метод calculate в планировщик задач
#Планировщик задач будет вызывать метод calculate каждые 5 минут
