import token
from typing import Callable

from httpx import request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from src.redis_repository.redis_repo import STORAGE_CACHE_TIME, RedisCache
from src.routes.deps import get_user_cache_by_redis
from starlette.responses import JSONResponse
import json
from src.redis_repository.redis_repo import RedisCache
from src.services.jwt_token_services import JWTService
from src.redis_repository.infrastructure import redis_client


class CashMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, cache_ttl: int = 30):
        super().__init__(app)
        self.redis = RedisCache(redis_client)
        self.cache_ttl = cache_ttl

    async def dispatch(self, request: Request, call_next):
        if request.method != "GET":
            return await call_next(request)

        path = request.url.path

        if "/test/user" in path:
            user_id = path.split("/")[-1]
            cache_key = f"user:{user_id}"

            cached = self.redis.get(cache_key)
            if cached is not None:
                # print("CACHE HIT → REDIS")
                return JSONResponse(content=cached, status_code=200)
            # print("CACHE MISS → DB")
            response = await call_next(request)

            body = b""
            async for chunk in response.body_iterator:
                body += chunk

            if not body:
                return response

            try:
                data = json.loads(body)
            except Exception:
                return response  

            self.redis.set(cache_key, data, self.cache_ttl)

            return JSONResponse(content=data, status_code=response.status_code)

        return await call_next(request)



class IdempodencyMiddlewere(BaseHTTPMiddleware):
     def __init__(self, app, jwt_service):
        super().__init__(app)
        self.redis = RedisCache(redis_client)
        self.jwt_service = JWTService(jwt_service)

     def dispatch(self, request: Request, call_next: Callable):
        idempotency_key = request.headers.get("idempotency_key")
        if idempotency_key:
            user_id = self.jwt_service.check_jwt(token.credentials)
            # Присвоили айди подписки и её уникальный номер
            cache_key = f"{user_id}: idempotency key{idempotency_key}"
            # Проверить не создовал\не хранится ли Редис уже такуюже подписку 
            cashe_result = self.redis.get(cache_key)

            if cashe_result:
                return cashe_result

            if not cashe_result:
                result = call_next(request)
                if result.status_code == 201 or result.status_code == 200:
                    self.redis.set(key=f'{idempotency_key} {user_id}', value = result, ttl = STORAGE_CACHE_TIME)
        else:
            return call_next(request)



# Написать тесты на миддлевейр





'''
POST /subscriptions HTTP/1.1
Host: api.example.com
Authorization: Bearer <JWT_TOKEN>
Content-Type: application/json
Idempotency-Key: 550e8400-e29b-41d4-a716-446655440000

{
  "plan_id": 1,
  "duration_months": 12
}
'''