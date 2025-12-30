from fastapi import WebSocket
from src.repository.subscription import SubscriptionRepo
from src.routes.deps import get_session
from src.routes.ws_routers import active_connections

class Notification:

    def __init__(self, subscriptionrepo:SubscriptionRepo, active_connections:dict[int, WebSocket]):
        self.subscriptionrepo = subscriptionrepo
        self.active_connections = active_connections

    async def send_notitfications(self):
        users_to_notify = self.subscriptionrepo.get_subs_from_bd()
        # print(f'Users to notify {len(users_to_notify)}')
        for i in users_to_notify:
            active_ws = self.active_connections[i.user_id]
            await active_ws.send_text(f"Your subscription {i.name} will expire on {i.next_payment}") 

notification_service = Notification(subscriptionrepo=SubscriptionRepo(session=next(get_session())),
                                          active_connections=active_connections)

# https://refactoring.guru/ru/design-patterns/creational-patterns

# def sample(x, y):
#     return x + y

# sample(x=1, y=2)
