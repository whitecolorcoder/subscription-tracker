from src.redis_repository.redis_repo import AnalyticsRedis
from src.repository.subscription import SubscriptionRepo

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from src.routes.subscription import SubscriptionOverview


class ServiceAnalitics:
    def __init__(self, postgres_repo: SubscriptionRepo, redis_repo: AnalyticsRedis):
        self.postgres_repo = postgres_repo
        self.redis_repo = redis_repo

    def get_user_analytics(self, user_id: str) -> list["SubscriptionOverview"]:
        user_cache = self.redis_repo.get_user_cache(user_id)
        
        last_data = user_cache.get("last_data")
        
        data_from_database_postgres = self.postgres_repo.get_overview_by_analytics(user_id, last_data)
        
        if data_from_database_postgres:
            user_cache += data_from_database_postgres

            self.redis_repo.set_user_cache(user_id, user_cache)
            
            return user_cache
        else:
            return user_cache

#Написать редис репозиторий. https://redis.io/insight/. Написать логику: сходить в редис, 
# по уникальному ключу посмотреть какие  данные юзера закэшированны, взять последнюю дату кэша-с ней сходить в постгрес 
# и получить не закешированные объекты.

#Дописать тесты