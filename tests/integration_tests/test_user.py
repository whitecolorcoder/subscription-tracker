

def test(get_user_repo):
    user = get_user_repo.get_user_by_email("test@example.com")
    assert user is not None
    
    # Проверяем его подписку
    subscription = get_subscription_repo.get_user_subscription(user.id)
    assert subscription is not None
    
    # Проверяем связь между пользователем и подпиской
    assert subscription.user_id == user.id
    
