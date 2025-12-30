from datetime import date
from unittest import mock
from datetime import timedelta

from src.repository import subscription
from src.repository.subscription import SubscriptionRepo
from src.services.service_analitics import ServiceAnalitics

def test_redis_cache(redis_repo):
    user_id = '100'
    data = ["Yandex"]
    redis_repo.set_user_cache(user_id, data)
    response = redis_repo.get_user_cache(user_id)
    assert isinstance(response, dict)
    responce_date = redis_repo.get_last_updated(user_id)
    assert responce_date is not None
    

def test_services_class_get_user_analytics_empty_cache_and_db():
    mock_redis_repo =  mock.Mock()
    mock_redis_repo.get_user_cache.return_value = {}
    mock_postgres_repo = mock.Mock()
    mock_postgres_repo.get_new_data.return_value = []
    mock_postgres_repo.get_overview_by_analytics.return_value = []
    
    service = ServiceAnalitics(redis_repo=mock_redis_repo, postgres_repo=mock_postgres_repo)
    assert service.get_user_analytics('100') == {}

def test_get_overview_by_analytics(get_session, add_expenses):
    subscription, total = add_expenses
    repo = SubscriptionRepo(get_session).get_overview_by_analytics(subscription.user_id)
    assert len(repo) == 1

def test_get_overview_by_analytics_with_date(get_session, add_expenses):
    subscription, total= add_expenses
    repo = SubscriptionRepo(get_session).get_overview_by_analytics(subscription.user_id, date.today()- timedelta(days=30))
    assert len(repo) == 1
    # assert repo[0].total_expences == total
    subscription, counted = repo[0]
    assert counted == total
    
# Убрать из м
    
    
