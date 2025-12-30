from fastapi.security import HTTPBearer
from fastapi.websockets import WebSocket, WebSocketDisconnect
from fastapi import APIRouter, Depends
from pydantic import BaseModel
from src.routes.deps import JWTServiceDep

active_connections: dict[int, WebSocket] = {}

router = APIRouter()

class ExpensesWS(BaseModel):
    jwt_token: str

@router.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket,  service: JWTServiceDep):
    jwt_token =  websocket.headers.get("Authorization")
    user_id = service.check_jwt(jwt_token)
    active_connections[user_id] = websocket
    try:
        await websocket.accept()
        await websocket.send_json({"msg": "Hello you builed a connection!"})
        while True:
            data = await websocket.receive_text()
            await websocket.send_text(f"Message text was: {data}")
    except WebSocketDisconnect:
        del active_connections[user_id]






# Роутер на который мы обращаемся а он находит всех пользователей которым надо отправить сообщение
# а если надо то отправляем с помощью вебсокета


# # @router.websocket("/6/{user_id}")

# Запрос от клиента:
# GET /ws/user123 HTTP/1.1 - на каком роутере можно получить постоянное соединение
# Host: localhost:8000
# Upgrade: websocket
# Connection: Upgrade -  обязательный заголовок
# Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ== - генерируется автоматический браузером
# Sec-WebSocket-Version: 13
# Origin: http://localhost:3000
# На стороне сервера
# Парсинг Sec-WebSocket-Key от клиента

# Так ответит сервер:
# HTTP/1.1 101 Switching Protocols
# Upgrade: websocket
# Connection: Upgrade
# Sec-WebSocket-Accept: s3pPLMBiTxaQ9kYGzzhZRbK+xOo= - генерируется автоматический сервером
