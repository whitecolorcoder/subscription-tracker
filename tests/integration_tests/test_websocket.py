

def test_websocket(get_app, user_with_jwt):
    with get_app.websocket_connect("/ws", headers={'Authorization':user_with_jwt.token}) as websocket:
        data = websocket.receive_json()
        assert data['msg'] is not None


# GET /ws/user123 HTTP/1.1 - на каком роутере можно получить постоянное соединение
# Host: localhost:8000
# Upgrade: websocket
# Connection: Upgrade -  обязательный заголовок
# Sec-WebSocket-Key: dGhlIHNhbXBsZSBub25jZQ== - генерируется автоматический браузером
# Sec-WebSocket-Version: 13
# Origin: http://localhost:3000
