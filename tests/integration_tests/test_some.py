# import pytest
# from httpx import ASGITransport, AsyncClient
# from fastapi.websockets import WebSocket
# from src.__main__ import app

# @pytest.mark.anyio
# async def test_root():
#     async with AsyncClient(
#         transport=ASGITransport(app=app), base_url="http://test"
#     ) as ac:
#         response = await ac.websocket_connect("/ws?jwt_token=test_token")
#         assert response is not None
